import os
from pyomo.environ import *
from pyomo.opt import SolverFactory
import time as timer
import shutil

def MSSP_model(I, T, T_end, S, Cpr_is, D_its, probability, D_ssp, Phi_tssp, c_t, rho, sigma, M, Cpu):
	
	model = ConcreteModel()
	
	# Uncertain parameters
	model.Cpr_is = Param(I,S, initialize=Cpr_is, mutable=True)
	model.D_its = Param(I,T,S, initialize=D_its, mutable=True)
	
	# Post-realization decision and differentiator variables
	model.z_its = Var(I,T,S,within=Binary)

	# Post-realization decision variables
	model.y_its = Var(I,T,S, within=NonNegativeIntegers)
	
	# At-realization decision variables
	model.x_ijts = Var(I,I,T,S, within=NonNegativeIntegers)
	
	# Other variables for complete recourse
	model.w_its = Var(I,T,S, within=NonNegativeIntegers)
	
	# Indicator variable
	model.Z_tssp = Var(T,S,S, within=Integers)

	def A12(model):
		return sum(probability[s]*sum((sum(sigma*model.z_its[i,t,s] + model.Cpr_is[i,s]*model.y_its[i,t,s] + Cpu*model.w_its[i,t,s] for i in I) + rho*sum(model.x_ijts[i,j,t,s] for i in I for j in I if j<i)) for t in T) for s in S)
	model.objective = Objective(sense=minimize, rule=A12)
	# model.objective.pprint()
	
	def A13(model,i,j,t,s):
		return sum(model.x_ijts[i,j,t,s] for i in I if i>=j) + model.w_its[i,t,s] >= model.D_its[i,t,s]
	model.A13 = Constraint(I,I,T,S, rule = A13)
	# model.A13.pprint()
	
	def A3_34(model,i,t,s):
		return sum(sum(model.x_ijts[i,j,tp,s] for j in I if j<=i) - model.y_its[i,tp,s] for tp in T if tp <=t) <= 0
	model.A3_34 = Constraint(I,T,S, rule = A3_34)
	# model.A3_34.pprint()

	def A4_35(model,i,t,s):
		return model.y_its[i,t,s] - M*model.z_its[i,t,s] <= 0
	model.A4_35 = Constraint(I,T,S, rule = A4_35)
	# model.A4_35.pprint()
	
	def A5_36(model,t,s):
		return sum(model.y_its[i,t,s] for i in I) <= c_t[t]
	model.A5_36 = Constraint(T,S, rule = A5_36)
	# model.A5_36.pprint()

	##### Initial NACs #####
	def A6(model,i,s,sp):
		if s < sp:
			return model.z_its[i,1,s] == model.z_its[i,1,sp]
		else:
			return Constraint.Skip
	model.A6 = Constraint(I,S,S, rule = A6)
	# model.A6.pprint()
	
	def A7(model,i,s,sp):
		if s < sp:
			return model.y_its[i,1,s] == model.y_its[i,1,sp]
		else:
			return Constraint.Skip
	model.A7 = Constraint(I,S,S, rule = A7)
	# model.A7.pprint()
	
	##### Indicator Constraints #####
	def A8_a(model,t,s,sp):
		if s < sp:
			return model.Z_tssp[t,s,sp] <= 1 - sum(sum(model.z_its[i,tp,s] for i in D_ssp[s,sp]) for tp in T if tp <=t)
		else:
			return Constraint.Skip
	model.A8_a = Constraint(T,S,S, rule = A8_a)
	# model.A8_a.pprint()
	
	def A8_b(model,t,s,sp):
		if s < sp:
			return model.Z_tssp[t,s,sp] >= 1 - sum(sum(model.z_its[i,tp,s] for i in D_ssp[s,sp]) for tp in T if tp <=t)
		else:
			return Constraint.Skip
	model.A8_b = Constraint(T,S,S, rule = A8_b)
	# model.A8_b.pprint()
	
	##### Conditional NACs #####
	def A9_a(model,i,t,s,sp):
		if s < sp and t+1 <= T_end:
			return model.z_its[i,t+1,s] - model.z_its[i,t+1,sp] >= -(2 - (Phi_tssp[t,s,sp] + model.Z_tssp[t,s,sp]))
		else:
			return Constraint.Skip
	model.A9_a = Constraint(I,T,S,S, rule = A9_a)
	# model.A9_a.pprint()
	
	def A9_b(model,i,t,s,sp):
		if s < sp and t+1 <= T_end:
			return (2 - (Phi_tssp[t,s,sp] + model.Z_tssp[t,s,sp])) >= model.z_its[i,t+1,s] - model.z_its[i,t+1,sp]
		else:
			return Constraint.Skip
	model.A9_b = Constraint(I,T,S,S, rule = A9_b)
	# model.A9_b.pprint()

	def A10_a(model,i,t,s,sp):
		if s < sp and t+1 <= T_end:
			return model.y_its[i,t+1,s] - model.y_its[i,t+1,sp] >= -M*(2 - (Phi_tssp[t,s,sp] + model.Z_tssp[t,s,sp]))
		else:
			return Constraint.Skip
	model.A10_a = Constraint(I,T,S,S, rule = A10_a)
	# model.A10_a.pprint()
	
	def A10_b(model,i,t,s,sp):
		if s < sp and t+1 <= T_end:
			return M*(2 - (Phi_tssp[t,s,sp] + model.Z_tssp[t,s,sp])) >= model.y_its[i,t+1,s] - model.y_its[i,t+1,sp]
		else:
			return Constraint.Skip
	model.A10_b = Constraint(I,T,S,S, rule = A10_b)
	# model.A10_b.pprint()

	def A11_a(model,i,j,t,s,sp):
		if s < sp:
			return model.x_ijts[i,j,t,s] - model.x_ijts[i,j,t,sp] >= -M*(2 - (Phi_tssp[t,s,sp] + model.Z_tssp[t,s,sp]))
		else:
			return Constraint.Skip
	model.A11_a = Constraint(I,I,T,S,S, rule = A11_a)
	# model.A11_a.pprint()

	def A11_b(model,i,j,t,s,sp):
		if s < sp:
			return M*(2 - (Phi_tssp[t,s,sp] + model.Z_tssp[t,s,sp])) >= model.x_ijts[i,j,t,s] - model.x_ijts[i,j,t,sp]
		else:
			return Constraint.Skip
	model.A11_b = Constraint(I,I,T,S,S, rule = A11_b)
	# model.A11_b.pprint()
	
	return model
