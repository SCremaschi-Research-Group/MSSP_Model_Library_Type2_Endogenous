import os
import sys
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pdb
import numpy
import itertools
import time as timer
import shutil

def MSSP_model(N, N_product, N_feed, T, T_end, I, SG, I_PF, S,
		MCst_n, CX_i0, cd_t, RD_i0, XMax_i, CC0_i, gamma_iPDFD, RDMax, Valpha, Vbeta, Bound_M, DeltaRDmin_i, DeltaCXmin_i, Big_M, MAX_D_nts,
		D_nts, CXMin_isg, theta_is, chip_is, alpha_is, beta_is, phi_D_tssp, Dpsi_ssp, Dchi_ssp, Dalpha_ssp, Dbeta_ssp, probability):
	
	model = ConcreteModel()
	
	# Uncertain parameters 
	model.theta_is = Param(I,S, initialize = theta_is, mutable=True)
	model.chip_is = Param(I,S, initialize = chip_is, mutable=True)
	model.alpha_is = Param(I,S, initialize = alpha_is, mutable=True)
	model.beta_is = Param(I,S, initialize = beta_is, mutable=True)
	model.D_nts = Param(N,T,S, initialize= D_nts, mutable=True)
	
	# Post-realization decision variables
	model.RD_its = Var(I,T,S, within = NonNegativeReals) # Cumulative research investments
	model.CX_its = Var(I,T,S, within = NonNegativeReals) # Cumulative installed capacity of technology i
	
	# At-realization decision variables
	model.M_ints = Var(I,N_feed,T,S, within = NonNegativeReals) # Amount of chemical n produced in technology i
	model.F_nts = Var(N,T,S, within = NonNegativeReals) # The amount of chemical n purchased, wait-and-see decision only for n = 3

	# Other variables and differentiator variables
	model.NNalpha_its = Var(I,T,S, within=Binary) # 1 if the realization of alpha has occurred.
	model.NNbeta_its = Var(I,T,S, within=Binary) # 1 if the realization of beta has occurred.
	model.Y_isgts = Var(I,SG,T,S, within=Binary) # 1 if technology i has completed stage sg

	# Other variables
	model.Nalpha_its = Var(I,T,S, within=Binary) # 1 if an investment has been made for R&D at t.
	model.Nbeta_its = Var(I,T,S, within=Binary) # 1 if an investment has been made for capacity expansion at t
	model.RDCst_s = Var(S) # Total R&D costs
	model.X_its = Var(I,T,S) # Capacity expansion of technology i
	model.YCX_its = Var(I,T,S, within = NonNegativeReals) # For the linearization of (24)
	model.ETC = Var(initialize = 80000)
	model.MatCst_s = Var(S) # Total raw material costs
	model.CapExCst_s = Var(S) # Total capacity expansion costs
	model.CC_its = Var(I,T,S) # Linearized capacity expansion cost of technology i
	model.g_ints = Var(I,N_product,T,S) # Net production at technology i
	model.G_nts = Var(N_product,T,S) # Total net production
	model.chi_its = Var(I,T,S) # Yield of technology i after reaching commercialization stage
	model.ZM_ints = Var(I,N_feed,T,S, within=NonNegativeReals) # For the linearization of (18)
	model.alpha_its = Var(I,T,S) 
	model.beta_its = Var(I,T,S)
	
	def objective_function(model):
		return model.ETC
	model.objective = Objective(sense=minimize,rule=objective_function)
	
	def J1_8(model):
		return model.ETC == sum(probability[s]*(model.MatCst_s[s] + model.CapExCst_s[s] + model.RDCst_s[s]) for s in S)
	model.J1_8 = Constraint(rule= J1_8)
	# model.J1_8.pprint()
	
	def J2_9(model,s):
		return model.MatCst_s[s] == sum(cd_t[t]*MCst_n[n]*model.F_nts[n,t,s] for n in N for t in T) 
	model.J2_9 = Constraint(S, rule= J2_9)
	# model.J2_9.pprint()
	
	def J3_10(model,s):
		return model.RDCst_s[s] == sum(cd_t[1]*(model.RD_its[i,1,s] - RD_i0[i]) for i in I)\
									+ sum(cd_t[t]*(model.RD_its[i,t,s] - model.RD_its[i,t-1,s]) for t in T if t>=2 for i in I)
	model.J3_10 = Constraint(S, rule = J3_10)
	# model.J3_10.pprint()
	
	def J4_11(model,s): # Non-linear
		return model.CapExCst_s[s] == sum(1000*cd_t[t]*model.CC_its[i,t,s]*model.X_its[i,t,s] for t in T for i in I)
	model.J4_11 = Constraint(S, rule = J4_11)
	# model.J4_11.pprint()
	
	def J5J6_12(model,i,t,s):
		if t == 1:
			return model.X_its[i,t,s] == model.CX_its[i,t,s] - CX_i0[i]
		else:
			return model.X_its[i,t,s] == model.CX_its[i,t,s] - model.CX_its[i,t-1,s]
	model.J5J6_12 = Constraint(I,T,S, rule = J5J6_12)
	# model.J5J6_12.pprint()
	
	def J7_13(model,i,t,s): # Non-linear
		return model.CC_its[i,t,s] == CC0_i[i]*((model.CX_its[i,t,s]/CX_i0[i])**model.beta_its[i,t,s])*((model.RD_its[i,t,s]/RD_i0[i])**model.alpha_its[i,t,s])
	model.J7_13 = Constraint(I,T,S, rule = J7_13)
	# model.J7_13.pprint()
	
	def J8J9(model,i,t,s):
		if t >= 2:
			return model.RD_its[i,t,s] - model.RD_its[i,t-1,s] >= 0
		else:
			return model.RD_its[i,t,s] - RD_i0[i] >= 0 # t = 1
	model.J8J9 = Constraint(I,T,S, rule = J8J9)
	# model.J8J9.pprint()
	
	def J10_14(model,i,t,s):
		return model.beta_its[i,t,s] == model.beta_is[i,s]*model.NNbeta_its[i,t,s]
	model.J10_14 = Constraint(I,T,S, rule = J10_14)
	# model.J10_14.pprint()
	
	def J11_15(model,i,t,s):
		return model.alpha_its[i,t,s] == model.alpha_is[i,s]*model.NNalpha_its[i,t,s]
	model.J11_15 = Constraint(I,T,S, rule = J11_15)
	# model.J11_15.pprint()
	
	def J12J13_17(model,n,t,s):
		if n in N_product:
			return 0 == model.F_nts[n,t,s] - model.D_nts[n,t,s] + model.G_nts[n,t,s]
		else:
			return 0 == model.F_nts[n,t,s] - sum(model.M_ints[i,n,t,s] for i in I)
	model.J12J13_17 = Constraint(N,T,S, rule = J12J13_17)
	# model.J12J13_17.pprint()
	
	##### Linearization of J14 by J16-J19
	def J15_18(model,i,t,s): # additional
		return model.G_nts[I_PF[i][0],t,s] == sum(model.g_ints[i,I_PF[i][0],t,s] for i in I)
	model.J15_18 = Constraint(I,T,S, rule = J15_18)
	# model.J15_18.pprint()
	
	def J16_75(model,i,t,s):
		return model.g_ints[i,I_PF[i][0],t,s] == gamma_iPDFD[i,I_PF[i][0],I_PF[i][1]]*model.chip_is[i,s]*model.ZM_ints[i,I_PF[i][1],t,s]
	model.J16_75 = Constraint(I,T,S, rule = J16_75)
	# model.J16_75.pprint()
	
	def J17_76(model,i,t,s):
		return model.ZM_ints[i,I_PF[i][1],t,s] <= model.Y_isgts[i,3,t,s]*Big_M
	model.J17_76 = Constraint(I,T,S, rule = J17_76)
	# model.J17_76.pprint()

	def J18(model,i,t,s): # additional
		return model.ZM_ints[i,I_PF[i][1],t,s] >= model.M_ints[i,I_PF[i][1],t,s] - (1-model.Y_isgts[i,3,t,s])*Big_M
	model.J18 = Constraint(I,T,S, rule = J18)
	# model.J18.pprint()

	def J19_78(model,i,t,s):
		return model.ZM_ints[i,I_PF[i][1],t,s] <= model.M_ints[i,I_PF[i][1],t,s]
	model.J19_78 = Constraint(I,T,S, rule = J19_78)
	# model.J19_78.pprint()

	def J20_20(model,i,sg,t,s):
		return model.CX_its[i,t,s] >= CXMin_isg[i,sg]*model.Y_isgts[i,sg,t,s]
	model.J20_20 = Constraint(I,SG,T,S, rule = J20_20)
	# model.J20_20.pprint()
	
	def J21(model,i,t,s): # additional
		return model.CX_its[i,t,s] >= CX_i0[i]
	model.J21 = Constraint(I,T,S, rule = J21)
	# model.J21.pprint()

	def J22_21(model,i,t,s):
		return model.CX_its[i,t,s] <= CX_i0[i] + sum((CXMin_isg[i,sg+1] - CXMin_isg[i,sg])*model.Y_isgts[i,sg,t,s] for sg in SG if sg < 3) + model.Y_isgts[i,3,t,s]*Big_M
	model.J22_21 = Constraint(I,T,S, rule = J22_21)
	# model.J22_21.pprint()

	def J23_22(model,i,sg,t,s):
		if sg>1:
			return model.Y_isgts[i,sg,t,s] <= model.Y_isgts[i,sg-1,t,s]
		else:
			return Constraint.Skip
	model.J23_22 = Constraint(I,SG,T,S, rule = J23_22)
	# model.J23_22.pprint()

	def J24_23(model,i,sg,t,s):
		if t>1:
			return model.Y_isgts[i,sg,t,s] >= model.Y_isgts[i,sg,t-1,s]
		else:
			return Constraint.Skip
	model.J24_23 = Constraint(I,SG,T,S, rule = J24_23)
	# model.J24_23.pprint()
	
	# def Eq_24(model,i,t,s): # (24)
	# 	return model.g_ints[i,I_PR[i][0],t,s] <= model.Y_isgts[i,3,t,s]*model.CX_its[i,t,s]*theta_is[i,s]
	# model.Eq_24_con = Constraint(I,T,S, rule = Eq_24)
	# # model.Eq_24_con.pprint()
	
	##### Linearization of J26_24 by J27-J30
	def J26(model,i,t,s):
		return model.g_ints[i,I_PF[i][0],t,s] <= model.YCX_its[i,t,s]*model.theta_is[i,s]
	model.J26 = Constraint(I,T,S, rule = J26)
	# model.J26.pprint()
	
	def J27(model,i,t,s):
		return model.YCX_its[i,t,s] <= model.Y_isgts[i,3,t,s]*Big_M
	model.J27 = Constraint(I,T,S, rule = J27)
	# model.J27.pprint()
	
	def J28(model,i,t,s):
		return model.YCX_its[i,t,s] >= model.CX_its[i,t,s] - (1-model.Y_isgts[i,3,t,s])*Big_M
	model.J28 = Constraint(I,T,S, rule = J28)
	# model.J28.pprint()
	
	def J29(model,i,t,s):
		return model.YCX_its[i,t,s] <= model.CX_its[i,t,s]
	model.J29 = Constraint(I,T,S, rule = J29)
	# model.J29.pprint()
	
	def J30aJ31a_37(model,i,t,s):
		if t >= 2:
			return model.RD_its[i,t,s] - model.RD_its[i,t-1,s] <= model.Nalpha_its[i,t,s]*RDMax
		else:
			return model.RD_its[i,t,s] - RD_i0[i] <= model.Nalpha_its[i,t,s]*RDMax # t = 1
	model.J30aJ31a_37 = Constraint(I,T,S, rule = J30aJ31a_37)
	# model.J30aJ31a_37.pprint()
	
	def J30bJ31b_37(model,i,t,s):
		if t >= 2:
			return model.RD_its[i,t,s] - model.RD_its[i,t-1,s] >= DeltaRDmin_i[i]*model.Nalpha_its[i,t,s]
		else:
			return model.RD_its[i,t,s] - RD_i0[i] >= DeltaRDmin_i[i]*model.Nalpha_its[i,t,s] # t = 1
	model.J30bJ31b_37 = Constraint(I,T,S, rule = J30bJ31b_37)
	# model.J30bJ31b_37.pprint()
	
	def J32a_38(model,i,t,s):
		return model.X_its[i,t,s] <= model.Nbeta_its[i,t,s]*XMax_i[i]
	model.J32a_38 = Constraint(I,T,S, rule = J32a_38)
	# model.J32a_38.pprint()
	
	def J32b_38(model,i,t,s):
		return model.X_its[i,t,s] >= DeltaCXmin_i[i]*model.Nbeta_its[i,t,s]
	model.J32b_38 = Constraint(I,T,S, rule = J32b_38)
	# model.J32b_38.pprint()
	
	def J33a_39(model,i,t,s):
		return sum(model.Nalpha_its[i,tp,s] for tp in T if tp<t) <= T_end*model.NNalpha_its[i,t,s] - 1 + Valpha
	model.J33a_39 = Constraint(I,T,S, rule = J33a_39)
	# model.J33a_39.pprint()
	
	def J33b_39(model,i,t,s):
		return sum(model.Nalpha_its[i,tp,s] for tp in T if tp<t)/Valpha >= model.NNalpha_its[i,t,s]
	model.J33b_39 = Constraint(I,T,S, rule = J33b_39)
	# model.J33b_39.pprint()

	def J34a_40(model,i,t,s):
		return sum(model.Nbeta_its[i,tp,s] for tp in T if tp<t) <= T_end*model.NNbeta_its[i,t,s] - 1 + Vbeta
	model.J34a_40 = Constraint(I,T,S, rule = J34a_40)
	# model.J34a_40.pprint()
	
	def J34b_40(model,i,t,s):
		return sum(model.Nbeta_its[i,tp,s] for tp in T if tp<t)/Vbeta >= model.NNbeta_its[i,t,s]
	model.J34b_40 = Constraint(I,T,S, rule = J34b_40)
	# model.J34b_40.pprint()

	#### Initial NACs #####
	def J35a(model,i,s,sp): # Equality constraints generate 'too few degrees of freedom error'
		if s<sp:
			return model.CX_its[i,1,s] - model.CX_its[i,1,sp] >= 0
		else:
			return Constraint.Skip
	model.J35a = Constraint(I,S,S, rule = J35a)
	# model.J35a.pprint()
	
	def J35b(model,i,s,sp): # Equality constraints generate 'too few degrees of freedom error'
		if s<sp:
			return model.CX_its[i,1,s] - model.CX_its[i,1,sp] <= 0
		else:
			return Constraint.Skip
	model.J35b = Constraint(I,S,S, rule = J35b)
	# model.J35b.pprint()
	
	def J36a(model,i,s,sp): # Equality constraints generate 'too few degrees of freedom error'
		if s<sp:
			return model.RD_its[i,1,s] - model.RD_its[i,1,sp] >= 0
		else:
			return Constraint.Skip
	model.J36a = Constraint(I,S,S, rule = J36a)
	# model.J36a.pprint()
	
	def J36b(model,i,s,sp): # Equality constraints generate 'too few degrees of freedom error'
		if s<sp:
			return model.RD_its[i,1,s] - model.RD_its[i,1,sp] <= 0
		else:
			return Constraint.Skip
	model.J36b = Constraint(I,S,S, rule = J36b)
	# model.J36b.pprint()
	
	#### Conditional NACs #####
	def J37a(model,i,t,s,sp):
		if t<T_end and s<sp:
			return  -XMax_i[i]*(t+1)*phi_D_tssp[t,s,sp]\
					-XMax_i[i]*(t+1)*sum(model.Y_isgts[issp,sgssp,t,s] for (issp,sgssp) in Dpsi_ssp[s,sp])\
					-XMax_i[i]*(t+1)*sum(model.Y_isgts[issp,3,t,s] for issp in Dchi_ssp[s,sp])\
					-XMax_i[i]*(t+1)*sum(model.NNalpha_its[issp,t,s] for issp in Dalpha_ssp[s,sp])\
					-XMax_i[i]*(t+1)*sum(model.NNbeta_its[issp,t,s] for issp in Dbeta_ssp[s,sp])\
					<= model.CX_its[i,t+1,s] - model.CX_its[i,t+1,sp]
		else:
			return Constraint.Skip
	model.J37a = Constraint(I,T,S,S, rule = J37a)
	# model.J37a.pprint()
	
	def J37b(model,i,t,s,sp):
		if t < T_end and s<sp:
			return    XMax_i[i]*(t+1)*phi_D_tssp[t,s,sp] \
					+ XMax_i[i]*(t+1)*sum(model.Y_isgts[issp,sgssp,t,s] for (issp,sgssp) in Dpsi_ssp[s,sp])\
					+ XMax_i[i]*(t+1)*sum(model.Y_isgts[issp,3,t,s] for issp in Dchi_ssp[s,sp])\
					+ XMax_i[i]*(t+1)*sum(model.NNalpha_its[issp,t,s] for issp in Dalpha_ssp[s,sp])\
					+ XMax_i[i]*(t+1)*sum(model.NNbeta_its[issp,t,s] for issp in Dbeta_ssp[s,sp])\
					>= model.CX_its[i,t+1,s] - model.CX_its[i,t+1,sp]
		else:
			return Constraint.Skip
	model.J37b = Constraint(I,T,S,S, rule = J37b)
	# model.J37b.pprint()
	
	def J38a(model,i,t,s,sp):
		if t<T_end and s<sp:
			return  -RDMax*(t+1)*phi_D_tssp[t,s,sp]\
					-RDMax*(t+1)*sum(model.Y_isgts[issp,sgssp,t,s] for (issp,sgssp) in Dpsi_ssp[s,sp])\
					-RDMax*(t+1)*sum(model.Y_isgts[issp,3,t,s] for issp in Dchi_ssp[s,sp])\
					-RDMax*(t+1)*sum(model.NNalpha_its[issp,t,s] for issp in Dalpha_ssp[s,sp])\
					-RDMax*(t+1)*sum(model.NNbeta_its[issp,t,s] for issp in Dbeta_ssp[s,sp])\
					<= model.RD_its[i,t+1,s] - model.RD_its[i,t+1,sp]
		else:
			return Constraint.Skip
	model.J38a = Constraint(I,T,S,S, rule = J38a)
	# model.J38a.pprint()
	
	def J38b(model,i,t,s,sp):
		if t<T_end and s<sp:
			return    RDMax*(t+1)*phi_D_tssp[t,s,sp] \
					+ RDMax*(t+1)*sum(model.Y_isgts[issp,sgssp,t,s] for (issp,sgssp) in Dpsi_ssp[s,sp])\
					+ RDMax*(t+1)*sum(model.Y_isgts[issp,3,t,s] for issp in Dchi_ssp[s,sp])\
					+ RDMax*(t+1)*sum(model.NNalpha_its[issp,t,s] for issp in Dalpha_ssp[s,sp])\
					+ RDMax*(t+1)*sum(model.NNbeta_its[issp,t,s] for issp in Dbeta_ssp[s,sp])\
					>= model.RD_its[i,t+1,s] - model.RD_its[i,t+1,sp]
		else:
			return Constraint.Skip
	model.J38b = Constraint(I,T,S,S, rule = J38b)
	# model.J38b.pprint()
	
	def J39a(model,i,n,t,s,sp):
		if s<sp:
			return  -Bound_M*phi_D_tssp[t,s,sp]\
					-Bound_M*sum(model.Y_isgts[issp,sgssp,t,s] for (issp,sgssp) in Dpsi_ssp[s,sp])\
					-Bound_M*sum(model.Y_isgts[issp,3,t,s] for issp in Dchi_ssp[s,sp])\
					-Bound_M*sum(model.NNalpha_its[issp,t,s] for issp in Dalpha_ssp[s,sp])\
					-Bound_M*sum(model.NNbeta_its[issp,t,s] for issp in Dbeta_ssp[s,sp])\
					<= model.M_ints[i,n,t,s] - model.M_ints[i,n,t,sp]
		else:
			return Constraint.Skip
	model.J39a = Constraint(I,N_feed,T,S,S, rule = J39a)
	# model.J39a.pprint()
	
	def J39b(model,i,n,t,s,sp):
		if s<sp:
			return    Bound_M*phi_D_tssp[t,s,sp] \
					+ Bound_M*sum(model.Y_isgts[issp,sgssp,t,s] for (issp,sgssp) in Dpsi_ssp[s,sp])\
					+ Bound_M*sum(model.Y_isgts[issp,3,t,s] for issp in Dchi_ssp[s,sp])\
					+ Bound_M*sum(model.NNalpha_its[issp,t,s] for issp in Dalpha_ssp[s,sp])\
					+ Bound_M*sum(model.NNbeta_its[issp,t,s] for issp in Dbeta_ssp[s,sp])\
					>= model.M_ints[i,n,t,s] - model.M_ints[i,n,t,sp]
		else:
			return Constraint.Skip
	model.J39b = Constraint(I,N_feed,T,S,S, rule = J39b)
	# model.J39b.pprint()
	
	def J40a(model,n,t,s,sp):
		if s<sp:
			return  -MAX_D_nts*phi_D_tssp[t,s,sp]\
					-MAX_D_nts*sum(model.Y_isgts[issp,sgssp,t,s] for (issp,sgssp) in Dpsi_ssp[s,sp])\
					-MAX_D_nts*sum(model.Y_isgts[issp,3,t,s] for issp in Dchi_ssp[s,sp])\
					-MAX_D_nts*sum(model.NNalpha_its[issp,t,s] for issp in Dalpha_ssp[s,sp])\
					-MAX_D_nts*sum(model.NNbeta_its[issp,t,s] for issp in Dbeta_ssp[s,sp])\
					<= model.F_nts[n,t,s] - model.F_nts[n,t,sp]
		else:
			return Constraint.Skip
	model.J40a = Constraint(N_product,T,S,S, rule = J40a)
	# model.J40a.pprint()
	
	def J40b(model,n,t,s,sp):
		if s<sp:
			return    MAX_D_nts*phi_D_tssp[t,s,sp] \
					+ MAX_D_nts*sum(model.Y_isgts[issp,sgssp,t,s] for (issp,sgssp) in Dpsi_ssp[s,sp])\
					+ MAX_D_nts*sum(model.Y_isgts[issp,3,t,s] for issp in Dchi_ssp[s,sp])\
					+ MAX_D_nts*sum(model.NNalpha_its[issp,t,s] for issp in Dalpha_ssp[s,sp])\
					+ MAX_D_nts*sum(model.NNbeta_its[issp,t,s] for issp in Dbeta_ssp[s,sp])\
					>= model.F_nts[n,t,s] - model.F_nts[n,t,sp]
		else:
			return Constraint.Skip
	model.J40b = Constraint(N_product,T,S,S, rule = J40b)
	# model.J40b.pprint()
	
	return model