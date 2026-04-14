import pandas as pd
import random
import itertools

def Parameter_setting(MD, Case_csv):
	
	# sets
	I = MD.sets['I'] # Aggregates
	S = MD.sets['S'] # Scenarios

	# Parameters
	p_s = MD.make['p_s'] # Probability
	c1_t= MD.make['c1_t'] # Revenue of sold metal
	cmng_t = MD.make['cmng_t'] # Cost for rock mining
	cproc_t = MD.make['cproc_t'] # Cost for rock processing
	P_ave = MD.make['P_ave'] # Rock processing capacity
	M_ave = MD.make['M_ave'] # Rock mining capacity
	CMadd = MD.parameters['CMadd']

	# Check parameters in Case_data. If not, generate test parameters
	if p_s == {}:
		for s in S:
			p_s[s] = 1/len(S)
	# print("p_s =", p_s)
	
	# uncertain parameters
	a0a1= pd.read_csv(Case_csv) # If you want to ignore the header, add ", header=None"
	a0_is = dict((tuple((a, b)), c) for a,b,c,d in a0a1.values)
	a1_is = dict((tuple((a, b)), d) for a,b,c,d in a0a1.values)
	# print("a0_is =", a0_is)
	# print("a1_is =", a1_is)
	
	g_is = {} # grade
	for i_s in a1_is:
		g_is[i_s] = a1_is[i_s]/a0_is[i_s]
	# print("g_is =", g_is)
	
	# Create scenario-wise parameter dictionary
	All_outcomes = {}
	scenario_param = {}
	for s in S:
		All_outcomes[s] = {}
		for i in I:
			All_outcomes[s][i] = g_is[i,s]
			# print('All_outcomes =', All_outcomes)
		scenario_param[s] = (p_s[s], All_outcomes[s])
	# print('scenario_param =', scenario_param)
	
	probability = {}
	for s in scenario_param:
		probability[s] = scenario_param[s][0]
	# print('probability =', probability)
	
	Ave_a0 = sum(a0_is.values())/len(a0_is)
	# a0 = MD.parameters['a0'] # Total amount of rock
	# print("Ave_a0 =:", Ave_a0)

	Total_a0 = Ave_a0*len(I)
	T_end = int(round(Total_a0/M_ave))+1
	# print("Total_rock =", Total_a0, "Mining_cap_ave =", M_ave, "T_end =", T_end)
	T = range(1,T_end+1)
	
	random.seed(314) # set the random seed
	M_t = {}
	P_t = {}
	cmng_t = {}
	cproc_t = {}
	c1_t = {}
	for t in T:
		if t not in cmng_t:
			cmng_t[t] = round(random.uniform(0.5, 1.5),2) # Cost for rock mining
		if t not in cproc_t:
			cproc_t[t] = round(random.uniform(6, 12),1) # Cost for rock processing
		if t not in c1_t:
			c1_t[t] = round(random.uniform(45, 55),1) # Revenue of sold metal
		M_t[t] = round(random.uniform(M_ave-M_ave*0.2, M_ave+M_ave*0.2),1) # Rock mining capacity
		P_t[t] = round(random.uniform(P_ave-P_ave*0.1, P_ave+P_ave*0.1),1) # Rock processing capacity
	# print("cmng_t =", cmng_t)
	# print("cproc_t =", cproc_t)
	# print("c1_t =", c1_t)
	# print("M_t =", M_t)
	
	Precedence_ij = MD.parameters['Precedence'] # j must be mined before i
	
	IJ = {}
	for i in Precedence_ij:
		for j in Precedence_ij[i]:
			IJ[i,j] = 1
	# print('IJ =', IJ)
	
	a1_i_exped = {} # Averaged a1 for aggregate i
	for i in I:
		a1_i_exped[i,] = 0
		for s in S:
			a1_i_exped[i,] += p_s[s]*a1_is[(i,s)]
	# print("a1_i_exped =", a1_i_exped)
	
	a0_i_exped = {} # Averaged a0 for aggregate i
	for i in I:
		a0_i_exped[i,] = 0
		for s in S:
			a0_i_exped[i,] += p_s[s]*a0_is[(i,s)]
	# print("a0_i_exped =", a0_i_exped)
	
	D_ssp = {} ######## Remove s = sp case and s>sp case
	for i in I:
		for s in S:
			for sp in S:
				if s!=sp:
					D_ssp[s,sp] = []
	for i in I:
		for s in S:
			for sp in S:
				if s!=sp:
					if g_is[i,s] != g_is[i,sp]:
						D_ssp[s,sp].append(i)
	# print("D_ssp =", D_ssp)
	
	# Only for GKDA to modify a0_i and a1_i considering the precidence relationship.
	linkage_i = {}
	for i in I:
		linkage_i[i] = [i]
	# print(linkage_i)
	
	for i in linkage_i:
		len_before = 0
		len_after = 1
		while len_before != len_after:
			len_before = len(linkage_i[i])
			for ipp in linkage_i[i]:
				for ip in Precedence_ij:
					if ipp in Precedence_ij[ip] and ip not in linkage_i[i]:
						linkage_i[i].append(ip)
			len_after = len(linkage_i[i])
		linkage_i[i] = tuple(sorted(linkage_i[i]))
	# print('linkage_i =', linkage_i)
	
	return T, T_end, I, S, cmng_t, cproc_t, c1_t, M_t, P_t, a0_is, a0_i_exped, a1_is, a1_i_exped, g_is, D_ssp, IJ, scenario_param, probability, CMadd, Precedence_ij, linkage_i
	
	##### dictionary to csv #####
	# import csv
	# with open('dict.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in D.items():
	# 		writer.writerow([k, v])
