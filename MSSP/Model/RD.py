import os
from pyomo.environ import *
from pyomo.opt import SolverFactory
import time as timer
import shutil

def MSSP_model(I, IJ_Z_tilda, T, T_end, S, IT_beta_set, IJT_delta_set, theta_is, Max_theta_is, Z_is, probability, Y, H,\
		delta_i, delta_bar_ij, B_t, f_i, r, D_i, theta_theta, theta_Z, delta_bar, Z_tilda_ijs, Big_M, Big_M_F3, Big_M_F17F19):
	
	model = ConcreteModel()
	
	# Uncertain parameters 
	model.Z_is = Param(I,S, initialize = Z_is, mutable=True)
	model.theta_is = Param(I,S, initialize = theta_is, mutable=True)
	model.Z_tilda_ijs = Param(IJ_Z_tilda,S, initialize = Z_tilda_ijs, mutable=True)
	
	# At-realization decision variables #
	model.x_its = Var(I,T,S, within=NonNegativeReals)

	# Other variables and differentiator variables
	model.y_its = Var(I,T[1:],S, within=Binary)
	model.h_its = Var(I,T[1:],S, within=Binary)

	# Other variables
	model.alpha_its = Var(I,T,S, within=Binary)
	model.beta_its = Var(IT_beta_set, S, within=Binary)
	model.gamma_its = Var(I,T,S, within=Binary)
	model.delta_ijts = Var(IJT_delta_set, S, within=Binary)	
	model.tau_its = Var(I,T,S, within=NonNegativeReals)
	model.obj1 = Var(I,S, within=Reals)
	model.obj2 = Var(I,S, within=Reals)
	model.obj3 = Var(I,S, within=Reals)
	model.obj4 = Var(I,S, within=Reals)
	
	def F1_2(model):
		return sum(probability[s]*sum(model.obj1[i,s] + model.obj2[i,s] + model.obj3[i,s] + model.obj4[i,s] for i in I) for s in S)
	model.objective = Objective(sense=maximize, rule=F1_2)
	# model.objective.pprint()
	
	### divided objective
	def F1_obj1(model,i,s):
		return model.obj1[i,s] == sum(model.beta_its[i,t+delta_i[i],s]*model.Z_is[i,s]*(1+r)**(-t-delta_i[i]) for t in T if t<=T_end-1)
	model.F1_obj1 = Constraint(I,S, rule = F1_obj1)
	# model.F1_obj1.pprint()

	def F1_obj2(model,i,s):
		return model.obj2[i,s] == model.beta_its[i,T_end+delta_i[i],s]*model.Z_is[i,s]*((1+r)**(-T_end-delta_bar)/r + sum((1+r)**(-T_end-delta_i[i]-l) for l in range(0,delta_bar-delta_i[i])))
	model.F1_obj2 = Constraint(I,S, rule = F1_obj2)
	# model.F1_obj2.pprint()

	def F1_obj3(model,i,s):
		return model.obj3[i,s] == sum(model.delta_ijts[i,j,t+delta_bar_ij[i,j],s]*model.Z_tilda_ijs[i,j,s]*(1+r)**(-t-delta_bar_ij[i,j]) for t in T if t<=T_end-1 for j in D_i[i] if j>i)
	model.F1_obj3 = Constraint(I,S, rule = F1_obj3)
	# model.F1_obj3.pprint()

	def F1_obj4(model,i,s):
		return model.obj4[i,s] == sum(model.delta_ijts[i,j,T_end+delta_bar_ij[i,j],s]*model.Z_tilda_ijs[i,j,s]*((1+r)**(-T_end-delta_bar)/r + sum((1+r)**(-T_end-delta_bar_ij[i,j]-l) for l in range(0, delta_bar - delta_bar_ij[i,j]))) for j in D_i[i] if j>i)
	model.F1_obj4 = Constraint(I,S, rule = F1_obj4)
	# model.F1_obj4.pprint()

	def F2_3(model,i,t,s):
		return model.alpha_its[i,t,s] - model.beta_its[i,t+delta_i[i],s] >= 0
	model.F2_3 = Constraint(I,T,S, rule = F2_3)
	# model.F2_3.pprint()
	
	def F3_4(model,i,t,s):
		return sum(model.x_its[i,tp,s] for tp in T if tp<=t) - Big_M_F3*model.alpha_its[i,t,s] <= 0
	model.F3_4 = Constraint(I,T,S, rule = F3_4)
	# model.F3_4.pprint()

	def F4_5(model,t,s):
		return sum(model.x_its[i,t,s] for i in I) <= B_t[t]
	model.F4_5 = Constraint(T,S, rule = F4_5)	
	# model.F4_5.pprint()
	
	def F5_6(model,i,t,s):
		return model.x_its[i,t,s] - B_t[t]*(model.alpha_its[i,t,s] - model.beta_its[i,t+delta_i[i]-1,s] - model.gamma_its[i,t,s]) <=0
	model.F5_6 = Constraint(I,T,S, rule = F5_6)
	# model.F5_6.pprint()

	def F6F7F8_7(model,i,j,t,s):
		if j in D_i[i] and j>i and t+delta_bar_ij[i,j]<= T_end + min(delta_i[i],delta_i[j]): # from t=1+max{delta} to Tend+min{delta}
			return model.beta_its[i,t+delta_bar_ij[i,j],s] + model.beta_its[j,t+delta_bar_ij[i,j],s] - model.delta_ijts[i,j,t+delta_bar_ij[i,j],s] <= 1
		elif j in D_i[i] and j>i and t+delta_bar_ij[i,j] > T_end + min(delta_i[i],delta_i[j]): # After Tend+min{delta} to Tend+max{delta} 
			if delta_i[i] >= delta_i[j]: # If Δi >= Δj
				return model.beta_its[i,t+delta_bar_ij[i,j],s] + model.beta_its[j,T_end+delta_i[j],s] - model.delta_ijts[i,j,t+delta_bar_ij[i,j],s] <= 1
			else:
				return model.beta_its[i,T_end+delta_i[i],s] + model.beta_its[j,t+delta_bar_ij[i,j],s] - model.delta_ijts[i,j,t+delta_bar_ij[i,j],s] <= 1
		else:
			return Constraint.Skip
	model.F6F7F8_7 = Constraint(I,I,T,S, rule = F6F7F8_7)
	# model.F6F7F8_7.pprint()

	def F9F10F11_8(model,i,j,t,s):
		if j in D_i[i] and j>i and t+delta_bar_ij[i,j]<= T_end + min(delta_i[i],delta_i[j]): # from t=1+max{delta} to Tend+min{delta}
			return model.beta_its[i,t+delta_bar_ij[i,j],s] + model.beta_its[j,t+delta_bar_ij[i,j],s] - 2*model.delta_ijts[i,j,t+delta_bar_ij[i,j],s] >= 0
		elif j in D_i[i] and j>i and t+delta_bar_ij[i,j] > T_end + min(delta_i[i],delta_i[j]): # After Tend+min{delta} to Tend+max{delta} 
			if delta_i[i] >= delta_i[j]: # If Δi >= Δj
				return model.beta_its[i,t+delta_bar_ij[i,j],s] + model.beta_its[j,T_end+delta_i[j],s] - 2*model.delta_ijts[i,j,t+delta_bar_ij[i,j],s] >= 0
			else:
				return model.beta_its[i,T_end+delta_i[i],s] + model.beta_its[j,t+delta_bar_ij[i,j],s] - 2*model.delta_ijts[i,j,t+delta_bar_ij[i,j],s] >= 0
		else:
			return Constraint.Skip
	model.F9F10F11_8 = Constraint(I,I,T,S, rule = F9F10F11_8)
	# model.F9F10F11_8.pprint()

	def F12F13_9(model,i,t,s):
		if t>= 2:
			return model.tau_its[i,t,s] - model.tau_its[i,t-1,s] + model.x_its[i,t,s] - f_i[i]*(model.alpha_its[i,t,s] - model.beta_its[i,t+delta_i[i]-1,s] - model.gamma_its[i,t,s]) >= 0
		else:
			return model.tau_its[i,t,s] -model.theta_is[i,s] + model.x_its[i,t,s] - f_i[i]*(model.alpha_its[i,t,s] - model.beta_its[i,t+delta_i[i]-1,s] - model.gamma_its[i,t,s]) >= 0
	model.F12F13_9 = Constraint(I,T,S, rule = F12F13_9)	
	# model.F12F13_9.pprint()

	def F14_10(model,i,t,s):
		return model.x_its[i,t,s] - f_i[i]*(model.alpha_its[i,t,s] - model.beta_its[i,t+delta_i[i]-1,s] - model.gamma_its[i,t,s]) >= 0
	model.F14_10 = Constraint(I,T,S, rule = F14_10)	
	# model.F14_10.pprint()

	def F15_11(model,i,t,s):
		return model.tau_its[i,t,s] + model.theta_is[i,s]*model.beta_its[i,t+delta_i[i],s] <= model.theta_is[i,s]
	model.F15_11 = Constraint(I,T,S, rule = F15_11)
	# model.F15_11.pprint()

	def F16_12(model,i,t,s):
		if t != 1:
			return sum(model.x_its[i,tp,s] - f_i[i]*(model.alpha_its[i,tp,s] - model.beta_its[i,tp+delta_i[i]-1,s] - model.gamma_its[i,tp,s]) for tp in T if tp< t) - theta_theta[i]*model.y_its[i,t,s] >=0
		else:
			return Constraint.Skip
	model.F16_12 = Constraint(I,T,S, rule = F16_12)
	# model.F16_12.pprint()
	
	def F17_13(model,i,t,s):
		if t != 1:
			return sum(model.x_its[i,tp,s] for tp in T if tp < t) - (Big_M_F17F19 - theta_theta[i])*model.y_its[i,t,s] <= theta_theta[i]
		else:
			return Constraint.Skip
	model.F17_13 = Constraint(I,T,S, rule = F17_13)
	# model.F17_13.pprint()
	
	def F18_14(model,i,t,s):
		if t != 1:
			return sum(model.x_its[i,tp,s] - f_i[i]*(model.alpha_its[i,tp,s] - model.beta_its[i,tp+delta_i[i]-1,s] - model.gamma_its[i,tp,s]) for tp in T if tp < t) - theta_Z[i]*model.h_its[i,t,s] >=0
		else:
			return Constraint.Skip
	model.F18_14 = Constraint(I,T,S, rule = F18_14)
	# model.F18_14.pprint()
	
	def F19_15(model,i,t,s):
		if t != 1:
			return sum(model.x_its[i,tp,s] for tp in T if tp < t) -(Big_M_F17F19 - theta_Z[i])*model.h_its[i,t,s] <= theta_Z[i]
		else:
			return Constraint.Skip
	model.F19_15 = Constraint(I,T,S, rule = F19_15)
	# model.F19_15.pprint()
	
	def F20_16(model,i,t,s):
		if t != 1:
			return model.beta_its[i,t+delta_i[i],s] + model.gamma_its[i,t,s] <=1
		else:
			return Constraint.Skip
	model.F20_16 = Constraint(I,T,S, rule = F20_16)	
	# model.F20_16.pprint()
	
	def F21_17(model,i,t,s):
		if t<=T_end-1:
			return  model.alpha_its[i,t,s] - model.gamma_its[i,t+1,s] >= 0
		else:
			return Constraint.Skip
	model.F21_17 = Constraint(I,T,S, rule = F21_17)
	# model.F21_17.pprint()
	
	def F22(model,i,t,s): # α must be zero if the investment is not made.
		return model.alpha_its[i,t,s] <= Big_M*sum(model.x_its[i,tp,s] for tp in T if tp<=t)
	model.F22 = Constraint(I,T,S, rule = F22)
	# model.F22.pprint()
	
	def F23(model,i,t,s): # γ must keep one once it gets one.
		if t>=2:
			return model.gamma_its[i,t,s] >= model.gamma_its[i,t-1,s]
		else:
			return Constraint.Skip
	model.F23 = Constraint(I,T,S, rule = F23)
	# model.F23.pprint()
	
	##### Initial NACs #####
	def F24_18(model,i,s):
		return model.x_its[i,1,s] - sum(probability[sp]*model.x_its[i,1,sp] for sp in S) == 0
	model.F24_18 = Constraint(I,S, rule = F24_18)	
	# model.F24_18.pprint()

	##### Conditional NACs #####
	def F25_19(model,i,t,s,sp):
		if t != 1:
			return  model.x_its[i,t,s] - model.x_its[i,t,sp] + B_t[t]*(sum(model.y_its[j,t,s] + model.y_its[j,t,sp] for j in Y[s,sp]) + sum(model.h_its[j,t,s] + model.h_its[j,t,sp] for j in H[s,sp])) >= 0
		else:
			return Constraint.Skip
	model.F25_19 = Constraint(I,T,S,S, rule = F25_19)
	# model.F25_19.pprint()

	return model