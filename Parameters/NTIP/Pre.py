import pandas as pd
import random
import itertools
import numpy as np
import copy
import collections

def Parameter_setting(MD):
	
	def flatten(l): # Function to Flatten an irregularlly nested lists or tuples
		for el in l:
			if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
				yield from flatten(el)
			else:
				yield el
	
	# sets
	N = MD.sets['N'] # Chemicals
	N_product = MD.sets['N_product'] # Product
	N_feed = MD.sets['N_feed'] # Raw material and intermediate
	T = MD.sets['T'] # Time steps
	# T_un_demand = MD.sets['T_un_demand'] # Time when demand is uncertain
	T_end = T[-1]
	I = MD.sets['I'] # Technologies
	SG = MD.sets['SG'] # Technology stages
	# NP = MD.sets['NP'] # Partition of Capacity expansion X_its (For linearization of (11))
	I_PF = MD.sets['I_PF'] # Primary reactant/feedstock of technology i
	
	# Uncertain parameters
	alpha =	MD.uncertain['alpha']
	beta = MD.uncertain['beta']
	chi = MD.uncertain['chi'] # Uncertain yield
	demand = MD.uncertain['demand'] # Only for chem 3
	psi = MD.uncertain['psi'] # Project outcome
	
	# Generate all outcomes
	Un_param = {}
	for i in I:
		Un_param[i+'_psi'] = []
		Un_param[i+'_alpha'] = []
		Un_param[i+'_beta'] = []
		Un_param[i+'_chi'] = []
		for PF in psi[i].values():
			Un_param[i+'_psi'].append(PF)
		for LH in alpha[i].values():
			Un_param[i+'_alpha'].append(LH)
		for LH in beta[i].values():
			Un_param[i+'_beta'].append(LH)
		for LH in chi[i].values():
			Un_param[i+'_chi'].append(LH)
	for t in T:
		Un_param[str(t)+'_demand'] = []
		for LH in demand[t].values():
			Un_param[str(t)+'_demand'].append(LH)
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
	alpha_prob = MD.prob['alpha_prob']
	beta_prob =	MD.uncertain['beta_prob']
	chi_prob = MD.uncertain['chi_prob']
	demand_prob = MD.uncertain['demand_prob']
	psi_prob = MD.uncertain['psi_prob']
	
	# Link uncertain outcomes with probabilities
	Un_prob = {}
	for i in I:
		Un_prob[i+'_psi'] = {}
		for PF in psi[i]:
			Un_prob[i+'_psi'][psi[i][PF]] = psi_prob[i][PF]
		Un_prob[i+'_alpha'] = {}
		for LH in alpha[i]:
			Un_prob[i+'_alpha'][alpha[i][LH]] = alpha_prob[i][LH]
		Un_prob[i+'_beta'] = {}
		for LH in beta[i]:
			Un_prob[i+'_beta'][beta[i][LH]] = beta_prob[i][LH]
		Un_prob[i+'_chi'] = {}
		for LH in chi[i]:
			Un_prob[i+'_chi'][chi[i][LH]] = chi_prob[i][LH]
	for t in T:
		Un_prob[str(t)+'_demand'] = {}
		for LH in demand[t]:
			Un_prob[str(t)+'_demand'][demand[t][LH]] = demand_prob[t][LH]
	# print('Un_prob =', Un_prob)
	
	# Create scenario-wise parameter dictionary
	S = []
	scenario_counter = 1
	scenario_param = {}
	for outcome in All_outcomes_keyed:
		prob_outcome = []
		for source in outcome:
			prob_outcome.append(Un_prob[source][outcome[source]])
		scenario_param[scenario_counter] = (np.prod(prob_outcome), outcome)
		# print(outcome)
		# print(np.prod(prob_outcome))
		S.append(scenario_counter)
		scenario_counter += 1
	# print('scenario_param =', scenario_param)
	# print('S =', S)
	# print('len(S) =', len(S))
	probability = {}
	for s in scenario_param:
		probability[s] = scenario_param[s][0]
	# print('prob =', prob)
	
	## dictionary to csv #####
	# import csv
	# with open('scenario_param.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in scenario_param.items():
	# 		writer.writerow([k, v])
	
	# Total probability check #
	All_prob = []
	for s in S:
		All_prob.append(scenario_param[s][0])
	# print('All_prob =', All_prob)
	# print('total prob =', np.sum(All_prob))
	
	CX_i0 = MD.parameters['CX_i0'] # Initial installed capacity of technology i
	XMax_i = MD.parameters['XMax_i'] # Maximum allowable capacity Expansion
	RD_i0 = MD.parameters['RD_i0'] # Initial R&D Investment
	CC0_i = MD.parameters['CC0_i'] # Initial capacity expansion cost for technology i [$/kg]
	
	D_nts = {}
	for n in N:
		if n not in N_product:
			for t in T:
				for s in S:
					D_nts[n,t,s] = 0
		elif n in N_product:
			for t in T:
				for s in S:
					D_nts[n,t,s] = scenario_param[s][1][str(t)+'_demand']
	# print('D_nts =', D_nts)
	
	D_nt_exped = {}
	for n in N:
		for t in T:
			D_nt_exped[n,t] = 0
			for s in S:
				D_nt_exped[n,t] += scenario_param[s][0]*D_nts[n,t,s]
	# print("D_nt_exped =", D_nt_exped)
	MAX_D_nts = max(D_nts.values())
	# Create success or abandonment dictionary
	theta_is = {}
	for i in I:
		for s in S:
			if scenario_param[s][1][i+'_psi'] == '2_CP':
				theta_is[i,s] = 1
			else:
				theta_is[i,s] = 0
	# print('theta_is =', theta_is)
	
	# theta_is_outcome = {}
	# for i in I:
	# 	for s in S:
	# 		theta_is_outcome[i,s] = scenario_param[s][1][i+'_psi']
	# print('theta_is_outcome =', theta_is_outcome)
	
	theta_i_exped = {}
	for i in I:
		theta_i_exped[i] = 0
		for s in S:
			theta_i_exped[i] += scenario_param[s][0]*theta_is[i,s]
	# print("theta_i_exped =", theta_i_exped)
	
	# Create yield dictionary
	chip_is = {}
	for i in I:
		for s in S:
			chip_is[i,s] = scenario_param[s][1][i+'_chi']
	# print('chip_is =', chip_is)
	
	chip_i_exped = {}
	for i in I:
		chip_i_exped[i] = 0
		for s in S:
			chip_i_exped[i] += scenario_param[s][0]*chip_is[i,s]
	# print("chip_i_exped =", chip_i_exped)
	
	# Create alpha dictionary
	alpha_is = {}
	for i in I:
		for s in S:
			alpha_is[i,s] = scenario_param[s][1][i+'_alpha']
	# print('alpha_is =', alpha_is)
	
	alpha_i_exped = {}
	for i in I:
		alpha_i_exped[i] = 0
		for s in S:
			alpha_i_exped[i] += scenario_param[s][0]*alpha_is[i,s]
	# print("alpha_i_exped =", alpha_i_exped)
	
	# Create beta dictionary
	beta_is = {}
	for i in I:
		for s in S:
			beta_is[i,s] = scenario_param[s][1][i+'_beta']
	# print('beta_is =', beta_is)
	
	beta_i_exped = {}
	for i in I:
		beta_i_exped[i] = 0
		for s in S:
			beta_i_exped[i] += scenario_param[s][0]*beta_is[i,s]
	# print("beta_i_exped =", beta_i_exped)
	
	##### Other deterministic parameters #####
	MCst_n = MD.parameters['MCst_n'] # Raw material cost [$/tonne]
	# print('MCst =', MCst)
	cd_t = MD.parameters['cd_t'] # Discounting Factor
	# print('cd_t =', cd_t)
	CXMin_isg = MD.parameters['CXMin_isg'] # Minimum capacity of stage sg for technology i
	Big_M = MD.parameters['Big_M']
	RDMax = MD.parameters['RDMax'] # Maximum research investment at each time period
	Valpha = MD.parameters['Valpha'] # Research Threshold - The number of investments needed to realize Alpha
	Vbeta = MD.parameters['Vbeta'] # Capacity Threshold - The number of expansions needed to realize Beta
	DeltaRDmin_i = MD.parameters['DeltaRDmin_i'] # Minimum investment required to count up the number of investments in research
	DeltaCXmin_i = MD.parameters['DeltaCXmin_i'] # Minimum expansion required to count up the number of expansions of capacity
	
	# Create stoichiometric ratio dictionary from primary reactant rp to chemical n
	gamma_innp = MD.parameters['gamma_innp'] # Stoichiometric ratio between chemical n and n' in technology i
	gamma_iPDFD = {}
	for i in I:
		for n in N:
			for rp in N:
				if (i,n,rp) in gamma_innp:
					gamma_iPDFD[i,n,rp] = gamma_innp[i,n,rp]
				else:
					gamma_iPDFD[i,n,rp] = 0
	# print('gamma_inRP =', gamma_inRP)
	Bound_M = max(D_nts.values())/min(gamma_innp.values())/min(chip_is.values())
	
	##### Create distingusher sets #####
	Dpsi_ssp = {} # For Pass or Fail
	for s in S:
		for sp in S:
			if s<sp:
				Dpsi_ssp[s,sp] = []
				for i in I:
					if scenario_param[s][1][i+'_psi'] != scenario_param[sp][1][i+'_psi']:
						Dpsi_ssp[s,sp].append((i, min(int(scenario_param[s][1][i+'_psi'].rsplit('_', 1)[0]), int(scenario_param[sp][1][i+'_psi'].rsplit('_', 1)[0]))))
	# print('Dpsi_ssp =', Dpsi_ssp)
	
	### dictionary to csv #####
	# import csv
	# with open('Dpsi_ssp.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in Dpsi_ssp.items():
	# 		writer.writerow([k, v])
	
	###### CHECK BEFORE AEEV ########
	# phi_psi_issp = {}
	# for i in I:
	# 	for s in S:
	# 		for sp in S:
	# 			if s<sp:
	# 				if scenario_param[s][1][i+'_psi'] != scenario_param[sp][1][i+'_psi']:
	# 					phi_psi_issp[i,s,sp] = 1
	# 				else:
	# 					phi_psi_issp[i,s,sp] = 0
	# # print('phi_psi_issp =', phi_psi_issp)
	
	# psi_sg_ssp = {}
	# for i in I:
	# 	for s in S:
	# 		for sp in S:
	# 			if s<sp:
	# 				psi_sg_ssp[s,sp] = min(int(scenario_param[s][1][i+'_psi'].rsplit('_', 1)[0]), int(scenario_param[sp][1][i+'_psi'].rsplit('_', 1)[0]))
	# # print('psi_sg_ssp =', psi_sg_ssp) # With dummy
	
	### dictionary to csv #####
	# import csv
	# with open('psi_sg_ssp.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in psi_sg_ssp.items():
	# 		writer.writerow([k, v])

	theta_isgs = {} # For AEEV and GKDA distinguisher
	for i in I:
		for sg in SG:
			for s in S:
				if sg == 2:
					if scenario_param[s][1][i+'_psi'] == '2_CP':
						theta_isgs[i,sg,s] = 1
					else:
						theta_isgs[i,sg,s] = 0
				elif sg == 1:
					if scenario_param[s][1][i+'_psi'] == '1_PA':
						theta_isgs[i,sg,s] = 0
					else:
						theta_isgs[i,sg,s] = 1
	# print('theta_isgs =', theta_isgs)

	# theta_isgs = {} # For AEEV and GKDA distinguisher
	# for i in I:
	# 	for sg in SG:
	# 		s_list = []
	# 		for s in S:
	# 			for sp in S:
	# 				if s<sp and psi_sg_ssp[s,sp] == sg:
	# 					s_list.append(s)
	# 					theta_isgs[i,sg,min(s_list)] = 0 # indistinguishable if s = sp
	# 					theta_isgs[i,sg,sp] = phi_psi_issp[i,min(s_list),sp]
	# print('theta_isgs =', theta_isgs)
	###### CHECK BEFORE AEEV ここまで ########

	t_diff_ssp = {} # For uncertain demand
	for s in S:
		for sp in S:
			if s<sp:
				t_diff = []
				for t in T:
					if scenario_param[s][1][str(t)+'_demand'] != scenario_param[sp][1][str(t)+'_demand']:
						t_diff.append(t)
				if len(t_diff) > 0:
					t_diff_ssp[s,sp] = min(t_diff)
				else:
					t_diff_ssp[s,sp] = 0
	# print('t_diff_ssp =', t_diff_ssp)
	
	### dictionary to csv #####
	# import csv
	# with open('t_diff_ssp.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in t_diff_ssp.items():
	# 		writer.writerow([k, v])
	
	phi_D_tssp = {} # For uncertain demand
	for t in T:
		for s in S:
			for sp in S:
				if s<sp:
					if t_diff_ssp[s,sp] == 0: # Never become distinguishable by which time goes by
						phi_D_tssp[t,s,sp] = 0
					elif t >= t_diff_ssp[s,sp]: # Scenarios are distinguishable once they become distinguishable
						phi_D_tssp[t,s,sp] = 1 # Distinguishable
					else:
						phi_D_tssp[t,s,sp] = 0 # Indistinguishable
	
	### dictionary to csv #####
	# import csv
	# with open('phi_D_tssp.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in phi_D_tssp.items():
	# 		writer.writerow([k, v])
	
	Dchi_ssp = {} # For yield
	for s in S:
		for sp in S:
			if s<sp:
				Dchi_ssp[s,sp] = []
				for i in I:
					if scenario_param[s][1][i+'_chi'] != scenario_param[sp][1][i+'_chi']:
						Dchi_ssp[s,sp].append(i)
	
	##### Create distingusher sets #####
	DchiAEEV_ssp = {} # For Pass or Fail
	for s in S:
		for sp in S:
			if s<sp:
				DchiAEEV_ssp[s,sp] = []
				for i in I:
					if scenario_param[s][1][i+'_chi'] != scenario_param[sp][1][i+'_chi']:
						DchiAEEV_ssp[s,sp].append((i,3))
	# print('DchiAEEV_ssp =', DchiAEEV_ssp)
	
	### dictionary to csv #####
	# import csv
	# with open('Dchi_ssp.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in Dchi_ssp.items():
	# 		writer.writerow([k, v])
	
	Dalpha_ssp = {} # For alpha
	for s in S:
		for sp in S:
			if s<sp:
				Dalpha_ssp[s,sp] = []
				for i in I:
					if scenario_param[s][1][i+'_alpha'] != scenario_param[sp][1][i+'_alpha']:
						Dalpha_ssp[s,sp].append(i)
	
	### dictionary to csv #####
	# import csv
	# with open('Dalpha_ssp.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in Dalpha_ssp.items():
	# 		writer.writerow([k, v])
	
	Dbeta_ssp = {} # For beta
	for s in S:
		for sp in S:
			if s<sp:
				Dbeta_ssp[s,sp] = []
				for i in I:
					if scenario_param[s][1][i+'_beta'] != scenario_param[sp][1][i+'_beta']:
						Dbeta_ssp[s,sp].append(i)
	
	### dictionary to csv #####
	# import csv
	# with open('Dbeta_ssp.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in Dbeta_ssp.items():
	# 		writer.writerow([k, v])
	
	return N, N_product, N_feed, T, T_end, I, SG, I_PF, S,\
		MCst_n, CX_i0, cd_t, RD_i0, XMax_i, CC0_i, gamma_iPDFD, RDMax, Valpha, Vbeta, Bound_M, DeltaRDmin_i, DeltaCXmin_i, Big_M, MAX_D_nts, \
		D_nts, CXMin_isg, theta_is, chip_is, alpha_is, beta_is, phi_D_tssp, Dpsi_ssp, Dchi_ssp, DchiAEEV_ssp, Dalpha_ssp, Dbeta_ssp, scenario_param, \
		D_nt_exped, theta_i_exped, chip_i_exped, alpha_i_exped, beta_i_exped, theta_isgs, probability,\
