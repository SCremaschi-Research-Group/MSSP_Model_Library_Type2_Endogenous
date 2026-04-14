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

def MSSP_model(I, L, K, T, Tend, R, Rend, R_i, aapSET_r, aapLIST, S,
		d, g_l, h_l, umin_l, umax_l, dp_i, gp_ik, hp_ik, alpha_i, v_i, e_i, wmin_k, wmax_k, fmin_i, fmax_i, c_i, b, beta_t, Fmax_t, a_r, ap_r, Max_thetamax_i, MAX_umax, 
		thetamax_is, m_is, D_ssp, probability):
	
	model = ConcreteModel()
	
	# Uncertain parameters 
	model.thetamax_is = Param(I,S, initialize = thetamax_is, mutable=True)
	model.m_is = Param(I,S, initialize = m_is, mutable=True)
	
	# Post-realization decision variables and differentiator variables
	model.deltap_ikrs = Var(I,K,R,S, within = Binary) # 1 if the secondary pipeline of type k is established for reservoir i during the rth planning segment
	
	# At-realization decision variables
	model.x_its = Var(I,T,S, within = NonNegativeReals) # The amount of oil (Mbbls) recovered by reservoir i
	model.q_ikts = Var(I,K,T,S, within = NonNegativeReals) # The flow on the secondary pipeline associated with reservoir i and pipeline type k
	model.u_lts = Var(L,T,S, within = NonNegativeReals) # CO2 flow on the primary pipeline l
	model.eta_ikts = Var(I,K,T,S, within = Binary) # 1 if reservoir i and secondary pipeline k are used
	model.y_is = Var(I,S, within = NonNegativeReals) # Time period the utilization of reservoir i is started for the first time, otherwise 0
	model.w_is = Var(I,S, within = NonNegativeReals) # The flow (like line capacity) on the secondary pipeline associated with reservoir i
	
	# Other variables
	model.delta_ls = Var(L,S, within = Binary) # 1 if the primary pipeline of size l is established
	
	model.Obj1st_s = Var(S) # 1st term of the objective function
	model.Obj2nd_s = Var(S) # 2nd term of the objective function
	model.Obj3rd_s = Var(S) # 3rd term of the objective function
	model.Obj4th_s = Var(S) # 4th term of the objective function
	model.Obj5th_s = Var(S) # 5th term of the objective function
	model.Obj6th_s = Var(S) # 6th term of the objective function
	
	# For NACs
	model.phi_rssp = Var(R,S,S)
	
	def M1_1p(model):
		return sum(probability[s]*(model.Obj1st_s[s] + model.Obj2nd_s[s] - model.Obj3rd_s[s] - model.Obj4th_s[s] - model.Obj5th_s[s] - model.Obj6th_s[s]) for s in S)  
	model.objective = Objective(sense=maximize,rule=M1_1p)

	def Obj1(model,s): # M1 1st term. Revenue from recovered oil
		return model.Obj1st_s[s] == sum(beta_t[t]*v_i[i]*model.x_its[i,t,s] for t in T for i in I)
	model.Obj1 = Constraint(S, rule= Obj1)
	# model.Obj1.pprint()

	def Obj2(model,s): # M1 2nd term. Revenue from CO2 credit
		return model.Obj2nd_s[s] == sum(beta_t[t]*b*alpha_i[i]*model.q_ikts[i,k,t,s] for t in T for k in K for i in I)
	model.Obj2 = Constraint(S, rule= Obj2)
	# model.Obj2.pprint()

	def Obj3(model,s): # M1 3rd term. The cost of establishing the primary pipeline
		return model.Obj3rd_s[s] == sum(g_l[l]*model.delta_ls[l,s] for l in L)
	model.Obj3 = Constraint(S, rule= Obj3)
	# model.Obj3.pprint()

	def Obj4(model,s): # M1 4th term. The cost of establishing the secondary pipeline
		return model.Obj4th_s[s] == sum(beta_t[a_r[r]]*gp_ik[i,k]*model.deltap_ikrs[i,k,r,s] for i in I for k in K for r in R_i[i])
	model.Obj4 = Constraint(S, rule= Obj4)
	# model.Obj4.pprint()

	def Obj5(model,s): # M1 5th term. Variable costs to transfer CO2 through a primary pipeline
		return model.Obj5th_s[s] == sum(beta_t[t]*d*h_l[l]*model.u_lts[l,t,s] for l in L for t in T)
	model.Obj5 = Constraint(S, rule= Obj5)
	# model.Obj5.pprint()

	def Obj6(model,s): # M1 6th term. Variable costs to transfer CO2 through secondary pipelines
		return model.Obj6th_s[s] == sum(beta_t[t]*dp_i[i]*hp_ik[i,k]*model.q_ikts[i,k,t,s] for k in K for i in I for t in T)
	model.Obj6 = Constraint(S, rule= Obj6)
	# model.Obj6.pprint()

	def M2_2p(model,s): # At most, one type is selected for the primary pipeline.
		return sum(model.delta_ls[l,s] for l in L) <= 1
	model.M2_2p = Constraint(S, rule= M2_2p)
	# model.M2_2p.pprint()

	def M3_3p(model,i,s): # If there is no primary pipeline then the secondary pipelines are not established.
		return sum(model.deltap_ikrs[i,k,r,s] for k in K for r in R_i[i]) <= sum(model.delta_ls[l,s] for l in L)
	model.M3_3p = Constraint(I,S, rule= M3_3p)
	# model.M3_3p.pprint()

	def M4_4p(model,i,t,s): # At most, one type is selected for the secondary pipeline k associated with reservoir i.
		return sum(model.eta_ikts[i,k,t,s] for k in K) <= 1
	model.M4_4p = Constraint(I,T,S, rule= M4_4p)
	# model.M4_4p.pprint()

	# M5 and M6 imply that the operating life of reservoir i (in the case of utilization) equals e_i consective periods.
	def M5_5p(model,i,k,s): 
		return sum(model.eta_ikts[i,k,t,s] for t in T) == e_i[i]*sum(model.deltap_ikrs[i,k,r,s] for r in R_i[i])
	model.M5_5p = Constraint(I,K,S, rule= M5_5p)
	# model.M5_5p.pprint()

	def M6_6p(model,i,k,t,s):
		if t<=Tend-2:
			return sum(model.eta_ikts[i,k,tp,s] for tp in T if tp>=t+2) <= e_i[i]*(1 - model.eta_ikts[i,k,t,s] + model.eta_ikts[i,k,t+1,s])
		else:
			return Constraint.Skip
	model.M6_6p = Constraint(I,K,T,S, rule= M6_6p)
	# model.M6_6p.pprint()

	# M7 and M8 determine y_is, the time period in which the utilization of reservoir i is started for the first time.
	def M7a_7p(model,i,k,s): 
		return model.eta_ikts[i,k,1,s] <= model.y_is[i,s]
	model.M7a_7p = Constraint(I,K,S, rule= M7a_7p)
	# model.M7a_7p.pprint()

	def M7b_7p(model,i,k,s):
		return model.y_is[i,s] <= 1 + Tend*(1 - model.eta_ikts[i,k,1,s])
	model.M7b_7p = Constraint(I,K,S, rule= M7b_7p)
	# model.M7b_7p.pprint()

	def M8a_8p(model,i,k,t,s):
		if t>=2:
			return -t*(model.eta_ikts[i,k,t-1,s] - model.eta_ikts[i,k,t,s]) <= model.y_is[i,s]
		else:
			return Constraint.Skip
	model.M8a_8p = Constraint(I,K,T,S, rule= M8a_8p)
	# model.M8a_8p.pprint()

	def M8b_8p(model,i,k,t,s):
		if t>=2:
			return model.y_is[i,s] <= t + Tend*(1 + model.eta_ikts[i,k,t-1,s] - model.eta_ikts[i,k,t,s])
		else:
			return Constraint.Skip
	model.M8b_8p = Constraint(I,K,T,S, rule= M8b_8p)
	# model.M8b_8p.pprint()

	# In the case of utilization of reservoir i, the start time of operation belongs to one of the planning segments r.
	def M9a_9p(model,i,s):
		return sum(a_r[r]*model.deltap_ikrs[i,k,r,s] for k in K for r in R_i[i]) <= model.y_is[i,s]
	model.M9a_9p = Constraint(I,S, rule= M9a_9p)
	# model.M9a_9p.pprint()

	def M9b_9p(model,i,s): 
		return model.y_is[i,s] <= sum(ap_r[r]*model.deltap_ikrs[i,k,r,s] for k in K for r in R_i[i])
	model.M9b_9p = Constraint(I,S, rule= M9b_9p)
	# model.M9b_9p.pprint()

	# CO2 flow rate in secondary pipelines must be within the upper and lower bounds.
	def M10a_10p(model,i,s):
		return sum(max(fmin_i[i],wmin_k[k])*model.deltap_ikrs[i,k,r,s] for k in K for r in R_i[i]) <= model.w_is[i,s]
	model.M10a_10p = Constraint(I,S, rule= M10a_10p)
	# model.M10a_10p.pprint()

	def M10b_10p(model,i,s):
		return  model.w_is[i,s] <= sum(min(fmax_i[i],wmax_k[k])*model.deltap_ikrs[i,k,r,s] for k in K for r in R_i[i])
	model.M10b_10p = Constraint(I,S, rule= M10b_10p)
	# model.M10b_10p.pprint()

	# M11 and M12 ensure that if secondary pipe k is used for resevoir i, q_ikts = w_is, otherwise q_ikts = 0.
	def M11a_11p(model,i,k,t,s): 
		return model.w_is[i,s] - fmax_i[i]*(1-model.eta_ikts[i,k,t,s]) <= model.q_ikts[i,k,t,s]
	model.M11a_11p = Constraint(I,K,T,S, rule= M11a_11p)
	# model.M11a_11p.pprint()
	
	def M11b_11p(model,i,k,t,s): 
		return model.q_ikts[i,k,t,s] <= model.w_is[i,s]
	model.M11b_11p = Constraint(I,K,T,S, rule= M11b_11p)
	# model.M11b_11p.pprint()

	def M12_12p(model,i,k,t,s):
		return model.q_ikts[i,k,t,s] <= fmax_i[i]*model.eta_ikts[i,k,t,s]
	model.M12_12p = Constraint(I,K,T,S, rule= M12_12p)
	# model.M12_12p.pprint()

	def M13_13p(model,i,k,s): # Amount of stored CO2 in a reservoir cannot exceed its capacity.
		return sum(alpha_i[i]*model.q_ikts[i,k,t,s] for t in T) <= c_i[i]
	model.M13_13p = Constraint(I,K,S, rule= M13_13p)
	# model.M13_13p.pprint()

	def M14a_14p(model,t,s): # Total flowrate of secondary pipelines = Flowrate of primary pipeline
		return sum(model.q_ikts[i,k,t,s] for i in I for k in K) == sum(model.u_lts[l,t,s] for l in L)
	model.M14a_14p = Constraint(T,S, rule= M14a_14p)
	# model.M14a_14p.pprint()

	def M14b_14p(model,t,s): # Flowrate of primary pipeline <= Maximum flowrate
		return sum(model.u_lts[l,t,s] for l in L) <= Fmax_t[t]
	model.M14b_14p = Constraint(T,S, rule= M14b_14p)
	# model.M14b_14p.pprint()

	# CO2 flow rate in primary pipeline must be within the upper and lower bounds.
	def M15a_15p(model,l,t,s):
		return umin_l[l]*model.delta_ls[l,s] <= model.u_lts[l,t,s]
	model.M15a_15p = Constraint(L,T,S, rule= M15a_15p)
	# model.M15a_15p.pprint()
	
	def M15b_15p(model,l,t,s):
		return model.u_lts[l,t,s] <= umax_l[l]*model.delta_ls[l,s]
	model.M15b_15p = Constraint(L,T,S, rule= M15b_15p)
	# model.M15b_15p.pprint()
	
	# M16 and M17 indicate the decrease in oil yield during the oil recovery periods.
	def M16_16p(model,i,k,t,s): 
		return model.x_its[i,t,s] <= model.thetamax_is[i,s]*model.q_ikts[i,k,t,s]
	model.M16_16p = Constraint(I,K,T,S, rule= M16_16p)
	# model.M16_16p.pprint()
	
	def M17_17p(model,i,k,t,s):
		if t>=2:
			return model.x_its[i,t,s] <= model.m_is[i,s]*model.x_its[i,t-1,s] + model.thetamax_is[i,s]*fmax_i[i]*(2-model.eta_ikts[i,k,t-1,s]-model.eta_ikts[i,k,t,s])
		else:
			return Constraint.Skip
	model.M17_17p = Constraint(I,K,T,S, rule= M17_17p)
	# model.M17_17p.pprint()

	##### Initial NACs #####
	def M18(model,i,k,s,sp):
		if s<sp:
			return model.deltap_ikrs[i,k,1,s] == model.deltap_ikrs[i,k,1,sp]
		else:
			return Constraint.Skip
	model.M18 = Constraint(I,K,S,S, rule = M18)
	# model.M18.pprint()
	
	##### Indicator variable #####
	def M19_21(model,r,s,sp):
		if s<sp:
			return model.phi_rssp[r,s,sp] == sum(model.deltap_ikrs[i,k,rp,s] for i in D_ssp[s,sp] for k in K for rp in R_i[i] if rp<=r)
		else:
			return Constraint.Skip
	model.M19_21 = Constraint(R,S,S, rule= M19_21)
	# model.M19_21.pprint()
	
	##### Conditional NACs #####
	def M20a_22(model,i,r,s,sp):
		if s<sp:
			return model.y_is[i,s] - model.y_is[i,sp] >= - Tend*(model.phi_rssp[r,s,sp] + 1 - sum(model.deltap_ikrs[i,k,r,s] for k in K))
		else:
			return Constraint.Skip
	model.M20a_22 = Constraint(I,R,S,S, rule = M20a_22)
	# model.M20a_22.pprint()
	
	def M20b_22(model,i,r,s,sp):
		if s<sp:
			return model.y_is[i,s] - model.y_is[i,sp] <= Tend*(model.phi_rssp[r,s,sp] + 1 - sum(model.deltap_ikrs[i,k,r,s] for k in K))
		else:
			return Constraint.Skip
	model.M20b_22 = Constraint(I,R,S,S, rule = M20b_22)
	# model.M20b_22.pprint()
	
	def M21a_23(model,r,t,l,s,sp):
		if s<sp:
			return model.u_lts[l,t,s] - model.u_lts[l,t,sp] >= - max(MAX_umax,Fmax_t[t])*model.phi_rssp[r,s,sp]
		else:
			return Constraint.Skip
	model.M21a_23 = Constraint(aapLIST,L,S,S, rule = M21a_23)
	# model.M21a_23.pprint()
	
	def M21b_23(model,r,t,l,s,sp):
		if s<sp:
			return model.u_lts[l,t,s] - model.u_lts[l,t,sp] <= max(MAX_umax,Fmax_t[t])*model.phi_rssp[r,s,sp]
		else:
			return Constraint.Skip
	model.M21b_23 = Constraint(aapLIST,L,S,S, rule = M21b_23)
	# model.M21b_23.pprint()

	def M22a_24(model,i,k,r,t,s,sp):
		if s<sp:
			return model.eta_ikts[i,k,t,s] - model.eta_ikts[i,k,t,sp] >= - model.phi_rssp[r,s,sp]
		else:
			return Constraint.Skip
	model.M22a_24 = Constraint(I,K,aapLIST,S,S, rule = M22a_24)
	# model.M22a_24.pprint()

	def M22b_24(model,i,k,r,t,s,sp):
		if s<sp:
			return model.eta_ikts[i,k,t,s] - model.eta_ikts[i,k,t,sp] <= model.phi_rssp[r,s,sp]
		else:
			return Constraint.Skip
	model.M22b_24 = Constraint(I,K,aapLIST,S,S, rule = M22b_24)
	# model.M22b_24.pprint()

	def M23a_25(model,i,k,r,t,s,sp):
		if s<sp:
			return model.q_ikts[i,k,t,s] - model.q_ikts[i,k,t,sp] >= - max(fmax_i[i],Fmax_t[t])*model.phi_rssp[r,s,sp]
		else:
			return Constraint.Skip
	model.M23a_25 = Constraint(I,K,aapLIST,S,S, rule = M23a_25)
	# model.M23a_25.pprint()

	def M23b_25(model,i,k,r,t,s,sp):
		if s<sp:
			return model.q_ikts[i,k,t,s] - model.q_ikts[i,k,t,sp] <= max(fmax_i[i],Fmax_t[t])*model.phi_rssp[r,s,sp]
		else:
			return Constraint.Skip
	model.M23b_25 = Constraint(I,K,aapLIST,S,S, rule = M23b_25)
	# model.M23b_25.pprint()

	def M24a_26(model,i,r,s,sp):
		if s<sp:
			return model.w_is[i,s] - model.w_is[i,sp] >= - (fmax_i[i]-fmin_i[i])*(model.phi_rssp[r,s,sp] + 1 - sum(model.deltap_ikrs[i,k,r,s] for k in K))
		else:
			return Constraint.Skip
	model.M24a_26 = Constraint(I,R,S,S, rule = M24a_26)
	# model.M24a_26.pprint()

	def M24b_26(model,i,r,s,sp):
		if s<sp:
			return model.w_is[i,s] - model.w_is[i,sp] <= (fmax_i[i]-fmin_i[i])*(model.phi_rssp[r,s,sp] + 1 - sum(model.deltap_ikrs[i,k,r,s] for k in K))
		else:
			return Constraint.Skip
	model.M24b_26 = Constraint(I,R,S,S, rule = M24b_26)
	# model.M24b_26.pprint()
	
	def M25a_27(model,i,r,t,s,sp):
		if s<sp:
			return model.x_its[i,t,s] - model.x_its[i,t,sp] >= - max(fmax_i[i],Fmax_t[t])*Max_thetamax_i[i]*model.phi_rssp[r,s,sp]
		else:
			return Constraint.Skip
	model.M25a_27 = Constraint(I,aapLIST,S,S, rule = M25a_27)
	# model.M25a_27.pprint()
	
	def M25b_27(model,i,r,t,s,sp):
		if s<sp:
			return model.x_its[i,t,s] - model.x_its[i,t,sp] <= max(fmax_i[i],Fmax_t[t])*Max_thetamax_i[i]*model.phi_rssp[r,s,sp]
		else:
			return Constraint.Skip
	model.M25b_27 = Constraint(I,aapLIST,S,S, rule = M25b_27)
	# model.M25b_27.pprint()
	
	def M26a_28(model,i,k,r,s,sp):
		if s<sp and r != Rend:
			return model.deltap_ikrs[i,k,r+1,s] - model.deltap_ikrs[i,k,r+1,sp] >= - model.phi_rssp[r,s,sp]
		else:
			return Constraint.Skip
	model.M26a_28 = Constraint(I,K,R,S,S, rule = M26a_28)
	# model.M26a_28.pprint()
	
	def M26b_28(model,i,k,r,s,sp):
		if s<sp and r != Rend:
			return model.deltap_ikrs[i,k,r+1,s] - model.deltap_ikrs[i,k,r+1,sp] <= model.phi_rssp[r,s,sp]
		else:
			return Constraint.Skip
	model.M26b_28 = Constraint(I,K,R,S,S, rule = M26b_28)
	# model.M26b_28.pprint()
	
	return model