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
	I = MD.sets['I'] # potential ALMs
	T_end = MD.parameters['T_end']
	# time_planning = T[-1]
	T = range(1,T_end+1)
	
	# Uncertain parameters
	Qrc_i = MD.uncertain['Qrc_i'] # Possible flow rate change ratio when ALM i is installed
	
	# Generate all outcomes
	Un_param = {}
	for i in I:
		Un_param[i] = []
		for LH in Qrc_i[i].values():
			Un_param[i].append(LH)
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

	# # Probabilities
	Qrc_i_prob = MD.prob['Qrc_i_prob'] # Possible flow rate change ratio when ALM i is installed

	# Link uncertain outcomes with probabilities
	Un_prob = {}
	for i in I:
		Un_prob[i] = {}
		for LH in Qrc_i[i]:
			Un_prob[i][Qrc_i[i][LH]] = Qrc_i_prob[i][LH]
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
	for s in S:
		All_prob.append(scenario_param[s][0])
	# print('All_prob =', All_prob)
	# print('total prob =', np.sum(All_prob))
	
	Qrc_is = {}
	### define the endogenous uncertainty values:
	for i in I:
		for s in S:
			Qrc_is[i,s] = scenario_param[s][1][i]
	# print('Qrc_is =', Qrc_is)
	Max_Qrc = max(Qrc_is.values())
	# print('Max_Qrc =', Max_Qrc)
	
	Qrc_i_exped = {}
	for i in I:
		Qrc_i_exped[i] = 0
		for s in S:
			Qrc_i_exped[i] += scenario_param[s][0]*Qrc_is[i,s]
	# print("Qrc_i_exped =", Qrc_i_exped)
	
	B_issp = {}
	### define the distinguishble scenario sets for endogenous uncertainties:
	for i in I:
		for s in S:
			for sp in S:
				if s<sp:
					if Qrc_is[i,s] == Qrc_is[i,sp]:
						B_issp[i,s,sp]=1
	# print('B_issp =', B_issp)
	
	D_ssp = {}
	### define the distinguishble scenario sets for endogenous uncertainties:
	for s in S:
		for sp in S:
			if s<sp:
				D_ssp[s,sp] = []
				for i in I:
					if Qrc_is[i,s] != Qrc_is[i,sp]:
						D_ssp[s,sp].append(i)
	# print('D_ssp =', D_ssp)
	
	##### Other deterministic parameters #####
	Pg = MD.parameters['Pg']
	Po = MD.parameters['Po']
	Png = MD.parameters['Png']
	WI = MD.parameters['WI']
	MARR = MD.parameters['MARR']
	FT = MD.parameters['FT']
	Cm_i = MD.parameters['Cm_i']
	Co_i = MD.parameters['Co_i']
	Ce_i = MD.parameters['Ce_i']
	b = MD.parameters['b']
	D = MD.parameters['D']
	LT = MD.parameters['LT']
	RT = MD.parameters['RT']
	n = MD.parameters['n']
	Qg1 = MD.parameters['Qg1']
	Qo1 = MD.parameters['Qo1']
	Qng1 = MD.parameters['Qng1']
	LFR_LB_i = MD.parameters['LFR_LB_i']
	LFR_UB_i = MD.parameters['LFR_UB_i']
	CLIM = MD.parameters['CLIM']
	
	BC_Qg_pr = {}
	for p in T:
		for r in T:
			if r>=p:
				BC_Qg_pr[p,r] = Max_Qrc*Qg1*(1+b*D*(r-p+1))**(-1/b)
	## dictionary to csv #####
	# import csv
	# with open('BC_Qg_pr.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in BC_Qg_pr.items():
	# 		writer.writerow([k, v])
	
	return I, T, T_end, S,\
			Pg, Po, Png, WI, MARR, FT, Cm_i, Co_i, Ce_i, b, D, LT, RT, n, Max_Qrc, Qg1, Qo1, Qng1, LFR_LB_i, LFR_UB_i, CLIM,\
			Qrc_i, Qrc_is, B_issp, D_ssp, probability,\
			Qrc_i_exped
