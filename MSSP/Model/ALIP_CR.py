import os
import sys
from pyomo.environ import *
from pyomo.opt import SolverFactory
import time as timer

def MSSP_model(I, T, T_end, S,
		Pg, Po, Png, WI, Max_Qrc, MARR, FT, Cm_i, Co_i, Ce_i, b, D, LT, RT, n, Qg1, Qo1, Qng1, LFR_LB_i, LFR_UB_i, Qrc_is, D_ssp, probability):
	
	model = ConcreteModel()
	
	# Uncertain parameters 
	model.Qrc_is = Param(I,S, initialize = Qrc_is, mutable=True)
	
	# Post-realization decision variables and differentiator variables
	model.w_ips = Var(I,T,S, within=Binary) # 1 if method ALM i is installed at month p
	
	# At-realization decision variables
	model.z_its = Var(I,T,S, within=Binary) # 1 if ALM i is uninstalled at month t
	
	# Other variables
	model.CC_s = Var(S) # Capital cost
	model.Dep_rs = Var(T,S) # Depreciation at month r
	model.GI_rs = Var(T,S) # Total gross income at month r

	model.Qg_rs = Var(T,S) # Gas flow rate at month r
	model.QgALM_irs = Var(I,T,S, within=NonNegativeReals)
	model.Qge_iprs = Var(I,T,T,S) # The gas flow rate at r with ALM i installed at p and uninstalled at t. 

	model.Qng_rs = Var(T,S) # Natural gas liquid flow rate at month r
	model.QngALM_irs = Var(I,T,S, within=NonNegativeReals)
	model.Qnge_iprs = Var(I,T,T,S) # The natural gas flow rate at r with ALM i installed at p and uninstalled at t.

	model.Qo_rs = Var(T,S) # Oil flow rate at month r
	model.QoALM_irs = Var(I,T,S, within=NonNegativeReals)
	model.Qoe_iprs = Var(I,T,T,S) # The oil flow rate at r with ALM i installed at p and uninstalled at t.

	model.Rev_rs = Var(T,S) # Revenues from gas, oil, and natural gas liquid sales
	model.TI_rs = Var(T,S) # Taxable income at month r
	model.x_rs = Var(T,S, within = Binary) # 0 if the taxanable income TI_rs is negative
	model.XTI_rs = Var(T,S, within = NonNegativeReals) # For linearization. XTI_rs = x_rs*TI_rs
	model.XTI1_rs = Var(T,S, within = NegativeReals) # For the linearization of x_rs*TI_rs
	model.y_itps = Var(I,T,T,S, within=Binary) # For linearization. y_itps = w_ips*z_its. 1 if ALM i is installed at p and uninstalled at t
	model.yQg_itprs = Var(I,T,T,T,S, within=NonNegativeReals) # Gas flow rate at r with ALM i installed at p and uninstalled at t
	model.yQg1_itprs = Var(I,T,T,T,S, within=NonNegativeReals)
	model.yQng_itprs = Var(I,T,T,T,S,within=NonNegativeReals) # Natural gas flow rate at r with ALM i installed at p and uninstalled at t
	model.yQng1_itprs = Var(I,T,T,T,S, within=NonNegativeReals)
	model.yQo_itprs = Var(I,T,T,T,S, within=NonNegativeReals) # Oil flow rate at r with ALM i installed at p and uninstalled at t
	model.yQo1_itprs = Var(I,T,T,T,S, within=NonNegativeReals)
	
	# Other variables for complete recourse
	model.bLIM_irs = Var(I,T,S, within = Binary)
	model.bREC_irs = Var(I,T,S, within = Binary)
	model.LFRbALMLIM_irs = Var(I,T,S) # Liquid flow rate at month r
	
	model.QgALMbLIM_irs = Var(I,T,S, within=NonNegativeReals)
	model.QoALMbLIM_irs = Var(I,T,S, within=NonNegativeReals)
	model.QngALMbLIM_irs = Var(I,T,S, within=NonNegativeReals)
	
	def K1_76(model):
		return sum(probability[s]*(sum((model.GI_rs[r,s] - model.XTI_rs[r,s]*FT)*1/(1+MARR)**r for r in T) - model.CC_s[s]*(1 - FT)) for s in S) #- CLIM*sum(model.bLIM_irs[i,r,s] for i in I for r in T)
	model.objective = Objective(sense=maximize, rule=K1_76)
	
	def K2_36(model,r,s):
		return model.GI_rs[r,s] == (model.Rev_rs[r,s]*(1 - RT)*(1 - LT) - sum(Cm_i[i]*model.y_itps[i,t,p,s] for i in I for t in T if t>=r for p in T if p<=r))*WI
	model.K2_36 = Constraint(T,S, rule = K2_36)
	# model.K2_36.pprint()
	
	def K3_19(model,r,s):
		return model.Rev_rs[r,s] == model.Qg_rs[r,s]*Pg + Po*model.Qo_rs[r,s] + Png*model.Qng_rs[r,s]
	model.K3_19 = Constraint(T,S, rule = K3_19)
	# model.K3_19.pprint()
	
	##### K4-K6 linearize x_rs*TI_rs. XTI_rs = x_rs*TI_rs
	def K4_60(model,r,s):
		return model.XTI_rs[r,s] + model.XTI1_rs[r,s] == model.TI_rs[r,s]
	model.K4_60 = Constraint(T,S, rule = K4_60)
	
	def K5_61(model,r,s):
		return model.x_rs[r,s]*Max_Qrc*(Pg*Qg1 + Po*Qo1 + Png*Qng1)*WI >= model.XTI_rs[r,s]
	model.K5_61 = Constraint(T,S, rule = K5_61)
	
	def K6_62(model,r,s):
		return - (1 - model.x_rs[r,s])*Max_Qrc*(Pg*Qg1 + Po*Qo1 + Png*Qng1)*WI <= model.XTI1_rs[r,s]
	model.K6_62 = Constraint(T,S, rule = K6_62)
	
	def K7_21(model,r,s):
		return model.TI_rs[r,s] == model.GI_rs[r,s] - model.Dep_rs[r,s] 
	model.K7_21 = Constraint(T,S, rule = K7_21)
	# model.K7_21.pprint()
	
	def K8_22(model,r,s):
		return model.TI_rs[r,s] <= model.x_rs[r,s]*Max_Qrc*(Pg*Qg1 + Po*Qo1 + Png*Qng1)*WI
	model.K8_22 = Constraint(T,S, rule = K8_22)
	# model.K8_22.pprint()
	
	def K9_23(model,r,s):
		return model.TI_rs[r,s] >= (model.x_rs[r,s]-1)*Max_Qrc*(Pg*Qg1 + Po*Qo1 + Png*Qng1)*WI
	model.K9_23 = Constraint(T,S, rule = K9_23)
	# model.K9_23.pprint()

	def K10_38(model,r,s):
		return model.Dep_rs[r,s] == sum(Ce_i[i]/n*model.y_itps[i,t,p,s] for i in I for t in T for p in T if t>=r and p+n-1>=r and p<=r)
	model.K10_38_con = Constraint(T,S, rule = K10_38)
	# model.K10_38_con.pprint()
	
	def K11_37(model,s):
		return  model.CC_s[s] == sum(Co_i[i]*model.y_itps[i,t,p,s]/((1+MARR)**p) for i in I for t in T for p in T)*WI
	model.K11_37_con = Constraint(S, rule = K11_37)
	# model.K11_37_con.pprint()
	
	def K12_28(model,i,s):
		return sum(model.y_itps[i,t,p,s] for t in T for p in T) <= 1
	model.K12_28 = Constraint(I,S, rule=K12_28)
	# model.K12_28.pprint()
	
	def K13_29(model,p,s):
		return sum(model.y_itps[i,t,p,s] for i in I for t in T) <= 1
	model.K13_29 = Constraint(T,S, rule=K13_29)
	# model.K13_29.pprint()
	
	def K14_30(model,t,s):
		return sum(model.y_itps[i,t,p,s] for i in I for p in T) <= 1
	model.K14_30 = Constraint(T,S, rule=K14_30)
	# model.K14_30.pprint()

	def K15_31(model,i,t,p,s):
		if t<=p: # +3:
			return model.y_itps[i,t,p,s] == 0
		else:
			return Constraint.Skip
	model.K15_31 = Constraint(I,T,T,S, rule=K15_31)
	# model.K15_31.pprint()

	def K16_32(model,i,t,p,j,k,l,s):
		if i!=j and p+1<=l and l<=t:
			return model.y_itps[i,t,p,s] + model.y_itps[j,k,l,s] <= 1
		else:
			return Constraint.Skip
	model.K16_32 = Constraint(I,T,T,I,T,T,S, rule=K16_32)
	# model.K16_32.pprint()
	
	def K17_70(model,i,r,s):
		return model.QgALM_irs[i,r,s] == sum(model.yQg_itprs[i,t,p,r,s] for t in T for p in T if t>=r and r>=p and p>=2)
	model.K17_70 = Constraint(I,T,S, rule=K17_70)
	# model.K17_70.pprint()

	def K18K50(model,r,s):
		if r>=2:
			return model.Qg_rs[r,s] == sum(model.QgALMbLIM_irs[i,r,s] for i in I)
		else:
			return model.Qg_rs[1,s] == Qg1
	model.K18K50 = Constraint(T,S, rule=K18K50)
	# model.K18K50.pprint()

	def K20_71(model,i,p,r,s):
		if r>=p and p>=2:
			return model.Qge_iprs[i,p,r,s] == model.Qg_rs[p-1,s]*model.Qrc_is[i,s]*(1+b*D*(r-p+1))**(-1/b)
		else:
			return Constraint.Skip
	model.K20_71 = Constraint(I,T,T,S, rule=K20_71)
	# model.K20_71.pprint()

	def K21_72(model,i,t,p,r,s):
		if t>=r and r>=p and p>=2:
			return model.yQg_itprs[i,t,p,r,s] + model.yQg1_itprs[i,t,p,r,s] == model.Qge_iprs[i,p,r,s]
		else:
			return Constraint.Skip
	model.K21_72 = Constraint(I,T,T,T,S, rule=K21_72)
	# model.K21_72.pprint()

	def K22_73(model,i,t,p,r,s): # Combined with (67)?
		if t>=r and r>=p and p>=2:
			return model.yQg_itprs[i,t,p,r,s] <= Max_Qrc*Qg1*model.y_itps[i,t,p,s]
		else:
			return Constraint.Skip
	model.K22_73 = Constraint(I,T,T,T,S, rule=K22_73)
	# model.K22_73.pprint()
	
	def K23_74(model,i,t,p,r,s): # Combined with (68)?
		if t>=r and r>=p and p>=2:
			return model.yQg1_itprs[i,t,p,r,s] <= sum(model.Qrc_is[i,s] for i in I)*Qg1*(1 - model.y_itps[i,t,p,s])
		else:
			return Constraint.Skip
	model.K23_74 = Constraint(I,T,T,T,S, rule=K23_74)
	# model.K23_74.pprint()
	
	def K51(model,i,r,s):
		return model.QgALMbLIM_irs[i,r,s] <= Max_Qrc*Qg1*(1-model.bLIM_irs[i,r,s])
	model.K51 = Constraint(I,T,S, rule=K51)
	# model.K51.pprint()

	def K52(model,i,r,s):
		return model.QgALMbLIM_irs[i,r,s] >= model.QgALM_irs[i,r,s] - Max_Qrc*Qg1*model.bLIM_irs[i,r,s]
	model.K52 = Constraint(I,T,S, rule=K52)
	# model.K52.pprint()

	def K53(model,i,r,s):
		return model.QgALMbLIM_irs[i,r,s] <= model.QgALM_irs[i,r,s]
	model.K53 = Constraint(I,T,S, rule=K53)
	# model.K53.pprint()

	def K24_70(model,i,r,s):
		return model.QoALM_irs[i,r,s] == sum(model.yQo_itprs[i,t,p,r,s] for t in T for p in T if t>=r and r>=p and p>=2)
	model.K24_70 = Constraint(I,T,S, rule=K24_70)
	# model.K24_70.pprint()

	def K54K25(model,r,s):
		if r>=2:
			return model.Qo_rs[r,s] == sum(model.QoALMbLIM_irs[i,r,s] for i in I)
		else:
			return model.Qo_rs[1,s] == Qo1
	model.K54K25 = Constraint(T,S, rule=K54K25)
	# model.K54K25.pprint()

	def K27_71(model,i,p,r,s):
		if r>=p and p>=2:
			return model.Qoe_iprs[i,p,r,s] == model.Qo_rs[p-1,s]*model.Qrc_is[i,s]*(1+b*D*(r-p+1))**(-1/b)
		else:
			return Constraint.Skip
	model.K27_71 = Constraint(I,T,T,S, rule=K27_71)
	# model.K27_71.pprint()

	def K28_72(model,i,t,p,r,s):
		if t>=r and r>=p and p>=2:
			return model.yQo_itprs[i,t,p,r,s] + model.yQo1_itprs[i,t,p,r,s] == model.Qoe_iprs[i,p,r,s]
		else:
			return Constraint.Skip
	model.K28_72 = Constraint(I,T,T,T,S, rule=K28_72)
	# model.K28_72.pprint()
	
	def K29_73(model,i,t,p,r,s): # Combined with (67)?
		if t>=r and r>=p and p>=2:
			return model.yQo_itprs[i,t,p,r,s] <= Max_Qrc*Qo1*model.y_itps[i,t,p,s]
		else:
			return Constraint.Skip
	model.K29_73 = Constraint(I,T,T,T,S, rule=K29_73)
	# model.K29_73.pprint()
	
	def K30_74(model,i,t,p,r,s): # Combined with (68)?
		if t>=r and r>=p and p>=2:
			return model.yQo1_itprs[i,t,p,r,s] <= sum(model.Qrc_is[i,s] for i in I)*Qo1*(1 - model.y_itps[i,t,p,s])
		else:
			return Constraint.Skip
	model.K30_74 = Constraint(I,T,T,T,S, rule=K30_74)
	# model.K30_74.pprint()
	
	def K55(model,i,r,s):
		return model.QoALMbLIM_irs[i,r,s] <= Max_Qrc*Qo1*(1-model.bLIM_irs[i,r,s])
	model.K55 = Constraint(I,T,S, rule=K55)
	# model.K55.pprint()

	def K56(model,i,r,s):
		return model.QoALMbLIM_irs[i,r,s] >= model.QoALM_irs[i,r,s] - Max_Qrc*Qo1*model.bLIM_irs[i,r,s]
	model.K56 = Constraint(I,T,S, rule=K56)
	# model.K56.pprint()

	def K57(model,i,r,s):
		return model.QoALMbLIM_irs[i,r,s] <= model.QoALM_irs[i,r,s]
	model.K57 = Constraint(I,T,S, rule=K57)
	# model.K57.pprint()

	def K31_70(model,i,r,s):
		return model.QngALM_irs[i,r,s] == sum(model.yQng_itprs[i,t,p,r,s] for t in T for p in T if t>=r and r>=p and p>=2)
	model.K31_70 = Constraint(I,T,S, rule=K31_70)
	# model.K31_70.pprint()

	def K32K58(model,r,s):
		if r>=2:
			return model.Qng_rs[r,s] == sum(model.QngALMbLIM_irs[i,r,s] for i in I)
		else:
			return model.Qng_rs[1,s] == Qng1
	model.K32K58 = Constraint(T,S, rule=K32K58)
	# model.K32K58.pprint()

	def K34_71(model,i,p,r,s):
		if r>=p and p>=2:
			return model.Qnge_iprs[i,p,r,s] == model.Qng_rs[p-1,s]*model.Qrc_is[i,s]*(1+b*D*(r-p+1))**(-1/b)
		else:
			return Constraint.Skip	
	model.K34_71 = Constraint(I,T,T,S, rule=K34_71)
	# model.K34_71.pprint()

	def K35_72(model,i,t,p,r,s):
		if t>=r and r>=p and p>=2:
			return model.yQng_itprs[i,t,p,r,s] + model.yQng1_itprs[i,t,p,r,s] == model.Qnge_iprs[i,p,r,s]
		else:
			return Constraint.Skip	
	model.K35_72 = Constraint(I,T,T,T,S, rule=K35_72)
	# model.K35_72.pprint()

	def K36_73(model,i,t,p,r,s): # Combined with (67)?
		if t>=r and r>=p and p>=2:
			return model.yQng_itprs[i,t,p,r,s] <= Max_Qrc*Qng1*model.y_itps[i,t,p,s]
		else:
			return Constraint.Skip	
	model.K36_73 = Constraint(I,T,T,T,S, rule=K36_73)
	# model.K36_73.pprint()
	
	def K37_74(model,i,t,p,r,s): # Combined with (68)?
		if t>=r and r>=p and p>=2:
			return model.yQng1_itprs[i,t,p,r,s] <= sum(model.Qrc_is[i,s] for i in I)*Qng1*(1 - model.y_itps[i,t,p,s])
		else:
			return Constraint.Skip	
	model.K37_74 = Constraint(I,T,T,T,S, rule=K37_74)
	# model.K37_74.pprint()
	
	def K59(model,i,r,s):
		return model.QngALMbLIM_irs[i,r,s] <= Max_Qrc*Qng1*(1-model.bLIM_irs[i,r,s])
	model.K59 = Constraint(I,T,S, rule=K59)
	# model.K59.pprint()

	def K60(model,i,r,s):
		return model.QngALMbLIM_irs[i,r,s] >= model.QngALM_irs[i,r,s] - Max_Qrc*Qng1*model.bLIM_irs[i,r,s]
	model.K60 = Constraint(I,T,S, rule=K60)
	# model.K60.pprint()

	def K61(model,i,r,s):
		return model.QngALMbLIM_irs[i,r,s] <= model.QngALM_irs[i,r,s]
	model.K61 = Constraint(I,T,S, rule=K61)
	# model.K61.pprint()
	
	def K38_78(model,r,s):
		if r>=2:
			return model.Qg_rs[r,s] <= Max_Qrc*Qg1*(1+b*D*(r-1))**(-1/b)
		else:
			return Constraint.Skip	
	model.K38_78 = Constraint(T,S, rule=K38_78)
	# model.K38_78.pprint()
	
	def K39_79(model,r,s): 
		if r>=2:
			return model.Qo_rs[r,s] <= Max_Qrc*Qo1*(1+b*D*(r-1))**(-1/b)
		else:
			return Constraint.Skip	
	model.K39_79 = Constraint(T,S, rule=K39_79)
	# model.K39_79.pprint()
	
	def K40_80(model,r,s): 
		if r>=2:
			return model.Qng_rs[r,s] <= Max_Qrc*Qng1*(1+b*D*(r-1))**(-1/b)
		else:
			return Constraint.Skip	
	model.K40_80 = Constraint(T,S, rule=K40_80)
	# model.K40_80.pprint()

	def K62(model,i,r,s): # LFR = Oil + Natural gas.
		return model.LFRbALMLIM_irs[i,r,s] == model.QoALMbLIM_irs[i,r,s] + model.QngALMbLIM_irs[i,r,s]
	model.K62 = Constraint(I,T,S, rule=K62)
	# model.K62.pprint()
	
	def K63(model,i,r,s):
		return model.bREC_irs[i,r,s] >= model.bLIM_irs[i,r,s]
	model.K63 = Constraint(I,T,S, rule=K63)
	# model.K63.pprint()

	def K64(model,i,r,s):
		if r<T_end:
			return model.bREC_irs[i,r,s] <= model.bREC_irs[i,r+1,s]
		else:
			return Constraint.Skip	
	model.K64 = Constraint(I,T,S, rule=K64)
	# model.K64.pprint()

	def K65(model,i,r,s):
		return Max_Qrc*Qg1*(1 - model.bREC_irs[i,r,s]) >= model.QgALMbLIM_irs[i,r,s]
	model.K65 = Constraint(I,T,S, rule=K65)
	# model.K65.pprint()

	def K66(model,i,r,s):
		return Max_Qrc*Qo1*(1 - model.bREC_irs[i,r,s]) >= model.QoALMbLIM_irs[i,r,s]
	model.K66 = Constraint(I,T,S, rule=K66)
	# model.K66.pprint()

	def K67(model,i,r,s):
		return Max_Qrc*Qng1*(1 - model.bREC_irs[i,r,s]) >= model.QngALMbLIM_irs[i,r,s]
	model.K67 = Constraint(I,T,S, rule=K67)
	# model.K67.pprint()
	
	def K68a(model,i,r,s): # Lower bound for LFR
		return (sum(model.w_ips[i,p,s] for p in T if p<=r) - sum(model.z_its[i,t,s] for t in T if t<=r-1))*LFR_LB_i[i] - model.bLIM_irs[i,r,s]*LFR_LB_i[i] <= model.LFRbALMLIM_irs[i,r,s]
	model.K68a = Constraint(I,T,S, rule = K68a)
	# model.K68a.pprint()
	
	def K68b(model,i,r,s): # Upper bound for LFR
		return (sum(model.w_ips[i,p,s] for p in T if p<=r) - sum(model.z_its[i,t,s] for t in T if t<=r-1))*LFR_UB_i[i] - model.bLIM_irs[i,r,s]*LFR_UB_i[i] >= model.LFRbALMLIM_irs[i,r,s]
	model.K68b = Constraint(I,T,S, rule = K68b)
	# model.K68b.pprint()
	
	##### Translation of Eq. (82) #####
	def K43_83(model,i,t,p,s):
		return model.y_itps[i,t,p,s] >= model.w_ips[i,p,s] + model.z_its[i,t,s] - 1
	model.K43_83 = Constraint(I,T,T,S, rule=K43_83)
	# model.K43_83.pprint()
	
	def K44_84(model,i,t,p,s):
		return model.z_its[i,t,s] >= model.y_itps[i,t,p,s]
	model.K44_84 = Constraint(I,T,T,S, rule=K44_84)
	# model.K44_84.pprint()
	
	def K45_85(model,i,t,p,s):
		return  model.w_ips[i,p,s] >= model.y_itps[i,t,p,s]
	model.K45_85 = Constraint(I,T,T,S, rule=K45_85)
	# model.K45_85.pprint()
	
	def K46_86(model,i,s):
		return sum(model.z_its[i,t,s] for t in T) == sum(model.w_ips[i,p,s] for p in T)
	model.K46_86 = Constraint(I,S, rule=K46_86)
	# model.K46_86.pprint()
	
	##### Initial NACs #####
	def K47_87(model,i,s):
		if s != 1:
			return model.w_ips[i,2,s] == model.w_ips[i,2,1]
		else:
			return Constraint.Skip
	model.K47_87 = Constraint(I,S, rule=K47_87)
	# model.K47_87.pprint()
	
	##### Conditional NACs #####
	def K48a(model,i,p,s,sp):
		if s<sp and 2<=p and p<T_end:
			return model.w_ips[i,p+1,s] - model.w_ips[i,p+1,sp] <= sum(model.w_ips[issp,r,s] for issp in D_ssp[s,sp] if i!=issp for r in T if r<=p)
		else:
			return Constraint.Skip
	model.K48a = Constraint(I,T,S,S, rule=K48a)
	# model.K48a.pprint()
	
	def K48b(model,i,p,s,sp):
		if s<sp and 2<=p and p<T_end:
			return model.w_ips[i,p+1,s] - model.w_ips[i,p+1,sp] >= - sum(model.w_ips[issp,r,s] for issp in D_ssp[s,sp] if i!=issp for r in T if r<=p)
		else:
			return Constraint.Skip
	model.K48b = Constraint(I,T,S,S, rule=K48b)
	# model.K48b.pprint()
	
	def K49a(model,i,t,s,sp):
		if s<sp and 2<=t:
			return model.z_its[i,t,s] - model.z_its[i,t,sp] <= sum(model.w_ips[issp,p,s] for issp in D_ssp[s,sp] for p in T if p<=t)
		else:
			return Constraint.Skip
	model.K49a = Constraint(I,T,S,S, rule=K49a)
	# model.K49a.pprint()
	
	def K49b(model,i,t,s,sp):
		if s<sp and 2<=t:
			return model.z_its[i,t,s] - model.z_its[i,t,sp] >= - sum(model.w_ips[issp,p,s] for issp in D_ssp[s,sp] for p in T if p<=t)
		else:
			return Constraint.Skip
	model.K49b = Constraint(I,T,S,S, rule=K49b)
	# model.K49b.pprint()
	
	return model