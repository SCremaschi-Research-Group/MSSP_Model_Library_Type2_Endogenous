import os
import sys
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pdb
import numpy
import itertools
import time as timer
import shutil

def MSSP_model(I, IU, K, K126, STEP, T, T_end, S,
		FE_it, VE_it, FO_it, VO_kt, FIPP_it, FOPP_it, delta_t, alpha_t, beta_t, gamma_t, Big_M, CARD_t, theta_i, d_t, Wcap_inital_i, UQE_i, LQE_i, Uout_i, Lout_i,
		theta_ils, D_ssp, D_ssp_AEEV, M_issp, p_s):
	
	model = ConcreteModel()
	
	# Uncertain parameters 
	model.theta_ils = Param(IU,STEP,S, initialize = theta_ils, mutable=True)
	
	# Post-realization decision variables
	model.Yexp_its = Var(I,T,S, within = Binary) # process i is expanded or not
	model.WQE_its = Var(I,T,S, within = NonNegativeReals) # Capacity expansion of process i
	model.Yoper_its = Var(I,T,S, within = Binary) # Whether or not process i is operated
	model.Ypilot_its = Var(I,T,S, within = Binary) # Whether or not pilot plant is built for process i
	model.Wrate_kts = Var(K,T,S, within = NonNegativeReals) # Flow rate of stream k
	
	# At-realization decision variables
	model.Xpurch_ts = Var(T,S, within = NonNegativeReals) # Amount of purchases of final product
	model.Xsales_ts = Var(T,S, within = NonNegativeReals) # Amount of sales of final product
	
	# Other variables and differentiator variables
	model.B_ilts = Var(I,STEP,T,S, within = Binary) # B = 1 if no expansion or pilot plant installation

	# Other variables
	model.NPV_s = Var(S) # Net present value of project
	model.Winv_ts = Var(T,S, within =NonNegativeReals) # Inventory of final product
	model.Wcap_its = Var(I,T,S, within =NonNegativeReals) # Capacity expansion of process i in time t
	model.dummy_itssp = Var(I,T,S,S, within = Binary) # 1 if s and s' are indistinguishable when process i is either operated for just one time period or a pilot plant is installed.
	
	# Indicator variable
	model.Z_tssp = Var(T,S,S, within = Binary)
	
	def E1_B1(model):
		return sum(p_s[s]*model.NPV_s[s] for s in S)
	model.objective = Objective(sense=maximize, rule=E1_B1)
	# model.objective.pprint()
	
	def E2_B2(model,s):
		return model.NPV_s[s] == -sum((FE_it[i,t]*model.Yexp_its[i,t,s] + VE_it[i,t]*model.WQE_its[i,t,s]) for i in I for t in T) \
								- sum(FO_it[i,t]*model.Yoper_its[i,t,s]*delta_t[t] for i in I for t in T) \
								- sum(VO_kt[k,t]*model.Wrate_kts[k,t,s]*delta_t[t] for k in K for t in T) \
								- sum((FOPP_it[i,t] + FIPP_it[i,t])*model.Ypilot_its[i,t,s] for i in IU for t in T) \
								- sum((alpha_t[t]*model.Xpurch_ts[t,s] - beta_t[t]*model.Xsales_ts[t,s])*delta_t[t] for t in T) \
								- sum(gamma_t[t]*model.Winv_ts[t,s] for t in T)
	model.E2_B2 = Constraint(S, rule=E2_B2)
	# model.E2_B2.pprint()
	
	def E48(model,l,t,s): 
		return model.Wrate_kts[3,t,s] <= model.theta_ils[1,l,s]*(model.Wrate_kts[1,t,s] - model.Wrate_kts[9,t,s]) + Big_M*(1-model.B_ilts[1,l,t,s]) # Stream 9 is a vent for complete recourse
	model.E48 = Constraint(STEP,T,S, rule = E48)
	# model.E48.pprint()

	def E49(model,l,t,s): 
		return model.Wrate_kts[3,t,s] >= model.theta_ils[1,l,s]*(model.Wrate_kts[1,t,s] - model.Wrate_kts[9,t,s]) - Big_M*(1-model.B_ilts[1,l,t,s]) # Stream 9 is a vent for complete recourse
	model.E49 = Constraint(STEP,T,S, rule = E49)
	# model.E49.pprint()

	def E50(model,l,t,s): 
		return model.Wrate_kts[4,t,s] <= model.theta_ils[2,l,s]*(model.Wrate_kts[2,t,s] - model.Wrate_kts[10,t,s]) + Big_M*(1-model.B_ilts[2,l,t,s]) # Stream 10 is a vent for complete recourse
	model.E50 = Constraint(STEP,T,S, rule = E50)
	# model.E50.pprint()

	def E51(model,l,t,s): 
		return model.Wrate_kts[4,t,s] >= model.theta_ils[2,l,s]*(model.Wrate_kts[2,t,s] - model.Wrate_kts[10,t,s]) - Big_M*(1-model.B_ilts[2,l,t,s]) # Stream 10 is a vent for complete recourse
	model.E51 = Constraint(STEP,T,S, rule = E51)
	# model.E51.pprint()
	
	def E7_B7(model,i,t,s):
		return sum(model.Yexp_its[i,tau,s] + model.Ypilot_its[i,tau,s] for tau in T if tau<=t) <= CARD_t[t]*(1 - model.B_ilts[i,1,t,s])
	model.E7_B7 = Constraint(IU,T,S, rule = E7_B7)
	# model.E7_B7.pprint()
	
	def E8_B8(model,i,t,s):
		return (1 - model.B_ilts[i,1,t,s]) <= sum(model.Yexp_its[i,tau,s] + model.Ypilot_its[i,tau,s] for tau in T if tau<=t)
	model.E8_B8 = Constraint(IU,T,S, rule = E8_B8)
	# model.E8_B8.pprint()

	def E9_B9(model,i,t,s):
		return sum(model.Yoper_its[i,tau,s] + model.Ypilot_its[i,tau,s] for tau in T if tau<=t) <= 1 + CARD_t[t]*(1 - model.B_ilts[i,2,t,s])
	model.E9_B9 = Constraint(IU,T,S, rule = E9_B9)
	# model.E9_B9.pprint()

	def E10_B10(model,i,t,s):
		return sum(model.Yoper_its[i,tau,s] + model.Ypilot_its[i,tau,s] for tau in T if tau<=t) >= 1 - CARD_t[t]*(1 - model.B_ilts[i,2,t,s])
	model.E10_B10 = Constraint(IU,T,S, rule = E10_B10)
	# model.E10_B10.pprint()

	def E11_B11(model,i,t,s):
		return sum(model.Yoper_its[i,tau,s] + model.Ypilot_its[i,tau,s] for tau in T if tau<=t) >= 2*model.B_ilts[i,3,t,s]
	model.E11_B11 = Constraint(IU,T,S, rule = E11_B11)
	# model.E11_B11.pprint()

	def E12_B12(model,i,t,s):
		return sum(model.Yoper_its[i,tau,s] + model.Ypilot_its[i,tau,s] for tau in T if tau<=t) <= CARD_t[t]*(1 - model.B_ilts[i,1,t,s])
	model.E12_B12 = Constraint(IU,T,S, rule = E12_B12)
	# model.E12_B12.pprint()

	def E13_B13(model,i,t,s):
		return sum(model.B_ilts[i,l,t,s] for l in STEP) == 1
	model.E13_B13 = Constraint(IU,T,S, rule = E13_B13)
	# model.E13_B13.pprint()

	def E14_B14(model,t,s):
		return model.Wrate_kts[8,t,s] == theta_i[3]*model.Wrate_kts[7,t,s]
	model.E14_B14 = Constraint(T,S, rule = E14_B14)
	# model.E14_B14.pprint()
	
	def E15_B15(model,t,s):
		return model.Wrate_kts[5,t,s] == model.Wrate_kts[3,t,s] + model.Wrate_kts[4,t,s]
	model.E15_B15 = Constraint(T,S, rule = E15_B15)
	# model.E15_B15.pprint()

	def E16_B16(model,t,s):
		return model.Wrate_kts[7,t,s] == model.Wrate_kts[5,t,s] + model.Wrate_kts[6,t,s]
	model.E16_B16 = Constraint(T,S, rule = E16_B16)
	# model.E16_B16.pprint()

	def E17_B17(model,t,s):
		if t == 1:
			return model.Winv_ts[t,s] == (model.Wrate_kts[8,t,s] + model.Xpurch_ts[t,s] - model.Xsales_ts[t,s])*delta_t[t]
		else:
			return model.Winv_ts[t,s] == model.Winv_ts[t-1,s] + (model.Wrate_kts[8,t,s] + model.Xpurch_ts[t,s] - model.Xsales_ts[t,s])*delta_t[t]
	model.E17_B17 = Constraint(T,S, rule = E17_B17)
	# model.E17_B17.pprint()
	
	def E18_B18(model,t,s):
		return delta_t[t]*model.Xsales_ts[t,s] == d_t[t]
	model.E18_B18 = Constraint(T,S, rule = E18_B18)
	# model.E18_B18.pprint()

	def E19_B19(model,t,s):
		return model.Wrate_kts[3,t,s] <= model.Wcap_its[1,t,s]
	model.E19_B19 = Constraint(T,S, rule = E19_B19)
	# model.E19_B19.pprint()

	def E20_B20(model,t,s):
		return model.Wrate_kts[4,t,s] <= model.Wcap_its[2,t,s]
	model.E20_B20 = Constraint(T,S, rule = E20_B20)
	# model.E20_B20.pprint()

	def E21_B21(model,t,s):
		return model.Wrate_kts[8,t,s] <= model.Wcap_its[3,t,s]
	model.E21_B21 = Constraint(T,S, rule = E21_B21)
	# model.E21_B21.pprint()
	
	def E22_B22(model,i,t,s):
		if t == 1:
			return model.Wcap_its[i,t,s] == Wcap_inital_i[i] + model.WQE_its[i,t,s]
		else:
			return model.Wcap_its[i,t,s] == model.Wcap_its[i,t-1,s] + model.WQE_its[i,t,s]
	model.E22_B22 = Constraint(I,T,S, rule = E22_B22)
	# model.E22_B22.pprint()

	def E23_B23a(model,i,t,s):
		return LQE_i[i]*model.Yexp_its[i,t,s] <= model.WQE_its[i,t,s]
	model.E23_B23a = Constraint(I,T,S, rule = E23_B23a)
	# model.E23_B23a.pprint()

	def E23_B23b(model,i,t,s):
		return UQE_i[i]*model.Yexp_its[i,t,s] >= model.WQE_its[i,t,s]
	model.E23_B23b = Constraint(I,T,S, rule = E23_B23b)
	# model.E23_B23b.pprint()

	def E24_B24a(model,t,s):
		return Lout_i[1]*model.Yoper_its[1,t,s] <= model.Wrate_kts[3,t,s]
	model.E24_B24a = Constraint(T,S, rule = E24_B24a)
	# model.E24_B24a.pprint()

	def E24_B24b(model,t,s):
		return Uout_i[1]*model.Yoper_its[1,t,s] >= model.Wrate_kts[3,t,s]
	model.E24_B24b = Constraint(T,S, rule = E24_B24b)
	# model.E24_B24b.pprint()

	def E25_B25a(model,t,s):
		return Lout_i[2]*model.Yoper_its[2,t,s] <= model.Wrate_kts[4,t,s]
	model.E25_B25a = Constraint(T,S, rule = E25_B25a)
	# model.E25_B25a.pprint()

	def E25_B25b(model,t,s):
		return Uout_i[2]*model.Yoper_its[2,t,s] >= model.Wrate_kts[4,t,s]
	model.E25_B25b = Constraint(T,S, rule = E25_B25b)
	# model.E25_B25b.pprint()

	def E26_B26a(model,t,s):
		return Lout_i[3]*model.Yoper_its[3,t,s] <= model.Wrate_kts[8,t,s]
	model.E26_B26a = Constraint(T,S, rule = E26_B26a)
	# model.E26_B26a.pprint()

	def E26_B26b(model,t,s):
		return Uout_i[3]*model.Yoper_its[3,t,s] >= model.Wrate_kts[8,t,s]
	model.E26_B26b = Constraint(T,S, rule = E26_B26b)
	# model.E26_B26b.pprint()

	def E27_B27(model,i,t,s):
		return sum(model.Yexp_its[i,tau,s] for tau in T if tau<=t) >= model.Yoper_its[i,t,s]
	model.E27_B27 = Constraint(IU,T,S, rule = E27_B27)
	# model.E27_B27.pprint()

	def E28_B28(model,i,t,s):
		return model.Yoper_its[i,t,s] >= model.Yexp_its[i,t,s]
	model.E28_B28 = Constraint(I,T,S, rule = E28_B28)
	# model.E28_B28.pprint()

	def E29_B34(model,i,s):
		return sum(model.Ypilot_its[i,tau,s] for tau in T) <= 1
	model.E29_B34 = Constraint(IU,S, rule = E29_B34)
	# model.E29_B34.pprint()

	def E30_B35(model,i,t,tau,s):
		if tau <= t:
			return model.Yexp_its[i,tau,s] + model.Ypilot_its[i,t,s] <= 1
		else:
			return Constraint.Skip
	model.E30_B35 = Constraint(IU,T,T,S, rule = E30_B35)
	# model.E30_B35.pprint()

	##### Initial NACs #####
	def E31_B29(model,i,s,sp):
		if s<sp:
			return model.Yoper_its[i,1,s] == model.Yoper_its[i,1,sp]
		else:
			return Constraint.Skip
	model.E31_B29 = Constraint(I,S,S, rule = E31_B29)
	# model.E31_B29.pprint()

	def E32_B30(model,i,s,sp):
		if s<sp:
			return model.Ypilot_its[i,1,s] == model.Ypilot_its[i,1,sp]
		else:
			return Constraint.Skip
	model.E32_B30 = Constraint(IU,S,S, rule = E32_B30)
	# model.E32_B30.pprint()

	def E33_B31(model,i,s,sp):
		if s<sp:
			return model.Yexp_its[i,1,s] == model.Yexp_its[i,1,sp]
		else:
			return Constraint.Skip
	model.E33_B31 = Constraint(I,S,S, rule = E33_B31)
	# model.E33_B31.pprint()

	def E34_B32(model,i,s,sp):
		if s<sp:
			return model.WQE_its[i,1,s] == model.WQE_its[i,1,sp]
		else:
			return Constraint.Skip
	model.E34_B32 = Constraint(I,S,S, rule = E34_B32)
	# model.E34_B32.pprint()

	def E35_B33(model,k,s,sp):
		if s<sp:
			return model.Wrate_kts[k,1,s] == model.Wrate_kts[k,1,sp]
		else:
			return Constraint.Skip
	model.E35_B33 = Constraint(K126,S,S, rule = E35_B33)
	# model.E35_B33.pprint()
	
	##### indicator constraints #####
	def E36_B36(model,i,t,s,sp):
		if s<sp and i in D_ssp[s,sp]:
			return model.B_ilts[i,1,t,s] + model.dummy_itssp[i,t,s,sp] >= model.Z_tssp[t,s,sp]
		else:
			return Constraint.Skip
	model.E36_B36 = Constraint(IU,T,S,S, rule = E36_B36)
	# model.E36_B36.pprint()

	def E37_B37(model,t,s,sp):
		if s<sp:
			return sum((1 - (model.B_ilts[i,1,t,s] + model.dummy_itssp[i,t,s,sp])) for i in D_ssp[s,sp]) + model.Z_tssp[t,s,sp] >= 1
		else:
			return Constraint.Skip
	model.E37_B37 = Constraint(T,S,S, rule = E37_B37)
	# model.E37_B37.pprint()

	def E38_B38(model,i,t,s,sp):
		if s<sp:
			return model.dummy_itssp[i,t,s,sp] >= model.B_ilts[i,2,t,s] + M_issp[i,s,sp] - 1 
		else:
			return Constraint.Skip
	model.E38_B38 = Constraint(IU,T,S,S, rule = E38_B38)
	# model.E38_B38.pprint()

	def E39_B39(model,i,t,s,sp):
		if s<sp:
			return model.B_ilts[i,2,t,s] >= model.dummy_itssp[i,t,s,sp] 
		else:
			return Constraint.Skip
	model.E39_B39 = Constraint(IU,T,S,S, rule = E39_B39)
	# model.E39_B39.pprint()

	def E40_B40(model,i,t,s,sp):
		if s<sp:
			return M_issp[i,s,sp] >= model.dummy_itssp[i,t,s,sp] 
		else:
			return Constraint.Skip
	model.E40_B40 = Constraint(IU,T,S,S, rule = E40_B40)
	# model.E40_B40.pprint()

	##### Conditional NACs #####
	def E41a_B41(model,t,s,sp):
		if s<sp:
			return model.Xpurch_ts[t,s] <= model.Xpurch_ts[t,sp] + Big_M*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E41a_B41 = Constraint(T,S,S, rule = E41a_B41)
	# model.E41a_B41.pprint()

	def E41b_B42(model,t,s,sp):
		if s<sp:
			return model.Xpurch_ts[t,s] >= model.Xpurch_ts[t,sp] - Big_M*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E41b_B42 = Constraint(T,S,S, rule = E41b_B42)
	# model.E41b_B42.pprint()

	def E42a_B43(model,t,s,sp):
		if s<sp:
			return model.Xsales_ts[t,s] <= model.Xsales_ts[t,sp] + Big_M*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E42a_B43 = Constraint(T,S,S, rule = E42a_B43)
	# model.E42a_B43.pprint()

	def E42b_B44(model,t,s,sp):
		if s<sp:
			return model.Xsales_ts[t,s] >= model.Xsales_ts[t,sp] - Big_M*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E42b_B44 = Constraint(T,S,S, rule = E42b_B44)
	# model.E42b_B44.pprint()

	def E43a_B45(model,i,t,s,sp):
		if s<sp and t<=T_end-1:
			return model.Yoper_its[i,t+1,s] <= model.Yoper_its[i,t+1,sp] + (1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E43a_B45 = Constraint(I,T,S,S, rule = E43a_B45)
	# model.E43a_B45.pprint()

	def E43b_B46(model,i,t,s,sp):
		if s<sp and t<=T_end-1:
			return model.Yoper_its[i,t+1,s] >= model.Yoper_its[i,t+1,sp] - (1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E43b_B46 = Constraint(I,T,S,S, rule = E43b_B46)
	# model.E43b_B46.pprint()

	def E44a_B47(model,i,t,s,sp):
		if s<sp and t<=T_end-1:
			return model.Yexp_its[i,t+1,s] <= model.Yexp_its[i,t+1,sp] + (1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E44a_B47 = Constraint(I,T,S,S, rule = E44a_B47)
	# model.E44a_B47.pprint()

	def E44b_B48(model,i,t,s,sp):
		if s<sp and t<=T_end-1:
			return model.Yexp_its[i,t+1,s] >= model.Yexp_its[i,t+1,sp] - (1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E44b_B48 = Constraint(I,T,S,S, rule = E44b_B48)
	# model.E44b_B48.pprint()

	def E45a_B49(model,i,t,s,sp):
		if s<sp and t<=T_end-1:
			return model.Ypilot_its[i,t+1,s] <= model.Ypilot_its[i,t+1,sp] + (1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E45a_B49 = Constraint(IU,T,S,S, rule = E45a_B49)
	# model.E45a_B49.pprint()

	def E45b_B50(model,i,t,s,sp):
		if s<sp and t<=T_end-1:
			return model.Ypilot_its[i,t+1,s] >= model.Ypilot_its[i,t+1,sp] - (1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E45b_B50 = Constraint(IU,T,S,S, rule = E45b_B50)
	# model.E45b_B50.pprint()

	def E46a_B51(model,i,t,s,sp):
		if s<sp and t<=T_end-1:
			return model.WQE_its[i,t+1,s] <= model.WQE_its[i,t+1,sp] + Big_M*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E46a_B51 = Constraint(I,T,S,S, rule = E46a_B51)
	# model.E46a_B51.pprint()

	def E46b_B52(model,i,t,s,sp):
		if s<sp and t<=T_end-1:
			return model.WQE_its[i,t+1,s] >= model.WQE_its[i,t+1,sp] - Big_M*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E46b_B52 = Constraint(I,T,S,S, rule = E46b_B52)
	# model.E46b_B52.pprint()

	def E47a_B53(model,k,t,s,sp):
		if s<sp and t<=T_end-1:
			return model.Wrate_kts[k,t+1,s] <= model.Wrate_kts[k,t+1,sp] + Big_M*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E47a_B53 = Constraint(K126,T,S,S, rule = E47a_B53)
	# model.E47a_B53.pprint()

	def E47b_B54(model,k,t,s,sp):
		if s<sp and t<=T_end-1:
			return model.Wrate_kts[k,t+1,s] >= model.Wrate_kts[k,t+1,sp] - Big_M*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.E47b_B54 = Constraint(K126,T,S,S, rule = E47b_B54)
	# model.E47b_B54.pprint()

	return model