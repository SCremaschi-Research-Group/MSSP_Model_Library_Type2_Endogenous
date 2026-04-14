import os
from pyomo.environ import *
from pyomo.opt import SolverFactory
import time as timer
import shutil

def MSSP_model(F, FPSO, RF, F_rf, F_fpso, F_fpsoLIST, I, Iend, T, T1, TC, Tend, K, S,
		FC_ffpsot, FCwell_ft, FCFPSO_fpsot, VCliq_fpsot, VCgas_fpsot, OCgas_rft, OCliq_rft, ftax_rft, fPO_rfi, fCR_rft, Loil_rfi, Uoil_rfi, alpha_t, l1, l2,
		a_oil_ffpso, b_oil_ffpso, c_oil_ffpso, d_oil_ffpso, dis_t, delta_t, Big_M, Big_U, Big_Uwelloil_ffpso, Uoil_fpso, Uliq_fpso, Ugas_fpso, myu, UIwell_t, UNwell_f, max_REC, min_REC, epsilon,
		REC_fs, alpha_o_fs, alpha_wc_fs, alpha_gc_fs, a_wc_ffpsos, b_wc_ffpsos, c_wc_ffpsos, d_wc_ffpsos, a_gc_ffpsos, b_gc_ffpsos, c_gc_ffpsos, d_gc_ffpsos, Big_Mwc_ffpsos, Big_Mgc_ffpsos, N1_f, N2_f, D_ssp, probability):
	
	model = ConcreteModel()
	
	# Uncertain parameters 
	model.a_gc_ffpsos = Param(F,FPSO,S, initialize = a_gc_ffpsos, mutable=True)
	model.b_gc_ffpsos = Param(F,FPSO,S, initialize = b_gc_ffpsos, mutable=True)
	model.c_gc_ffpsos = Param(F,FPSO,S, initialize = c_gc_ffpsos, mutable=True)
	model.d_gc_ffpsos = Param(F,FPSO,S, initialize = d_gc_ffpsos, mutable=True)
	model.a_wc_ffpsos = Param(F,FPSO,S, initialize = a_wc_ffpsos, mutable=True)
	model.b_wc_ffpsos = Param(F,FPSO,S, initialize = b_wc_ffpsos, mutable=True)
	model.c_wc_ffpsos = Param(F,FPSO,S, initialize = c_wc_ffpsos, mutable=True)
	model.d_wc_ffpsos = Param(F,FPSO,S, initialize = d_wc_ffpsos, mutable=True)
	model.Big_Mgc_ffpsos = Param(F,FPSO,S, initialize = Big_Mgc_ffpsos, mutable=True)
	model.Big_Mwc_ffpsos = Param(F,FPSO,S, initialize = Big_Mwc_ffpsos, mutable=True)
	model.REC_fs = Param(F,S, initialize = REC_fs, mutable=True)
	model.alpha_gc_fs = Param(F,S, initialize = alpha_gc_fs, mutable=True)
	model.alpha_o_fs = Param(F,S, initialize = alpha_o_fs, mutable=True)
	model.alpha_wc_fs = Param(F,S, initialize = alpha_wc_fs, mutable=True)
	
	# At-realization decision variables
	model.b_fpsots = Var(FPSO,T,S, within = Binary) # 1 if FPSO fpso is installed.
	model.bC_ffpsots = Var(F,FPSO,T,S, within = Binary) # 1 if a connection between field f and FPSO fpso is installed.
	model.bex_fpsots = Var(FPSO,T,S, within = Binary) # 1 if FPSO fpso is expanded.
	model.Iwell_fts = Var(F,T,S, within = NonNegativeIntegers) # Number of wells drilled in field f
	model.QIoil_fpsots  = Var(FPSO,T,S, within = NonNegativeReals) # Oil installation capacity of FPSO fpso
	model.QEoil_fpsots  = Var(FPSO,T,S, within = NonNegativeReals) # Oil expansion capacity of FPSO fpso
	model.QIliq_fpsots  = Var(FPSO,T,S, within = NonNegativeReals) # Liquid installation capacity of FPSO fpso
	model.QEliq_fpsots  = Var(FPSO,T,S, within = NonNegativeReals) # Liquid expansion capacity of FPSO fpso
	model.QIgas_fpsots  = Var(FPSO,T,S, within = NonNegativeReals) # Gas installation capacity of FPSO fpso
	model.QEgas_fpsots  = Var(FPSO,T,S, within = NonNegativeReals) # Liquid expansion capacity of FPSO fpso

	# Other variables and differentiator variables
	model.w3_fts = Var(F,T,S, within = Binary) # Indicator variable. 1 if either w1_fts or w2_fts is 1

	# Other variables
	# Capacity
	model.Qoil_fpsots = Var(FPSO,T,S) # Oil capacity of FPSO fpso
	model.Qliq_fpsots = Var(FPSO,T,S) # Liquid capacity of FPSO fpso
	model.Qgas_fpsots = Var(FPSO,T,S) # Gas capacity of FPSO fpso
	
	model.ENPV = Var(initialize = 7000)
	
	# Revenue
	model.TConSh_ts = Var(T,S) # Total contractor's gross revenue share
	model.ConSh_rfts = Var(RF,T,S) # contractor's gross revenue share of a ring-fence rf
	model.ConShaftertax_rfts = Var(RF,T,S) # Sum of contractor's after-tax profit oil share for ringfence rf
	model.ConShbeforetax_rfts = Var(RF,T,S) # Sum of contractor's before-tax profit oil share for ringfence rf
	model.CO_rfts = Var(RF,T,S) # Cost oil for ringfence rf
	model.Tax_rfts = Var(RF,T,S) # Income tax for ringfence rf
	
	# Capital cost
	model.TCAP_ts  = Var(T,S) # Total capital cost
	model.CAP_rfts  = Var(RF,T,S) # Capital expenses for a ring-fence rf
	model.CAP1_rfts  = Var(RF,T,S) # Field specific capital expense such as drilling, connections among fields and FPSOs for a ring-fence rf
	model.CAP2_rfts  = Var(RF,T,S) # FPSO specific capital expense for a ring-fence rf
	model.DFPSOC_rffpsots  = Var(RF,FPSO,T,S) # Disaggregated cost of FPSO fpso for ring-fence rf
	model.DFPSOCfield_ffpsots = Var(F,FPSO,T,S) # Disaggregated cost of FPSO fpso for field f
	model.FPSOC_fpsots  = Var(FPSO,T,S) # Total cost of FPSO fpso
	
	# Operation cost
	model.TOPER_ts = Var(T,S) # Total operating cost
	model.OPER_rfts = Var(RF,T,S) # Operating costs for a ring-fence
	
	# Oil flow rate or cumulative production
	model.xtot_rfts = Var(RF,T,S) # Total oil production rate from ringfence rf. Per day.
	model.xtot_ts = Var(T,S) # Total oil production rate to FPSO fpso. Per day.
	model.xwell_ffpsots = Var(F,FPSO,T,S, within = NonNegativeReals) # Oil flow rate from each well. Per day.
	model.xc_rfts = Var(RF,T,S) # Cummulative oil produced from ringfence rf by the end of t
	model.xcfield_fts = Var(F,T,S) # Cummulative oil produced from field f by the end of t
	model.x_fts = Var(F,T,S) # Oil production rate from field f. Per day.
	model.x_ffpsots = Var(F,FPSO,T,S) # Oil production rate from field f to FPSO fpso. Per day.
	model.x_fpsots = Var(FPSO,T,S) # Oil production rate from all fields to FPSO fpso. Per day.
	
	# Water flow rate or cumulative production
	model.wtot_rfts = Var(RF,T,S) # Total water production rate from ringfence rf. Per day.
	model.wtot_ts = Var(T,S) # Total water production rate to FPSO fpso. Per day.
	model.wc_ffpsots = Var(F,FPSO,T,S) # Cummulative water produced from field f to FPSO fpso
	model.w_fts = Var(F,T,S) # Water production rate from field f. Per day.
	model.Qwc_ffpsots = Var(F,FPSO,T,S) # Cummulative water produced from field f to FPSO fpso (Dummy)
	model.w_ffpsots = Var(F,FPSO,T,S) # Daily water flow rate from field f to FPSO fpso. Per day.
	model.w_fpsots = Var(FPSO,T,S) # Water production rate from all fields to FPSO fpso. Per day.

	# Gas flow rate or cumulative production
	model.gtot_rfts = Var(RF,T,S) # Total gas production rate from ringfence rf. Per day.
	model.gtot_ts = Var(T,S) # Total gas production rate to FPSO fpso. Per day.
	model.gc_ffpsots = Var(F,FPSO,T,S) # Cummulative gas produced from field f to FPSO fpso
	model.g_fts = Var(F,T,S) # Gas production rate from field f. Per day.
	model.Qgc_ffpsots = Var(F,FPSO,T,S) # Cummulative gas produced from field f to FPSO fpso (Dummy)
	model.g_ffpsots = Var(F,FPSO,T,S) # Daily gas flow rate from field f to FPSO fpso. Per day.
	model.g_fpsots = Var(FPSO,T,S) # Gas production rate from all fields to FPSO fpso. Per day.
	
	model.bon_ffpsos = Var(F,FPSO,S, within = Binary) # 1 if a connection between field f and FPSO is installed.
	
	model.PO_rfts = Var(RF,T,S) # Profit oil for ringfence rf
	model.DPO_rfits = Var(RF,I,T,S, within = NonNegativeReals) # Disaggregated profit oil for tier i for ringfence rf
	model.DConShbeforetax_rfits = Var(RF,I,T,S) # Disaggregated contractor before-tax profit oil share for tier i for ringfence rf
	model.Dxc_rfits = Var(RF,I,T,S) # Disaggregated cummulative oil produced from ringfence rf by the end of t for tier i
	model.Z_rfits = Var(RF,I,T,S, within = Binary) # 1 if tier i is active for ringfence rf.
	model.REV_rfts = Var(RF,T,S) # Total revenues for ringfence rf
	model.bCO_rfts = Var(RF,T,S, within = Binary) # 1 if cost ceiling is active.
	model.CR_rfts = Var(RF,T,S) # Cost recovery for ringfence rf
	model.CRF_rfts = Var(RF,T,S) # Cost recovery carried forward for ringfence rf
	model.Qdwell_ffpsots = Var(F,FPSO,T,S) # Field deliverability (maximum oil flow rate) per well
	model.fc_fts = Var(F,T,S) # Fraction of oil recovered from field f
	model.Nwell_fts = Var(F,T,S) # Number of wells available
	
	# Auxiliary variable to exactly linearize (14)
	model.ZDfield_fpffpsots = Var(F,F,FPSO,T,S, within = NonNegativeReals)
	model.ZD1field_fpffpsots = Var(F,F,FPSO,T,S, within = NonNegativeReals)
	model.ZD_ffpsots = Var(F,FPSO,T,S, within = NonNegativeReals)
	model.ZD1_ffpsots = Var(F,FPSO,T,S, within = NonNegativeReals)

	# Auxiliary variable to exactly linearize (70)
	model.Zwell_fkts = Var(F,K,T,S, within = Binary)
	model.ZXwell_ffpsokts = Var(F,FPSO,K,T,S, within = NonNegativeReals)
	model.ZXwell1_ffpsokts = Var(F,FPSO,K,T,S, within = NonNegativeReals)

	# NACs
	model.w1_fts = Var(F,T,S, within = Binary) # Indicator variable. 1 if required number of wells is NOT ready to reveal uncertainty.
	model.bprod_fts = Var(F,T,S, within = Binary) # Indicator variable. 1 if oil production from field f has been made.
	model.w2_fts = Var(F,T,S, within = Binary) # Indicator variable. 1 if required years to reveal uncertainty have NOT been passed.
	
	# Indicator variables
	model.Z_tssp =  Var(T,S,S, within = Binary) # Indicator variable. 1 if scenario s and s' are indistinguishable.

	def G1_1(model):
		return model.ENPV
	model.objective = Objective(sense=maximize, rule=G1_1)
	# model.objective.pprint()

	def G2_2(model):
		return model.ENPV == sum(probability[s]*sum(dis_t[t]*(model.TConSh_ts[t,s] - model.TCAP_ts[t,s] - model.TOPER_ts[t,s]) for t in T) for s in S)
	model.G2_2 = Constraint(rule = G2_2)
	# model.G2_2.pprint()
	
	def G3_3(model,t,s):
		return model.TConSh_ts[t,s] == sum(model.ConSh_rfts[rf,t,s] for rf in RF)
	model.G3_3 = Constraint(T,S, rule = G3_3)
	# model.G3_3.pprint()
	
	def G4_4(model,t,s):
		return model.TCAP_ts[t,s] == sum(model.CAP_rfts[rf,t,s] for rf in RF)
	model.G4_4 = Constraint(T,S, rule = G4_4)
	# model.G4_4.pprint()
	
	def G5_5(model,t,s):
		return model.TOPER_ts[t,s] == sum(model.OPER_rfts[rf,t,s] for rf in RF)
	model.G5_5 = Constraint(T,S, rule = G5_5)
	# model.G5_5.pprint()

	def G6_6(model,rf,t,s):
		return model.CAP_rfts[rf,t,s] == model.CAP1_rfts[rf,t,s] + model.CAP2_rfts[rf,t,s]
	model.G6_6 = Constraint(RF,T,S, rule = G6_6)
	# model.G6_6.pprint()

	def G7_7(model,rf,t,s): # Field specific capital expense = connections among fields and FPSOs + drilling
		return model.CAP1_rfts[rf,t,s] == sum(FC_ffpsot[f,fpso,t]*model.bC_ffpsots[f,fpso,t,s] for fpso in FPSO for f in F_rf[rf]) + sum(FCwell_ft[f,t]*model.Iwell_fts[f,t,s] for f in F_rf[rf])
	model.G7_7 = Constraint(RF,T,S, rule = G7_7)
	# model.G7_7.pprint()

	def G8_8(model,rf,t,s): # FPSO specific capital expense = Sum of disaggregated cost of FPSO
		return model.CAP2_rfts[rf,t,s] == sum(model.DFPSOC_rffpsots[rf,fpso,t,s] for fpso in FPSO)
	model.G8_8 = Constraint(RF,T,S, rule = G8_8)
	# model.G8_8.pprint()

	def G9_9(model,fpso,t,s): # Total cost of FPSO facility = Liquid and gas installation + Liquid and gas expansion
		return model.FPSOC_fpsots[fpso,t,s] == FCFPSO_fpsot[fpso,t]*model.b_fpsots[fpso,t,s] \
												+ VCliq_fpsot[fpso,t]*(model.QIliq_fpsots[fpso,t,s] + model.QEliq_fpsots[fpso,t,s]) \
												+ VCgas_fpsot[fpso,t]*(model.QIgas_fpsots[fpso,t,s] + model.QEgas_fpsots[fpso,t,s])
	model.G9_9 = Constraint(FPSO,T,S, rule = G9_9)
	# model.G9_9.pprint()

	def G10_10(model,fpso,t,s): # Total cost of FPSO facility = Sum of disaggregated cost of FPSO over connected field f
		return model.FPSOC_fpsots[fpso,t,s] == sum(model.DFPSOCfield_ffpsots[f,fpso,t,s] for f in F_fpso[fpso])
	model.G10_10 = Constraint(FPSO,T,S, rule = G10_10)
	# model.G10_10.pprint()

	def G11_11(model,rf,fpso,t,s): # Disaggregated cost of FPSO for ringfence rf = Sum of total cost of FPSO fpso involved in ringfence rf
		return model.DFPSOC_rffpsots[rf,fpso,t,s] == sum(model.DFPSOCfield_ffpsots[f,fpso,t,s] for f in F_rf[rf])
	model.G11_11 = Constraint(RF,FPSO,T,S, rule = G11_11)
	# model.G11_11.pprint()

	def G12_12(model,f,fpso,s): # Connection between field f and FPSO fpso is installed only once over the time horizon
		return model.bon_ffpsos[f,fpso,s] == sum(model.bC_ffpsots[f,fpso,t,s] for t in T)
	model.G12_12 = Constraint(F,FPSO,S, rule = G12_12)
	# model.G12_12.pprint()
	
	def G13_13(model,f,fpso,t,s): # Disaggregated cost of FPSO for field f is 0 if connection between field f and FPSO fpso is not installed. 
		return model.DFPSOCfield_ffpsots[f,fpso,t,s] <= Big_M*model.bon_ffpsos[f,fpso,s]
	model.G13_13 = Constraint(F,FPSO,T,S, rule = G13_13)
	# model.G13_13.pprint()
	
	def G15_15(model,f,fpso,t,s): # G15-G21 are for the exact linearization of G14
		return sum(model.ZDfield_fpffpsots[fp,f,fpso,t,s]*model.REC_fs[fp,s] for fp in F_fpso[fpso]) == model.ZD_ffpsots[f,fpso,t,s]*model.REC_fs[f,s]
	model.G15_15 = Constraint(F,FPSO,T,S, rule = G15_15)
	# model.G15_15.pprint()
	
	def G16_16(model,f,fpso,fp,t,s): # G15-G21 are for the exact linearization of G14 
		return model.ZDfield_fpffpsots[fp,f,fpso,t,s] + model.ZD1field_fpffpsots[fp,f,fpso,t,s] == model.DFPSOCfield_ffpsots[f,fpso,t,s]
	model.G16_16 = Constraint(F,F_fpsoLIST,T,S, rule = G16_16)
	# model.G16_16.pprint()

	def G17_17(model,f,fpso,fp,t,s): # G15-G21 are for the exact linearization of G14 
		return model.ZDfield_fpffpsots[fp,f,fpso,t,s] <= Big_M*model.bon_ffpsos[fp,fpso,s]
	model.G17_17 = Constraint(F,F_fpsoLIST,T,S, rule = G17_17)
	# model.G17_17.pprint()

	def G18_18(model,f,fpso,fp,t,s): # G15-G21 are for the exact linearization of G14 
		return model.ZD1field_fpffpsots[fp,f,fpso,t,s] <= Big_M*(1-model.bon_ffpsos[fp,fpso,s])
	model.G18_18 = Constraint(F,F_fpsoLIST,T,S, rule = G18_18)
	# model.G18_18.pprint()

	def G19_20(model,f,fpso,t,s): # G15-G21 are for the exact linearization of G14 
		return model.ZD_ffpsots[f,fpso,t,s] + model.ZD1_ffpsots[f,fpso,t,s] == model.FPSOC_fpsots[fpso,t,s]
	model.G19_20 = Constraint(F,FPSO,T,S, rule = G19_20)
	# model.G19_20.pprint()

	def G20_21(model,f,fpso,t,s): # G15-G21 are for the exact linearization of G14
		return model.ZD_ffpsots[f,fpso,t,s] <= Big_M*model.bon_ffpsos[f,fpso,s]
	model.G20_21 = Constraint(F,FPSO,T,S, rule = G20_21)
	# model.G20_21.pprint()

	def G21_22(model,f,fpso,t,s): # G15-G21 are for the exact linearization of G14 
		return model.ZD1_ffpsots[f,fpso,t,s] <= Big_M*(1-model.bon_ffpsos[f,fpso,s])
	model.G21_22 = Constraint(F,FPSO,T,S, rule = G21_22)
	# model.G21_22.pprint()

	def G22_24(model,rf,t,s): # Total operating costs = total amount of liquid and gas produced 
		return model.OPER_rfts[rf,t,s] == delta_t[t]*(OCliq_rft[rf,t]*(model.xtot_rfts[rf,t,s] + model.wtot_rfts[rf,t,s]) + OCgas_rft[rf,t]*model.gtot_rfts[rf,t,s])
	model.G22_24 = Constraint(RF,T,S, rule = G22_24)
	# model.G22_24.pprint()
	
	def G23_25(model,rf,t,s): # Contractor's gross revenue share = contractor's after-tax profit oil share + Cost oil 
		return model.ConSh_rfts[rf,t,s] == model.ConShaftertax_rfts[rf,t,s] + model.CO_rfts[rf,t,s]
	model.G23_25 = Constraint(RF,T,S, rule = G23_25)
	# model.G23_25.pprint()

	def G24_26(model,rf,t,s): # Contractor's after-tax profit oil share = Before-tax - Tax 
		return model.ConShaftertax_rfts[rf,t,s] == model.ConShbeforetax_rfts[rf,t,s] - model.Tax_rfts[rf,t,s]
	model.G24_26 = Constraint(RF,T,S, rule = G24_26)
	# model.G24_26.pprint()

	def G25_27(model,rf,t,s): # Tax = Income tax rate * Before-tax 
		return model.Tax_rfts[rf,t,s] == ftax_rft[rf,t]*model.ConShbeforetax_rfts[rf,t,s]
	model.G25_27 = Constraint(RF,T,S, rule = G25_27)
	# model.G25_27.pprint()

	def G26_29(model,rf,t,s): # G26-G33 are convex-hull for disjunction (28) 
		return model.ConShbeforetax_rfts[rf,t,s] == sum(model.DConShbeforetax_rfits[rf,i,t,s] for i in I)
	model.G26_29 = Constraint(RF,T,S, rule = G26_29)
	# model.G26_29.pprint()

	def G27_30(model,rf,t,s): # G26-G33 are convex-hull for disjunction (28) 
		return model.PO_rfts[rf,t,s] == sum(model.DPO_rfits[rf,i,t,s] for i in I)
	model.G27_30 = Constraint(RF,T,S, rule = G27_30)
	# model.G27_30.pprint()

	def G28_31(model,rf,t,s): # G26-G33 are convex-hull for disjunction (28) 
		return model.xc_rfts[rf,t,s] == sum(model.Dxc_rfits[rf,i,t,s] for i in I)
	model.G28_31 = Constraint(RF,T,S, rule = G28_31)
	# model.G28_31.pprint()

	def G29_32(model,rf,i,t,s): # G26-G33 are convex-hull for disjunction (28) 
		return model.DConShbeforetax_rfits[rf,i,t,s] == fPO_rfi[rf,i]*model.DPO_rfits[rf,i,t,s]
	model.G29_32 = Constraint(RF,I,T,S, rule = G29_32)
	# model.G29_32.pprint()

	def G30_33(model,rf,i,t,s): # G26-G33 are convex-hull for disjunction (28) 
		return model.DConShbeforetax_rfits[rf,i,t,s] <= Big_M*model.Z_rfits[rf,i,t,s]
	model.G30_33 = Constraint(RF,I,T,S, rule = G30_33)
	# model.G30_33.pprint()

	def G31_34(model,rf,i,t,s): # G26-G33 are convex-hull for disjunction (28) 
		return model.DPO_rfits[rf,i,t,s] <= Big_M*model.Z_rfits[rf,i,t,s]
	model.G31_34 = Constraint(RF,I,T,S, rule = G31_34)
	# model.G31_34.pprint()

	def G32a_35a(model,rf,i,t,s): # G26-G33 are convex-hull for disjunction (28) 
		return Loil_rfi[rf,i]*model.Z_rfits[rf,i,t,s] <= model.Dxc_rfits[rf,i,t,s]
	model.G32a_35a = Constraint(RF,I,T,S, rule = G32a_35a)
	# model.G32a_35a.pprint()

	def G32b_35b(model,rf,i,t,s): # G26-G33 are convex-hull for disjunction (28) 
		return model.Dxc_rfits[rf,i,t,s] <= Uoil_rfi[rf,i]*model.Z_rfits[rf,i,t,s]
	model.G32b_35b = Constraint(RF,I,T,S, rule = G32b_35b)
	# model.G32b_35b.pprint()

	def G33_36(model,rf,t,s): # G26-G33 are convex-hull for disjunction (28) 
		return sum(model.Z_rfits[rf,i,t,s] for i in I) == 1
	model.G33_36 = Constraint(RF,T,S, rule = G33_36)
	# model.G33_36.pprint()

	def G34_37(model,rf,t,s): # Cummulative oil amount produced in ringfence rf = Sum of cummulative oil amount produced in field f 
		return model.xc_rfts[rf,t,s] == sum(model.xcfield_fts[f,t,s] for f in F_rf[rf])
	model.G34_37 = Constraint(RF,T,S, rule = G34_37)
	# model.G34_37.pprint()
	
	def G35_38(model,rf,t,s): # Total profit oil = Total revenues - Cost oil 
		return model.PO_rfts[rf,t,s] == model.REV_rfts[rf,t,s] - model.CO_rfts[rf,t,s]
	model.G35_38 = Constraint(RF,T,S, rule = G35_38)
	# model.G35_38.pprint()
	
	def G36_39(model,rf,t,s): # Total revenues = Selling price of total oil production rate 
		return model.REV_rfts[rf,t,s] == delta_t[t]*alpha_t[t]*model.xtot_rfts[rf,t,s]
	model.G36_39 = Constraint(RF,T,S, rule = G36_39)
	# model.G36_39.pprint()

	def G37_40(model,rf,t,s): # total oil production rate for ringfence rf = Oil production rate from field f 
		return model.xtot_rfts[rf,t,s] == sum(model.x_fts[f,t,s] for f in F_rf[rf])
	model.G37_40 = Constraint(RF,T,S, rule = G37_40)
	# model.G37_40.pprint()

	def G38(model,rf,t,s): # total water production rate for ringfence rf = Water production rate from field f 
		return model.wtot_rfts[rf,t,s] == sum(model.w_fts[f,t,s] for f in F_rf[rf])
	model.G38 = Constraint(RF,T,S, rule = G38)
	# model.G38.pprint()

	def G39(model,rf,t,s): # total gas production rate for ringfence rf = Gas production rate from field f 
		return model.gtot_rfts[rf,t,s] == sum(model.g_fts[f,t,s] for f in F_rf[rf])
	model.G39 = Constraint(RF,T,S, rule = G39)
	# model.G39.pprint()

	def G41_42(model,rf,t,s): # G41-G46 are linearization for G40 which calculates cost oil 
		return model.CO_rfts[rf,t,s] <= model.CR_rfts[rf,t,s] + Big_M*(1 - model.bCO_rfts[rf,t,s])
	model.G41_42 = Constraint(RF,T,S, rule = G41_42)
	# model.G41_42.pprint()

	def G42_43(model,rf,t,s): # G41-G46 are linearization for G40 which calculates cost oil 
		return model.CO_rfts[rf,t,s] >= model.CR_rfts[rf,t,s] - Big_M*(1 - model.bCO_rfts[rf,t,s])
	model.G42_43 = Constraint(RF,T,S, rule = G42_43)
	# model.G42_43.pprint()

	def G43_44(model,rf,t,s): # G41-G46 are linearization for G40 which calculates cost oil 
		return model.CO_rfts[rf,t,s] <= fCR_rft[rf,t]*model.REV_rfts[rf,t,s] + Big_M*model.bCO_rfts[rf,t,s]
	model.G43_44 = Constraint(RF,T,S, rule = G43_44)
	# model.G43_44.pprint()

	def G44_45(model,rf,t,s): # G41-G46 are linearization for G40 which calculates cost oil 
		return model.CO_rfts[rf,t,s] >= fCR_rft[rf,t]*model.REV_rfts[rf,t,s] - Big_M*model.bCO_rfts[rf,t,s]
	model.G44_45 = Constraint(RF,T,S, rule = G44_45)
	# model.G44_45.pprint()

	def G45_46(model,rf,t,s): # G41-G46 are linearization for G40 which calculates cost oil 
		return model.CO_rfts[rf,t,s] <= model.CR_rfts[rf,t,s]
	model.G45_46 = Constraint(RF,T,S, rule = G45_46)
	# model.G45_46.pprint()

	def G46_47(model,rf,t,s): # G41-G46 are linearization for G40 which calculates cost oil 
		return model.CO_rfts[rf,t,s] <= fCR_rft[rf,t]*model.REV_rfts[rf,t,s]
	model.G46_47 = Constraint(RF,T,S, rule = G46_47)
	# model.G46_47.pprint()

	def G47G48_48(model,rf,t,s): # Cost recovery = Capital costs + Operating costs + Cost recovery carried forward
		if t == 1:
			return model.CR_rfts[rf,t,s] == model.CAP_rfts[rf,t,s] + model.OPER_rfts[rf,t,s]
		else:
			return model.CR_rfts[rf,t,s] == model.CAP_rfts[rf,t,s] + model.OPER_rfts[rf,t,s] + model.CRF_rfts[rf,t-1,s]
	model.G47G48_48 = Constraint(RF,T,S, rule = G47G48_48)
	# model.G47G48_48.pprint()

	def G49_49(model,rf,t,s): # Cost recovery carried forward = Cost recovery - Cost oil 
		return model.CRF_rfts[rf,t,s] == model.CR_rfts[rf,t,s] - model.CO_rfts[rf,t,s]
	model.G49_49 = Constraint(RF,T,S, rule = G49_49)
	# model.G49_49.pprint()

	def G50_52(model,rf,i,ip,t,tau,s): # G50 and G51 tighten tier sequencing. 
		if ip < i and t <= tau and tau <= Tend:
			return model.Z_rfits[rf,i,t,s] + model.Z_rfits[rf,ip,tau,s] <= 1
		else:
			return Constraint.Skip
	model.G50_52 = Constraint(RF,I,I,T,T,S, rule = G50_52)
	# model.G50_52.pprint()

	def G51_53(model,rf,i,ip,t,tau,s): # G50 and G51 tighten tier sequencing.
		if ip > i and 1 <= tau and tau <= t:
			return model.Z_rfits[rf,i,t,s] + model.Z_rfits[rf,ip,tau,s] <= 1
		else:
			return Constraint.Skip
	model.G51_53 = Constraint(RF,I,I,T,T,S, rule = G51_53)
	# model.G51_53.pprint()

	## (54) doesn't make sense because Contshbeforetax_rftaus is not used in other constraints. 
	## Contshbeforetax_rftaus is different from ConShbeforetax_rftaus according to its definition.
	# def con_54(model,rf,i,t,s): # (54), Bound for the cummulative contractor before tax share based on the sliding scale profit oil and cost oil
	# 	return sum(model.Contshbeforetax_rfts[rf,tau,s]/alpha_t[tau] for tau in T if tau<=t) <= sum((fPO_rfi[rf,ip] - fPO_rfi[rf,ip-1])*(model.xc_rfts[rf,t,s] - Loil_rfi[rf,ip]) for ip in I if ip<=i)\
	# 																						- fPO_rfi[rf,Iend]*sum(model.CO_rfts[rf,tau,s]/alpha_t[tau] for tau in T if tau<=t)
	# model.con_54m = Constraint(RF,I,T,S, rule = con_54)
	# model.con_54m.pprint()
	
	def G52_55(model,f,fpso,t,s): # Oil flow rate from each well must be less than deliverability. 
		return model.xwell_ffpsots[f,fpso,t,s] <= model.Qdwell_ffpsots[f,fpso,t,s]
	model.G52_55 = Constraint(F,FPSO,T,S, rule = G52_55)
	# model.G52_55.pprint()

	def G53_56a(model,f,fpso,s): # Definition of initial deliverability. 
		return model.Qdwell_ffpsots[f,fpso,1,s] == model.alpha_o_fs[f,s]*d_oil_ffpso[f,fpso]
	model.G53_56a = Constraint(F,FPSO,S, rule = G53_56a)
	# model.G53_56a.pprint()
	
	### Non-linear ###
	def G54_56b(model,f,fpso,t,s): # Definition of oil deliverability curve 
		if t < Tend:
			return model.Qdwell_ffpsots[f,fpso,t+1,s] == model.alpha_o_fs[f,s]*(a_oil_ffpso[f,fpso]*(model.fc_fts[f,t,s]**(3))\
																		+ b_oil_ffpso[f,fpso]*(model.fc_fts[f,t,s]**(2))\
																		+ c_oil_ffpso[f,fpso]*model.fc_fts[f,t,s]\
																		+ d_oil_ffpso[f,fpso])
		else:
			return Constraint.Skip
	model.G54_56b = Constraint(F,FPSO,T,S, rule = G54_56b)
	# model.G54_56b.pprint()
	
	### Non-linear ###
	def G55_57(model,f,fpso,t,s): # Definition of cumulative water production curve (Dummy)
		return model.Qwc_ffpsots[f,fpso,t,s] == model.alpha_wc_fs[f,s]*(model.a_wc_ffpsos[f,fpso,s]*(model.fc_fts[f,t,s]**(4))\
																		+ model.b_wc_ffpsos[f,fpso,s]*(model.fc_fts[f,t,s]**(3))\
																		+ model.c_wc_ffpsos[f,fpso,s]*(model.fc_fts[f,t,s]**(2))\
																		+ model.d_wc_ffpsos[f,fpso,s]*model.fc_fts[f,t,s])
	model.G55_57 = Constraint(F,FPSO,T,S, rule = G55_57)
	# model.G55_57.pprint()
	
	### Non-linear ###
	def G56_58(model,f,fpso,t,s): # Definition of cumulative gas production curve (Dummy)
		return model.Qgc_ffpsots[f,fpso,t,s] == model.alpha_gc_fs[f,s]*(model.a_gc_ffpsos[f,fpso,s]*(model.fc_fts[f,t,s]**(4))\
																		+ model.b_gc_ffpsos[f,fpso,s]*(model.fc_fts[f,t,s]**(3))\
																		+ model.c_gc_ffpsos[f,fpso,s]*(model.fc_fts[f,t,s]**(2))\
																		+ model.d_gc_ffpsos[f,fpso,s]*model.fc_fts[f,t,s])
	model.G56_58 = Constraint(F,FPSO,T,S, rule = G56_58)
	# model.G56_58.pprint()

	def G57_59(model,f,fpso,t,s): # G57 to G64 ensure the actual cumulative water and gas production is 0 if there is no connection between field f and FPSO fpso. 
		return model.wc_ffpsots[f,fpso,t,s] <= model.Qwc_ffpsots[f,fpso,t,s] + model.Big_Mwc_ffpsos[f,fpso,s]*(1 - sum(model.bC_ffpsots[f,fpso,tau,s] for tau in T if tau<=t))
	model.G57_59 = Constraint(F,FPSO,T,S, rule = G57_59)
	# model.G57_59.pprint()

	def G58_60(model,f,fpso,t,s): # G57 to G64 ensure the actual cumulative water and gas production is 0 if there is no connection between field f and FPSO fpso. 
		return model.wc_ffpsots[f,fpso,t,s] >= model.Qwc_ffpsots[f,fpso,t,s] - model.Big_Mwc_ffpsos[f,fpso,s]*(1 - sum(model.bC_ffpsots[f,fpso,tau,s] for tau in T if tau<=t))
	model.G58_60 = Constraint(F,FPSO,T,S, rule = G58_60)
	# model.G58_60.pprint()

	def G59_61(model,f,fpso,t,s): # G57 to G64 ensure the actual cumulative water and gas production is 0 if there is no connection between field f and FPSO fpso. 
		return model.wc_ffpsots[f,fpso,t,s] <= model.Big_Mwc_ffpsos[f,fpso,s]*sum(model.bC_ffpsots[f,fpso,tau,s] for tau in T if tau<=t)
	model.G59_61 = Constraint(F,FPSO,T,S, rule = G59_61)
	# model.G59_61.pprint()

	def G60_62(model,f,fpso,t,s): # G57 to G64 ensure the actual cumulative water and gas production is 0 if there is no connection between field f and FPSO fpso. 
		return model.wc_ffpsots[f,fpso,t,s] >= - model.Big_Mwc_ffpsos[f,fpso,s]*sum(model.bC_ffpsots[f,fpso,tau,s] for tau in T if tau<=t)
	model.G60_62 = Constraint(F,FPSO,T,S, rule = G60_62)
	# model.G60_62.pprint()

	def G61_63(model,f,fpso,t,s): # G57 to G64 ensure the actual cumulative water and gas production is 0 if there is no connection between field f and FPSO fpso. 
		return model.gc_ffpsots[f,fpso,t,s] <= model.Qgc_ffpsots[f,fpso,t,s] + model.Big_Mgc_ffpsos[f,fpso,s]*(1 - sum(model.bC_ffpsots[f,fpso,tau,s] for tau in T if tau<=t))
	model.G61_63 = Constraint(F,FPSO,T,S, rule = G61_63)
	# model.G61_63.pprint()

	def G62_64(model,f,fpso,t,s): # G57 to G64 ensure the actual cumulative water and gas production is 0 if there is no connection between field f and FPSO fpso. 
		return model.gc_ffpsots[f,fpso,t,s] >= model.Qgc_ffpsots[f,fpso,t,s] - model.Big_Mgc_ffpsos[f,fpso,s]*(1 - sum(model.bC_ffpsots[f,fpso,tau,s] for tau in T if tau<=t))
	model.G62_64 = Constraint(F,FPSO,T,S, rule = G62_64)
	# model.G62_64.pprint()

	def G63_65(model,f,fpso,t,s): # G57 to G64 ensure the actual cumulative water and gas production is 0 if there is no connection between field f and FPSO fpso. 
		return model.gc_ffpsots[f,fpso,t,s] <= model.Big_Mgc_ffpsos[f,fpso,s]*sum(model.bC_ffpsots[f,fpso,tau,s] for tau in T if tau<=t)
	model.G63_65 = Constraint(F,FPSO,T,S, rule = G63_65)
	# model.G63_65.pprint()

	def G64_66(model,f,fpso,t,s): # G57 to G64 ensure the actual cumulative water and gas production is 0 if there is no connection between field f and FPSO fpso. 
		return model.gc_ffpsots[f,fpso,t,s] >= - model.Big_Mgc_ffpsos[f,fpso,s]*sum(model.bC_ffpsots[f,fpso,tau,s] for tau in T if tau<=t)
	model.G64_66 = Constraint(F,FPSO,T,S, rule = G64_66)
	# model.G64_66.pprint()

	def G65G66_67(model,f,fpso,t,s): # Definition of daily water flow rate from field f to FPSO fpso
		if t == 1:
			return model.w_ffpsots[f,fpso,t,s] == model.wc_ffpsots[f,fpso,t,s]/delta_t[t]
		else: 
			return model.w_ffpsots[f,fpso,t,s] == (model.wc_ffpsots[f,fpso,t,s] - model.wc_ffpsots[f,fpso,t-1,s])/delta_t[t]
	model.G65G66_67 = Constraint(F,FPSO,T,S, rule = G65G66_67)
	# model.G65G66_67.pprint()

	def G67G68_68(model,f,fpso,t,s): # Definition of daily gas flow rate from field f to FPSO fpso
		if t == 1:
			return model.g_ffpsots[f,fpso,t,s] == model.gc_ffpsots[f,fpso,t,s]/delta_t[t]
		else: 
			return model.g_ffpsots[f,fpso,t,s] == (model.gc_ffpsots[f,fpso,t,s] - model.gc_ffpsots[f,fpso,t-1,s])/delta_t[t]
	model.G67G68_68 = Constraint(F,FPSO,T,S, rule = G67G68_68)
	# model.G67G68_68.pprint()

	def G69_69(model,f,t,s): # Oil production rate of field f = Sum of oil production rate from field f to FPSO fpso
		return model.x_fts[f,t,s] == sum(model.x_ffpsots[f,fpso,t,s] for fpso in FPSO)
	model.G69_69 = Constraint(F,T,S, rule = G69_69)
	# model.G69_69.pprint()

	def G70(model,f,t,s): # Water production rate of field f = Sum of water production rate from field f to FPSO fpso
		return model.w_fts[f,t,s] == sum(model.w_ffpsots[f,fpso,t,s] for fpso in FPSO)
	model.G70 = Constraint(F,T,S, rule = G70)
	# model.G70.pprint()

	def G71(model,f,t,s): # Gas production rate of field f = Sum of gas production rate from field f to FPSO fpso
		return model.g_fts[f,t,s] == sum(model.g_ffpsots[f,fpso,t,s] for fpso in FPSO)
	model.G71 = Constraint(F,T,S, rule = G71)
	# model.G71.pprint()

	def G73_75_2012a(model,f,t,s): # G73-G77 exactly linearize G72
		return model.Nwell_fts[f,t,s] == sum(2**(k-1)*model.Zwell_fkts[f,k,t,s] for k in K)
	model.G73_75_2012a = Constraint(F,T,S, rule = G73_75_2012a)
	# model.G73_75_2012a.pprint()

	def G74_77_2012a(model,f,fpso,t,s): # G73-G77 exactly linearize G72
		return model.x_ffpsots[f,fpso,t,s] == sum(2**(k-1)*model.ZXwell_ffpsokts[f,fpso,k,t,s] for k in K)
	model.G74_77_2012a = Constraint(F,FPSO,T,S, rule = G74_77_2012a)
	# model.G74_77_2012a.pprint()

	def G75_78_2012a(model,f,fpso,k,t,s): # G73-G77 exactly linearize G72
		return model.ZXwell_ffpsokts[f,fpso,k,t,s] + model.ZXwell1_ffpsokts[f,fpso,k,t,s] == model.xwell_ffpsots[f,fpso,t,s]
	model.G75_78_2012a = Constraint(F,FPSO,K,T,S, rule = G75_78_2012a)
	# model.G75_78_2012a.pprint()

	def G76_79_2012a(model,f,fpso,k,t,s): # G73-G77 exactly linearize G72
		return model.ZXwell_ffpsokts[f,fpso,k,t,s] <= Big_Uwelloil_ffpso[f,fpso]*model.Zwell_fkts[f,k,t,s]
	model.G76_79_2012a = Constraint(F,FPSO,K,T,S, rule = G76_79_2012a)
	# model.G76_79_2012a.pprint()

	def G77_80_2012a(model,f,fpso,k,t,s): # G73-G77 exactly linearize G72
		return model.ZXwell1_ffpsokts[f,fpso,k,t,s] <= Big_Uwelloil_ffpso[f,fpso]*(1 - model.Zwell_fkts[f,k,t,s])
	model.G77_80_2012a = Constraint(F,FPSO,K,T,S, rule = G77_80_2012a)
	# model.G77_80_2012a.pprint()

	def G78_71(model,f,t,s): # Cummulative oil production from field f = Sum of oil production rate of field f
		return model.xcfield_fts[f,t,s] == sum(model.x_fts[f,tau,s]*delta_t[tau] for tau in T if tau<=t)
	model.G78_71 = Constraint(F,T,S, rule = G78_71)
	# model.G78_71.pprint()

	def G79_72(model,f,t,s): # The definition of the fractional oil recovery
		return model.fc_fts[f,t,s] == model.xcfield_fts[f,t,s]/model.REC_fs[f,s]
	model.G79_72 = Constraint(F,T,S, rule = G79_72)
	# model.G79_72.pprint()

	def G80_73(model,f,t,s): # Cummulative oil production from field f must be less than total amount of recoverable oil
		return model.xcfield_fts[f,t,s] <= model.REC_fs[f,s]
	model.G80_73 = Constraint(F,T,S, rule = G80_73)
	# model.G80_73.pprint()

	def G81_74(model,fpso,t,s): # Total oil flow rate into each FPSO from all fields
		return model.x_fpsots[fpso,t,s] == sum(model.x_ffpsots[f,fpso,t,s] for f in F_fpso[fpso])
	model.G81_74 = Constraint(FPSO,T,S, rule = G81_74)
	# model.G81_74.pprint()

	def G82_75(model,fpso,t,s): # Total water flow rate into each FPSO from all fields
		return model.w_fpsots[fpso,t,s] == sum(model.w_ffpsots[f,fpso,t,s] for f in F_fpso[fpso])
	model.G82_75 = Constraint(FPSO,T,S, rule = G82_75)
	# model.G82_75.pprint()

	def G83_76(model,fpso,t,s): # Total gas flow rate into each FPSO from all fields
		return model.g_fpsots[fpso,t,s] == sum(model.g_ffpsots[f,fpso,t,s] for f in F_fpso[fpso])
	model.G83_76 = Constraint(FPSO,T,S, rule = G83_76)
	# model.G83_76.pprint()

	def G84_77(model,t,s): # Total oil flow rate to all FPSOs
		return model.xtot_ts[t,s] == sum(model.x_fpsots[fpso,t,s] for fpso in FPSO)
	model.G84_77 = Constraint(T,S, rule = G84_77)
	# model.G84_77.pprint()

	def G85_78(model,t,s): # Total water flow rate to all FPSOs
		return model.wtot_ts[t,s] == sum(model.w_fpsots[fpso,t,s] for fpso in FPSO)
	model.G85_78 = Constraint(T,S, rule = G85_78)
	# model.G85_78.pprint()

	def G86_79(model,t,s): # Total gas flow rate to all FPSOs
		return model.gtot_ts[t,s] == sum(model.g_fpsots[fpso,t,s] for fpso in FPSO)
	model.G86_79 = Constraint(T,S, rule = G86_79)
	# model.G86_79.pprint()

	def G87_80(model,fpso,t,s): # Oil flow rate to each FPSO must be less than capacity
		return model.x_fpsots[fpso,t,s] <= model.Qoil_fpsots[fpso,t,s]
	model.G87_80 = Constraint(FPSO,T,S, rule = G87_80)
	# model.G87_80.pprint()

	def G88_81(model,fpso,t,s): # Liquid flow rate to each FPSO must be less than capacity
		return model.x_fpsots[fpso,t,s] + model.w_fpsots[fpso,t,s] <= model.Qliq_fpsots[fpso,t,s]
	model.G88_81 = Constraint(FPSO,T,S, rule = G88_81)
	# model.G88_81.pprint()

	def G89_82(model,fpso,t,s): # Gas flow rate to each FPSO must be less than capacity
		return model.g_fpsots[fpso,t,s] <= model.Qgas_fpsots[fpso,t,s]
	model.G89_82 = Constraint(FPSO,T,S, rule = G89_82)
	# model.G89_82.pprint()

	def G90_83(model,fpso,t,s): # FPSO capacity for oil
		if t>l1 and t>l2 and t>1:
			return model.Qoil_fpsots[fpso,t,s] == model.Qoil_fpsots[fpso,t-1,s] + model.QIoil_fpsots[fpso,t-l1,s] + model.QEoil_fpsots[fpso,t-l2,s]
		elif t>l1 and t>l2 and t==1:
			return model.Qoil_fpsots[fpso,t,s] == model.QIoil_fpsots[fpso,t-l1,s] + model.QEoil_fpsots[fpso,t-l2,s]
		elif t>l1 and t<=l2 and t>1:
			return model.Qoil_fpsots[fpso,t,s] == model.Qoil_fpsots[fpso,t-1,s] + model.QIoil_fpsots[fpso,t-l1,s]
		elif t<=l1 and t>l2 and t>1:
			return model.Qoil_fpsots[fpso,t,s] == model.Qoil_fpsots[fpso,t-1,s] + model.QEoil_fpsots[fpso,t-l2,s]
		elif t>l1 and t<=l2 and t==1:
			return model.Qoil_fpsots[fpso,t,s] == model.QIoil_fpsots[fpso,t-l1,s]
		elif t<=l1 and t>l2 and t==1:
			return model.Qoil_fpsots[fpso,t,s] == model.QEoil_fpsots[fpso,t-l2,s]
		elif t<=l1 and t<=l2 and t>1:
			return model.Qoil_fpsots[fpso,t,s] == model.Qoil_fpsots[fpso,t-1,s]
		elif t<=l1 and t<=l2 and t==1:
			return model.Qoil_fpsots[fpso,t,s] == 0
	model.G90_83 = Constraint(FPSO,T,S, rule = G90_83)
	# model.G90_83.pprint()

	def G91_84(model,fpso,t,s): # FPSO capacity for liquid
		if t>l1 and t>l2 and t>1:
			return model.Qliq_fpsots[fpso,t,s] == model.Qliq_fpsots[fpso,t-1,s] + model.QIliq_fpsots[fpso,t-l1,s] + model.QEliq_fpsots[fpso,t-l2,s]
		elif t>l1 and t>l2 and t==1:
			return model.Qliq_fpsots[fpso,t,s] == model.QIliq_fpsots[fpso,t-l1,s] + model.QEliq_fpsots[fpso,t-l2,s]
		elif t>l1 and t<=l2 and t>1:
			return model.Qliq_fpsots[fpso,t,s] == model.Qliq_fpsots[fpso,t-1,s] + model.QIliq_fpsots[fpso,t-l1,s]
		elif t<=l1 and t>l2 and t>1:
			return model.Qliq_fpsots[fpso,t,s] == model.Qliq_fpsots[fpso,t-1,s] + model.QEliq_fpsots[fpso,t-l2,s]
		elif t>l1 and t<=l2 and t==1:
			return model.Qliq_fpsots[fpso,t,s] == model.QIliq_fpsots[fpso,t-l1,s]
		elif t<=l1 and t>l2 and t==1:
			return model.Qliq_fpsots[fpso,t,s] == model.QEliq_fpsots[fpso,t-l2,s]
		elif t<=l1 and t<=l2 and t>1:
			return model.Qliq_fpsots[fpso,t,s] == model.Qliq_fpsots[fpso,t-1,s]
		elif t<=l1 and t<=l2 and t==1:
			return model.Qliq_fpsots[fpso,t,s] == 0
	model.G91_84 = Constraint(FPSO,T,S, rule = G91_84)
	# model.G91_84.pprint()

	def G92_85(model,fpso,t,s): # FPSO capacity for gas
		if t>l1 and t>l2 and t>1:
			return model.Qgas_fpsots[fpso,t,s] == model.Qgas_fpsots[fpso,t-1,s] + model.QIgas_fpsots[fpso,t-l1,s] + model.QEgas_fpsots[fpso,t-l2,s]
		elif t>l1 and t>l2 and t==1:
			return model.Qgas_fpsots[fpso,t,s] == model.QIgas_fpsots[fpso,t-l1,s] + model.QEgas_fpsots[fpso,t-l2,s]
		elif t>l1 and t<=l2 and t>1:
			return model.Qgas_fpsots[fpso,t,s] == model.Qgas_fpsots[fpso,t-1,s] + model.QIgas_fpsots[fpso,t-l1,s]
		elif t<=l1 and t>l2 and t>1:
			return model.Qgas_fpsots[fpso,t,s] == model.Qgas_fpsots[fpso,t-1,s] + model.QEgas_fpsots[fpso,t-l2,s]
		elif t>l1 and t<=l2 and t==1:
			return model.Qgas_fpsots[fpso,t,s] == model.QIgas_fpsots[fpso,t-l1,s]
		elif t<=l1 and t>l2 and t==1:
			return model.Qgas_fpsots[fpso,t,s] == model.QEgas_fpsots[fpso,t-l2,s]
		elif t<=l1 and t<=l2 and t>1:
			return model.Qgas_fpsots[fpso,t,s] == model.Qgas_fpsots[fpso,t-1,s]
		elif t<=l1 and t<=l2 and t==1:
			return model.Qgas_fpsots[fpso,t,s] == 0
	model.G92_85 = Constraint(FPSO,T,S, rule = G92_85)
	# model.G92_85.pprint()

	def G93_86(model,fpso,s): # Each FPSO can be installed only once. 
		return sum(model.b_fpsots[fpso,t,s] for t in T) <= 1
	model.G93_86 = Constraint(FPSO,S, rule = G93_86)
	# model.G93_86.pprint()

	def G94_87(model,fpso,s): # Each FPSO can be expanded only once. 
		return sum(model.bex_fpsots[fpso,t,s] for t in T) <= 1
	model.G94_87 = Constraint(FPSO,S, rule = G94_87)
	# model.G94_87.pprint()

	def G95_88(model,f,fpso,s): # Each connection between FPSO and field can be installed only once. 
		return sum(model.bC_ffpsots[f,fpso,t,s] for t in T) <= 1
	model.G95_88 = Constraint(F,FPSO,S, rule = G95_88)
	# model.G95_88.pprint()

	def G96_89(model,f,t,s): # A field can be connected to at most one FPSO. 
		return sum(model.bC_ffpsots[f,fpso,t,s] for fpso in FPSO) <= 1
	model.G96_89 = Constraint(F,T,S, rule = G96_89)
	# model.G96_89.pprint()

	def G97_90(model,f,s): # A field can be connected to at most one FPSO over the entire time horizon. 
		return sum(model.bC_ffpsots[f,fpso,t,s] for fpso in FPSO for t in T) <= 1
	model.G97_90 = Constraint(F,S, rule = G97_90)
	# model.G97_90.pprint()

	def G98_91(model,fpso,t,s): # FPSO expansion can be made only after FPSO installation. 
		return model.bex_fpsots[fpso,t,s] <= sum(model.b_fpsots[fpso,tau,s] for tau in T if tau<=t-l1)
	model.G98_91 = Constraint(FPSO,T,S, rule = G98_91)
	# model.G98_91.pprint()

	def G99_92(model,f,fpso,t,s): # FPSO connections can be made only after FPSO installation. 
		return model.bC_ffpsots[f,fpso,t,s] <= sum(model.b_fpsots[fpso,tau,s] for tau in T if tau<=t-l1)
	model.G99_92 = Constraint(F,FPSO,T,S, rule = G99_92)
	# model.G99_92.pprint()

	def G100_93(model,f,fpso,t,s): # Oil flow rate per well must be zero if FPSO-field connection is not available. 
		return model.xwell_ffpsots[f,fpso,t,s] <= Big_Uwelloil_ffpso[f,fpso]*sum(model.bC_ffpsots[f,fpso,tau,s] for tau in T if tau<=t)
	model.G100_93 = Constraint(F,FPSO,T,S, rule = G100_93)
	# model.G100_93.pprint()

	def G101_94(model,fpso,t,s): # Installed FPSO capacity for oil must be less than its upper limit
		return model.QIoil_fpsots[fpso,t,s] <= Uoil_fpso[fpso]*model.b_fpsots[fpso,t,s]
	model.G101_94 = Constraint(FPSO,T,S, rule = G101_94)
	# model.G101_94.pprint()

	def G102_95(model,fpso,t,s): # Installed FPSO capacity for liquid must be less than its upper limit
		return model.QIliq_fpsots[fpso,t,s] <= Uliq_fpso[fpso]*model.b_fpsots[fpso,t,s]
	model.G102_95 = Constraint(FPSO,T,S, rule = G102_95)
	# model.G102_95.pprint()

	def G103_96(model,fpso,t,s): # Installed FPSO capacity for gas must be less than its upper limit
		return model.QIgas_fpsots[fpso,t,s] <= Ugas_fpso[fpso]*model.b_fpsots[fpso,t,s]
	model.G103_96 = Constraint(FPSO,T,S, rule = G103_96)
	# model.G103_96.pprint()

	def G104_97(model,fpso,t,s): # Expanded FPSO capacity for oil must be less than its upper limit
		return model.QEoil_fpsots[fpso,t,s] <= Uoil_fpso[fpso]*model.bex_fpsots[fpso,t,s]
	model.G104_97 = Constraint(FPSO,T,S, rule = G104_97)
	# model.G104_97.pprint()

	def G105_98(model,fpso,t,s): # Expanded FPSO capacity for liquid must be less than its upper limit
		return model.QEliq_fpsots[fpso,t,s] <= Uliq_fpso[fpso]*model.bex_fpsots[fpso,t,s]
	model.G105_98 = Constraint(FPSO,T,S, rule = G105_98)
	# model.G105_98.pprint()

	def G106_99(model,fpso,t,s): # Expanded FPSO capacity for gas must be less than its upper limit
		return model.QEgas_fpsots[fpso,t,s] <= Ugas_fpso[fpso]*model.bex_fpsots[fpso,t,s]
	model.G106_99 = Constraint(FPSO,T,S, rule = G106_99)
	# model.G106_99.pprint()

	def G107_100(model,fpso,t,s): # Expanded FPSO capacity for oil must be less than its upper limit
		if t>1:
			return model.QEoil_fpsots[fpso,t,s] <= myu*model.Qoil_fpsots[fpso,t-1,s]
		else:
			return Constraint.Skip
	model.G107_100 = Constraint(FPSO,T,S, rule = G107_100)
	# model.G107_100.pprint()

	def G108_101(model,fpso,t,s): # Expanded FPSO capacity for liq must be less than its upper limit
		if t>1:
			return model.QEliq_fpsots[fpso,t,s] <= myu*model.Qliq_fpsots[fpso,t-1,s]
		else:
			return Constraint.Skip
	model.G108_101 = Constraint(FPSO,T,S, rule = G108_101)
	# model.G108_101.pprint()

	def G109_102(model,fpso,t,s): # Expanded FPSO capacity for gas must be less than its upper limit
		if t>1:
			return model.QEgas_fpsots[fpso,t,s] <= myu*model.Qgas_fpsots[fpso,t-1,s]
		else:
			return Constraint.Skip
	model.G109_102 = Constraint(FPSO,T,S, rule = G109_102)
	# model.G109_102.pprint()

	def G110G111_103(model,f,t,s): # Number of wells available = Sum of Number of wells drilled
		if t==1:
			return model.Nwell_fts[f,t,s] == model.Iwell_fts[f,t,s]
		else:
			return model.Nwell_fts[f,t,s] == model.Nwell_fts[f,t-1,s] + model.Iwell_fts[f,t,s]
	model.G110G111_103 = Constraint(F,T,S, rule = G110G111_103)
	# model.G110G111_103.pprint()

	def G112_104(model,t,s): # Number of wells drilled over all fields must be less than it's limit
		return sum(model.Iwell_fts[f,t,s] for f in F) <= UIwell_t[t]
	model.G112_104 = Constraint(T,S, rule = G112_104)
	# model.G112_104.pprint()

	def G113_105(model,f,t,s): # Number of wells available at field f must be less than it's limit
		return model.Nwell_fts[f,t,s] <= UNwell_f[f]
	model.G113_105 = Constraint(F,T,S, rule = G113_105)
	# model.G113_105.pprint()
	
	# ##### Initial NACs #####
	def G114_106(model,fpso,t,s,sp): # Installation of FPSO
		if s<sp:
			return model.b_fpsots[fpso,t,s] == model.b_fpsots[fpso,t,sp]
		else:
			return Constraint.Skip
	model.G114_106 = Constraint(FPSO,T1,S,S, rule = G114_106)
	# model.G114_106.pprint()

	def G115_107(model,fpso,t,s,sp): # Expansion of FPSO
		if s<sp:
			return model.bex_fpsots[fpso,t,s] == model.bex_fpsots[fpso,t,sp]
		else:
			return Constraint.Skip
	model.G115_107 = Constraint(FPSO,T1,S,S, rule = G115_107)
	# model.G115_107.pprint()

	def G116_108(model,f,fpso,t,s,sp): # Connection between fields and FPSOs
		if s<sp:
			return model.bC_ffpsots[f,fpso,t,s] == model.bC_ffpsots[f,fpso,t,sp]
		else:
			return Constraint.Skip
	model.G116_108 = Constraint(F,FPSO,T1,S,S, rule = G116_108)
	# model.G116_108.pprint()

	def G117_109(model,f,t,s,sp): # Number of wells drilled in field f
		if s<sp:
			return model.Iwell_fts[f,t,s] == model.Iwell_fts[f,t,sp]
		else:
			return Constraint.Skip
	model.G117_109 = Constraint(F,T1,S,S, rule = G117_109)
	# model.G117_109.pprint()

	def G118_110(model,fpso,t,s,sp): # Oil installation capacity of FPSO
		if s<sp:
			return model.QIoil_fpsots[fpso,t,s] == model.QIoil_fpsots[fpso,t,sp]
		else:
			return Constraint.Skip
	model.G118_110 = Constraint(FPSO,T1,S,S, rule = G118_110)
	# model.G118_110.pprint()
	
	def G119_111(model,fpso,t,s,sp): # Liquid installation capacity of FPSO
		if s<sp:
			return model.QIliq_fpsots[fpso,t,s] == model.QIliq_fpsots[fpso,t,sp]
		else:
			return Constraint.Skip
	model.G119_111 = Constraint(FPSO,T1,S,S, rule = G119_111)
	# model.G119_111.pprint()
	
	def G120_112(model,fpso,t,s,sp): # Gas installation capacity of FPSO
		if s<sp:
			return model.QIgas_fpsots[fpso,t,s] == model.QIgas_fpsots[fpso,t,sp]
		else:
			return Constraint.Skip
	model.G120_112 = Constraint(FPSO,T1,S,S, rule = G120_112)
	# model.G120_112.pprint()

	def G121_113(model,fpso,t,s,sp): # Oil expansion capacity of FPSO
		if s<sp:
			return model.QEoil_fpsots[fpso,t,s] == model.QEoil_fpsots[fpso,t,sp]
		else:
			return Constraint.Skip
	model.G121_113 = Constraint(FPSO,T1,S,S, rule = G121_113)
	# model.G121_113.pprint()
	
	def G122_114(model,fpso,t,s,sp): # Liquid expansion capacity of FPSO
		if s<sp:
			return model.QEliq_fpsots[fpso,t,s] == model.QEliq_fpsots[fpso,t,sp]
		else:
			return Constraint.Skip
	model.G122_114 = Constraint(FPSO,T1,S,S, rule = G122_114)
	# model.G122_114.pprint()
	
	def G123_115(model,fpso,t,s,sp): # Gas expansion capacity of FPSO
		if s<sp:
			return model.QEgas_fpsots[fpso,t,s] == model.QEgas_fpsots[fpso,t,sp]
		else:
			return Constraint.Skip
	model.G123_115 = Constraint(FPSO,T1,S,S, rule = G123_115)
	# model.G123_115.pprint()
	
	# Bound indecator variable w1_fts
	def G124G125a_116a(model,f,t,s):
		if t == 1:
			return model.w1_fts[f,t,s] == 1
		else:
			return N1_f[f] - model.Nwell_fts[f,t-1,s] >= 2*UNwell_f[f]*(model.w1_fts[f,t,s]-1) + 1
	model.G124G125a_116a = Constraint(F,T,S, rule = G124G125a_116a)
	# model.G124G125a_116a.pprint()
	
	def G124G125b_116b(model,f,t,s):
		if t == 1:
			return model.w1_fts[f,t,s] == 1
		else:
			return N1_f[f] - model.Nwell_fts[f,t-1,s] <= 2*UNwell_f[f]*model.w1_fts[f,t,s]
	model.G124G125b_116b = Constraint(F,T,S, rule = G124G125b_116b)
	# model.G124G125b_116b.pprint()

	# Bound indecator variable w2_fts
	def G126G127a_117a(model,f,t,s):
		if t == 1:
			return model.w2_fts[f,t,s] == 1
		else:
			return N2_f[f] - sum(model.bprod_fts[f,tau,s] for tau in T if tau<=t-1) >= 2*Tend*(model.w2_fts[f,t,s]-1) + 1
	model.G126G127a_117a = Constraint(F,T,S, rule = G126G127a_117a)
	# model.G126G127a_117a.pprint()
	
	def G126G127b_117b(model,f,t,s):
		if t == 1:
			return model.w2_fts[f,t,s] == 1
		else:
			return N2_f[f] - sum(model.bprod_fts[f,tau,s] for tau in T if tau<=t-1) <= 2*Tend*model.w2_fts[f,t,s]
	model.G126G127b_117b = Constraint(F,T,S, rule = G126G127b_117b)
	# model.G126G127b_117b.pprint()

	# Bound indecator variable bprod_fts
	def G128a_118a(model,f,t,s): # If there is production during the year, oil production rate must be greater than epsilon
		return model.x_fts[f,t,s] >= min_REC*epsilon + max_REC*(model.bprod_fts[f,t,s] - 1)
	model.G128a_118a = Constraint(F,T,S, rule = G128a_118a)
	# model.G128a_118a.pprint()
	
	def G128b_118b(model,f,t,s):
		return model.x_fts[f,t,s] <= max_REC*model.bprod_fts[f,t,s]
	model.G128b_118b = Constraint(F,T,S, rule = G128b_118b)
	# model.G128b_118b.pprint()

	# Bound indecator variable w3_fts
	def G129_119a(model,f,t,s):
		return model.w3_fts[f,t,s] >= model.w1_fts[f,t,s]
	model.G129_119a = Constraint(F,T,S, rule = G129_119a)
	# model.G129_119a.pprint()
	
	def G130_119b(model,f,t,s):
		return model.w3_fts[f,t,s] >= model.w2_fts[f,t,s]
	model.G130_119b = Constraint(F,T,S, rule = G130_119b)
	# model.G130_119b.pprint()
	
	def G131_119c(model,f,t,s):
		return model.w3_fts[f,t,s] <= model.w1_fts[f,t,s] + model.w2_fts[f,t,s]
	model.G131_119c = Constraint(F,T,S, rule = G131_119c)
	# model.G131_119c.pprint()

	# Bound indecator variable Z_tssp
	def G132a_120a(model,f,t,s,sp):
		if s<sp and f in D_ssp[s,sp]:
			return model.Z_tssp[t,s,sp] >= model.w3_fts[f,t,s]
		else:
			return Constraint.Skip
	model.G132a_120a = Constraint(F,T,S,S, rule = G132a_120a)
	# model.G132a_120a.pprint()
	
	def G132b_120b(model,f,t,s,sp):
		if s<sp and f in D_ssp[s,sp]:
			return model.Z_tssp[t,s,sp] <= model.w3_fts[f,t,s]
		else:
			return Constraint.Skip
	model.G132b_120b = Constraint(F,T,S,S, rule = G132b_120b)
	# model.G132b_120b.pprint()

	##### Conditional NACs (121) #####

	def G133a_121(model,fpso,t,s,sp):
		if s<sp:
			return model.b_fpsots[fpso,t,s] - model.b_fpsots[fpso,t,sp] <= 1 - model.Z_tssp[t,s,sp]
		else:
			return Constraint.Skip
	model.G133a_121 = Constraint(FPSO,TC,S,S, rule = G133a_121)
	# model.G133a_121.pprint()

	def G133b_121(model,fpso,t,s,sp):
		if s<sp:
			return model.b_fpsots[fpso,t,s] - model.b_fpsots[fpso,t,sp] >= model.Z_tssp[t,s,sp] - 1 
		else:
			return Constraint.Skip
	model.G133b_121 = Constraint(FPSO,TC,S,S, rule = G133b_121)
	# model.G133b_121.pprint()

	def G134a_121(model,fpso,t,s,sp):
		if s<sp:
			return model.bex_fpsots[fpso,t,s] - model.bex_fpsots[fpso,t,sp] <= 1 - model.Z_tssp[t,s,sp]
		else:
			return Constraint.Skip
	model.G134a_121 = Constraint(FPSO,TC,S,S, rule = G134a_121)
	# model.G134a_121.pprint()

	def G134b_121(model,fpso,t,s,sp):
		if s<sp:
			return model.bex_fpsots[fpso,t,s] - model.bex_fpsots[fpso,t,sp] >= model.Z_tssp[t,s,sp] - 1 
		else:
			return Constraint.Skip
	model.G134b_121 = Constraint(FPSO,TC,S,S, rule = G134b_121)
	# model.G134b_121.pprint()

	def G135a_121(model,f,fpso,t,s,sp):
		if s<sp:
			return model.bC_ffpsots[f,fpso,t,s] - model.bC_ffpsots[f,fpso,t,sp] <= 1 - model.Z_tssp[t,s,sp]
		else:
			return Constraint.Skip
	model.G135a_121 = Constraint(F,FPSO,TC,S,S, rule = G135a_121)
	# model.G135a_121.pprint()

	def G135b_121(model,f,fpso,t,s,sp):
		if s<sp:
			return model.bC_ffpsots[f,fpso,t,s] - model.bC_ffpsots[f,fpso,t,sp] >= model.Z_tssp[t,s,sp] - 1 
		else:
			return Constraint.Skip
	model.G135b_121 = Constraint(F,FPSO,TC,S,S, rule = G135b_121)
	# model.G135b_121.pprint()

	def G136a_121(model,f,t,s,sp):
		if s<sp:
			return model.Iwell_fts[f,t,s] - model.Iwell_fts[f,t,sp] <= 2*UNwell_f[f]*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.G136a_121 = Constraint(F,TC,S,S, rule = G136a_121)
	# model.G136a_121.pprint()

	def G136b_121(model,f,t,s,sp):
		if s<sp:
			return model.Iwell_fts[f,t,s] - model.Iwell_fts[f,t,sp] >= 2*UNwell_f[f]*(model.Z_tssp[t,s,sp] - 1)
		else:
			return Constraint.Skip
	model.G136b_121 = Constraint(F,TC,S,S, rule = G136b_121)
	# model.G136b_121.pprint()

	def G137a_121(model,fpso,t,s,sp):
		if s<sp:
			return model.QIoil_fpsots[fpso,t,s] - model.QIoil_fpsots[fpso,t,sp] <= Uoil_fpso[fpso]*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.G137a_121 = Constraint(FPSO,TC,S,S, rule = G137a_121)
	# model.G137a_121.pprint()

	def G137b_121(model,fpso,t,s,sp):
		if s<sp:
			return model.QIoil_fpsots[fpso,t,s] - model.QIoil_fpsots[fpso,t,sp] >= Uoil_fpso[fpso]*(model.Z_tssp[t,s,sp] - 1)
		else:
			return Constraint.Skip
	model.G137b_121 = Constraint(FPSO,TC,S,S, rule = G137b_121)
	# model.G137b_121.pprint()

	def G138a_121(model,fpso,t,s,sp):
		if s<sp:
			return model.QIliq_fpsots[fpso,t,s] - model.QIliq_fpsots[fpso,t,sp] <= Uliq_fpso[fpso]*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.G138a_121 = Constraint(FPSO,TC,S,S, rule = G138a_121)
	# model.G138a_121.pprint()

	def G138b_121(model,fpso,t,s,sp):
		if s<sp:
			return model.QIliq_fpsots[fpso,t,s] - model.QIliq_fpsots[fpso,t,sp] >= Uliq_fpso[fpso]*(model.Z_tssp[t,s,sp] - 1)
		else:
			return Constraint.Skip
	model.G138b_121 = Constraint(FPSO,TC,S,S, rule = G138b_121)
	# model.G138b_121.pprint()

	def G139a_121(model,fpso,t,s,sp):
		if s<sp:
			return model.QIgas_fpsots[fpso,t,s] - model.QIgas_fpsots[fpso,t,sp] <= Ugas_fpso[fpso]*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.G139a_121 = Constraint(FPSO,TC,S,S, rule = G139a_121)
	# model.G139a_121.pprint()

	def G139b_121(model,fpso,t,s,sp):
		if s<sp:
			return model.QIgas_fpsots[fpso,t,s] - model.QIgas_fpsots[fpso,t,sp] >= Ugas_fpso[fpso]*(model.Z_tssp[t,s,sp] - 1)
		else:
			return Constraint.Skip
	model.G139b_121 = Constraint(FPSO,TC,S,S, rule = G139b_121)
	# model.G139b_121.pprint()

	def G140a_121(model,fpso,t,s,sp):
		if s<sp:
			return model.QEoil_fpsots[fpso,t,s] - model.QEoil_fpsots[fpso,t,sp] <= Uoil_fpso[fpso]*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.G140a_121 = Constraint(FPSO,TC,S,S, rule = G140a_121)
	# model.G140a_121.pprint()

	def G140b_121(model,fpso,t,s,sp):
		if s<sp:
			return model.QEoil_fpsots[fpso,t,s] - model.QEoil_fpsots[fpso,t,sp] >= Uoil_fpso[fpso]*(model.Z_tssp[t,s,sp] - 1)
		else:
			return Constraint.Skip
	model.G140b_121 = Constraint(FPSO,TC,S,S, rule = G140b_121)
	# model.G140b_121.pprint()

	def G141a_121(model,fpso,t,s,sp):
		if s<sp:
			return model.QEliq_fpsots[fpso,t,s] - model.QEliq_fpsots[fpso,t,sp] <= Uliq_fpso[fpso]*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.G141a_121 = Constraint(FPSO,TC,S,S, rule = G141a_121)
	# model.G141a_121.pprint()

	def G141b_121(model,fpso,t,s,sp):
		if s<sp:
			return model.QEliq_fpsots[fpso,t,s] - model.QEliq_fpsots[fpso,t,sp] >= Uliq_fpso[fpso]*(model.Z_tssp[t,s,sp] - 1)
		else:
			return Constraint.Skip
	model.G141b_121 = Constraint(FPSO,TC,S,S, rule = G141b_121)
	# model.G141b_121.pprint()

	def G142a_121(model,fpso,t,s,sp):
		if s<sp:
			return model.QEgas_fpsots[fpso,t,s] - model.QEgas_fpsots[fpso,t,sp] <= Ugas_fpso[fpso]*(1 - model.Z_tssp[t,s,sp])
		else:
			return Constraint.Skip
	model.G142a_121 = Constraint(FPSO,TC,S,S, rule = G142a_121)
	# model.G142a_121.pprint()

	def G142b_121(model,fpso,t,s,sp):
		if s<sp:
			return model.QEgas_fpsots[fpso,t,s] - model.QEgas_fpsots[fpso,t,sp] >= Ugas_fpso[fpso]*(model.Z_tssp[t,s,sp] - 1)
		else:
			return Constraint.Skip
	model.G142b_121 = Constraint(FPSO,TC,S,S, rule = G142b_121)
	# model.G142b_121.pprint()
	
	return model