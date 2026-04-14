import os
from pyomo.environ import *
from pyomo.opt import SolverFactory
import time as timer
import shutil

def MSSP_model(K, K_end, J, S, A, C, f_jjp, R, Q, d_js, D_ssp, k_ssp, probability, Cp):
	
	model = ConcreteModel()
	
	# Uncertain parameters 
	model.d_js = Param(J,S, initialize = d_js, mutable=True)
	
	# Post-realization decision variables and differentiator variables
	model.delta_jjpks = Var(A,S, within=Binary)
	
	# Other variables
	model.y_ks = Var(K,S, within=NonNegativeReals) # Vehicle load
	
	# Other variables for complete recours
	model.P_ks = Var(K,S, within=NonNegativeReals)
	
	### Objective function ###
	def H1_1(model):
		return sum(probability[s]*(sum(f_jjp[j,jp]*model.delta_jjpks[j,jp,k,s] for j in J for jp in J for k in K if (j,jp,k) in A)) for s in S)
	model.objective = Objective(sense=minimize, rule=H1_1)
	# model.objective.pprint()
	
	### Constraint except NACs ###
	def H2_2(model,s):
		return sum(model.delta_jjpks[0,j,1,s] for j in J if (0,j,1) in A) == 1
	model.H2_2 = Constraint(S, rule = H2_2)
	# model.H2_2.pprint()
	
	def H3_3(model,s):
		return sum(model.delta_jjpks[j,0,K_end,s] for j in J if (j,0,K_end) in A) == 1
	model.H3_3 = Constraint(S, rule = H3_3)
	# model.H3_3.pprint()
	
	def H4_4(model,j,s):
		if j!= 0:
			return sum(model.delta_jjpks[jp,j,k,s] for jp in J for k in K if (jp,j,k) in A) == 1
		else:
			return Constraint.Skip
	model.H4_4 = Constraint(J,S, rule = H4_4)
	# model.H4_4.pprint()

	def H5_5(model,j,s):
		if j!= 0:
			return sum(model.delta_jjpks[j,jp,k,s] for jp in J for k in K if (j,jp,k) in A) == 1
		else:
			return Constraint.Skip
	model.H5_5 = Constraint(J,S, rule = H5_5)
	# model.H5_5.pprint()
	
	def H6_6(model,j,k,s):
		if j!= 0 and k<K_end:
			return sum(model.delta_jjpks[jp,j,k,s] for jp in J if (jp,j,k) in A) == sum(model.delta_jjpks[j,jp,k+1,s] for jp in J if (j,jp,k+1) in A)
		else:
			return Constraint.Skip
	model.H6_6 = Constraint(C,S, rule = H6_6)
	# model.H6_6.pprint()
	
	# def con_7(model,j,s): # Redundant constraint
	# 	if j!= 0:
	# 		return sum(k*sum(model.x[j,jp,k,s] for jp in J if (j,jp,k) in AA) for k in K if k>=2 and (j,jp,k) in AA) - sum(k*sum(model.x[jp,j,k,s] for jp in J if (jp,j,k) in AA) for k in K if (jp,j,k) in AA) == 1
	# 	else:
	# 		return Constraint.Skip
	# model.con_7m = Constraint(model.JK, rule = con_7)	
	
	def H7_8(model,jp,s):
		if jp<0 and jp>-R:
			return sum(k*model.delta_jjpks[j,jp,k,s] for k in K for j in J if (j,jp,k) in A) <= sum(k*model.delta_jjpks[j,jp-1,k,s] for k in K for j in J if (j,jp-1,k) in A)
		else:
			return Constraint.Skip
	model.H7_8 = Constraint(J,S, rule = H7_8)	
	# model.H7_8.pprint()

	def H8_9(model,s):
		return model.y_ks[1,s] == Q - sum(model.d_js[j,s]*model.delta_jjpks[0,j,1,s] for j in J if (0,j,1) in A)
	model.H8_9 = Constraint(S, rule = H8_9)
	# model.H8_9.pprint()
	
	def H9_10(model,k,s):
		if k>1:
			return model.y_ks[k,s] <= model.y_ks[k-1,s] - sum(model.d_js[jp,s]*model.delta_jjpks[j,jp,k,s] for jp in J for j in J if (j,jp,k) in A)
		else:
			return Constraint.Skip
	model.H9_10 = Constraint(K,S, rule = H9_10)
	# model.H9_10.pprint()
	
	def H10_11(model,k,s):
		return model.y_ks[k,s] <= Q
	model.H10_11 = Constraint(K,S, rule = H10_11)	
	#model.H10_11.pprint()
	
	def H11_12(model,k,s): # Redundant constraint
		if k>1:
			return model.y_ks[k,s] >= Q*sum(model.delta_jjpks[j,jp,k,s] for j in J for jp in J if jp<=0 and (j,jp,k) in A)
		else:
			return Constraint.Skip
	model.H11_12 = Constraint(K,S, rule = H11_12)	
	# model.H11_12.pprint()
	
	### NACs ###
	
	def H12_16(model,j,s,sp): # Initial NACs
		if (0,j,1) in A and sp == s + 1:
			return model.delta_jjpks[0,j,1,s] == model.delta_jjpks[0,j,1,sp]
		else:
			return Constraint.Skip
	model.H12_16 = Constraint(J,S,S, rule = H12_16)
	# model.H12_16.pprint()

	def H13_18p(model,jpp,jppp,k,s,sp): # (18)', Conditional NACs
		if k>1 and k<= k_ssp[s,sp] and s<sp:
			return model.delta_jjpks[jpp,jppp,k,s] - model.delta_jjpks[jpp,jppp,k,sp] <= sum(model.delta_jjpks[j,jp,kp,s] for kp in K if kp<k for j in J for jp in D_ssp[s,sp] if (j,jp,kp) in A)
		else:
			return Constraint.Skip
	model.H13_18p = Constraint(A,S,S, rule = H13_18p)
	# model.H13_18p.pprint()

	def H14_18pp(model,jpp,jppp,k,s,sp): # (18)'', Conditional NACs
		if k>1 and k<= k_ssp[s,sp] and s<sp:
			return -model.delta_jjpks[jpp,jppp,k,s] + model.delta_jjpks[jpp,jppp,k,sp] <= sum(model.delta_jjpks[j,jp,kp,s] for kp in K if kp<k for j in J for jp in D_ssp[s,sp] if (j,jp,kp) in A)
		else:
			return Constraint.Skip
	model.H14_18pp = Constraint(A,S,S, rule = H14_18pp)

	return model