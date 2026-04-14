import pandas as pd
import random
import itertools
import numpy as np
import copy

def Parameter_setting(MD):
	
	# sets
	I = MD.sets['I']
	J = MD.sets['J']
	J_end = J[-1]
	T = MD.sets['T']
	T_end = T[-1]
	R = MD.sets['R']
	
	# Uncertain parameter
	FP = MD.uncertain['FP'] #  = ['F','P']
	
	# Probabilities
	phat_ij = MD.uncertain['phat_ij']

	# Link uncertain outcomes with probabilities
	Un_prob = {}
	Un_param = {}
	for i in I:
		prob_P = 1
		Un_prob[str(i)+'_zai'] = {}
		Un_param[str(i)+'_zai'] = {}
		list_for_Un_param = []
		for j in J:
			for ForP in FP:
				if ForP == 'F': # Probability for fails
					prob_F = prob_P*(1 - phat_ij[i,j]) 
					Un_prob[str(i)+'_zai'][str(j)+'F'] = prob_F
					list_for_Un_param.append(str(j)+'F')
				elif ForP == 'P': # Probability for success
					prob_P = prob_P*phat_ij[i,j]
					if j == J_end: 
						Un_prob[str(i)+'_zai'][str(j)+'P'] = prob_P
						list_for_Un_param.append(str(j)+'P')
					Un_param[str(i)+'_zai'] = list_for_Un_param
	# print('Un_param =', Un_param)
	# print('Un_prob =', Un_prob)
	
	# Generate all outcomes
	outcome_element = []
	for element in Un_param:
		outcome_element.append(element)
	# print('outcome_element =', outcome_element)
	
	All_outcomes = [x for x in itertools.product(*Un_param.values())]
	# print('All_outcomes =', All_outcomes)
	All_outcomes_keyed = [dict(zip(Un_param.keys(), r)) for r in All_outcomes]
	# print('All_outcomes_keyed =', All_outcomes_keyed)
	# print(len(All_outcomes_keyed))
	
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
	# print('probability =', probability)
	
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
	
	SI_s = {}
	for s in scenario_param:
		P_drug_list = []
		for trial_result in scenario_param[s][1]:
			if scenario_param[s][1][trial_result] == '3P':
				P_drug_list.append(int(trial_result.rsplit('_', 1)[0]))
			SI_s[s] = P_drug_list
	# print('SI_s =', SI_s)
	
	ForP_is = {}
	for i in I:
		for s in SI_s:
			if i in SI_s[s]:
				ForP_is[i,s] = 1
			else:
				ForP_is[i,s] = 0
	# print('ForP_is =', ForP_is)
	
	ForP_i_exped = {}
	for i in I:
		ForP_i_exped[i,] = 0
		for s in S:
			ForP_i_exped[i,] += scenario_param[s][0]*ForP_is[(i,s)]
	# print("ForP_i_exped =", ForP_i_exped)
	
	gammaD_i = MD.parameters['gammaD_i']
	gammaL_i = MD.parameters['gammaL_i']
	
	# Generate differenting drug i and trial j
	D_ssp= {}
	D_AEEV_ssp = {}
	different_outcome = {}
	for s in S:
		for sp in S:
			if sp > s:
				different_outcome[s,sp] = []
				for i_zai in scenario_param[s][1]:
					if scenario_param[s][1][i_zai] != scenario_param[sp][1][i_zai]:
						different_outcome[s,sp].append(i_zai)
				list_for_D_AEEV = []
				for outcome in different_outcome[s,sp]:
					list_for_D_AEEV.append((int(outcome.rsplit('_', 1)[0]), min(int(scenario_param[s][1][outcome][:-1]), int(scenario_param[sp][1][outcome][:-1]))))
				D_AEEV_ssp[s,sp] = tuple(list_for_D_AEEV)
	# print('different_outcome =', different_outcome)
	# print('D_AEEV_ssp =', D_AEEV_ssp)
	
	one_difference = {}
	for s_sp in different_outcome:
		if len(different_outcome[s_sp]) <= 1:
			one_difference[s_sp] = different_outcome[s_sp][0]
	# print('one_difference =', one_difference)
	
	for s_sp in one_difference:
		if abs(int(scenario_param[s_sp[0]][1][one_difference[s_sp]][:-1]) - int(scenario_param[s_sp[1]][1][one_difference[s_sp]][:-1])) == 1: # if different trials are consecutive
			if scenario_param[s_sp[0]][1][one_difference[s_sp]][-1:] == scenario_param[s_sp[1]][1][one_difference[s_sp]][-1:]: # if different trial outcomes are both F
				D_ssp[s_sp] = int(one_difference[s_sp].rsplit('_', 1)[0]), int(scenario_param[s_sp[0]][1][one_difference[s_sp]][:-1]) # (issp,jssp)
		elif abs(int(scenario_param[s_sp[0]][1][one_difference[s_sp]][:-1]) == J_end and int(scenario_param[s_sp[1]][1][one_difference[s_sp]][:-1])) == J_end: # if different trials are P and F at the final trial
			D_ssp[s_sp] = int(one_difference[s_sp].rsplit('_', 1)[0]), int(scenario_param[s_sp[0]][1][one_difference[s_sp]][:-1]) # (issp,jssp)
	
	# print("Phi_ssp =", Phi_ssp)
	# print("Phi_ssp =", len(Phi_ssp))
	# print("D_ssp =", D_ssp)
	
	for s_sp in D_ssp:
		in_list = [D_ssp[s_sp]]
		D_ssp[s_sp] = tuple(in_list)
	# print("D_ssp =", D_ssp)
	
	# dictionary to csv #####
	# import csv
	# with open('D_ssp.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in D_ssp.items():
	# 		writer.writerow([k, v])
	
	gammaD_i = MD.parameters['gammaD_i']
	gammaL_i = MD.parameters['gammaL_i']
	tau_ij = MD.parameters['tau_ij']
	revmax_i = MD.parameters['revmax_i']
	c_ij = MD.parameters['c_ij']
	n_t = MD.parameters['n_t']
	
	# Open revenue (B1)
	revopen_ij = {}
	for i in I:
		for j in J:
			revopen_ij[i,j] = revmax_i[i] - gammaL_i[i]*(T_end + sum(tau_ij[i,jp] for jp in J if jp>=j))
				
	# Running revenue (B2)
	revrun_ijt = {}
	for i in I:
		for j in J:
			for t in T:
				revrun_ijt[i,j,t] = revmax_i[i] - gammaL_i[i]*(t + sum(tau_ij[i,jp] for jp in J if jp>=j))
	
	# Discounting factor for open revenue (B3)
	f_ij = {}
	for i in I:
		for j in J:
			top = revmax_i[i] - gammaL_i[i]*T_end - sum(c_ij[i,jp] for jp in J if jp>=j) 
			bottom = revmax_i[i] - gammaL_i[i]*T_end
			f_ij[i,j] = 0.9*top/bottom
	
	# Discounting factor for time value of money (B4)
	cd_t = {}
	for t in T:
		cd_t[t] = 1 - n_t[t]*(t-1)
	
	rho_ijr = MD.parameters['rho_ijr']
	rhomax_r = MD.parameters['rhomax_r']
	
	return I, J, J_end, T, T_end, R, S, SI_s,\
	gammaD_i, gammaL_i, tau_ij, revmax_i, c_ij, revopen_ij, revrun_ijt, f_ij, cd_t, rho_ijr, rhomax_r,\
	ForP_is, ForP_i_exped, D_ssp, D_AEEV_ssp, probability 

