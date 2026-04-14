import os
import sys
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pdb
import numpy
import itertools
import time as timer
import shutil

def MSSP_model(K, R, I, T, Tend, Ht, S,
		Cbark0, Deltabar_ki, b_kt, alpha_t, n_t, beta_kth, gamma_th, d_th, Omega_k, UT_k, DT_k, eta_kth, BigMy, BigMP,
		integral_kis, D_ssp, probability):
	
	model = ConcreteModel()
	
	# Uncertain parameters 
	model.integral_kis = Param(K,I,S, initialize = integral_kis, mutable=True)
	
	# Post-realization decision variables and differentiator variables
	model.x_kits = Var(K,I,T,S, within = Binary) # 1 if a process k undergoes capacity expansion permissible point i
	
	# At-realization decision variables
	model.P_kths = Var(K,T,Ht,S, within = NonNegativeReals) # Amount of reference resource produced or consumed by process k in interval h of time t 
	model.V_ths = Var(T,Ht,S, within = NonNegativeReals) # Influx of resource j (only one resource) in interval h of time t. Can be used to mitigate resource shortage
	model.y_kths = Var(K,T,Ht,S, within = PositiveIntegers) # The number of operating units for a process k in interval h of tiem t
	
	# Other variables
	model.C_kts = Var(K,T,S) # Cumulative installed capacity of a process k
	model.Delta_kts = Var(K,T,S) # Additional capacity installed of a process k
	model.Q_ths = Var(T,Ht,S, within = NonNegativeReals) # Inventory of resource j (only one resource) in interval h of time t
	model.w_kths = Var(K,T,Ht,S) # The number of units of technology k starting up
	model.wp_kths = Var(K,T,Ht,S) # The number of units of technology k shutting down
	model.Obj1st_s = Var(S) # 1st term of the objective function
	model.Obj2nd_s = Var(S) # 2nd term of the objective function
	model.Obj3rd_s = Var(S) # 3rd term of the objective function
	model.Z_tssp = Var(T,S,S, within = Binary) # Indicator variable
	
	def L1_C0(model):
		return sum(probability[s]*(model.Obj1st_s[s] + model.Obj2nd_s[s] + model.Obj3rd_s[s]) for s in S)  
	model.objective = Objective(sense=minimize,rule=L1_C0)
	
	def L1_1st(model,s): # 1st term 
		return model.Obj1st_s[s] == sum(alpha_t[t]*model.integral_kis[k,i,s]*model.x_kits[k,i,t,s] for t in T for k in K for i in I)
	model.L1_1st = Constraint(S, rule= L1_1st)
	# model.L1_1st.pprint()
	
	def L1_2nd(model,s): # 2nd term 
		return model.Obj2nd_s[s] == sum(alpha_t[t]*n_t[t]*beta_kth[k,t,h]*model.P_kths[k,t,h,s] for t in T for h in Ht for k in K)
	model.L1_2nd = Constraint(S, rule= L1_2nd)
	# model.L1_2nd.pprint()
	
	def L1_3rd(model,s): # 3rd term 
		return model.Obj3rd_s[s] == sum(n_t[t]*gamma_th[t,h]*model.V_ths[t,h,s] for t in T for h in Ht)
	model.L1_3rd = Constraint(S, rule= L1_3rd)
	# model.L1_3rd.pprint()
	
	def L2L3_C1C2(model,k,t,s):
		if t == 1:
			return model.C_kts[k,t,s] == Cbark0 + model.Delta_kts[k,t,s]
		else:
			return model.C_kts[k,t,s] == model.C_kts[k,t-1,s] + model.Delta_kts[k,t,s]
	model.L2L3_C1C2 = Constraint(K,T,S, rule= L2L3_C1C2)
	# model.L2L3_C1C2.pprint()
	
	def L4_C3(model,k,t,s):  
		return model.Delta_kts[k,t,s] == sum(model.x_kits[k,i,t,s]*Deltabar_ki[k,i] for i in I)
	model.L4_C3 = Constraint(K,T,S, rule= L4_C3)
	# model.L4_C3.pprint()

	def L5_C4(model,k,t,s): 
		return model.Delta_kts[k,t,s] <= b_kt[k,t]
	model.L5_C4 = Constraint(K,T,S, rule= L5_C4)
	# model.L5_C4.pprint()

	def L6_C5(model,k,i,t,s): 
		if i != 1:
			return model.x_kits[k,i,t,s] <= sum(model.x_kits[k,i-1,tau,s] for tau in T if tau<=t)
		else:
			return Constraint.Skip
	model.L6_C5 = Constraint(K,I,T,S, rule= L6_C5)
	# model.L6_C5.pprint()

	def L7_C6(model,k,i,t,s):
		return sum(model.x_kits[k,i,tau,s] for tau in T if tau<=t) <= 1
	model.L7_C6 = Constraint(K,I,T,S, rule= L7_C6)
	# model.L7_C6.pprint()
	
	def L8L9_C7(model,t,h,s):
		if h == 1:
			return model.Q_ths[t,h,s] == sum(model.P_kths[k,t,h,s] for k in K) + model.V_ths[t,h,s] - d_th[t,h]
		else:
			return model.Q_ths[t,h,s] == model.Q_ths[t,h-1,s] + sum(model.P_kths[k,t,h,s] for k in K) + model.V_ths[t,h,s] - d_th[t,h]
	model.L8L9_C7 = Constraint(T,Ht,S, rule= L8L9_C7)
	# model.L8L9_C7.pprint()

	def L10_C9(model,k,t,h,s):
		return Omega_k[k]*model.y_kths[k,t,h,s] <= model.C_kts[k,t,s]
	model.L10_C9 = Constraint(K,T,Ht,S, rule= L10_C9)
	# model.L10_C9.pprint()

	def L11L12_C10(model,k,t,h,s):
		if h == 1:
			return model.w_kths[k,t,h,s] == model.y_kths[k,t,h,s]
		else:
			return model.w_kths[k,t,h,s] == model.y_kths[k,t,h,s] - model.y_kths[k,t,h-1,s]
	model.L11L12_C10 = Constraint(K,T,Ht,S, rule= L11L12_C10)
	# model.L11L12_C10.pprint()

	def L13L14_C11(model,k,t,h,s):
		if h == 1:
			return model.wp_kths[k,t,h,s] == - model.y_kths[k,t,h,s]
		else:
			return model.wp_kths[k,t,h,s] == model.y_kths[k,t,h-1,s] - model.y_kths[k,t,h,s]
	model.L13L14_C11 = Constraint(K,T,Ht,S, rule= L13L14_C11)
	# model.L13L14_C11.pprint()

	def L15_C12(model,k,t,h,hp,s): 
		if h<=hp and hp<=h+UT_k[k]-1:
			return model.w_kths[k,t,h,s] <= model.y_kths[k,t,hp,s]
		else:
			return Constraint.Skip
	model.L15_C12 = Constraint(K,T,Ht,Ht,S, rule= L15_C12)
	# model.L15_C12.pprint()

	def L16_C13(model,k,t,h,hp,s): 
		if h<=hp and hp<=h+DT_k[k]-1:
			return model.wp_kths[k,t,h,s] <= model.C_kts[k,t,s]/Omega_k[k] - model.y_kths[k,t,hp,s]
		else:
			return Constraint.Skip
	model.L16_C13 = Constraint(K,T,Ht,Ht,S, rule= L16_C13)
	# model.L16_C13.pprint()

	def L17_C14(model,k,t,h,s): 
		return model.P_kths[k,t,h,s] <= eta_kth[k,t,h]*Omega_k[k]*model.y_kths[k,t,h,s]
	model.L17_C14 = Constraint(K,T,Ht,S, rule= L17_C14)
	# model.L17_C14.pprint()

	##### Initial NACs #####
	def L18_8a(model,k,i,s): 
		if s<len(S):
			return model.x_kits[k,i,1,s] == model.x_kits[k,i,1,s+1]
		else:
			return Constraint.Skip
	model.L18_8a = Constraint(K,I,S, rule= L18_8a)
	# model.L18_8a.pprint()
	
	def L19_B1(model,r,i,tau,t,s,sp):
		if s<sp and (r,i) in D_ssp[s,sp] and tau<=t:
			return model.Z_tssp[t,s,sp] <= 1 - model.x_kits[r,i,tau,s]
		else:
			return Constraint.Skip
	model.L19_B1 = Constraint(R,I,T,T,S,S, rule = L19_B1)
	# model.L19_B1.pprint()

	def L20_B2(model,t,s,sp):
		if s<sp:
			return model.Z_tssp[t,s,sp] >= 1 - sum(model.x_kits[r,i,tau,s] for (r,i) in D_ssp[s,sp] for tau in T if tau<=t)
		else:
			return Constraint.Skip
	model.L20_B2 = Constraint(T,S,S, rule = L20_B2)
	# model.L20_B2.pprint()

	##### Conditional NACs #####
	def L21a_A5(model,k,i,t,s,sp):
		if s<sp and t!=Tend:
			return model.x_kits[k,i,t+1,s] - model.x_kits[k,i,t+1,sp] >= - (1-model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.L21a_A5 = Constraint(K,I,T,S,S, rule = L21a_A5)
	# model.L21a_A5.pprint()
	
	def L21b_A5(model,k,i,t,s,sp):
		if s<sp and t!=Tend:
			return model.x_kits[k,i,t+1,s] - model.x_kits[k,i,t+1,sp] <= 1-model.Z_tssp[t,s,sp]
		else:
			return Constraint.Skip
	model.L21b_A5 = Constraint(K,I,T,S,S, rule = L21b_A5)
	# model.L21b_A5.pprint()
	
	def L22a(model,k,t,h,s,sp): # Additional NACs 
		if s<sp:
			return model.P_kths[k,t,h,s] - model.P_kths[k,t,h,sp] <= BigMP*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.L22a = Constraint(K,T,Ht,S,S, rule = L22a)
	# model.L22a.pprint()
	
	def L22b(model,k,t,h,s,sp): # Additional NACs 
		if s<sp:
			return model.P_kths[k,t,h,s] - model.P_kths[k,t,h,sp] >= - BigMP*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.L22b = Constraint(K,T,Ht,S,S, rule = L22b)
	# model.L22b.pprint()

	def L23a(model,t,h,s,sp): # Additional NACs 
		if s<sp:
			return model.V_ths[t,h,s] - model.V_ths[t,h,sp] <= BigMP*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.L23a = Constraint(T,Ht,S,S, rule = L23a)
	# model.L23a.pprint()
	
	def L23b(model,t,h,s,sp): # Additional NACs 
		if s<sp:
			return model.V_ths[t,h,s] - model.V_ths[t,h,sp] >= - BigMP*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.L23b = Constraint(T,Ht,S,S, rule = L23b)
	# model.L23b.pprint()

	def L24a(model,k,t,h,s,sp): # Additional NACs 
		if s<sp:
			return model.y_kths[k,t,h,s] - model.y_kths[k,t,h,sp] <= BigMy*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.L24a = Constraint(K,T,Ht,S,S, rule = L24a)
	# model.L24a.pprint()
	
	def L24b(model,k,t,h,s,sp): # Additional NACs 
		if s<sp:
			return model.y_kths[k,t,h,s] - model.y_kths[k,t,h,sp] >= - BigMy*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.L24b = Constraint(K,T,Ht,S,S, rule = L24b)
	# model.L24b.pprint()
	
	return model