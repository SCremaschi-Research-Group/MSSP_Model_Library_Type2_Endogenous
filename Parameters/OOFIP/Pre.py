import pandas as pd
import random
import itertools
import numpy as np
import copy

def Parameter_setting(MD):
	
	# sets
	F =	MD.sets['F']
	FPSO = MD.sets['FPSO']
	RF = MD.sets['rf']
	F_rf = MD.sets['F_rf']
	F_fpso = MD.sets['F_fpso']
	F_fpsoLIST = []
	for fpso in FPSO:
		for fp in F_fpso[fpso]:
			F_fpsoLIST.append((fpso,fp))
	# print('F_fpsoLIST=', F_fpsoLIST)
	I = MD.sets['I']
	Iend = I[-1]
	T = MD.sets['T']
	Tend = T[-1]
	T1 = MD.sets['T1']
	TC = sorted(list(set(T) - set(T1)), reverse=False)
	
	##### Other deterministic parameters #####
	FC_ffpso = MD.parameters['FC_ffpso']
	FC_ffpsot = {}
	for f in F:
		for fpso in FPSO:
			for t in T:
				FC_ffpsot[f,fpso,t] = FC_ffpso[f,fpso]
	# print('FC_ffpsot =', FC_ffpsot)
	
	FCwell_f = MD.parameters['FCwell_f']
	FCwell_ft = {}
	for f in F:
		for t in T:
			FCwell_ft[f,t] = FCwell_f[f]
	# print('FCwell_ft =', FCwell_ft)

	FCFPSO_fpso = MD.parameters['FCFPSO_fpso']
	FCFPSO_fpsot = {}
	for fpso in FPSO:
		for t in T:
			FCFPSO_fpsot[fpso,t] = FCFPSO_fpso[fpso]
	# print('FCFPSO_fpsot =', FCFPSO_fpsot)
	
	VCliq_fpso = MD.parameters['VCliq_fpso']
	VCliq_fpsot = {}
	for fpso in FPSO:
		for t in T:
			VCliq_fpsot[fpso,t] = VCliq_fpso[fpso]
	# print('VCliq_fpsot =', VCliq_fpsot)
	
	VCgas_fpso = MD.parameters['VCgas_fpso']
	VCgas_fpsot = {}
	for fpso in FPSO:
		for t in T:
			VCgas_fpsot[fpso,t] = VCgas_fpso[fpso]
	# print('VCgas_fpsot =', VCgas_fpsot)
	
	OCliq_rf = MD.parameters['OCliq_rf']
	OCliq_rft = {}
	for rf in RF:
		for t in T:
			OCliq_rft[rf,t] = OCliq_rf[rf]
	# print('OCliq_rft =', OCliq_rft)
	
	OCgas_rf = MD.parameters['OCgas_rf']
	OCgas_rft = {}
	for rf in RF:
		for t in T:
			OCgas_rft[rf,t] = OCgas_rf[rf]
	# print('OCgas_rft =', OCgas_rft)
	
	ftax_rf = MD.parameters['ftax_rf']
	ftax_rft = {}
	for rf in RF:
		for t in T:
			ftax_rft[rf,t] = ftax_rf[rf]
	# print('ftax_rft =', ftax_rft)
	
	fPO_rfi = MD.parameters['fPO_rfi']
	Loil_rfi = MD.parameters['Loil_rfi']
	Uoil_rfi = MD.parameters['Uoil_rfi']
	
	fCR_rf = MD.parameters['fCR_rf']
	fCR_rft = {}
	for rf in RF:
		for t in T:
			fCR_rft[rf,t] = fCR_rf[rf]
	# print('fCR_rft =', fCR_rft)
	
	alpha = MD.parameters['alpha']
	alpha_t = {}
	for t in T:
		alpha_t[t] = alpha
	# print('alpha_t =', alpha_t)
	
	l1 = MD.parameters['l1']
	l2 = MD.parameters['l2']
	
	Uoil_fpso = MD.parameters['Uoil_fpso']
	Uliq_fpso =	MD.parameters['Uliq_fpso']
	Ugas_fpso =	MD.parameters['Ugas_fpso']
	myu = MD.parameters['myu']
	UIwell = MD.parameters['UIwell']
	UIwell_t = {}
	for t in T:
		UIwell_t[t] = UIwell
	# print('UIwell_t =', UIwell_t)
	UNwell_f = MD.parameters['UNwell_f']
	
	k = 1
	while 2**(k-1) <= max(UNwell_f.values()):
		k += 1
	Kend = k - 1
	# print('Kend =', Kend)
	K = list(range(1,Kend+1))
	# print('K =', K)
	
	epsilon = MD.parameters['epsilon']
	
	dis_t = MD.parameters['dis_t']
	# print('dis_t =', dis_t)
	delta = MD.parameters['delta']
	delta_t = {}
	for t in T:
		delta_t[t] = delta
	# print('delta_t =', delta_t)
	
	# Big_M =	MD.parameters['Big_M']
	Big_M = max(FCFPSO_fpsot.values()) + max(VCliq_fpsot.values())*2*max(Uliq_fpso.values()) +  max(VCgas_fpsot.values())*2*max(Ugas_fpso.values())
	Big_U =	Big_M # MD.parameters['Big_U']
	# print('Big_M =', Big_M)
	
	# uncertain parameters
	FieldSize = MD.uncertain['FieldSize']
	alpha_o_fs = MD.uncertain['alpha_o_fs']
	alpha_wc_fs = MD.uncertain['alpha_wc_fs']
	alpha_gc_fs = MD.uncertain['alpha_gc_fs']
	
	# Generate all outcomes
	Un_param = {}
	for f in F:
		Un_param[str(f)+'_FieldSize'] = []
		for SrNo in FieldSize[f].values():
			Un_param[str(f)+'_FieldSize'].append(SrNo)
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
	FieldSize_prob = MD.uncertain['FieldSize_prob']
	Un_prob = {}
	for f in F:
		Un_prob[str(f)+'_FieldSize'] = {}
		for SrNo in FieldSize_prob[f]:
			Un_prob[str(f)+'_FieldSize'][FieldSize[f][SrNo]] = FieldSize_prob[f][SrNo]
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
	
	alpha_owg = {}
	for s in S:
		alpha_owg[s]={}
		for f in F:
			alpha_owg[s][str(f)+'_alpha_o'] = alpha_o_fs[f,s]
			alpha_owg[s][str(f)+'_alpha_wc'] = alpha_wc_fs[f,s]
			alpha_owg[s][str(f)+'_alpha_gc'] = alpha_gc_fs[f,s]
	# print('alpha_owg =', alpha_owg)
	
	for s in S:
		scenario_param[s][1].update(alpha_owg[s])
	# print('scenario_param =', scenario_param)
	
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
	
	D_ssp = {}
	for s in S:
		for sp in S:
			if s<sp:
				D_ssp[s,sp] = []
				for f in F:
					if scenario_param[s][1][str(f)+'_FieldSize'] != scenario_param[sp][1][str(f)+'_FieldSize']\
						or scenario_param[s][1][str(f)+'_alpha_o'] != scenario_param[sp][1][str(f)+'_alpha_o']\
						or scenario_param[s][1][str(f)+'_alpha_wc'] != scenario_param[sp][1][str(f)+'_alpha_wc']\
						or scenario_param[s][1][str(f)+'_alpha_gc'] != scenario_param[sp][1][str(f)+'_alpha_gc']:
						D_ssp[s,sp].append(f)
	# print('D_ssp =', D_ssp)
	
	##### dictionary to csv #####
	# import csv
	# with open('D_ssp.csv', 'w', newline="") as f:  
	# 	writer = csv.writer(f)
	# 	for k, v in D_ssp.items():
	# 		writer.writerow([k, v])
	
	REC_fs = {}
	for f in F:
		for s in S:
			REC_fs[f,s] = scenario_param[s][1][str(f)+'_FieldSize']
	# print('REC_fs =', REC_fs)
	
	REC_f_exped = {}
	for f in F:
		REC_f_exped[f] = 0
		for s in S:
			REC_f_exped[f] += scenario_param[s][0]*REC_fs[f,s]
	# print("REC_f_exped =", REC_f_exped)
	
	alpha_o_f_exped = {}
	for f in F:
		alpha_o_f_exped[f] = 0
		for s in S:
			alpha_o_f_exped[f] += scenario_param[s][0]*alpha_o_fs[f,s]
	# print("alpha_o_f_exped =", alpha_o_f_exped)
	
	alpha_wc_f_exped = {}
	for f in F:
		alpha_wc_f_exped[f] = 0
		for s in S:
			alpha_wc_f_exped[f] += scenario_param[s][0]*alpha_wc_fs[f,s]
	# print("alpha_wc_f_exped =", alpha_wc_f_exped)
	
	alpha_gc_f_exped = {}
	for f in F:
		alpha_gc_f_exped[f] = 0
		for s in S:
			alpha_gc_f_exped[f] += scenario_param[s][0]*alpha_gc_fs[f,s]
	# print("alpha_gc_f_exped =", alpha_gc_f_exped)
	
	a_oil_ffpso = MD.parameters['a_oil_ffpso']
	b_oil_ffpso = MD.parameters['b_oil_ffpso']
	c_oil_ffpso = MD.parameters['c_oil_ffpso']
	d_oil_ffpso = MD.parameters['d_oil_ffpso']
	a_wor_ffpso	= MD.parameters['a_wor_ffpso']
	b_wor_ffpso = MD.parameters['b_wor_ffpso']
	c_wor_ffpso = MD.parameters['c_wor_ffpso']
	d_wor_ffpso = MD.parameters['d_wor_ffpso']
	a_gor_ffpso = MD.parameters['a_gor_ffpso']
	b_gor_ffpso = MD.parameters['b_gor_ffpso']
	c_gor_ffpso = MD.parameters['c_gor_ffpso']
	d_gor_ffpso = MD.parameters['d_gor_ffpso']
	
	a_wc_ffpsos = {}
	for f in F:
		for fpso in FPSO:
			for s in S:
				a_wc_ffpsos[f,fpso,s] = a_wor_ffpso[f,fpso]*REC_fs[f,s]*1/4
	# print('a_wc_ffpsos =', a_wc_ffpsos)
	b_wc_ffpsos = {}
	for f in F:
		for fpso in FPSO:
			for s in S:
				b_wc_ffpsos[f,fpso,s] = b_wor_ffpso[f,fpso]*REC_fs[f,s]*1/3
	# print('b_wc_ffpsos =', b_wc_ffpsos)
	c_wc_ffpsos = {}
	for f in F:
		for fpso in FPSO:
			for s in S:
				c_wc_ffpsos[f,fpso,s] = c_wor_ffpso[f,fpso]*REC_fs[f,s]*1/2
	# print('c_wc_ffpsos =', c_wc_ffpsos)
	d_wc_ffpsos = {}
	for f in F:
		for fpso in FPSO:
			for s in S:
				d_wc_ffpsos[f,fpso,s] = d_wor_ffpso[f,fpso]*REC_fs[f,s]
	# print('d_wc_ffpsos =', d_wc_ffpsos)

	a_wc_ffpso_exped = {}
	for f in F:
		for fpso in FPSO:
			a_wc_ffpso_exped[f,fpso] = a_wor_ffpso[f,fpso]*REC_f_exped[f]*1/4
	# print('a_wc_ffpso_exped =', a_wc_ffpso_exped)
	b_wc_ffpso_exped = {}
	for f in F:
		for fpso in FPSO:
			b_wc_ffpso_exped[f,fpso] = b_wor_ffpso[f,fpso]*REC_f_exped[f]*1/3
	# print('b_wc_ffpso_exped =', b_wc_ffpso_exped)
	c_wc_ffpso_exped = {}
	for f in F:
		for fpso in FPSO:
			c_wc_ffpso_exped[f,fpso] = c_wor_ffpso[f,fpso]*REC_f_exped[f]*1/2
	# print('c_wc_ffpso_exped =', c_wc_ffpso_exped)
	d_wc_ffpso_exped = {}
	for f in F:
		for fpso in FPSO:
			d_wc_ffpso_exped[f,fpso] = d_wor_ffpso[f,fpso]*REC_f_exped[f]
	# print('d_wc_ffpso_exped =', d_wc_ffpso_exped)
	
	Big_Mwc_ffpsos = {}
	for f in F:
		for fpso in FPSO:
			for s in S:
				Big_Mwc_ffpsos[f,fpso,s] = alpha_wc_fs[f,s]*(a_wc_ffpsos[f,fpso,s] + b_wc_ffpsos[f,fpso,s] + c_wc_ffpsos[f,fpso,s] + d_wc_ffpsos[f,fpso,s])
	# print('Big_Mwc_ffpsos =', Big_Mwc_ffpsos)
	
	Big_Mwc_ffpso_exped = {}
	for f in F:
		for fpso in FPSO:
			Big_Mwc_ffpso_exped[f,fpso] = alpha_wc_f_exped[f]*(a_wc_ffpso_exped[f,fpso] + b_wc_ffpso_exped[f,fpso] + c_wc_ffpso_exped[f,fpso] + d_wc_ffpso_exped[f,fpso])
	# print('Big_Mwc_ffpso_exped =', Big_Mwc_ffpso_exped)
	
	a_gc_ffpsos = {}
	for f in F:
		for fpso in FPSO:
			for s in S:
				a_gc_ffpsos[f,fpso,s] = a_gor_ffpso[f,fpso]*REC_fs[f,s]*1/4
	# print('a_gc_ffpsos =', a_gc_ffpsos)
	b_gc_ffpsos = {}
	for f in F:
		for fpso in FPSO:
			for s in S:
				b_gc_ffpsos[f,fpso,s] = b_gor_ffpso[f,fpso]*REC_fs[f,s]*1/3
	# print('b_gc_ffpsos =', b_gc_ffpsos)
	c_gc_ffpsos = {}
	for f in F:
		for fpso in FPSO:
			for s in S:
				c_gc_ffpsos[f,fpso,s] = c_gor_ffpso[f,fpso]*REC_fs[f,s]*1/2
	# print('c_gc_ffpsos =', c_gc_ffpsos)
	d_gc_ffpsos = {}
	for f in F:
		for fpso in FPSO:
			for s in S:
				d_gc_ffpsos[f,fpso,s] = d_gor_ffpso[f,fpso]*REC_fs[f,s]
	# print('d_gc_ffpsos =', d_gc_ffpsos)
	
	a_gc_ffpso_exped = {}
	for f in F:
		for fpso in FPSO:
			a_gc_ffpso_exped[f,fpso] = a_gor_ffpso[f,fpso]*REC_f_exped[f]*1/4
	# print('a_gc_ffpso_exped =', a_gc_ffpso_exped)
	b_gc_ffpso_exped = {}
	for f in F:
		for fpso in FPSO:
			b_gc_ffpso_exped[f,fpso] = b_gor_ffpso[f,fpso]*REC_f_exped[f]*1/3
	# print('b_gc_ffpso_exped =', b_gc_ffpso_exped)
	c_gc_ffpso_exped = {}
	for f in F:
		for fpso in FPSO:
			c_gc_ffpso_exped[f,fpso] = c_gor_ffpso[f,fpso]*REC_f_exped[f]*1/2
	# print('c_gc_ffpso_exped =', c_gc_ffpso_exped)
	d_gc_ffpso_exped = {}
	for f in F:
		for fpso in FPSO:
			d_gc_ffpso_exped[f,fpso] = d_gor_ffpso[f,fpso]*REC_f_exped[f]
	# print('d_gc_ffpso_exped =', d_gc_ffpso_exped)

	Big_Mgc_ffpsos = {}
	for f in F:
		for fpso in FPSO:
			for s in S:
				Big_Mgc_ffpsos[f,fpso,s] = alpha_gc_fs[f,s]*(a_gc_ffpsos[f,fpso,s] + b_gc_ffpsos[f,fpso,s] + c_gc_ffpsos[f,fpso,s] + d_gc_ffpsos[f,fpso,s])
	# print('Big_Mgc_ffpsos =', Big_Mgc_ffpsos)
	
	Big_Mgc_ffpso_exped = {}
	for f in F:
		for fpso in FPSO:
			Big_Mgc_ffpso_exped[f,fpso] = alpha_gc_f_exped[f]*(a_gc_ffpso_exped[f,fpso] + b_gc_ffpso_exped[f,fpso] + c_gc_ffpso_exped[f,fpso] + d_gc_ffpso_exped[f,fpso])
	# print('Big_Mgc_ffpso_exped =', Big_Mgc_ffpso_exped)

	Big_Uwelloil_ffpso = {}
	for f in F:
		for fpso in FPSO:
			Big_Uwelloil_ffpso[f,fpso] = max(alpha_o_fs.values())*d_oil_ffpso[f,fpso]
	# print('Big_Uwelloil_ffpso =', Big_Uwelloil_ffpso)

	N1_f = MD.uncertain['N1_f']
	N2_f = MD.uncertain['N2_f']
	
	max_REC = max(REC_fs.values())
	min_REC = min(REC_fs.values())
	# print('max_REC =', max_REC)
	# print('min_REC =', min_REC)
	
	return F, FPSO, RF, F_rf, F_fpso, F_fpsoLIST, I, Iend, T, T1, TC, Tend, K, S,\
		FC_ffpsot, FCwell_ft, FCFPSO_fpsot, VCliq_fpsot, VCgas_fpsot, OCgas_rft, OCliq_rft, ftax_rft, fPO_rfi, fCR_rft, Loil_rfi, Uoil_rfi, alpha_t, l1,l2,\
		a_oil_ffpso, b_oil_ffpso, c_oil_ffpso, d_oil_ffpso, dis_t, delta_t, Big_M, Big_U, Big_Uwelloil_ffpso, Uoil_fpso, Uliq_fpso, Ugas_fpso, myu, UIwell_t, UNwell_f, max_REC, min_REC, epsilon, a_wor_ffpso,b_wor_ffpso, c_wor_ffpso,d_wor_ffpso, a_gor_ffpso, b_gor_ffpso, c_gor_ffpso, d_gor_ffpso,\
		REC_fs, alpha_o_fs, alpha_wc_fs, alpha_gc_fs, a_wc_ffpsos, b_wc_ffpsos, c_wc_ffpsos, d_wc_ffpsos, a_gc_ffpsos, b_gc_ffpsos, c_gc_ffpsos, d_gc_ffpsos, Big_Mwc_ffpsos, Big_Mgc_ffpsos, N1_f, N2_f, D_ssp, probability,\
		REC_f_exped, alpha_o_f_exped, alpha_wc_f_exped, alpha_gc_f_exped, a_wc_ffpso_exped, b_wc_ffpso_exped, c_wc_ffpso_exped, d_wc_ffpso_exped, a_gc_ffpso_exped, b_gc_ffpso_exped, c_gc_ffpso_exped, d_gc_ffpso_exped, Big_Mwc_ffpso_exped, Big_Mgc_ffpso_exped
