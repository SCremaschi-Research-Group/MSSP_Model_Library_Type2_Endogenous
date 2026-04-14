import pandas as pd
import random
import itertools
import numpy as np
import copy
import collections

def Parameter_setting(MD, Case_csv):
	
	def flatten(l): # Function to Flatten an irregularlly nested lists or tuples
		for el in l:
			if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
				yield from flatten(el)
			else:
				yield el
	
	# sets
	T_end = MD.sets['Tend']
	T = range(1, T_end+1)
	I = MD.sets['I']
	IU = MD.sets['IU']
	Not_IU = set(I) - set(IU)
	Not_IU = list(Not_IU)
	K = MD.sets['K']
	K126 = MD.sets['K126']
	K910 = MD.sets['K910']
	STEP = MD.sets['STEP']
	
	##### Deterministic parameters #####
	
	### Fixed expansion cost 
	FE = MD.parameters['FE']
	FE_it = {}
	for i in I:
		for t in T:
			FE_it[i,t] = FE[i]
	# print('FE_it =', FE_it)

	### Variable expansion cost 
	VE = MD.parameters['VE']
	VE_it = {}
	for i in I:
		for t in T:
			VE_it[i,t] = VE[i]
	# print('VE_it =', VE_it)

	### Fixed operating cost
	FO = MD.parameters['FO']
	FO_it = {}
	for i in I:
		for t in T:
			FO_it[i,t] = FO[i]
	# print('FO_it =', FO_it)

	### Variable operating cost for stream k
	VO = MD.parameters['VO']
	VO_kt = {}
	for k in K:
		for t in T:
			VO_kt[k,t] = VO[k]
	# print('VO_kt =', VO_kt)

	### Fixed investment cost for pilot plant
	FIPP = MD.parameters['FIPP']
	FIPP_it = {}
	for i in I:
		for t in T:
			FIPP_it[i,t] = FIPP[i]
	# print('FIPP_it =', FIPP_it)

	### Fixed operating cost for pilot plant
	FOPP = MD.parameters['FOPP']
	FOPP_it = {}
	for i in I:
		for t in T:
			FOPP_it[i,t] = FOPP[i]
	# print('FOPP_it =', FOPP_it)

	### Duration of time period t
	delta = MD.parameters['delta']
	delta_t = {}
	for t in T:
		delta_t[t] = delta
	# print('delta_t =', delta_t)

	### Duration of time period t
	alpha = MD.parameters['alpha']
	alpha_t = {}
	for t in T:
		alpha_t[t] = alpha
	# print('alpha_t =', alpha_t)

	### Duration of time period t
	beta = MD.parameters['beta']
	beta_t = {}
	for t in T:
		beta_t[t] = beta
	# print('beta_t =', beta_t)
	
	### Duration of time period t
	gamma = MD.parameters['gamma']
	gamma_t = {}
	for t in T:
		gamma_t[t] = gamma
	# print('gamma_t =', gamma_t)
	
	Big_M = MD.parameters['Big_M']
	
	### Number of sum of expansion and pilot allowed at t
	CARD = MD.parameters['CARD']
	CARD_t = {}
	for t in T:
		CARD_t[t] = CARD + t-1
	# print('CARD_t =', CARD_t)
	
	### Yield of deterministic process
	theta_i = MD.parameters['theta']
	
	### Demand for final product
	d_t = MD.parameters['d']
	
	### Initial capacity of process i
	Wcap_inital_i = MD.parameters['Wcap_inital']
	
	### Max and min limit of capacity expansion of process i
	UQE_i =	MD.parameters['UQE']
	LQE_i =	MD.parameters['LQE']
	
	### Max and min limit of outflow of process i
	Uout_i = MD.parameters['Uoutflow']
	Lout_i = MD.parameters['Loutflow']
	
	# uncertain parameters
	Un_yield = pd.read_csv(Case_csv) # If you want to ignore the header, add ", header=None"
	theta_ils = dict((tuple((int(a),int(b),int(c))), d) for a,b,c,d in Un_yield.values)
	# print("theta_ils =", theta_ils)
	S = list(range(1, max(Un_yield["S"])+1))
	
	p_s = MD.uncertain['p_s']
	if p_s == {}:
		for s in S:
			p_s[s] = 1/len(S)
	# print("p_s =", p_s)
	
	# Create scenario-wise parameter dictionary
	All_outcomes = {}
	scenario_param = {}
	for s in S:
		All_outcomes[s] = {}
		for i in IU:
			for l in STEP:
				All_outcomes[s][i,l] = theta_ils[i,l,s]
				# print('All_outcomes =', All_outcomes)
		scenario_param[s] = (p_s[s], All_outcomes[s])
	# print('scenario_param =', scenario_param)
	
	theta_il_exped = {}
	for i in IU:
		for l in STEP:
			theta_il_exped[i,l] = 0
			for s in S:
				theta_il_exped[i,l] += p_s[s]*theta_ils[(i,l,s)]
	# print("theta_il_exped =", theta_il_exped)
	
	##### Create distingusher set #####
	D_ssp = {}
	for s in S:
		for sp in S:
			if s<sp:
				D_ssp[s,sp] = []
				for i in IU:
					diff_counter = 0
					for l in STEP:
						if theta_ils[i,l,s] != theta_ils[i,l,sp]:
							diff_counter += 1
					if diff_counter >= 1:
						D_ssp[s,sp].append(i)
	# print('D_ssp =', D_ssp)
	
	D_ssp_AEEV = {}
	for s in S:
		for sp in S:
			if s<sp:
				D_ssp_AEEV[s,sp] = []
				for i in IU:
					for l in STEP:
						if theta_ils[i,l,s] != theta_ils[i,l,sp]:
							D_ssp_AEEV[s,sp].append((i,l))
	# print('D_ssp_AEEV =', D_ssp_AEEV)
	
	##### Scenario pairs, s and s', which cannot be differentiated in the second step after operating or installing pilot plant for process i #####
	M_issp = {}
	if max(STEP) >= 2: # TSSP can't define M_issp
		for i in IU:
			for s in S:
				for sp in S:
					if s<sp:
						if theta_ils[i,2,s] == theta_ils[i,2,sp]:
							M_issp[i,s,sp] = 1
						else:
							M_issp[i,s,sp] = 0
		# print('M_issp =', M_issp) # 1 if indistinguishable
	else:
		pass
	
	return I, IU, Not_IU, K, K126, K910, STEP, T, T_end, S,\
		FE_it, VE_it, FO_it, VO_kt, FIPP_it, FOPP_it, delta_t, alpha_t, beta_t, gamma_t, Big_M, CARD_t, theta_i, d_t, Wcap_inital_i, UQE_i, LQE_i, Uout_i, Lout_i,\
		theta_ils, D_ssp, D_ssp_AEEV, M_issp, p_s, theta_il_exped
