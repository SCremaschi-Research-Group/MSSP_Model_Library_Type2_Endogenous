import os
from pyomo.environ import *
from pyomo.opt import SolverFactory
import time as timer
import shutil

def MSSP_model(WP, PP, T, S, theta1_wps, theta2_wps, probability, delta_t, shrink, D_ssp, L1, P_t,
		M_wp, M_pp, M_wpwp, M_wppp, FCC_wp, FCC_pp, FCC_wpwp, FCC_wppp, VCC_wp, VCC_pp, FOC_wp, FOC_pp, VOC_wp, VOC_pp, alpha_t, Max_theta2):
	
	model = ConcreteModel()
	
	# Uncertain parameters 
	model.theta1_wps = Param(WP,S, initialize = theta1_wps, mutable=True)
	model.theta2_wps = Param(WP,S, initialize = theta2_wps, mutable=True)
	
	# Post-realization decision variables and differentiator variables
	model.b_wpts = Var(WP,T,S, within=Binary)

	# Post-realization decision variables
	model.b_ppts = Var(PP,T,S, within=Binary)
	model.b_wpwppts = Var(WP,WP,T,S, within=Binary)
	model.b_wpppts = Var(WP,PP,T,S, within=Binary)
	model.e_wpts = Var(WP,T,S, within=NonNegativeReals)
	model.e_ppts = Var(PP,T,S, within=NonNegativeReals)
	
	# At-realization decision variables
	model.qprod_wpts = Var(WP,T,S, within=NonNegativeReals)
	
	# Other variables
	model.cap_wpts = Var(WP,T,S, within=NonNegativeReals)
	model.cap_ppts = Var(PP,T,S, within=NonNegativeReals)
	model.CCtot_ts = Var(T,S)
	model.NPV_s = Var(S)
	model.OCtot_ts = Var(T,S)
	model.qcum_wpts = Var(WP,T,S, within=NonNegativeReals)
	model.qdeliv_wpts = Var(WP,T,S, within=NonNegativeReals)
	model.qout_wpts = Var(WP,T,S, within=NonNegativeReals)
	model.qout_ppts = Var(PP,T,S, within=NonNegativeReals)
	model.qout_wpwppts = Var(WP,WP,T,S, within=NonNegativeReals)
	model.qout_wpppts = Var(WP,PP,T,S, within=NonNegativeReals)
	model.qshr_ts = Var(T,S, within=NonNegativeReals)
	model.Revtot_ts = Var(T,S)
	
	# Indicator variable
	model.Z_tssp = Var(T,S,S, within=Binary)
	
	def B1_1(model):
		return sum(probability[s]*model.NPV_s[s] for s in S)
	model.objective = Objective(sense=maximize, rule=B1_1)
	# model.objective.pprint()
	
	def B2_2(model,wp,t,s):
		return model.qdeliv_wpts[wp,t,s]/model.theta2_wps[wp,s] + model.qcum_wpts[wp,t,s]/model.theta1_wps[wp,s] == 1
	model.B2_2 = Constraint(WP,T,S, rule = B2_2)
	# model.B2_2.pprint()
	
	def B3_3(model,wp,t,s):
		return model.qcum_wpts[wp,t,s] == sum(model.qprod_wpts[wp,tau,s]*delta_t[tau] for tau in T if tau <= t)
	model.B3_3 = Constraint(WP,T,S, rule = B3_3)
	# model.B3_3.pprint()
	
	def B4_4(model,wp,t,s):
		return model.qprod_wpts[wp,t,s] <= model.qdeliv_wpts[wp,t,s]
	model.B4_4 = Constraint(WP,T,S, rule = B4_4)
	# model.B4_4.pprint()
	
	def B5_5(model,wp,t,s):
		return model.qout_wpts[wp,t,s] == model.qprod_wpts[wp,t,s] + sum(model.qout_wpwppts[wpp,wp,t,s] for wpp in WP)
	model.B5_5 = Constraint(WP,T,S, rule = B5_5)
	# model.B5_5.pprint()

	def B6_6(model,wp,t,s):
		return model.qout_wpts[wp,t,s] == sum(model.qout_wpwppts[wp,wpp,t,s] for wpp in WP) + sum(model.qout_wpppts[wp,pp,t,s] for pp in PP)
	model.B6_6 = Constraint(WP,T,S, rule = B6_6)
	# model.B6_6.pprint()

	def B7_7(model,pp,t,s):
		return model.qout_ppts[pp,t,s] == sum(model.qout_wpppts[wp,pp,t,s] for wp in WP)
	model.B7_7 = Constraint(PP,T,S, rule = B7_7)
	# model.B7_7.pprint()
	
	def B8_8(model,t,s):
		return model.qshr_ts[t,s] == (1-shrink)*sum(model.qout_ppts[pp,t,s] for pp in PP)
	model.B8_8 = Constraint(T,S, rule = B8_8)
	# model.B8_8.pprint()
	
	def B9_9(model,wp,t,s):
		return model.qout_wpts[wp,t,s] <= model.cap_wpts[wp,t,s]
	model.B9_9 = Constraint(WP,T,S, rule = B9_9)
	# model.B9_9.pprint()
	
	def B10_10(model,pp,t,s):
		return model.qout_ppts[pp,t,s] <= model.cap_ppts[pp,t,s]
	model.B10_10 = Constraint(PP,T,S, rule = B10_10)
	# model.B10_10.pprint()
	
	def B11_11(model,wp,t,s):
		if t>=2:
			return model.cap_wpts[wp,t,s] == model.cap_wpts[wp,t-1,s] + model.e_wpts[wp,t,s]
		else:
			return model.cap_wpts[wp,t,s] == model.e_wpts[wp,t,s]
	model.B11_11 = Constraint(WP,T,S, rule = B11_11)
	# model.B11_11.pprint()
	
	def B12_12(model,pp,t,s):
		if t>=2:
			return model.cap_ppts[pp,t,s] == model.cap_ppts[pp,t-1,s] + model.e_ppts[pp,t,s]
		else:
			return model.cap_ppts[pp,t,s] == model.e_ppts[pp,t,s]
	model.B12_12 = Constraint(PP,T,S, rule = B12_12)
	# model.B12_12.pprint()
	
	def B13_13(model,wp,t,s):
		return model.e_wpts[wp,t,s] <= M_wp[wp]*model.b_wpts[wp,t,s]
	model.B13_13 = Constraint(WP,T,S, rule = B13_13)
	# model.B13_13.pprint()
	
	def B14_14(model,pp,t,s):
		return model.e_ppts[pp,t,s] <= M_pp[pp]*model.b_ppts[pp,t,s]
	model.B14_14 = Constraint(PP,T,S, rule = B14_14)
	# model.B14_14.pprint()
	
	def B15_15(model,wp,wpp,t,s):
		return model.qout_wpwppts[wp,wpp,t,s] <= M_wpwp[wp,wpp]*sum(model.b_wpwppts[wp,wpp,tau,s] for tau in T if tau <= t)
	model.B15_15 = Constraint(WP, WP, T, S, rule = B15_15)
	# model.B15_15.pprint()
	
	def B16_16(model,wp,pp,t,s):
		return model.qout_wpppts[wp,pp,t,s] <= M_wppp[wp,pp]*sum(model.b_wpppts[wp,pp,tau,s] for tau in T if tau <= t)
	model.B16_16 = Constraint(WP,PP,T,S, rule = B16_16)
	# model.B16_16.pprint()
	
	def B17_17(model,wp,s):
		return sum(model.b_wpts[wp,t,s] for t in T) <= 1
	model.B17_17 = Constraint(WP,S, rule = B17_17)
	# model.B17_17.pprint()
	
	def B18_18(model,pp,s):
		return sum(model.b_ppts[pp,t,s] for t in T) <= 1
	model.B18_18 = Constraint(PP,S, rule = B18_18)
	# model.B18_18.pprint()
	
	def B19_19(model,wp,wpp,s):
		return sum(model.b_wpwppts[wp,wpp,t,s] for t in T) <= 1
	model.B19_19 = Constraint(WP,WP,S, rule = B19_19)
	# model.B19_19.pprint()
	
	def B20_20(model,wp,pp,s):
		return sum(model.b_wpppts[wp,pp,t,s] for t in T) <= 1
	model.B20_20 = Constraint(WP,PP,S, rule = B20_20)
	# model.B20_20.pprint()
	
	def B21_21(model,wp,t,s):
		return model.b_wpts[wp,t,s] == sum(model.b_wpwppts[wp,wpp,t,s] for wpp in WP) + sum(model.b_wpppts[wp,pp,t,s] for pp in PP)
	model.B21_21 = Constraint(WP,T,S, rule = B21_21)
	# model.B21_21.pprint()
	
	def B22_22(model,wp,wpp,t,s):
		return model.b_wpwppts[wp,wpp,t,s] <= sum(model.b_wpts[wpp,tau,s] for tau in T if tau <= t)
	model.B22_22 = Constraint(WP,WP,T,S, rule = B22_22)
	# model.B22_22.pprint()
	
	def B23_23(model,wp,pp,t,s):
		return model.b_wpppts[wp,pp,t,s] <= sum(model.b_ppts[pp,tau,s] for tau in T if tau <= t)
	model.B23_23 = Constraint(WP,PP,T,S, rule = B23_23)
	# model.B23_23.pprint()
	
	def B24_24(model,wp,wpp,t,s):
		return model.b_wpwppts[wp,wpp,t,s] + model.b_wpwppts[wpp,wp,t,s] <= 1
	model.B24_24 = Constraint(WP, WP, T, S, rule = B24_24)
	# model.B24_24.pprint()
	
	def B25_25(model,t,s):
		return model.CCtot_ts[t,s] == sum(FCC_wp[wp]*model.b_wpts[wp,t,s] + VCC_wp[wp]*model.e_wpts[wp,t,s] + \
										sum(FCC_wpwp[wp,wpp]*model.b_wpwppts[wp,wpp,t,s] for wpp in WP) + \
										sum(FCC_wppp[wp,pp]*model.b_wpppts[wp,pp,t,s] for pp in PP) for wp in WP) + \
								sum(FCC_pp[pp]*model.b_ppts[pp,t,s] + VCC_pp[pp]*model.e_ppts[pp,t,s] for pp in PP)
	model.B25_25 = Constraint(T, S, rule = B25_25)
	# model.B25_25.pprint()
	
	def B26_26(model,t,s):
		return model.OCtot_ts[t,s] == sum(FOC_wp[wp]*model.b_wpts[wp,t,s] + VOC_wp[wp]*model.qprod_wpts[wp,t,s] for wp in WP) + \
								sum(FOC_pp[pp]*model.b_ppts[pp,t,s] + VOC_pp[pp]*model.qout_ppts[pp,t,s] for pp in PP)
	model.B26_26 = Constraint(T,S, rule = B26_26)
	# model.B26_26.pprint()
	
	def B27_27(model,t,s):
		return model.Revtot_ts[t,s] == P_t[t]*delta_t[t]*model.qshr_ts[t,s]
	model.B27_27 = Constraint(T,S, rule = B27_27)
	# model.B27_27.pprint()
	
	def B28_28(model,s):
		return model.NPV_s[s] == sum(alpha_t[t]*(model.Revtot_ts[t,s] - model.CCtot_ts[t,s] - model.OCtot_ts[t,s]) for t in T)
	model.B28_28 = Constraint(S, rule = B28_28)
	# model.B28_28.pprint()
	
	##### Initial NACs #####
	def B29a_29a(model,wp,s,sp):
		if s<sp:
			return model.b_wpts[wp,1,s] == model.b_wpts[wp,1,sp]
		else:
			return Constraint.Skip
	model.B29a_29a = Constraint(WP,S,S, rule = B29a_29a)
	# model.B29a_29a.pprint()
	
	def B29b_29b(model,wp,s,sp):
		if s<sp:
			return model.e_wpts[wp,1,s] == model.e_wpts[wp,1,sp]
		else:
			return Constraint.Skip
	model.B29b_29b = Constraint(WP,S,S, rule = B29b_29b)
	# model.B29b_29b.pprint()
	
	def B29c_29c(model,pp,s,sp):
		if s<sp:
			return model.b_ppts[pp,1,s] == model.b_ppts[pp,1,sp]
		else:
			return Constraint.Skip
	model.B29c_29c = Constraint(PP,S,S, rule = B29c_29c)
	# model.B29c_29c.pprint()
	
	def B29d_29d(model,pp,s,sp):
		if s<sp:
			return model.e_ppts[pp,1,s] == model.e_ppts[pp,1,sp]
		else:
			return Constraint.Skip
	model.B29d_29d = Constraint(PP,S,S, rule = B29d_29d)
	# model.B29d_29d.pprint()
	
	def B29e_29e(model,wp,wpp,s,sp):
		if s<sp:
			return model.b_wpwppts[wp,wpp,1,s] == model.b_wpwppts[wp,wpp,1,sp]
		else:
			return Constraint.Skip
	model.B29e_29e = Constraint(WP,WP,S,S, rule = B29e_29e)
	# model.B29e_29e.pprint()
	
	def B29f_29f(model,wp,pp,s,sp):
		if s<sp:
			return model.b_wpppts[wp,pp,1,s] == model.b_wpppts[wp,pp,1,sp]
		else:
			return Constraint.Skip
	model.B29f_29f = Constraint(WP,PP,S,S, rule = B29f_29f)
	# model.B29f_29f.pprint()
	
	##### Indicator constraints #####
	def B30a_30a(model,wp,t,s,sp):
		if s<sp and (s,sp) in L1 and wp in D_ssp[s,sp]:
			return model.Z_tssp[t,s,sp] <= 1 - sum(model.b_wpts[wp,tau,s] for tau in T if tau <= t)
		else:
			return Constraint.Skip
	model.B30a_30a = Constraint(WP,T,S,S, rule = B30a_30a)
	# model.B30a_30a.pprint()
	
	def B30b_30b(model,wp,t,s,sp):
		if s<sp and (s,sp) in L1 and wp in D_ssp[s,sp]:
			return model.Z_tssp[t,s,sp] >= 1 - sum(model.b_wpts[wp,tau,s] for tau in T if tau <= t)
		else:
			return Constraint.Skip
	model.B30b_30b = Constraint(WP,T,S,S, rule = B30b_30b)
	# model.B30b_30b.pprint()
	
	##### Conditional NACs #####
	def B31aa_31aa(model,wp,t,s,sp):
		if s<sp and (s,sp) in L1 and t+1<=T[-1]:
			return model.b_wpts[wp,t+1,s] - model.b_wpts[wp,t+1,sp] <= 1 - model.Z_tssp[t,s,sp]
		else:
			return Constraint.Skip
	model.B31aa_31aa = Constraint(WP,T,S,S, rule = B31aa_31aa)
	# model.B31aa_31aa.pprint()
	
	def B31ab_31ab(model,wp,t,s,sp):
		if s<sp and (s,sp) in L1 and t+1<=T[-1]:
			return model.b_wpts[wp,t+1,s] - model.b_wpts[wp,t+1,sp] >= model.Z_tssp[t,s,sp] - 1
		else:
			return Constraint.Skip
	model.B31ab_31ab = Constraint(WP,T,S,S, rule = B31ab_31ab)
	# model.B31ab_31ab.pprint()
	
	def B31ba_31ba(model,wp,t,s,sp):
		if s<sp and (s,sp) in L1 and t+1<=T[-1]:
			return model.e_wpts[wp,t+1,s] - model.e_wpts[wp,t+1,sp] <= max(M_wp.values())*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.B31ba_31ba = Constraint(WP,T,S,S, rule = B31ba_31ba)
	# model.B31ba_31ba.pprint()
	
	def B31bb_31bb(model,wp,t,s,sp):
		if s<sp and (s,sp) in L1 and t+1<=T[-1]:
			return model.e_wpts[wp,t+1,s] - model.e_wpts[wp,t+1,sp] >= max(M_wp.values())*(model.Z_tssp[t,s,sp] - 1)
		else:
			return Constraint.Skip
	model.B31bb_31bb = Constraint(WP,T,S,S, rule = B31bb_31bb)
	# model.B31bb_31bb.pprint()
	
	def B31ca_31ca(model,pp,t,s,sp):
		if s<sp and (s,sp) in L1 and t+1<=T[-1]:
			return model.b_ppts[pp,t+1,s] - model.b_ppts[pp,t+1,sp] <= 1 - model.Z_tssp[t,s,sp]
		else:
			return Constraint.Skip
	model.B31ca_31ca = Constraint(PP,T,S,S, rule = B31ca_31ca)
	# model.B31ca_31ca.pprint()
	
	def B31cb_31cb(model,pp,t,s,sp):
		if s<sp and (s,sp) in L1 and t+1<=T[-1]:
			return model.b_ppts[pp,t+1,s] - model.b_ppts[pp,t+1,sp] >= model.Z_tssp[t,s,sp] - 1
		else:
			return Constraint.Skip
	model.B31cb_31cb = Constraint(PP,T,S,S, rule = B31cb_31cb)
	# model.B31cb_31cb.pprint()
	
	def B31da_31da(model,pp,t,s,sp):
		if s<sp and (s,sp) in L1 and t+1<=T[-1]:
			return model.e_ppts[pp,t+1,s] - model.e_ppts[pp,t+1,sp] <= max(M_pp.values())*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.B31da_31da = Constraint(PP,T,S,S, rule = B31da_31da)
	# model.B31da_31da.pprint()
	
	def B31db_31db(model,pp,t,s,sp):
		if s<sp and (s,sp) in L1 and t+1<=T[-1]:
			return model.e_ppts[pp,t+1,s] - model.e_ppts[pp,t+1,sp] >= max(M_pp.values())*(model.Z_tssp[t,s,sp] - 1)
		else:
			return Constraint.Skip
	model.B31db_31db = Constraint(PP,T,S,S, rule = B31db_31db)
	# model.B31db_31db.pprint()
	
	def B31ea_31ea(model,wp,wpp,t,s,sp):
		if s<sp and (s,sp) in L1 and t+1<=T[-1]:
			return model.b_wpwppts[wp,wpp,t+1,s] - model.b_wpwppts[wp,wpp,t+1,sp] <= 1 - model.Z_tssp[t,s,sp]
		else:
			return Constraint.Skip
	model.B31ea_31ea = Constraint(WP,WP,T,S,S, rule = B31ea_31ea)
	# model.B31ea_31ea.pprint()
	
	def B31eb_31eb(model,wp,wpp,t,s,sp):
		if s<sp and (s,sp) in L1 and t+1<=T[-1]:
			return model.b_wpwppts[wp,wpp,t+1,s] - model.b_wpwppts[wp,wpp,t+1,sp] >= model.Z_tssp[t,s,sp] - 1
		else:
			return Constraint.Skip
	model.B31eb_31eb = Constraint(WP,WP,T,S,S, rule = B31eb_31eb)
	# model.B31eb_31eb.pprint()
	
	def B31fa_31fa(model,wp,pp,t,s,sp):
		if s<sp and (s,sp) in L1 and t+1<=T[-1]:
			return model.b_wpppts[wp,pp,t+1,s] - model.b_wpppts[wp,pp,t+1,sp] <= 1 - model.Z_tssp[t,s,sp]
		else:
			return Constraint.Skip
	model.B31fa_31fa = Constraint(WP,PP,T,S,S, rule = B31fa_31fa)
	# model.B31fa_31fa.pprint()
	
	def B31fb_31fb(model,wp,pp,t,s,sp):
		if s<sp and (s,sp) in L1 and t+1<=T[-1]:
			return model.b_wpppts[wp,pp,t+1,s] - model.b_wpppts[wp,pp,t+1,sp] >= model.Z_tssp[t,s,sp] - 1
		else:
			return Constraint.Skip
	model.B31fb_31fb = Constraint(WP,PP,T,S,S, rule = B31fb_31fb)
	# model.B31fb_31fb.pprint()
	
	def B31ga_31ga(model,wp,t,s,sp):
		if s<sp and (s,sp) in L1:
			return model.qprod_wpts[wp,t,s] - model.qprod_wpts[wp,t,sp] <= Max_theta2*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.B31ga_31ga = Constraint(WP,T,S,S, rule = B31ga_31ga)
	# model.B31ga_31ga.pprint()
	
	def B31gb_31gb(model,wp,t,s,sp):
		if s<sp and (s,sp) in L1:
			return model.qprod_wpts[wp,t,s] - model.qprod_wpts[wp,t,sp] >= Max_theta2*(model.Z_tssp[t,s,sp] - 1)
		else:
			return Constraint.Skip
	model.B31gb_31gb = Constraint(WP,T,S,S, rule = B31gb_31gb)
	# model.B31gb_31gb.pprint()
	
	return model