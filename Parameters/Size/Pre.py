import pandas as pd
import random
import itertools
import numpy as np
import copy

def Parameter_setting(MD):
	
	# sets
	I = MD.sets['I']
	T = MD.sets['T']
	T_end = T[-1]
	# print(T_end)
	
	# Uncertain parameters
	Cpr_i =	MD.uncertain['Cpr_i']
	D_t = MD.uncertain['D_t']
	
	# Generate all outcomes
	Un_param = {}
	# Endogenous part
	for i in I:
		Un_param[str(i)+'_Cpr'] = []
		for outcome in Cpr_i[i].values():
			Un_param[str(i)+'_Cpr'].append(outcome)
	# Exogenous part
	for t in D_t:
		Un_param[str(t)+'_demand'] = []
		for outcome in D_t[t].values():
			Un_param[str(t)+'_demand'].append(outcome)
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
	Cpr_prob =	MD.uncertain['Cpr_prob']
	D_t_prob = MD.uncertain['D_t_prob']

	# Link uncertain outcomes with probabilities
	Un_prob = {}
	# Endogenous part
	for i in I:
		Un_prob[str(i)+'_Cpr'] = {}
		for outcome in Cpr_i[i]:
			Un_prob[str(i)+'_Cpr'][Cpr_i[i][outcome]] = Cpr_prob[i][outcome]
	# Exogenous part
	for t in D_t:
		Un_prob[str(t)+'_demand'] = {}
		for outcome in D_t[t]:
			Un_prob[str(t)+'_demand'][D_t[t][outcome]] = D_t_prob[t][outcome]
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
	
	##### Create uncertain dictionary #####
	
	# Create uncertain and expected dictionaries #
	Cpr_is = {}
	for i in I:
		for s in scenario_param:
			if i in I:
				Cpr_is[i,s] = scenario_param[s][1][str(i)+'_Cpr']
	# print('Cpr_is =', Cpr_is)
	
	Cpr_i_exped = {}
	for i in I:
		Cpr_i_exped[i] = 0
		for s in S:
			Cpr_i_exped[i] += scenario_param[s][0]*Cpr_is[(i,s)]
	# print("Cpr_i_exped =", Cpr_i_exped)
	
	t_realization = MD.uncertain['t_realization']
	D_its = {}
	for i in I:
		for t in T:
			for s in scenario_param:
				if t in D_t:
					D_its[i,t,s] = scenario_param[s][1][str(t)+'_demand']
				else:
					D_its[i,t,s] = scenario_param[s][1][str(t_realization)+'_demand']		
	# print('D_its =', D_its)
	
	D_it_exped = {}
	for i in I:
		for t in T:
			D_it_exped[i,t] = 0
			for s in S:
				D_it_exped[i,t] += scenario_param[s][0]*D_its[(i,t,s)]
	# print("D_it_exped =", D_it_exped)
	
	##### Create distingusher dictionary #####
	D_ssp = {}
	
	# Differentiator set D
	for s in S:
		for sp in S:
			if s<sp:
				D_ssp[s,sp] = []
				for i in I:
					if Cpr_is[i,s] != Cpr_is[i,sp]:
						D_ssp[s,sp].append(i)
	# print('D_ssp =', D_ssp)
	
	# Binary parameter Phi
	Phi_tssp = {}
	for t in T:
		for s in S:
			for sp in S:
				if s<sp:
					for i in I:
						if t == 1:
							if D_its[i,t,s] != D_its[i,t,sp]:
								Phi_tssp[t,s,sp] = 0 # Distinguishable
							elif D_its[i,t,s] == D_its[i,t,sp]:
								Phi_tssp[t,s,sp] = 1 # Indistinguishable
						else:
							if Phi_tssp[t-1,s,sp] == 0:
								Phi_tssp[t,s,sp] = 0 # Scenarios are distinguishable once they become distinguishable
							elif D_its[i,t,s] != D_its[i,t,sp]:
								Phi_tssp[t,s,sp] = 0
							elif D_its[i,t,s] == D_its[i,t,sp]:
								Phi_tssp[t,s,sp] = 1
	
	# print('Phi_tssp =', Phi_tssp)
	
	### dictionary to csv #####
	# import csv
	# with open('Phi_tssp.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in Phi_tssp.items():
	# 		writer.writerow([k, v])
	
	##### Other parameters #####
	c_t = MD.parameters['c_t']
	rho = MD.parameters['rho']
	sigma = MD.parameters['sigma']
	M = MD.parameters['M']
	
	##### Parameters for complete recouse #####
	Cpu = MD.parameters['Cpu']

	return I, T, T_end, S, Cpr_is, D_its, Cpr_i_exped, D_it_exped, probability, D_ssp, Phi_tssp, c_t, rho, sigma, M, Cpu
