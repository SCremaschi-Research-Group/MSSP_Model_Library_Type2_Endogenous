import pandas as pd
import random

def Parameter_setting(MD, Case_csv):
	
	# sets
	S = MD.sets['S'] # Scenarios
	I = MD.sets['I'] # Customers
	J = MD.sets['J'] # Returns to the depot R + customers I
	K = MD.sets['K'] # I + R + 1, Stages of decision making process
	
	# Deterministic parameters
	R = MD.parameters['R'] # Returns to the depot R
	r_set = MD.parameters['r_set']
	I_end = I[-1]
	K_end = K[-1]
	S_start = S[0]
	S_end = S[-1]
	I_end = I[-1]
	J_start = J[0]
	J_end = J[-1]
	K_end = K[-1]
	
	Q = MD.parameters['Q'] # Capacity of the vehicle
	# print("Q =:", Q)
	
	# uncertain parameters
	d_js = MD.uncertain['d_js'] # Demands of j (Depot + Start point + Customers) under scenario s
	if d_js == {}:
		dd= pd.read_csv(Case_csv) # If you want to ignore the header, add ", header=None"
		for j in range(len(dd['J'])): # Replace all demands to -Q if j < 0
			if dd['J'][j] < 0:
				dd['d'][j] = -Q
		d_js = dict((tuple((a, b)), c) for a,b,c in dd.values)
	# print('d_js =', d_js)
	
	# Probability of scenario s (equal probability)
	p_s = MD.uncertain['p_s']
	if p_s == {}:
		for s in S:
			p_s[s] = 1/len(S)
	#print(p_s)
	
	d_j_exped = {} # Expected demand for all scenarios
	for j in range(J_start, J_end+1):
		d_j_exped[j] = 0
		for s in range(S_start, S_end+1):
			d_j_exped[j] += p_s[s]*d_js[(j,s)]
	# print("d_j_exped =", d_j_exped)
	
	# Create scenario-wise parameter dictionary
	All_outcomes = {}
	scenario_param = {}
	for s in S:
		All_outcomes[s] = {}
		for j in J:
			All_outcomes[s][j] = d_js[j,s]
			# print('All_outcomes =', All_outcomes)
		scenario_param[s] = (p_s[s], All_outcomes[s])
	# print('scenario_param =', scenario_param)
	
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
	
	random.seed(314) # set the random seed
	f_jjp = MD.parameters['f_jjp'] # Travel cost from j to j'
	if f_jjp == {}:
		for j in J:
			for jp in J:
				if j<=0 and jp<=0:
					f_jjp[j,jp] = 0
				else:
					f_jjp[j,jp] = round(random.uniform(0.5, 1.5),2) # use the following to make the cost random values
	# print(f_jjp)
	
	A_extractor = {} # Extractor for all meaningful (j,j',k)
	# (5) customer to dummy
	for j in I:
		for r in list(range(1,R+1)): # jp = -r, r denotes dummy node
			for k in range(2*r, I_end+r+1):
				A_extractor[j,-r,k] = 1
	
	# (6) dummy to customer
	for r in list(range(1,R+1)):
		for jp in I:
			for k in range(2*r +1, I_end+r+1):
				A_extractor[-r,jp,k] = 1
	
	# (2) 0 to customer, and 0 to dummy(NA)
	for j in J:
		if j<=I_end and j>=1:
			A_extractor[0,j,1] = 1
	
	# (3) dummy to 0, and customer to 0
	for j in J:
		if j == -R:
			A_extractor[j,0,K_end] = 1
		if j<=I_end and j>=1:
			A_extractor[j,0,K_end] = 1
	
	# (4) dummy to dummy
	for (j,jp) in r_set:
		A_extractor[j,jp,-j+I_end+1] = 1
	
	# cutomer to customer - (1)
	for j in list(range(1,I_end+1)):
		for jp in list(range(1,I_end+1)):
			for k in K:
				if j != jp and k>1:
					A_extractor[j,jp,k] = 1
	# print('A_extractor =' A_extractor)
	
	D_ssp = {} # Customers who have different demands in two scenarios
	for s in S:
		for sp in S:
			for j in I:
				if d_js[j,s] != d_js[j,sp]:
					try:
						D_ssp[s,sp].append(j)
					except KeyError:
						D_ssp[s,sp] = [j]
	# print(D_ssp)
	
	n = {} # The number of customers who have the same demands between s and s'
	for s in S:
		for sp in S:
			if s != sp:
				n[s,sp] = I_end - len(D_ssp[s,sp])
	# print(n)
	
	k_ssp = {} # Two scenarios s and s' may stay indistinguishable until at most the (ks,s')th stage
	for s in S:
		for sp in S:
			if s != sp:
				k_ssp[s,sp] = min(2*n[s,sp], n[s,sp] + R) + 1
			if s == sp:
				k_ssp[s,sp] = K_end # s = sp
	# print(k_ssp)
	
	A = {(j,jp,k) for (j,jp,k) in A_extractor} # Set of all meaningful (j,j',k)
	C = {(jp,k) for j,jp,k in A} # Set of all meaningful (j',k)

	# print('A =', A)
	# print('B =', B)
	
	##### Parameters for complete recouse #####
	Cp = MD.parameters['Cp']
	
	
	
	##### Set for GKDA #####
	B = ()
	for j_jp_k in A:
		if j_jp_k[:-1] not in B:
			B += (j_jp_k[:-1],)
	# print("B =",B)

	# print(JpK)
	return K, K_end, J, S, A, C, B,\
		f_jjp, R, Q, d_js, D_ssp, k_ssp, probability, Cp,\
		d_j_exped