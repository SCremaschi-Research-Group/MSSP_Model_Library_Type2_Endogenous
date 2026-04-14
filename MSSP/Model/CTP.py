import os
import sys
from pyomo.environ import *
from pyomo.opt import SolverFactory
import time as timer

def MSSP_model(I, J, J_end, T, T_end, R, S, SI_s, gammaD_i, gammaL_i, tau_ij, revmax_i, c_ij, revopen_ij, revrun_ijt, f_ij, cd_t, rho_ijr, rhomax_r, ForP_is, D_ssp, probability):
	
	model = ConcreteModel()
	
	# Uncertain parameters 
	model.ForP_is = Param(I,S, initialize = ForP_is, mutable=True)
	
	# At-realization decision variables
	model.X_ijts = Var(I,J,T,S, within=Binary)
	
	# Other variables and differentiator variables
	model.Y_ijts = Var(I,J,T,S, within=Binary)

	# Other variables
	model.Cst_s = Var(S)
	model.FRv_s = Var(S)
	model.Rv_s = Var(S)
	model.Z_ijts = Var(I,J,T,S, within=Binary)
	
	def C1_20(model):
		return sum(probability[s]*(model.FRv_s[s] + model.Rv_s[s] - model.Cst_s[s]) for s in S)
	model.objective = Objective(rule=C1_20, sense=maximize)
	
	def C2_17(model,s):
		return model.Cst_s[s] == sum(cd_t[t]*c_ij[i,j]*model.X_ijts[i,j,t,s] for i in I for j in J for t in T)
	model.C2_17 = Constraint(S, rule=C2_17)
	# model.C2_17.pprint()
	
	def C3_18(model,s):
		return model.Rv_s[s] == sum(model.ForP_is[i,s]*sum(revmax_i[i]*model.X_ijts[i,J_end,t,s]\
									-gammaD_i[i]*sum(model.Z_ijts[i,j,t,s] for j in J if j > 1)\
									-gammaL_i[i]*(t + tau_ij[i,J_end])*model.X_ijts[i,J_end,t,s] for t in T) for i in I) 
	model.C3_18 = Constraint(S, rule=C3_18)
	# model.C3_18.pprint()
	
	def C4_19(model,s):
		return model.FRv_s[s] == sum(model.ForP_is[i,s]*sum(revopen_ij[i,j]*f_ij[i,j]*model.Z_ijts[i,j,T_end,s] for j in J) for i in I)\
								+ sum(model.ForP_is[i,s]*sum(revrun_ijt[i,j,t]*f_ij[i,j+1]*model.X_ijts[i,j,t,s] for j in J if j<J_end for t in T if t>T_end-tau_ij[i,j]) for i in I)
	model.C4_19 = Constraint(S, rule=C4_19)
	# model.C4_19.pprint()

	def C5C6C7_6(model,i,j,t,s):
		if t==1:
			return model.Y_ijts[i,j,t,s] == 0
		elif t>1 and t-tau_ij[i,j]<1:
			return model.Y_ijts[i,j,t,s] == model.Y_ijts[i,j,t-1,s]
		else:
			return model.Y_ijts[i,j,t,s] == model.Y_ijts[i,j,t-1,s] + model.X_ijts[i,j,t-tau_ij[i,j],s]
	model.C5C6C7_6 = Constraint(I,J,T,S, rule=C5C6C7_6)
	# model.C5C6C7_6.pprint()

	def C8_7(model,i,s):
		return model.Z_ijts[i,1,1,s] == 1 - model.X_ijts[i,1,1,s] 
	model.C8_7 = Constraint(I,S, rule=C8_7)
	# model.C8_7.pprint()

	def C9_8(model,i,t,s):
		if t>1:
			return model.Z_ijts[i,1,t,s] == model.Z_ijts[i,1,t-1,s] - model.X_ijts[i,1,t,s]
		else:
			return Constraint.Skip
	model.C9_8 = Constraint(I,T,S, rule=C9_8)
	# model.C9_8.pprint()

	def C10C11C12_9(model,i,j,t,s):
		if j>1 and t>tau_ij[i,j-1] and t>1:
			return model.Z_ijts[i,j,t,s] == model.Z_ijts[i,j,t-1,s] + model.X_ijts[i,j-1,t-tau_ij[i,j-1],s] - model.X_ijts[i,j,t,s]
		elif j>1 and t>1:
			return model.Z_ijts[i,j,t,s] == model.Z_ijts[i,j,t-1,s] - model.X_ijts[i,j,t,s]
		elif t==1 and j>1:
			return model.Z_ijts[i,j,t,s] == - model.X_ijts[i,j,t,s]
		else:
			return Constraint.Skip
	model.C10C11C12_9 = Constraint(I,J,T,S, rule=C10C11C12_9)
	# model.C10C11C12_9.pprint()

	def C13_12(model,i,j,s):
		return sum(model.X_ijts[i,j,t,s] for t in T) <= 1
	model.C13_12 = Constraint(I,J,S,rule=C13_12)
	# model.C13_12.pprint()

	def C14_13(model,i,j,t,s):
		if j>1:
			return sum(model.X_ijts[i,j,tp,s] for tp in T if tp<=t) <= model.Y_ijts[i,j-1,t,s]
		else:
			return Constraint.Skip
	model.C14_13 = Constraint(I,J,T,S, rule=C14_13)
	# model.C14_13.pprint()

	def C15_14(model,r,t,s):
		return sum(rho_ijr[i,j,r]*model.X_ijts[i,j,tp,s] for i in I for j in J for tp in T if tp>t-tau_ij[i,j] and tp<=t) <= rhomax_r[r]
	model.C15_14 = Constraint(R,T,S, rule=C15_14)
	# model.C15_14.pprint()

	### Initial NACs ###
	def C16_11(model,i,s):
		return  model.X_ijts[i,1,1,s] == model.X_ijts[i,1,1,1]
	model.C16_11 = Constraint(I,S, rule=C16_11)
	# model.C16_11.pprint()

	### Condiditional NACs ###
	def C17_10a(model,i,j,t,s,sp):
		if t>1 and (s,sp) in D_ssp:
			return - model.Y_ijts[D_ssp[s,sp][0][0],D_ssp[s,sp][0][1],t,s] <= model.X_ijts[i,j,t,s] - model.X_ijts[i,j,t,sp]
		else:
			return Constraint.Skip
	model.C17_10a = Constraint(I,J,T,S,S,rule=C17_10a)
	# model.C17_10a.pprint()

	def C17_10b(model,i,j,t,s,sp):
		if t>1 and (s,sp) in D_ssp:
			return model.Y_ijts[D_ssp[s,sp][0][0],D_ssp[s,sp][0][1],t,s] >= model.X_ijts[i,j,t,s] - model.X_ijts[i,j,t,sp]
		else:
			return Constraint.Skip
	model.C17_10b = Constraint(I,J,T,S,S,rule=C17_10b)
	# model.C17_10b.pprint()

	return model