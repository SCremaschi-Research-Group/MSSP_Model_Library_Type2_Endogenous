import pandas as pd
import random
import itertools
import numpy as np

def Parameter_setting(MD):
	
	# sets
	Omega_E = MD.sets['Omega_E'] # Epochs
	Omega_Estar = Omega_E[:-1] # Epochs except the last one
	Omega_L = MD.sets['Omega_L'] # Lines
	Omega_N = MD.sets['Omega_N'] # Buses
	Omega_O = MD.sets['Omega_O'] # Conventional investment alternatives
	Omega_T = MD.sets['Omega_T'] # Demand period
	Omega_G = MD.sets['Omega_G'] # all generation units and substation (typo?)
	Omega_DG = MD.sets['Omega_DG'] # DG units, indexed g*
	E_end = Omega_E[-1]
	
	delta = MD.parameters['delta']
	
	Omega_K = []
	k_count = 1
	for t in Omega_T:
		if k_count == t:
			Omega_K.append(t)
			k_count = t + delta
	# print('Omega_K =', Omega_K)
	
	Omega_KT_k = {}
	for k in Omega_K:
		Omega_KT_k[k] = list(range(k,k+delta))
	# print('Omega_KT_k =', Omega_KT_k)
	
	# uncertain parameters
	f_n =	MD.uncertain['f_n']
	
	# Generate all outcomes
	Un_param = {}
	# Endogenous part
	for n in Omega_N:
		Un_param[str(n)+'_f'] = []
		for outcome in f_n[n].values():
			Un_param[str(n)+'_f'].append(outcome)
	# print('Un_param =', Un_param)
	
	outcome_element = []
	for element in Un_param:
		outcome_element.append(element)
	# print('outcome_element =', outcome_element)
	
	All_outcomes = [x for x in itertools.product(*Un_param.values())]
	# print('All_outcomes =', All_outcomes)
	All_outcomes_keyed = [dict(zip(Un_param.keys(), r)) for r in All_outcomes]
	# print('All_outcomes_keyed =', All_outcomes_keyed)
	# print(len(All_outcomes_keyed))

	# Probabilities
	f_n_prob =	MD.uncertain['f_n_prob']

	# Link uncertain outcomes with probabilities
	Un_prob = {}
	# Endogenous part
	for n in Omega_N:
		Un_prob[str(n)+'_f'] = {}
		for outcome in f_n[n]:
			Un_prob[str(n)+'_f'][f_n[n][outcome]] = f_n_prob[n][outcome]
	# print('Un_prob =', Un_prob)

	# Create scenario-wise parameter dictionary
	Omega_S = []
	scenario_counter = 1
	scenario_param = {}
	for outcome in All_outcomes_keyed:
		prob_outcome = []
		for source in outcome:
			prob_outcome.append(Un_prob[source][outcome[source]])
		scenario_param[scenario_counter] = (np.prod(prob_outcome), outcome)
		# print(outcome)
		# print(np.prod(prob_outcome))
		Omega_S.append(scenario_counter)
		scenario_counter += 1
	# print('scenario_param =', scenario_param)
	# print('S =', S, 'len(S) =', len(S))
	
	probability = {}
	for s in scenario_param:
		probability[s] = scenario_param[s][0]
	# print('probability =', probability)
	
	## dictionary to csv #####
	# import csv
	# with open('scenario_param.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in scenario_param.items():
	# 		writer.writerow([k, v])
	
	# Total probability check #
	All_prob = []
	for s in Omega_S:
		All_prob.append(scenario_param[s][0])
	# print('All_prob =', All_prob)
	# print('total prob =', np.sum(All_prob))
	
	##### Create uncertain dictionary #####
	
	# Create uncertain and expected dictionaries #
	f_ns = {}
	for n in Omega_N:
		for s in scenario_param:
			if n in Omega_N:
				f_ns[n,s] = scenario_param[s][1][str(n)+'_f']
	# print('f_ns =', f_ns)
	
	f_n_exped = {}
	for n in Omega_N:
		f_n_exped[n] = 0
		for s in Omega_S:
			f_n_exped[n] += scenario_param[s][0]*f_ns[(n,s)]
	# print("f_n_exped =", f_n_exped)
	
	L_e = MD.parameters['L_e'] # Peak load at growing buses corresponding to e
	GB = MD.parameters['GB'] # Buses where peak load grows
	NGB = MD.parameters['NGB'] # Buses where peak load doesn't grow
	OffR = MD.parameters['OffR'] # Off-peak ratio to peak time
	
	random.seed(314) # set the random seed
	d_net = {} # demand
	for n in Omega_N:
		for e in Omega_E:
			PeakTime = MD.parameters['PeakTime'] # time at peak Load in Omega_T
			for k in Omega_KT_k:
				for t in Omega_KT_k[k]:
					if n in GB: # Growing buses
						if t in PeakTime:
							d_net[n,e,t] = L_e[e]
						else: 
							d_net[n,e,t] = round(random.uniform(L_e[e]*OffR-L_e[e]*OffR*0.2, L_e[e]*OffR+L_e[e]*OffR*0.2),1)
					elif n in NGB: # Non-growing buses
						if t in PeakTime:
							d_net[n,e,t] = L_e[1]
						else:  
							d_net[n,e,t] = round(random.uniform(L_e[1]*OffR-L_e[1]*OffR*0.1, L_e[1]*OffR+L_e[1]*OffR*0.1),1)
					else:
						d_net[n,e,t] = 0 # Zero-demand buses
				PeakTime = list(map(lambda x: x + delta, PeakTime))
	
	#### dictionary to csv #####
	# import csv
	# with open('d_net.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in d_net.items():
	# 		writer.writerow([k, v])

	zeta_g = MD.parameters['zeta_g']
	zeta_gt = {}
	for g in Omega_G:
		for t in Omega_T:
			zeta_gt[g,t] = zeta_g[g]
	# print(zeta_gt)

	Kmain_e = MD.parameters['Kmain_e'] # Installed capacity of main generator (g=1)
	Kwind_e = MD.parameters['Kwind_e'] # Capacity of DG wind unit (g=2, g*=1)
	
	K_ge = {}
	for e in Omega_E:
		for g in Omega_G:
			if g in Omega_DG:
				K_ge[g,e] = Kwind_e[e]
			else:
				K_ge[g,e] = Kmain_e[e]
	# print('K_ge =', K_ge)
	
	Max_K = {}
	for e in Omega_E:
		Max_K[e] = sum(K_ge[g,e] for g in Omega_G)
	# print('Max_K =', Max_K)
	
	Fini_l = MD.parameters['Fini_l'] # Initial capacity of line l
	
	Connection_ng = MD.parameters['Connection_ng']
	I_ng = {} # Bus-generator connection
	for n in Omega_N:
		for g in Omega_G:
			if (n,g) in Connection_ng:
				I_ng[n,g] = 1
			else:
				I_ng[n,g] = 0
	# print(I_ng)
	
	Connection_nl = MD.parameters['Connection_nl']
	L_nl = {} # Bus-line connection
	for n in Omega_N:
		for l in Omega_L:
			if (n,l) in Connection_nl:
				L_nl[n,l] = Connection_nl[n,l]
			else:
				L_nl[n,l] = 0
	# print(L_nl)
	
	gammaD = MD.parameters['gammaD'] # investment cost for DSR (Demand Side Response)
	gammaL_o = MD.parameters['gammaL_o'] # Investment cost for line upgrade with o
	rI_e = MD.parameters['rI_e'] # Cumulative discount factor for investment cost at epoch e
	# print('rI_e =', rI_e)
	ro_e = MD.parameters['ro_e'] # Cumulative discount factor for operational cost at epoch e
	# print('ro_e =', ro_e)
	
	kappaL_o = MD.parameters['kappaL_o'] # Time required for the upgraded line to become operational corresponding to o
	kappaD = MD.parameters['kappaD'] # Time for commissioning DSR scheme
	Q_o = MD.parameters['Q_o'] # Capacity addition by upgrading line corresponding to o
	Dmax_n = MD.parameters['Dmax_n'] # Max load can be shifted at bus n
	
	cDSR = MD.parameters['cDSR'] # ￡/kWh
	cDG = MD.parameters['cDG'] # ￡/kWh
	w = MD.parameters['w']
	w_t = {}
	for t in Omega_T:
		w_t[t] = w
	# print('w_t =', w_t)
	
	cDR = MD.parameters['cDR']
	
	D_ssp = {}
	for n in Omega_N:
		for s in Omega_S:
			for sp in Omega_S:
				if s!= sp:
					D_ssp[s,sp] = []
	for n in Omega_N:
		for s in Omega_S:
			for sp in Omega_S:
				if f_ns[n,s] != f_ns[n,sp] and s!= sp:
					D_ssp[s,sp].append(n)
	# print("D_ssp =", D_ssp)

	return Omega_S, Omega_E, Omega_Estar, Omega_L, Omega_N, Omega_O, Omega_T, Omega_G, Omega_DG, Omega_K, Omega_KT_k, E_end, gammaD, gammaL_o, rI_e, ro_e, w_t, kappaL_o, kappaD, Q_o, Dmax_n, f_ns, f_n_exped, d_net, zeta_gt,\
	K_ge, Fini_l, I_ng, L_nl, cDSR, cDG, cDR, D_ssp, Max_K, probability