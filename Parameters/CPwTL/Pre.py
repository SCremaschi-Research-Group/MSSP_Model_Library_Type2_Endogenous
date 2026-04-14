import pandas as pd
import random
import itertools
import numpy as np
import copy
import collections

def Parameter_setting(MD,Case_csv):
	
	def flatten(l): # Function to Flatten an irregularlly nested lists or tuples
		for el in l:
			if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
				yield from flatten(el)
			else:
				yield el
	
	# sets
	K = MD.sets['K']
	R = MD.sets['R']
	I = MD.sets['I']
	T = MD.sets['T']
	Tend = T[-1]
	HtSize = MD.parameters['HtSize']
	
	Ht = []
	for h in range(1,HtSize+1):
		Ht.append(h) # No time dependence
	# print('Ht =', Ht)
	
	##### Other deterministic parameters #####
	Cbark0 = MD.parameters['Cbark0']
	Deltabar_ki = MD.parameters['Deltabar_ki']
	# print(Deltabar_ki)
	
	Deltabar_k_exped = {}
	for k in K:
		Deltabar_k_exped[k] = 0
		for i in I:
			Deltabar_k_exped[k] += 1/len(I)*Deltabar_ki[k,i]
	# print("Deltabar_k_exped =", Deltabar_k_exped)
	
	bdist_kt = MD.parameters['bdist_kt']
	b_kt = {}
	for k in K:
		for t in T:
			b_kt[k,t] = bdist_kt[k,t]*Deltabar_k_exped[k]
	# print("b_kt =", b_kt)
	
	DetInt_ki = MD.parameters['DetInt_ki']
	
	alpha_t = MD.parameters['alpha_t']
	# print("alpha_t =", alpha_t)
	
	n = MD.parameters['n']
	n_t = {}
	for t in T:
		n_t[t] = n
	# print("n_t =", n_t)
	
	np.random.seed(313)
	beta = MD.parameters['beta']
	beta_kth = {}
	for k in K:
		for t in T:
			for h in Ht:
				beta_kth[k,t,h] = round(np.random.uniform(*beta),1)
	# print("beta_kth =", beta_kth)
	
	gamma = MD.parameters['gamma']
	gamma_th = {}
	for t in T:
		for h in Ht:
			gamma_th[t,h] = gamma
	# print("gamma_th =", gamma_th)
	
	d1bardist = MD.parameters['d1bardist']
	d1bar = round(d1bardist*sum(Cbark0 for k in K))
	# print('d1bar =', d1bar)
	
	dTbardist = MD.parameters['dTbardist']
	dTbar = round(dTbardist*(sum(Cbark0 for k in K) + sum(Deltabar_ki[k,i] for k in K for i in I)))
	# print('dTbar =', dTbar)
	
	np.random.seed(313)
	dtbar = sorted(np.random.randint(d1bar,dTbar,Tend-2), reverse=False)
	# print('dtbar =', dtbar)
	
	DemDistInh = MD.parameters['DemDistInh']
	d_th = {}
	for t in T:
		if t == 1:
			for h in Ht:
				np.random.seed(h+2*len(Ht))
				d_th[t,h] = round(d1bar*np.random.uniform(*DemDistInh))
				# print(d1bar)
		elif t == Tend:
			for h in Ht:
				np.random.seed(h+len(Ht))
				d_th[t,h] = round(dTbar*np.random.uniform(*DemDistInh))
				# print(dTbar)
		else:
			for h in Ht:
				np.random.seed(h)
				d_th[t,h] = round(dtbar[t-2]*np.random.uniform(*DemDistInh))
				# print(dtbar[t-2])
	# print('d_th =', d_th)
	
	##### dictionary to csv #####
	# import csv
	# with open('d_th.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in d_th.items():
	# 		writer.writerow([k, v])
	
	Omega_k = MD.parameters['Omega_k']
	UT_k = MD.parameters['UT_k']
	DT_k = MD.parameters['DT_k']
	
	eta = MD.parameters['eta']
	eta_kth = {}
	for k in K:
		for t in T:
			for h in Ht:
				eta_kth[k,t,h] = eta
	# print('eta_kth =', eta_kth)
	
	# Big-M calculation
	Csum = {}
	for k in K:
		Csum[k] = Cbark0 + sum(Deltabar_ki[k,i] for i in I)
	Cmax = max(Csum.values())
	# print('Cmax =', Cmax)
	
	etaMax = max(eta_kth.values())
	# print('etaMax =', etaMax)
	
	OmegaMin = min(Omega_k.values())
	# print('OmegaMin =', OmegaMin)
	
	BigMy = Cmax/OmegaMin
	BigMP = Cmax*etaMax
	# print('BigMy =', BigMy)
	# print('BigMP =', BigMP)
	
	# uncertain parameters
	uncertain_data = pd.read_csv(Case_csv) # If you want to ignore the header, add ", header=None"
	S = list(range(1, max(s for k,b,s,d in uncertain_data.values)+1))
	# print('S =', S)
	p_s = {}
	for s in S:
		p_s[s] = 1/len(S) # Equal probability
	# print('p_s =', p_s)
	
	integralinR_kis = dict((tuple((k,b,c)), d) for k,b,c,d in uncertain_data.values)
	integral_kis = {}
	for k in K:
		for i in I:
			for s in S:
				if k in R:
					integral_kis[k,i,s] = integralinR_kis[k,i,s]
				else:
					integral_kis[k,i,s] = DetInt_ki[k,i]
	# print("integral_kis =", integral_kis)
	
	# Create scenario-wise parameter dictionary
	scenario_param = {}
	for s in S:
		scenario_param[s] = [p_s[s], {}]
		for k in R:
			for i in I:
				# print('scenario_param =', scenario_param)
				scenario_param[s][1][k,i] = integral_kis[k,i,s]
				scenario_param[s] = tuple(scenario_param[s])
	# print('scenario_param =', scenario_param)
	
	probability = {}
	for s in scenario_param:
		probability[s] = scenario_param[s][0]
	# print('probability =', probability)
	
	integral_ki_exped = {}
	for k in K:
		for i in I:
			integral_ki_exped[k,i] = 0
			for s in S:
				integral_ki_exped[k,i] += scenario_param[s][0]*integral_kis[k,i,s]
	
	# print("integral_ki_exped =", integral_ki_exped)
	
	D_ssp = {}
	for s in S:
		for sp in S:
			if s<sp:
				D_ssp[s,sp] = []
				for r in R:
					for i in I:
						if integral_kis[r,i,s] != integral_kis[r,i,sp]:
							D_ssp[s,sp].append((r,i))
	# print('D_ssp =', D_ssp)
	
	##### dictionary to csv #####
	# import csv
	# with open('D_ssp.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in D_ssp.items():
	# 		writer.writerow([k, v])
	
	return K, R, I, T, Tend, Ht, S,\
		Cbark0, Deltabar_ki, b_kt, alpha_t, n_t, beta_kth, gamma_th, d_th, Omega_k, UT_k, DT_k, eta_kth, BigMy, BigMP,\
		integral_kis, D_ssp, probability,\
		integral_ki_exped