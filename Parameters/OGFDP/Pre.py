import pandas as pd
import random
import itertools
import numpy as np

def Parameter_setting(MD):
	
	# sets
	WP = MD.sets['WP']
	PP = MD.sets['PP']
	T = MD.sets['T']
	T_end = T[-1]
	
	# Uncertain parameters
	Size =	MD.uncertain['Size']
	Deliv = MD.uncertain['Deliv']

	# Generate all outcomes
	Un_param = {}
	for wp in WP:
		Un_param[wp+'_Size'] = []
		Un_param[wp+'_Deliv'] = []
		for LMH in Size[wp].values():
			Un_param[wp+'_Size'].append(LMH)
		for LMH in Deliv[wp].values():
			Un_param[wp+'_Deliv'].append(LMH)
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
	Size_prob =	MD.uncertain['Size_prob']
	Deliv_prob = MD.uncertain['Deliv_prob']

	# Link uncertain outcomes with probabilities
	Un_prob = {}
	for wp in WP:
		Un_prob[wp+'_Size'] = {}
		for LMH in Size[wp]:
			Un_prob[wp+'_Size'][Size[wp][LMH]] = Size_prob[wp][LMH]
		Un_prob[wp+'_Deliv'] = {}
		for LMH in Deliv[wp]:
			Un_prob[wp+'_Deliv'][Deliv[wp][LMH]] = Deliv_prob[wp][LMH]
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
	
	theta1_wps = {}
	for wp in WP:
		for s in S:
			theta1_wps[wp,s] = scenario_param[s][1][wp+'_Size']
	# print('theta1_wps =', theta1_wps)
	
	theta1_wp_exped = {}
	for wp in WP:
		theta1_wp_exped[wp] = 0
		for s in S:
			theta1_wp_exped[wp] += scenario_param[s][0]*theta1_wps[wp,s]
	# print("theta1_wp_exped =", theta1_wp_exped)

	theta2_wps = {}
	for wp in WP:
		for s in S:
			theta2_wps[wp,s] = scenario_param[s][1][wp+'_Deliv']
	# print('theta2_wps =', theta2_wps)
	
	theta2_wp_exped = {}
	for wp in WP:
		theta2_wp_exped[wp] = 0
		for s in S:
			theta2_wp_exped[wp] += scenario_param[s][0]*theta2_wps[wp,s]
	# print("theta2_wp_exped =", theta2_wp_exped)

	D_ssp = {}
	for s in S:
		for sp in S:
			if s<sp:
				D_ssp[s,sp] = []
				for wp in WP:
					if theta1_wps[wp,s] != theta1_wps[wp,sp] or theta2_wps[wp,s] != theta2_wps[wp,sp]:
						D_ssp[s,sp].append(wp)
	# print('D_ssp', D_ssp)
	
	L1 = {}
	for wp in WP:
		for s in S:
			for sp in S:
				if s<sp:
					if D_ssp[s,sp] == [wp]:
						if bool(theta1_wps[wp,s] != theta1_wps[wp,sp]) ^ bool(theta2_wps[wp,s] != theta2_wps[wp,sp]): # exclusive disjunction XOR
							L1[s,sp] = 1
	# print('L1 =', L1)
	
	# Parameters
	delta_t = {}
	P_t = {}
	alpha_t = {}
	for t in T:
		delta_t[t] = 1
		alpha_t[t] = 1-0.01*(t-1)
		if t <= 6:
			P_t[t] = 400+20*(t-1)
		else:
			P_t[t] = P_t[6]
	# print(alpha_t)
	# print(P_t)
	
	shrink = MD.parameters['shrink']
	M_wp = MD.parameters['M_wp']
	M_pp = MD.parameters['M_pp']
	M_wpwp = MD.parameters['M_wpwp']
	M_wppp = MD.parameters['M_wppp']
	FCC_wp = MD.parameters['FCC_wp']
	FCC_pp = MD.parameters['FCC_pp']
	FCC_wpwp = MD.parameters['FCC_wpwp']
	FCC_wppp = MD.parameters['FCC_wppp']
	VCC_wp = MD.parameters['VCC_wp']
	VCC_pp = MD.parameters['VCC_pp']
	FOC_wp = MD.parameters['FOC_wp']
	FOC_pp = MD.parameters['FOC_pp']
	VOC_wp = MD.parameters['VOC_wp']
	VOC_pp = MD.parameters['VOC_pp']

	Max_theta2 = max(theta2_wps.values())

	return WP, PP, T, T_end, S, theta1_wps, theta2_wps, theta1_wp_exped, theta2_wp_exped, probability, delta_t, shrink, D_ssp, L1, P_t, M_wp, M_pp, M_wpwp, M_wppp, FCC_wp, FCC_pp, FCC_wpwp, FCC_wppp, VCC_wp, VCC_pp, FOC_wp, FOC_pp, VOC_wp, VOC_pp, alpha_t, Max_theta2
