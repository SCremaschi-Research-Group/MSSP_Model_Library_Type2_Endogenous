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
	I = MD.sets['I']
	L = MD.sets['L']
	K = MD.sets['K']
	T = MD.sets['T']
	Tend = T[-1]
	R = MD.sets['R']
	Rend = R[-1]
	R_i = MD.sets['R_i']
	
	Delta = int(round(Tend/Rend))
	# print('Delta =', Delta)
	
	a_r = {} # The time period corresponding to the beginning of the rth planning segment
	for r in R:
		a_r[r] = (r-1)*Delta + 1
	# print('a_r =', a_r)
	
	ap_r = {} # The time period corresponding to the end of the rth planning segment
	for r in R:
		ap_r[r] = r*Delta
	# print('ap_r =', ap_r)
	aapSET_r = {}
	for r in R:
		aapSET_r[r] = [a_r[r], ap_r[r]]
	# print('aapSET_r =', aapSET_r)
	aapLIST = []
	for r in R:
		for aap in aapSET_r[r]:
			aapLIST.append((r,aap))
	# print('aapLIST =', aapLIST)
	
	##### Other deterministic parameters #####
	d = MD.parameters['d']
	g_l = MD.parameters['g_l']
	gp_ik = MD.parameters['gp_ik']
	alpha_i = MD.parameters['alpha_i']
	v_i = MD.parameters['v_i']
	b = MD.parameters['b']
	h_l = MD.parameters['h_l']
	dp_i = MD.parameters['dp_i']
	hp_ik = MD.parameters['hp_ik']
	e_i = MD.parameters['e_i']
	wmin_k = MD.parameters['wmin_k']
	wmax_k = MD.parameters['wmax_k']
	fmin_i = MD.parameters['fmin_i']
	fmax_i = MD.parameters['fmax_i']
	c_i = MD.parameters['c_i']
	beta_t = MD.parameters['beta_t']
	# print('beta_t =', beta_t)
	Fmax_t = MD.parameters['Fmax_t']
	# print('Fmax_t =', Fmax_t)
	
	umin_l = MD.parameters['umin_l']
	umax_l = MD.parameters['umax_l']
	
	MAX_umax = max(umax_l.values())
	# print('MAX_umax =', MAX_umax)
	
	# uncertain parameters
	thetamax_m = MD.uncertain['thetamax_m']
	
	# Generate all outcomes
	Un_param = {}
	for i in I:
		Un_param[str(i)+'_thetamax_m'] = []
		for SrNo in thetamax_m[i].values():
			Un_param[str(i)+'_thetamax_m'].append(SrNo)
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
	
	# Link uncertain outcomes with probabilities
	thetamax_m_prob = MD.uncertain['thetamax_m_prob']
	Un_prob = {}
	for i in I:
		Un_prob[str(i)+'_thetamax_m'] = {}
		for SrNo in thetamax_m_prob[i]:
			Un_prob[str(i)+'_thetamax_m'][thetamax_m[i][SrNo]] = thetamax_m_prob[i][SrNo]
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
	
	##### dictionary to csv #####
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
	
	thetamax_is = {}
	for i in I:
		for s in S:
			thetamax_is[i,s] = scenario_param[s][1][str(i)+'_thetamax_m'][0]
	# print('thetamax_is =', thetamax_is)
	
	Max_thetamax_i = {}
	for i in I:
		thetamax_list_i = []
		for s in S:
			thetamax_list_i.append(thetamax_is[i,s])
		Max_thetamax_i[i] = max(thetamax_list_i)
	# print('Max_thetamax_i =', Max_thetamax_i)
	
	thetamax_i_exped = {}
	for i in I:
		thetamax_i_exped[i] = 0
		for s in S:
			thetamax_i_exped[i] += scenario_param[s][0]*thetamax_is[i,s]
	# print("thetamax_i_exped =", thetamax_i_exped)
	
	m_is = {}
	for i in I:
		for s in S:
			m_is[i,s] = scenario_param[s][1][str(i)+'_thetamax_m'][1]
	# print('m_is =', m_is)
	
	m_i_exped = {}
	for i in I:
		m_i_exped[i] = 0
		for s in S:
			m_i_exped[i] += scenario_param[s][0]*m_is[i,s]
	# print("m_i_exped =", m_i_exped)
	
	D_ssp = {}
	for s in S:
		for sp in S:
			if s<sp:
				D_ssp[s,sp] = []
				for i in I:
					if scenario_param[s][1][str(i)+'_thetamax_m'] != scenario_param[sp][1][str(i)+'_thetamax_m']:
						D_ssp[s,sp].append(i)
	# print('D_ssp =', D_ssp)
	
	##### dictionary to csv #####
	# import csv
	# with open('D_ssp.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in D_ssp.items():
	# 		writer.writerow([k, v])
	
	return I, L, K, T, Tend, R, Rend, R_i, aapSET_r, aapLIST, S,\
		d, g_l, h_l, umin_l, umax_l, dp_i, gp_ik, hp_ik, alpha_i, v_i, e_i, wmin_k, wmax_k, fmin_i, fmax_i, c_i, b, beta_t, Fmax_t, a_r, ap_r, Max_thetamax_i, MAX_umax, \
		thetamax_is, m_is, D_ssp, probability,\
		thetamax_i_exped, m_i_exped