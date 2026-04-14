import os
import sys
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pdb
import numpy
import itertools
import datetime
import time as timer
import shutil

def MSSP_model(Omega_S, Omega_E, Omega_Estar, Omega_L, Omega_N, Omega_O, Omega_T, Omega_G, Omega_DG, Omega_K, Omega_KT_k,
		E_end, gammaD, gammaL_o, rI_e, ro_e, w_t, kappaL_o, kappaD, Q_o, Dmax_n, f_ns, d_net, zeta_gt, K_ge, Fini_l, I_ng, L_nl, cDSR, cDG, cDR, D_ssp, Max_K, probability):
	
	model = ConcreteModel()
	
	# Uncertain parameters 
	model.f_ns = Param(Omega_N,Omega_S, initialize = f_ns, mutable=True)
	
	# Post-realization decision variables
	model.B_loes = Var(Omega_L, Omega_O, Omega_E, Omega_S, within = Binary) # Binary decision to upgrade line l
	model.D_nes = Var(Omega_N, Omega_E, Omega_S, within = Binary) # Binary decision to invest in DSR
	
	# At-realization decision variables
	model.PL_lets = Var(Omega_L, Omega_E, Omega_T, Omega_S, within=Reals) # Power flow across l (kJ/month)
	model.Xi_nets = Var(Omega_N, Omega_E, Omega_T, Omega_S, within=NonNegativeReals) # Load at bus n, shifted away from t (kJ/month)

	# Other variables and differentiator variables
	model.Dtilde_nes = Var(Omega_N, Omega_E, Omega_S, within = Binary) # Sum of all investment decisions in DSR taken in the past

	# Other variables
	model.zaiILine_s = Var(Omega_S) # Investment cost for line
	model.zaiIDSR_s = Var(Omega_S) # Investment cost for DSR
	model.zaiODSR_s = Var(Omega_S) # DSR operational cost
	model.zaiODG_s = Var(Omega_S) # DG operational cost
	model.F_loes = Var(Omega_L, Omega_O, Omega_E, Omega_S, within=NonNegativeReals) # Extra capacity by which line l is upgraded (Continuous) (kJ/month)
	model.Ftilde_loes = Var(Omega_L, Omega_O, Omega_E, Omega_S, within=NonNegativeReals) # Sum of capacity in line l taken in the past (kJ/month)
	model.T_nets = Var(Omega_N, Omega_E, Omega_T, Omega_S, within=NonNegativeReals) # Load at bus n, shifted to t from t'(!=t) (kJ/month)
	model.PG_gets = Var(Omega_G, Omega_E, Omega_T, Omega_S, within=NonNegativeReals) # Output of generators (kJ/month)

	# Indicator variable
	model.Z_essp = Var(Omega_E, Omega_S, Omega_S, within=Integers) # Indicator variable

	# Other variables for complete recourse
	model.dR_nets = Var(Omega_N, Omega_E, Omega_T, Omega_S, within=NonNegativeReals) # Demand restriction
	
	def I1_1(model):
		return sum(probability[s]*(model.zaiILine_s[s] + model.zaiIDSR_s[s] + model.zaiODSR_s[s] + model.zaiODG_s[s]) for s in Omega_S)
	model.objective = Objective(sense=minimize, rule=I1_1)
	# model.objective.pprint()
	
	def I2Line_2(model,s): # Investment cost for lines
		return model.zaiILine_s[s] == sum(rI_e[e]*sum(model.B_loes[l,o,e,s]*gammaL_o[o] for l in Omega_L for o in Omega_O) for e in Omega_E)
	model.I2Line_2 = Constraint(Omega_S, rule = I2Line_2)
	# model.I2Line_2.pprint()
	
	def I2DSR_2(model,s): # Investment cost for DSRs
		return model.zaiIDSR_s[s] == sum(rI_e[e]*(sum(model.D_nes[n,e,s]*gammaD for n in Omega_N)) for e in Omega_E)
	model.I2DSR_2 = Constraint(Omega_S, rule = I2DSR_2)
	# model.I2DSR_2.pprint()
	
	def I3DSR(model,s): # DSR operational cost
		return model.zaiODSR_s[s] == sum(ro_e[e]*w_t[t]*model.Xi_nets[n,e,t,s]*cDSR for e in Omega_E for t in Omega_T for n in Omega_N)
	model.I3DSR = Constraint(Omega_S, rule = I3DSR)
	# model.I3DSR.pprint()
	
	def I3DG(model,s): # DG operational cost
		return model.zaiODG_s[s] == sum(ro_e[e]*cDG*(K_ge[g,e]*zeta_gt[g,t] - model.PG_gets[g,e,t,s]) for e in Omega_E for t in Omega_T for g in Omega_DG)
	model.I3DG = Constraint(Omega_S, rule = I3DG)
	# model.I3DG.pprint()
	
	def I4_4(model,l,o,e,s): # Aggregate all capacity for lines taken in the past while considering their build times
		return model.Ftilde_loes[l,o,e,s] == sum(model.F_loes[l,o,z,s] for z in Omega_E if z<=e-kappaL_o[o])
	model.I4_4 = Constraint(Omega_L, Omega_O, Omega_E, Omega_S, rule = I4_4)
	# model.I4_4.pprint()
	
	def I5_5(model,n,e,s): # Aggregate all investment decisions for DSR taken in the past while considering their build times
		return model.Dtilde_nes[n,e,s] <= sum(model.D_nes[n,z,s] for z in Omega_E if z<=e-kappaD)
	model.I5_5 = Constraint(Omega_N, Omega_E, Omega_S, rule = I5_5)
	# model.I5_5.pprint()
	
	def I6_5(model,n,e,s): # DSR is available until the end once installed
		return model.Dtilde_nes[n,e,s] <= model.Dtilde_nes[n,e+1,s]
	model.I6_5 = Constraint(Omega_N, Omega_Estar, Omega_S, rule = I6_5)
	# model.I6_5.pprint()
	
	def I7_6(model,l,o,e,s): # Capacity addition by upgrading line l
		return model.F_loes[l,o,e,s] == Q_o[o]*model.B_loes[l,o,e,s]
	model.I7_6 = Constraint(Omega_L, Omega_O, Omega_E, Omega_S, rule = I7_6)
	# model.I7_6.pprint()
	
	def I8_11(model,n,e,t,s): # Load shifted at bus n <= Max_load can be shifted
		return model.T_nets[n,e,t,s] <= model.Dtilde_nes[n,e,s]*Dmax_n[n]
	model.I8_11 = Constraint(Omega_N, Omega_E, Omega_T, Omega_S, rule = I8_11)
	# model.I8_11.pprint()
	
	def I9_12(model,n,e,t,s): # Load shifted at bus n <= Invested DSR*participation*load
		return model.Xi_nets[n,e,t,s] <= model.Dtilde_nes[n,e,s]*model.f_ns[n,s]*d_net[n,e,t]
	model.I9_12 = Constraint(Omega_N, Omega_E, Omega_T, Omega_S, rule = I9_12)
	# model.I9_12.pprint()
	
	def I10_13(model,n,e,k,s): # Energy equality in coupled operation times
		return sum((model.T_nets[n,e,t,s] - model.Xi_nets[n,e,t,s]) for t in Omega_KT_k[k]) == 0
	model.I10_13 = Constraint(Omega_N, Omega_E, Omega_K, Omega_S, rule = I10_13)
	# model.I10_13.pprint()
	
	def I11_14(model,g,e,t,s): # Output of g must be less than cap*max %
		return model.PG_gets[g,e,t,s] <= K_ge[g,e]*zeta_gt[g,t]
	model.I11_14 = Constraint(Omega_G, Omega_E, Omega_T, Omega_S, rule = I11_14)
	# model.I11_14.pprint()
	
	# def con_15(model,s,e,t,l): # Skipped
	# 	return model.P_l[s,e,t,l] <= (model.theta_u1[s,e,t] - model.theta_v1[s,e,t])/X[l]
	# model.con_15m = Constraint(Omega_S, Omega_E, Omega_T, Omega_L, rule = con_15)
	
	def I12a_16a(model,l,e,t,s): # Power flow must be smaller than the capacity of lines
		return model.PL_lets[l,e,t,s] <= Fini_l[l] + sum(model.Ftilde_loes[l,o,e,s] for o in Omega_O)
	model.I12a_16a = Constraint(Omega_L, Omega_E, Omega_T, Omega_S, rule = I12a_16a)
	# model.I12a_16a.pprint()
	
	def I12b_16b(model,l,e,t,s): # Power flow must be smaller than the capacity of lines
		return model.PL_lets[l,e,t,s] >= - Fini_l[l] - sum(model.Ftilde_loes[l,o,e,s] for o in Omega_O)
	model.I12b_16b = Constraint(Omega_L, Omega_E, Omega_T, Omega_S, rule = I12b_16b)
	# model.I12b_16b.pprint()

	def I13(model,n,e,t,s): # Energy balance at every bus n
		return sum(model.PG_gets[g,e,t,s]*I_ng[n,g] for g in Omega_G) + sum(model.PL_lets[l,e,t,s]*L_nl[n,l] for l in Omega_L) == model.T_nets[n,e,t,s] - model.Xi_nets[n,e,t,s] + d_net[n,e,t]
	model.I13 = Constraint(Omega_N, Omega_E, Omega_T, Omega_S, rule = I13)
	# model.I13.pprint()
	
	### Initial NACs ###
	def I14_7(model,l,o,s,sp):
		if s!=sp:
			return model.B_loes[l,o,1,s] == model.B_loes[l,o,1,sp]
		else:
			return Constraint.Skip
	model.I14_7 = Constraint(Omega_L, Omega_O, Omega_S, Omega_S, rule = I14_7)
	# model.I14_7.pprint()
	
	def I15_8(model,n,s,sp):
		if s!=sp:
			return model.D_nes[n,1,s] == model.D_nes[n,1,sp]
		else:
			return Constraint.Skip
	model.I15_8 = Constraint(Omega_N, Omega_S, Omega_S, rule = I15_8)
	# model.I15_8.pprint()
	
	def I16_18(model,n,e,s,sp): # Indicator constraint
		if s!=sp and n in D_ssp[s,sp]:
			return model.Z_essp[e,s,sp] <= 1 - model.Dtilde_nes[n,e,s]
		else:
			return Constraint.Skip
	model.I16_18 = Constraint(Omega_N, Omega_E, Omega_S, Omega_S, rule = I16_18)
	# model.I16_18.pprint()
	
	def I17_19(model,e,s,sp): # Indicator constraint
		if s!=sp:
			return model.Z_essp[e,s,sp] >= sum((1 - model.Dtilde_nes[n,e,s]) for n in D_ssp[s,sp]) - (len(D_ssp[s,sp]) - 1)
		else:
			return Constraint.Skip
	model.I17_19 = Constraint(Omega_E, Omega_S, Omega_S, rule = I17_19)
	# model.I17_19.pprint()

	def I18a_20(model,l,o,e,s,sp): # Conditional NACs
		if s!=sp:
			return model.B_loes[l,o,e+1,s] - model.B_loes[l,o,e+1,sp] >=  -(1 - model.Z_essp[e,s,sp])
		else:
			return Constraint.Skip
	model.I18a_20 = Constraint(Omega_L, Omega_O, Omega_Estar, Omega_S, Omega_S, rule = I18a_20)
	# model.I18a_20.pprint()

	def I18b_20(model,l,o,e,s,sp): # Conditional NACs
		if s!=sp:
			return model.B_loes[l,o,e+1,s] - model.B_loes[l,o,e+1,sp] <= (1 - model.Z_essp[e,s,sp])
		else:
			return Constraint.Skip
	model.I18b_20 = Constraint(Omega_L, Omega_O, Omega_Estar, Omega_S, Omega_S, rule = I18b_20)
	# model.I18b_20.pprint()

	def I19a_21(model,n,e,s,sp): # Conditional NACs
		if s!=sp:
			return model.D_nes[n,e+1,s] - model.D_nes[n,e+1,sp] >= - (1 - model.Z_essp[e,s,sp])
		else:
			return Constraint.Skip
	model.I19a_21 = Constraint(Omega_N, Omega_Estar, Omega_S, Omega_S, rule = I19a_21)
	# model.I19a_21.pprint()

	def I19b_21(model,n,e,s,sp): # Conditional NACs
		if s!=sp:
			return model.D_nes[n,e+1,s] - model.D_nes[n,e+1,sp] <= (1 - model.Z_essp[e,s,sp])
		else:
			return Constraint.Skip
	model.I19b_21 = Constraint(Omega_N, Omega_Estar, Omega_S, Omega_S, rule = I19b_21)
	# model.I19b_21.pprint()

	def I20a(model,l,e,t,s,sp):
		if s!=sp:
			return model.PL_lets[l,e,t,s] - model.PL_lets[l,e,t,sp] >= - Max_K[e]*(1 - model.Z_essp[e,s,sp])
		else:
			return Constraint.Skip
	model.I20a = Constraint(Omega_L, Omega_E, Omega_T, Omega_S, Omega_S, rule = I20a)
	# model.I20a.pprint()

	def I20b(model,l,e,t,s,sp):
		if s!=sp:
			return model.PL_lets[l,e,t,s] - model.PL_lets[l,e,t,sp] <= Max_K[e]*(1 - model.Z_essp[e,s,sp])
		else:
			return Constraint.Skip
	model.I20b = Constraint(Omega_L, Omega_E, Omega_T, Omega_S, Omega_S, rule = I20b)
	# model.I20b.pprint()

	def I21a(model,n,e,t,s,sp):
		if s!=sp:
			return model.Xi_nets[n,e,t,s] - model.Xi_nets[n,e,t,sp] >= - Max_K[e]*(1 - model.Z_essp[e,s,sp])
		else:
			return Constraint.Skip
	model.I21a = Constraint(Omega_N, Omega_E, Omega_T, Omega_S, Omega_S, rule = I21a)
	# model.I21a.pprint()

	def I21b(model,n,e,t,s,sp):
		if s!=sp:
			return model.Xi_nets[n,e,t,s] - model.Xi_nets[n,e,t,sp] <= Max_K[e]*(1 - model.Z_essp[e,s,sp])
		else:
			return Constraint.Skip
	model.I21b = Constraint(Omega_N, Omega_E, Omega_T, Omega_S, Omega_S, rule = I21b)
	# model.I21b.pprint()

	return model