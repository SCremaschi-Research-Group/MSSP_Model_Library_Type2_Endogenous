import pandas as pd
import random
import itertools
import numpy as np
import copy

def Parameter_setting(MD):
	
	# sets
	T_end = MD.sets['Tend']
	I = MD.sets['I']
	T = range(1, T_end+1)
	
	delta_i = MD.parameters['delta_i']
	delta_bar = max(delta_i.values())
	# print('delta_bar =', delta_bar)
	
	T_delta_i = {}
	for i in delta_i:
		T_delta_i[i] = range(delta_i[i], T_end + delta_i[i] + 1)
	# print('T_delta =', T_delta)
	
	IT_beta = {}
	for i in I:
		for t in T_delta_i[i]:
			IT_beta[i,t] = 1
	IT_beta_set = {(i,t) for (i,t) in IT_beta}
	# print('IT_beta =', IT_beta)
	# print('IT_beta_set =', IT_beta_set)
	
	delta_bar_ij = {} # Maximum Δ of i and j
	T_delta_range = {}
	D_i = MD.parameters['D_i']
	for i in D_i:
		for j in D_i[i]:
			delta_bar_ij[i,j] = max(delta_i[i],delta_i[j])
			T_delta_range[i,j] = range(1, T_end + delta_bar_ij[i,j]+1)
	# print('delta_bar_ij =', delta_bar_ij)
	# print('T_delta_range =', T_delta_range)
	
	delta_min_ij = {} # Minimum Δ of i and j
	for i in D_i:
		for j in D_i[i]:
			delta_min_ij[i,j] = min(delta_i[i],delta_i[j])
	# print('delta_min_ij =', delta_min_ij)
	
	IJT_delta = {}
	IJ_delta = {}
	for i in D_i:
		for j in D_i[i]:
			IJ_delta[i,j] = 1
			for t in T_delta_range[i,j]:
				IJT_delta[i,j,t] = 1
	IJT_delta_set = {(i,j,t) for (i,j,t) in IJT_delta}
	IJ_delta_set = {(i,j) for (i,j) in IJ_delta}
	# print('IJT_delta =', IJT_delta)
	# print('IJT_delta_set =', IJT_delta_set)
	# print('IJ_delta_set =', IJ_delta_set)
	
	##### Scenario and probability generation #####
	
	# Uncertain parameters
	theta =	MD.Uncertain['theta']
	Zhat = MD.Uncertain['Zhat']
	Z = Zhat

	# Generate all outcomes
	Un_param = {}
	for i in I:
		Un_param[str(i)+'_theta'] = []
		Un_param[str(i)+'_Z'] = []
		for MinMax in theta[i].values():
			Un_param[str(i)+'_theta'].append(MinMax)
		for MinMax in Z[i].values():
			Un_param[str(i)+'_Z'].append(MinMax)
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
	theta_prob = MD.Uncertain['theta_prob']
	# Zhat_prob = MD.Uncertain['Zhat_prob']
	Z_prob = MD.Uncertain['Z_prob']

	# Link uncertain outcomes with probabilities
	Un_prob = {}
	for i in I:
		Un_prob[str(i)+'_theta'] = {}
		for MinMax in theta[i]:
			Un_prob[str(i)+'_theta'][theta[i][MinMax]] = theta_prob[i][MinMax]
		Un_prob[str(i)+'_Z'] = {}
		for MinMax in Z[i]:
			Un_prob[str(i)+'_Z'][Z[i][MinMax]] = Z_prob[i][MinMax]
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

	##### Create joint return terms Z_tilda_ijs #####
	Z_MINorMAX = {}
	for s in scenario_param:
		Z_MINorMAX[s] = {}
		for i in Z:
			for minmax in Z[i]:
				if scenario_param[s][1][str(i)+'_Z'] == Z[i][minmax]:
					Z_MINorMAX[s][i] = minmax
	# print('Z_MINorMAX =', Z_MINorMAX)
	
	Z_tilda_ijs = {}
	IJ_Z_tilda = []
	Z_tilda_ij = MD.parameters['Ztilda']
	for i in D_i:
		for j in D_i[i]:
			IJ_Z_tilda.append((i,j))
			for s in Z_MINorMAX:
				if Z_MINorMAX[s][i] == 'min' and Z_MINorMAX[s][j] == 'min':
					Z_tilda_ijs[i,j,s] = Z_tilda_ij[j]['minmin']
				elif Z_MINorMAX[s][i] == 'max' and Z_MINorMAX[s][j] == 'max':
					Z_tilda_ijs[i,j,s] = Z_tilda_ij[j]['maxmax']
				else:
					Z_tilda_ijs[i,j,s] = Z_tilda_ij[j]['minmax']
	IJ_Z_tilda = tuple(IJ_Z_tilda)
	# print('Z_tilda_ijs =', Z_tilda_ijs)
	# print('IJ_Z_tilda =', IJ_Z_tilda)
	
	Ztilda_ij_exped = {}
	for i in D_i:
		for j in D_i[i]:
			Ztilda_ij_exped[i,j] = 0
			for s in S:
				Ztilda_ij_exped[i,j] += scenario_param[s][0]*Z_tilda_ijs[i,j,s]
	# print("Ztilda_ij_exped =", Ztilda_ij_exped)
	
	##### Create uncertain dictionary #####
	theta_is = {}
	for i in I:
		for s in S:
			theta_is[i,s] = scenario_param[s][1][str(i)+'_theta']
	# print('theta_is =', theta_is)
	
	Max_theta_is = max(theta_is.values())
	
	theta_i_exped = {}
	for i in I:
		theta_i_exped[i,] = 0
		for s in S:
			theta_i_exped[i,] += scenario_param[s][0]*theta_is[(i,s)]
	# print("theta_i_exped =", theta_i_exped)

	Z_is = {}
	for i in I:
		for s in S:
			Z_is[i,s] = scenario_param[s][1][str(i)+'_Z']
	# print('Z_is =', Z_is)

	Z_i_exped = {}
	for i in I:
		Z_i_exped[i,] = 0
		for s in S:
			Z_i_exped[i,] += scenario_param[s][0]*Z_is[(i,s)]
	# print("Z_i_exped =", Z_i_exped)
	
	##### Create distingusher dictionary #####
	Y = {}
	H = {}
	for s in S:
		for sp in S:
			# if s<sp:
				Y[s,sp] = []
				H[s,sp] = []
				for i in I:
					if theta_is[i,s] != theta_is[i,sp]:
						Y[s,sp].append(i)
					if Z_is[i,s] != Z_is[i,sp]:
						H[s,sp].append(i)
	# print('Y =', Y)
	# print('H =', H)

	### dictionary to csv #####
	# import csv
	# with open('D.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in D.items():
	# 		writer.writerow([k, v])
	
	##### Other parameters #####
	
	# Budget
	B_t = MD.parameters['B']
	# print(B_t)
	
	f_i = MD.parameters['f'] # fixed activity cost
	r = MD.parameters['r'] # discount factor
	Big_M = MD.parameters['Big_M'] # Additional parameter
	theta_theta = MD.parameters['theta_theta']
	theta_Z = MD.parameters['theta_Z']
	
	Big_M_F3 = max(theta_is[i,s] + t*f_i[i], max(B_t[tp] for tp in T if tp<=t))
	Big_M_F17F19 = min(sum(B_t[tp] for tp in T if tp < t), theta_is[i,s] + (t-1)*f_i[i])

	return I, IJ_Z_tilda, T, T_end, S, IT_beta_set, IJT_delta_set, IJ_delta_set, theta_is, Max_theta_is, Z_is, theta_i_exped, Z_i_exped, Ztilda_ij_exped, probability, Y, H,\
		delta_i, delta_bar_ij, B_t, f_i, r, D_i, theta_theta, theta_Z, delta_bar, delta_min_ij, Z_tilda_ijs, Big_M, Big_M_F3, Big_M_F17F19
