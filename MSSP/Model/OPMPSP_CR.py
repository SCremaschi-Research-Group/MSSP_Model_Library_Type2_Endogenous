import os
import sys
from pyomo.environ import *
from pyomo.opt import SolverFactory
import time as timer
import numpy
import shutil

def MSSP_model(T, I, S, cmng_t, cproc_t, c1_t, M_t, P_t, a0_is, a1_is, g_is, D_ssp, IJ, probability, CMadd):
	
	model = ConcreteModel()
	
	# Uncertain parameters 
	model.a0_is = Param(I,S, initialize=a0_is, mutable=True)
	model.a1_is = Param(I,S, initialize=a1_is, mutable=True)
	model.g_is = Param(I,S, initialize=g_is, mutable=True)
	
	# Post-realization decision variables and differentiator variables
	model.x_its = Var(I,T,S, within = Binary)

	# Post-realization decision variables
	model.y_its = Var(I,T,S, within = NonNegativeReals)
	
	# At-realization decision variables
	model.z_its = Var(I,T,S, within = NonNegativeReals)
	
	# Other variables for complete recourse
	model.Madd_ts = Var(T,S, within = NonNegativeReals)
	
	### Objective function ###
	def D13(model):
		return sum(probability[s]*sum(((c1_t[t]*model.a1_is[i,s] - cproc_t[t]*model.a0_is[i,s])*model.z_its[i,t,s] - model.a0_is[i,s]*cmng_t[t]*model.y_its[i,t,s]) for i in I for t in T) - sum(CMadd*model.Madd_ts[t,s] for t in T) for s in S)
	model.objective = Objective(sense=maximize, rule=D13)
	# model.objective.pprint()
	
	### Scenario specific constraints ###
	def D2_21(model,i,t,s):
		return model.z_its[i,t,s] <= model.y_its[i,t,s]
	model.D2_21 = Constraint(I,T,S, rule = D2_21)	
	# model.D2_21.pprint()
	
	def D3_22(model,t,s):
		return sum(model.a0_is[i,s]*model.z_its[i,t,s] for i in I) <= P_t[t]
	model.D3_22 = Constraint(T,S, rule = D3_22)
	# model.D3_22.pprint()
	
	def D14_23(model,t,s):
		return sum(model.a0_is[i,s]*model.y_its[i,t,s] for i in I) <= M_t[t] + model.Madd_ts[t,s]
	model.D14_23 = Constraint(T,S, rule = D14_23)
	
	def D5_24(model,i,j,t,s):
		return model.x_its[i,t,s] <= sum(model.y_its[j,tp,s] for tp in T if tp <= t)
	model.D5_24 = Constraint(IJ,T,S, rule = D5_24)
	# model.D5_24.pprint()
	
	def D6_25(model,i,t,s):
		return sum(model.y_its[i,tp,s] for tp in T if tp<=t) <= model.x_its[i,t,s]
	model.D6_25 = Constraint(I,T,S, rule = D6_25)
	# model.D6_25.pprint()
	
	def D7_26(model,i,t,s):
		if t<=T[-1]-1:
			return model.x_its[i,t,s] <= model.x_its[i,t+1,s]
		else:
			return Constraint.Skip
	model.D7_26 = Constraint(I,T,S, rule = D7_26)
	# model.D7_26.pprint()
	
	### NACs ###
	def D8_31(model,i,s,sp):
		if s!=sp:
			return model.x_its[i,1,s] == model.x_its[i,1,sp]
		else:
			return Constraint.Skip
	model.D8_31 = Constraint(I,S,S, rule = D8_31)	

	def D9_36(model,i,s,sp):
		if s!=sp:
			return model.y_its[i,1,s] == model.y_its[i,1,sp]
		else:
			return Constraint.Skip
	model.D9_36 = Constraint(I,S,S, rule = D9_36)	
	
	def D10_32(model,i,t,s,sp):
		if t>=2 and s!=sp:
			return model.x_its[i,t,s] - model.x_its[i,t,sp] <= sum(model.x_its[j,t-1,s] for j in D_ssp[sp,s])
		else:
			return Constraint.Skip
	model.D10_32 = Constraint(I,T,S,S, rule = D10_32)
	
	def D10_33(model,i,t,s,sp):
		if t>=2 and s!=sp :
			return model.x_its[i,t,s] - model.x_its[i,t,sp] >= -sum(model.x_its[j,t-1,s] for j in D_ssp[sp,s])
		else:
			return Constraint.Skip
	model.D10_33 = Constraint(I,T,S,S, rule = D10_33)
	
	def D11_37(model,i,t,s,sp):
		if t>=2 and s!=sp:
			return model.y_its[i,t,s] - model.y_its[i,t,sp] <= sum(model.x_its[j,t-1,s] for j in D_ssp[sp,s])
		else:
			return Constraint.Skip
	model.D11_37 = Constraint(I,T,S,S, rule = D11_37)
	#model.D11_37.pprint()
	
	def D11_38(model,i,t,s,sp):
		if t>=2 and s!=sp:
			return model.y_its[i,t,s] - model.y_its[i,t,sp] >= -sum(model.x_its[j,t-1,s] for j in D_ssp[sp,s])
		else:
			return Constraint.Skip
	model.D11_38m = Constraint(I,T,S,S, rule = D11_38)
	#model.D11_38m.pprint()
	
	def D12_41(model,i,t,s,sp):
		if s!=sp:
			return model.z_its[i,t,s] - model.z_its[i,t,sp] <= sum(model.x_its[j,t,s] for j in D_ssp[sp,s])
		else:
			return Constraint.Skip
	model.D12_41 = Constraint(I,T,S,S, rule = D12_41)
	
	def D12_42(model,i,t,s,sp):
		if s!=sp:
			return model.z_its[i,t,s] - model.z_its[i,t,sp] >= -sum(model.x_its[j,t,s] for j in D_ssp[sp,s])
		else:
			return Constraint.Skip
	model.D12_42 = Constraint(I,T,S,S, rule = D12_42)
	
	return model