from pyomo.opt import SolverFactory
import os
from importlib import import_module
import copy
import numpy as np
import MSSP.MSSP_sequence as MSSP_sequence

### Select the model name from the abbreviations below.
problem_name = 'Size' # Size, OGFDP, PNS, OPMPSP, CTP, RD, OOFIP, VR, ALIP, DSR, NTIP, CPwTL, CCSEOR

### Select 'True' for a complete-recourse added model. Select 'False' otherwise.
Complete_recourse_added = False # Available only for Size, PNS, OPMPSP, VR, ALIP, DSR
print('problem_name =', problem_name)
optimization_model = problem_name + '_CR' if Complete_recourse_added else problem_name
print('optimization_model =', optimization_model)

### Select the instance to run. To see instance names, go to 'Parameters', the selected model, 'Model name_Cases', and 'Case_data.py'. 
Instances = import_module('Parameters.' +problem_name+ '.' +problem_name+ '_Cases.Case_data')
MD = Instances.I3T3S8()
Case_name = str(MD.__class__.__name__)
print('Case_name =', Case_name)

### Import parameters and MSSP model ###
Pre = import_module('Parameters.' +problem_name+ '.Pre')
Formulation = import_module('MSSP.Model.' +optimization_model)

### Set the solver ###
sol_select = "glpk"
print('Selected solver =', sol_select)
solver = SolverFactory(sol_select)

if sol_select == "cplex":
	mipgap = 0.0001
	solver.options.mip_tolerances_mipgap = mipgap
	solver.options['timelimit'] = 172800
	sol_option = {'tee':False,'logfile':"slover.log"}

elif sol_select == "glpk":
	sol_option = {'tee':False,'logfile':"slover.log"}

elif sol_select == "gams":
	sol_option = {'solver':'baron', 'tee':True, 'keepfiles':True, 'logfile':"slover.log", 'add_options':[" Option OptCR = 0.05;Option reslim=172800"] }

elif sol_select == "baron":
	solver.options['EpsR'] = 0.001
	solver.options['MaxTime'] = 172800
	solver.options['times'] = 1
	solver.options['CplexLibName'] = '/tools/cplex-20.10/cplex/bin/x86-64_linux/libcplex2010.so'
	sol_option = {'tee':True, 'keepfiles':True, 'logfile':"slover.log"}

solver_info = {'solver':solver, 'solver_option': sol_option}

### Problem specific settings
if problem_name == 'Size': 
	### Prepare parameters ###
	I, T, T_end, S, Cpr_is, D_its, Cpr_i_exped, D_it_exped, probability, D_ssp, Phi_tssp, c_t, rho, sigma, M, Cpu = Pre.Parameter_setting(MD)
	time_set = T
	
	### Load MSSP model ###
	model_MSSP = Formulation.MSSP_model(I, T, T_end, S, Cpr_is, D_its, probability, D_ssp, Phi_tssp, c_t, rho, sigma, M, Cpu)
	
	### Differentiator variable information ###
	DF = {model_MSSP.z_its:{'t_index':1,'s_index':2,'sets':(I,T,S),'trigger_GT':0.8}}

	### Specify variables to save ###
	Var_output = {model_MSSP.z_its, model_MSSP.y_its, model_MSSP.x_ijts, model_MSSP.w_its}
	
	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.Cpr_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.z_its,'diff_set':D_ssp,'diff_index':(0,)}},)
	Exo_input = ({'param':model_MSSP.D_its,'t_index':1,'s_index':2},)
	Probability = probability
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

elif problem_name == 'OGFDP': 
	### Prepare parameters ###
	WP, PP, T, T_end, S, theta1_wps, theta2_wps, theta1_wp_exped, theta2_wp_exped, probability, delta_t, shrink, D_ssp,\
	L1, P_t, M_wp, M_pp, M_wpwp, M_wppp, FCC_wp, FCC_pp, FCC_wpwp, FCC_wppp, VCC_wp, VCC_pp, FOC_wp, FOC_pp, VOC_wp, VOC_pp, alpha_t, Max_theta2 = Pre.Parameter_setting(MD)
	
	time_set = T
	
	### Load MSSP model ###
	model_MSSP = Formulation.MSSP_model(WP, PP, T, S, theta1_wps, theta2_wps, probability, delta_t, shrink, D_ssp, L1, P_t,
		M_wp, M_pp, M_wpwp, M_wppp, FCC_wp, FCC_pp, FCC_wpwp, FCC_wppp, VCC_wp, VCC_pp, FOC_wp, FOC_pp, VOC_wp, VOC_pp, alpha_t, Max_theta2)
	
	### Differentiator variable information ###
	DF = {model_MSSP.b_wpts:{'t_index':1,'s_index':2,'sets':(WP,T,S),'trigger_GT':0.8}}
	
	### Specify variables to save ###
	Var_output = {model_MSSP.b_wpts, model_MSSP.b_ppts, model_MSSP.b_wpwppts, model_MSSP.b_wpppts, model_MSSP.qout_wpts, model_MSSP.qout_ppts, 
					model_MSSP.qout_wpwppts, model_MSSP.qout_wpppts, model_MSSP.e_wpts, model_MSSP.e_ppts, model_MSSP.qcum_wpts, model_MSSP.qprod_wpts, 
					model_MSSP.qdeliv_wpts, model_MSSP.cap_wpts, model_MSSP.cap_ppts, model_MSSP.qshr_ts}
	
	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.theta1_wps,'s_index':1, 'Differentiator':{'variable':model_MSSP.b_wpts,'diff_set':D_ssp, 'diff_index':(0,)}},
				{'param':model_MSSP.theta2_wps,'s_index':1, 'Differentiator':{'variable':model_MSSP.b_wpts,'diff_set':D_ssp, 'diff_index':(0,)}},)
	Exo_input = ()
	Probability = probability
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

elif problem_name == 'CTP':
	### Prepare parameters ###
	I, J, J_end, T, T_end, R, S, SI_s, gammaD_i, gammaL_i, tau_ij, revmax_i, c_ij, revopen_ij, revrun_ijt, f_ij, cd_t, rho_ijr, rhomax_r,\
	ForP_is, ForP_i_exped, D_ssp, D_AEEV_ssp, probability = Pre.Parameter_setting(MD)
	
	time_set = T
	
	### Load MSSP model ###
	model_MSSP = Formulation.MSSP_model(I, J, J_end, T, T_end, R, S, SI_s, gammaD_i, gammaL_i, tau_ij, revmax_i, c_ij, revopen_ij, revrun_ijt,
										f_ij, cd_t, rho_ijr, rhomax_r, ForP_is, D_ssp, probability)
	
	### Differentiator variable information ###
	DF = {model_MSSP.Y_ijts:{'t_index':2,'s_index':3,'sets':(I,J,T,S),'trigger_GT':0.8}}
	
	### Specify variables to save ###
	Var_output = {model_MSSP.X_ijts, model_MSSP.Y_ijts, model_MSSP.Z_ijts, model_MSSP.FRv_s, model_MSSP.Rv_s, model_MSSP.Cst_s}
	
	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.ForP_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.Y_ijts,'diff_set':D_AEEV_ssp,'diff_index':(0,1)}},)
	Exo_input = ()
	Probability = probability
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

elif problem_name == 'OPMPSP': 
	### Prepare parameters ###
	Case_csv = 'Parameters/' +problem_name+ '/' +problem_name+ '_Cases' + '/'+ str(Case_name)+".csv" # Load additional csv data file
	T, T_end, I, S, cmng_t, cproc_t, c1_t, M_t, P_t, a0_is, a0_i_exped, a1_is, a1_i_exped, g_is, D_ssp, IJ, scenario_param, probability, CMadd, Precedence_ij, linkage_i = Pre.Parameter_setting(MD, Case_csv)
	time_set = T
	
	### Load MSSP model ###
	model_MSSP = Formulation.MSSP_model(T, I, S, cmng_t, cproc_t, c1_t, M_t, P_t, a0_is, a1_is, g_is, D_ssp, IJ, probability, CMadd)
	
	### Differentiator variable information ###
	DF = {model_MSSP.x_its:{'t_index':1,'s_index':2,'sets':(I,T,S),'trigger_GT':0.8}}
	
	### Specify variables to save ###
	Var_output = {model_MSSP.x_its,model_MSSP.y_its,model_MSSP.z_its} # , model_MSSP.each_t:0
	
	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.a0_is,'s_index':1, 'Differentiator':{'variable':None,'var_set':None,'diff_set':None,'diff_index':None}},
				{'param':model_MSSP.a1_is,'s_index':1, 'Differentiator':{'variable':None,'var_set':None,'diff_set':None,'diff_index':None}},
				{'param':model_MSSP.g_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.x_its,'diff_set':D_ssp,'diff_index':(0,)}},)
	Exo_input = ()
	Probability = probability
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

elif problem_name == 'PNS': 
	### Prepare parameters ###
	Case_csv = 'Parameters/' +problem_name+ '/' +problem_name+ '_Cases' + '/'+ str(Case_name)+".csv" # Load additional csv data file
	I, IU, Not_IU, K, K126, K910, STEP, T, T_end, S,\
		FE_it, VE_it, FO_it, VO_kt, FIPP_it, FOPP_it, delta_t, alpha_t, beta_t, gamma_t, Big_M, CARD_t, theta_i, d_t, Wcap_inital_i, UQE_i, LQE_i, Uout_i, Lout_i,\
		theta_ils, D_ssp, D_ssp_AEEV, M_issp, p_s, theta_il_exped = Pre.Parameter_setting(MD, Case_csv)
	time_set = T
	
	### Load MSSP model ###
	model_MSSP = Formulation.MSSP_model(I, IU, K, K126, STEP, T, T_end, S,
		FE_it, VE_it, FO_it, VO_kt, FIPP_it, FOPP_it, delta_t, alpha_t, beta_t, gamma_t, Big_M, CARD_t, theta_i, d_t, Wcap_inital_i, UQE_i, LQE_i, Uout_i, Lout_i,
		theta_ils, D_ssp, D_ssp_AEEV, M_issp, p_s)
	
	### Differentiator variable information ###
	DF = {model_MSSP.B_ilts:{'t_index':2,'s_index':3,'sets':(I,STEP,T,S),'trigger_GT':0.8}}
	
	### Specify variables to save ###
	Var_output = {model_MSSP.Yexp_its, model_MSSP.Ypilot_its, model_MSSP.Yoper_its, model_MSSP.Wcap_its, model_MSSP.WQE_its, model_MSSP.Wrate_kts, 
					model_MSSP.Xpurch_ts, model_MSSP.Xsales_ts, model_MSSP.Winv_ts, model_MSSP.B_ilts}
	
	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.theta_ils,'s_index':2, 'Differentiator':{'variable':model_MSSP.B_ilts,'diff_set':D_ssp_AEEV, 'diff_index':(0,1)}},)
	Exo_input = ()
	Probability = p_s
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

elif problem_name == 'RD': 
	### Prepare problem-specific parameters ###
	I, IJ_Z_tilda, T, T_end, S, IT_beta_set, IJT_delta_set, IJ_delta_set, theta_is, Max_theta_is, Z_is, theta_i_exped, Z_i_exped, Ztilda_ij_exped, probability, Y, H,\
	delta_i, delta_bar_ij, B_t, f_i, r, D_i, theta_theta, theta_Z, delta_bar, delta_min_ij, Z_tilda_ijs, Big_M, Big_M_F3, Big_M_F17F19 = Pre.Parameter_setting(MD)
	
	time_set = T
	
	### Load MSSP model ###
	model_MSSP = Formulation.MSSP_model(I, IJ_Z_tilda, T, T_end, S, IT_beta_set, IJT_delta_set, theta_is, Max_theta_is, Z_is, probability, Y, H,\
		delta_i, delta_bar_ij, B_t, f_i, r, D_i, theta_theta, theta_Z, delta_bar, Z_tilda_ijs, Big_M, Big_M_F3, Big_M_F17F19)
	
	### Differentiator variable information ###
	DF = {model_MSSP.y_its:{'t_index':1,'s_index':2,'sets':(I,T[1:],S),'trigger_GT':0.8},model_MSSP.h_its:{'t_index':1,'s_index':2,'sets':(I,T[1:],S),'trigger_GT':0.8}}
	
	### Specify variables to save ###
	Var_output = {model_MSSP.x_its,model_MSSP.tau_its,model_MSSP.alpha_its,model_MSSP.beta_its,
					model_MSSP.gamma_its,model_MSSP.delta_ijts,model_MSSP.y_its,model_MSSP.h_its,
					model_MSSP.obj1,model_MSSP.obj2,model_MSSP.obj3,model_MSSP.obj4}
	
	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.Z_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.h_its,'diff_set':H,'diff_index':(0,)}},
				{'param':model_MSSP.theta_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.y_its,'diff_set':Y,'diff_index':(0,)}},
				{'param':model_MSSP.Z_tilda_ijs,'s_index':2, 'Differentiator':{'variable':None,'diff_set':None,'diff_index':None}},)
	Exo_input = ()
	Probability = probability
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

elif problem_name == 'OOFIP': 
	### Prepare parameters ###
	F, FPSO, RF, F_rf, F_fpso, F_fpsoLIST, I, Iend, T, T1, TC, Tend, K, S,\
		FC_ffpsot, FCwell_ft, FCFPSO_fpsot, VCliq_fpsot, VCgas_fpsot, OCgas_rft, OCliq_rft, ftax_rft, fPO_rfi, fCR_rft, Loil_rfi, Uoil_rfi, alpha_t, l1,l2,\
		a_oil_ffpso, b_oil_ffpso, c_oil_ffpso, d_oil_ffpso, dis_t, delta_t, Big_M, Big_U, Big_Uwelloil_ffpso, Uoil_fpso, Uliq_fpso, Ugas_fpso, myu, UIwell_t,\
		UNwell_f, max_REC, min_REC, epsilon, a_wor_ffpso,b_wor_ffpso, c_wor_ffpso,d_wor_ffpso, a_gor_ffpso, b_gor_ffpso, c_gor_ffpso, d_gor_ffpso,\
		REC_fs, alpha_o_fs, alpha_wc_fs, alpha_gc_fs, a_wc_ffpsos, b_wc_ffpsos, c_wc_ffpsos, d_wc_ffpsos, a_gc_ffpsos, b_gc_ffpsos, c_gc_ffpsos, d_gc_ffpsos, Big_Mwc_ffpsos, Big_Mgc_ffpsos, N1_f, N2_f, D_ssp, probability,\
		REC_f_exped, alpha_o_f_exped, alpha_wc_f_exped, alpha_gc_f_exped, a_wc_ffpso_exped, b_wc_ffpso_exped, c_wc_ffpso_exped, d_wc_ffpso_exped, a_gc_ffpso_exped, b_gc_ffpso_exped, c_gc_ffpso_exped, d_gc_ffpso_exped, Big_Mwc_ffpso_exped, Big_Mgc_ffpso_exped = Pre.Parameter_setting(MD)
	
	time_set = T
	
	### Load MSSP model ###
	model_MSSP = Formulation.MSSP_model(F, FPSO, RF, F_rf, F_fpso, F_fpsoLIST, I, Iend, T, T1, TC, Tend, K, S,
		FC_ffpsot, FCwell_ft, FCFPSO_fpsot, VCliq_fpsot, VCgas_fpsot, OCgas_rft, OCliq_rft, ftax_rft, fPO_rfi, fCR_rft, Loil_rfi, Uoil_rfi, alpha_t, l1, l2,
		a_oil_ffpso, b_oil_ffpso, c_oil_ffpso, d_oil_ffpso, dis_t, delta_t, Big_M, Big_U, Big_Uwelloil_ffpso, Uoil_fpso, Uliq_fpso, Ugas_fpso, myu, UIwell_t, UNwell_f, max_REC, min_REC, epsilon,
		REC_fs, alpha_o_fs, alpha_wc_fs, alpha_gc_fs, a_wc_ffpsos, b_wc_ffpsos, c_wc_ffpsos, d_wc_ffpsos, a_gc_ffpsos, b_gc_ffpsos, c_gc_ffpsos, d_gc_ffpsos, Big_Mwc_ffpsos, Big_Mgc_ffpsos,
		N1_f, N2_f, D_ssp, probability)
	
	### Differentiator variable information ###
	DF = {model_MSSP.w3_fts:{'t_index':1,'s_index':2,'sets':(F,T,S),'trigger_LT':0.2}}
	
	### Specify variables to save ###
	Var_output = {model_MSSP.b_fpsots, model_MSSP.QIoil_fpsots, model_MSSP.QEoil_fpsots, model_MSSP.Qoil_fpsots, model_MSSP.QIliq_fpsots, model_MSSP.QEliq_fpsots,
					model_MSSP.Qliq_fpsots, model_MSSP.QIgas_fpsots, model_MSSP.QEgas_fpsots, model_MSSP.Qgas_fpsots, model_MSSP.bC_ffpsots, model_MSSP.bex_fpsots, 
					model_MSSP.Iwell_fts, model_MSSP.Nwell_fts, model_MSSP.Qdwell_ffpsots, model_MSSP.xwell_ffpsots, model_MSSP.x_ffpsots, model_MSSP.x_fts, 
					model_MSSP.xcfield_fts, model_MSSP.fc_fts, model_MSSP.x_fpsots, model_MSSP.xtot_rfts, model_MSSP.xtot_ts, model_MSSP.xc_rfts, model_MSSP.w_ffpsots, 
					model_MSSP.wc_ffpsots, model_MSSP.w_fts, model_MSSP.w_fpsots, model_MSSP.wtot_rfts, model_MSSP.wtot_ts, model_MSSP.g_ffpsots, model_MSSP.gc_ffpsots, 
					model_MSSP.g_fts, model_MSSP.g_fpsots, model_MSSP.gtot_rfts, model_MSSP.gtot_ts, model_MSSP.bon_ffpsos, model_MSSP.TConSh_ts, model_MSSP.TCAP_ts, 
					model_MSSP.TOPER_ts,model_MSSP.w3_fts}
	
	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.REC_fs,'s_index':1, 'Differentiator':{'variable':model_MSSP.w3_fts,'diff_set':D_ssp,'diff_index':(0,)}},
				{'param':model_MSSP.alpha_gc_fs,'s_index':1, 'Differentiator':{'variable':model_MSSP.w3_fts,'diff_set':D_ssp,'diff_index':(0,)}},
				{'param':model_MSSP.alpha_o_fs,'s_index':1, 'Differentiator':{'variable':model_MSSP.w3_fts,'diff_set':D_ssp,'diff_index':(0,)}},
				{'param':model_MSSP.alpha_wc_fs,'s_index':1, 'Differentiator':{'variable':model_MSSP.w3_fts,'diff_set':D_ssp,'diff_index':(0,)}},
				{'param':model_MSSP.a_gc_ffpsos,'s_index':2, 'Differentiator':{'variable':None,'diff_set':None,'diff_index':None}},
				{'param':model_MSSP.b_gc_ffpsos,'s_index':2, 'Differentiator':{'variable':None,'diff_set':None,'diff_index':None}},
				{'param':model_MSSP.c_gc_ffpsos,'s_index':2, 'Differentiator':{'variable':None,'diff_set':None,'diff_index':None}},
				{'param':model_MSSP.d_gc_ffpsos,'s_index':2, 'Differentiator':{'variable':None,'diff_set':None,'diff_index':None}},
				{'param':model_MSSP.a_wc_ffpsos,'s_index':2, 'Differentiator':{'variable':None,'diff_set':None,'diff_index':None}},
				{'param':model_MSSP.b_wc_ffpsos,'s_index':2, 'Differentiator':{'variable':None,'diff_set':None,'diff_index':None}},
				{'param':model_MSSP.c_wc_ffpsos,'s_index':2, 'Differentiator':{'variable':None,'diff_set':None,'diff_index':None}},
				{'param':model_MSSP.d_wc_ffpsos,'s_index':2, 'Differentiator':{'variable':None,'diff_set':None,'diff_index':None}},
				{'param':model_MSSP.Big_Mgc_ffpsos,'s_index':2, 'Differentiator':{'variable':None,'diff_set':None,'diff_index':None}},
				{'param':model_MSSP.Big_Mwc_ffpsos,'s_index':2, 'Differentiator':{'variable':None,'diff_set':None,'diff_index':None}},)
	Exo_input = ()
	Probability = probability
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

elif problem_name == 'VR':
	### Prepare parameters ###
	Case_csv = 'Parameters/' +problem_name+ '/' +problem_name+ '_Cases' + '/'+ str(Case_name)+".csv" # Load additional csv data file
	K, K_end, J, S, A, C, B, f_jjp, R, Q, d_js, D_ssp, k_ssp, probability, Cp,	d_j_exped = Pre.Parameter_setting(MD, Case_csv)
	time_set = K
	
	### Load MSSP model ###
	model_MSSP = Formulation.MSSP_model(K, K_end, J, S, A, C, f_jjp, R, Q, d_js, D_ssp, k_ssp, probability, Cp)
	
	### Differentiator variable information ###
	DF = {model_MSSP.delta_jjpks:{'t_index':2,'s_index':3,'sets':(A,S),'trigger_GT':0.8}}
	
	### Specify variables to save ###
	Var_output = {model_MSSP.delta_jjpks,model_MSSP.y_ks,model_MSSP.P_ks}
	
	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.d_js,'s_index':1, 'Differentiator':{'variable':model_MSSP.delta_jjpks,'diff_set':D_ssp,'diff_index':(1,)}},)
	Exo_input = ()
	Probability = probability
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

elif problem_name == 'DSR':
	### Prepare problem-specific parameters ###
	Omega_S, Omega_E, Omega_Estar, Omega_L, Omega_N, Omega_O, Omega_T, Omega_G, Omega_DG, Omega_K, Omega_KT_k, E_end, gammaD, gammaL_o, rI_e, ro_e, w_t, kappaL_o, kappaD, Q_o, Dmax_n, f_ns, f_n_exped, d_net, zeta_gt,\
	K_ge, Fini_l, I_ng, L_nl, cDSR, cDG, cDR, D_ssp, Max_K, probability = Pre.Parameter_setting(MD)
	
	time_set = Omega_E
	
	### Load MSSP model ###
	model_MSSP = Formulation.MSSP_model(Omega_S, Omega_E, Omega_Estar, Omega_L, Omega_N, Omega_O, Omega_T, Omega_G, Omega_DG, Omega_K, Omega_KT_k,
		E_end, gammaD, gammaL_o, rI_e, ro_e, w_t, kappaL_o, kappaD, Q_o, Dmax_n, f_ns, d_net, zeta_gt, K_ge, Fini_l, I_ng, L_nl, cDSR, cDG, cDR, D_ssp, Max_K, probability)
	
	### Differentiator variable information ###
	DF = {model_MSSP.Dtilde_nes:{'t_index':1,'s_index':2,'sets':(Omega_N,Omega_E,Omega_S),'trigger_GT':0.8}}
	
	### Specify variables to save ###
	Var_output = {model_MSSP.D_nes, model_MSSP.B_loes, model_MSSP.T_nets, model_MSSP.Xi_nets, model_MSSP.PG_gets, model_MSSP.PL_lets, model_MSSP.dR_nets}
	
	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.f_ns,'s_index':1, 'Differentiator':{'variable':model_MSSP.Dtilde_nes,'diff_set':D_ssp,'diff_index':(0,)}},)
	Exo_input = ()
	Probability = probability
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

elif problem_name == 'NTIP': 
	### Prepare problem-specific parameters ###
	N, N_product, N_feed, T, T_end, I, SG, I_PF, S,\
		MCst_n, CX_i0, cd_t, RD_i0, XMax_i, CC0_i, gamma_iPDFD, RDMax, Valpha, Vbeta, Bound_M, DeltaRDmin_i, DeltaCXmin_i, Big_M, MAX_D_nts,\
		D_nts, CXMin_isg, theta_is, chip_is, alpha_is, beta_is, phi_D_tssp, Dpsi_ssp, Dchi_ssp, DchiAEEV_ssp, Dalpha_ssp, Dbeta_ssp, scenario_param, \
		D_nt_exped, theta_i_exped, chip_i_exped, alpha_i_exped, beta_i_exped, theta_isgs, probability = Pre.Parameter_setting(MD)
	time_set = T
	
	### Load MSSP model ###
	model_MSSP = Formulation.MSSP_model(N, N_product, N_feed, T, T_end, I, SG, I_PF, S,
		MCst_n, CX_i0, cd_t, RD_i0, XMax_i, CC0_i, gamma_iPDFD, RDMax, Valpha, Vbeta, Bound_M, DeltaRDmin_i, DeltaCXmin_i, Big_M, MAX_D_nts,
		D_nts, CXMin_isg, theta_is, chip_is, alpha_is, beta_is, phi_D_tssp, Dpsi_ssp, Dchi_ssp, Dalpha_ssp, Dbeta_ssp, probability)
	
	### Differentiator variable information ###
	DF = {model_MSSP.NNalpha_its:{'t_index':1,'s_index':2,'sets':(I,T,S),'trigger_GT':0.8}, model_MSSP.NNbeta_its:{'t_index':1,'s_index':2,'sets':(I,T,S),'trigger_GT':0.8},
			model_MSSP.Y_isgts:{'t_index':2,'s_index':3,'sets':(I,SG,T,S),'trigger_GT':0.8}} # All differentiator variables
	
	### Specify variables to save ###
	Var_output = {model_MSSP.RD_its,model_MSSP.CX_its,model_MSSP.M_ints,model_MSSP.F_nts,model_MSSP.CC_its,model_MSSP.X_its,model_MSSP.g_ints,model_MSSP.G_nts,
				model_MSSP.Y_isgts,model_MSSP.chi_its,model_MSSP.ZM_ints,model_MSSP.YCX_its,model_MSSP.alpha_its,model_MSSP.beta_its,model_MSSP.NNalpha_its,
				model_MSSP.NNbeta_its,model_MSSP.Nalpha_its,model_MSSP.Nbeta_its}
	
	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.theta_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.Y_isgts,'diff_set':Dpsi_ssp,'diff_index':(0,1)}},
				{'param':model_MSSP.chip_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.Y_isgts,'diff_set':DchiAEEV_ssp, 'diff_index':(0,1)}},
				{'param':model_MSSP.alpha_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.NNalpha_its,'diff_set':Dalpha_ssp,'diff_index':(0,)}},
				{'param':model_MSSP.beta_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.NNbeta_its,'diff_set':Dbeta_ssp,'diff_index':(0,)}},)
	Exo_input = ({'param':model_MSSP.D_nts,'t_index':1,'s_index':2},)
	Probability = probability
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

elif problem_name == 'ALIP':
	### Prepare problem-specific parameters ###
	I, T, T_end, S, Pg, Po, Png, WI, MARR, FT, Cm_i, Co_i, Ce_i, b, D, LT, RT, n, Max_Qrc, Qg1, Qo1, Qng1, LFR_LB_i, LFR_UB_i, CLIM,\
	Qrc_i, Qrc_is, B_issp, D_ssp, probability, Qrc_i_exped = Pre.Parameter_setting(MD)
	time_set = T
	
	### Load MSSP model ###
	model_MSSP = Formulation.MSSP_model(I, T, T_end, S,
		Pg, Po, Png, WI, Max_Qrc, MARR, FT, Cm_i, Co_i, Ce_i, b, D, LT, RT, n, Qg1, Qo1, Qng1, LFR_LB_i, LFR_UB_i, Qrc_is, D_ssp, probability)
	
	### Differentiator variable information ###
	DF = {model_MSSP.w_ips:{'t_index':1,'s_index':2,'sets':(I,T,S),'trigger_GT':0.8}}
	
	### Specify variables to save ###
	Var_output = {model_MSSP.w_ips, model_MSSP.z_its, model_MSSP.y_itps, model_MSSP.x_rs, model_MSSP.Qg_rs, model_MSSP.Qo_rs, model_MSSP.Qng_rs,
				model_MSSP.LFRbALMLIM_irs, model_MSSP.bLIM_irs, model_MSSP.bREC_irs}
	
	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.Qrc_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.w_ips,'diff_set':D_ssp,'diff_index':(0,)}},)
	Exo_input = ()
	Probability = probability
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

elif problem_name == 'CPwTL': 
	### Prepare problem-specific parameters ###
	Case_csv = 'Parameters/' +problem_name+ '/' +problem_name+ '_Cases' + '/'+ str(Case_name)+".csv" # Load additional csv data file
	K, R, I, T, Tend, Ht, S, Cbark0, Deltabar_ki, b_kt, alpha_t, n_t, beta_kth, gamma_th, d_th, Omega_k, UT_k, DT_k, eta_kth, BigMy, BigMP,\
		integral_kis, D_ssp, probability, integral_ki_exped = Pre.Parameter_setting(MD,Case_csv)
	
	time_set = T
	
	model_MSSP = Formulation.MSSP_model(K, R, I, T, Tend, Ht, S,
		Cbark0, Deltabar_ki, b_kt, alpha_t, n_t, beta_kth, gamma_th, d_th, Omega_k, UT_k, DT_k, eta_kth, BigMy, BigMP,
		integral_kis, D_ssp, probability)
	
	### Differentiator variable information ###
	DF = {model_MSSP.x_kits:{'t_index':2,'s_index':3,'sets':(K,I,T,S),'trigger_GT':0.8}}
	
	### Specify variables to save ###
	Var_output = {model_MSSP.x_kits, model_MSSP.C_kts, model_MSSP.Delta_kts, model_MSSP.Q_ths, model_MSSP.P_kths, model_MSSP.V_ths, model_MSSP.y_kths, model_MSSP.w_kths}

	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.integral_kis,'s_index':2, 'Differentiator':{'variable':model_MSSP.x_kits,'diff_set':D_ssp, 'diff_index':(0,1)}},)
	Exo_input = ()
	Probability = probability
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

elif problem_name == 'CCSEOR': 
	### Prepare problem-specific parameters ###
	I, L, K, T, Tend, R, Rend, R_i, aapSET_r, aapLIST, S,\
		d, g_l, h_l, umin_l, umax_l, dp_i, gp_ik, hp_ik, alpha_i, v_i, e_i, wmin_k, wmax_k, fmin_i, fmax_i, c_i, b, beta_t, Fmax_t, a_r, ap_r, Max_thetamax_i, MAX_umax, \
		thetamax_is, m_is, D_ssp, probability, thetamax_i_exped, m_i_exped = Pre.Parameter_setting(MD)
	
	time_set = R
	
	model_MSSP = Formulation.MSSP_model(I, L, K, T, Tend, R, Rend, R_i, aapSET_r, aapLIST, S,
		d, g_l, h_l, umin_l, umax_l, dp_i, gp_ik, hp_ik, alpha_i, v_i, e_i, wmin_k, wmax_k, fmin_i, fmax_i, c_i, b, beta_t, Fmax_t, a_r, ap_r, Max_thetamax_i, MAX_umax, 
		thetamax_is, m_is, D_ssp, probability)
	
	### Differentiator variable information ###
	DF = {model_MSSP.deltap_ikrs:{'t_index':2,'s_index':3,'sets':(I,K,R,S),'trigger_GT':0.8}}
	
	### Specify variables to save ###
	Var_output = {model_MSSP.delta_ls, model_MSSP.deltap_ikrs, model_MSSP.x_its, model_MSSP.q_ikts, model_MSSP.u_lts, 
				model_MSSP.eta_ikts, model_MSSP.y_is, model_MSSP.w_is}

	### Uncertain parameter information ###
	Endo_input = ({'param':model_MSSP.thetamax_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.deltap_ikrs,'diff_set':D_ssp, 'diff_index':(0,)}},
				{'param':model_MSSP.m_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.deltap_ikrs,'diff_set':D_ssp, 'diff_index':(0,)}})
	Exo_input = ()
	Probability = probability
	
	### Objective function of the MSSP model ###
	OBJ = model_MSSP.objective

print('Necessary information has been loaded.')

MSSP_sequence.solve(optimization_model=optimization_model, instance_name=Case_name, MSSP_model=model_MSSP, solver_info=solver_info, Var_output=Var_output,
					objective_function = OBJ, time_set=time_set, Differentiator=DF, Probability=Probability, Endo_input=Endo_input, Exo_input=Exo_input)
