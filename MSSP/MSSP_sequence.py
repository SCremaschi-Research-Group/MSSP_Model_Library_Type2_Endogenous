import os
from pyomo.environ import *
from pyomo.opt import SolverFactory
import time as timer
import shutil
import MSSP.ScenarioTreeAnalyzer as STA

def solve(optimization_model, instance_name, MSSP_model, Var_output, solver_info, objective_function, time_set, Differentiator, Probability, Endo_input, Exo_input):

	start_time = timer.time()
		
	results= solver_info['solver'].solve(MSSP_model, **solver_info['solver_option'])
	
	min_or_max = str(objective_function.sense)
	
	if min_or_max == 'minimize' or min_or_max == '1':
		Objective_value = results.Problem.Upper_bound
	elif min_or_max == 'maximize' or min_or_max == '-1':
		Objective_value = results.Problem.Lower_bound
	else:
		raise ValueError('Cannot retrieve the objective value.')
	
	finish_time = timer.time()
	solution_time = finish_time - start_time
	print('Objective_value =', Objective_value, "solution_time =:", solution_time)
	
	### Retrieve scenario tree information
	### The following code retrieves the number of maximum stages, the number of total realizations, and information to draw the scenario tree from the solution.
	### Reorganize the indexes for the differentiator with one tuple ###
	
	index_location, coord_length = STA.input_data_processor(Differentiator, MSSP_model)
	# print('index_location =', index_location)
	# print('coord_length =', coord_length)
	
	### Convert elements in sets to tuple ###
	Endo_input = STA.tupler(Endo_input)
	# print('Endo_input =', Endo_input)
	
	Endogenous, Exogenous = STA.Complete_uncertainty_info(Endo_input, Exo_input, coord_length)
	# print('Endogenous =', Endogenous)
	# print('Exogenous =', Exogenous)
	
	endo_diffed_S, exo_diffed_S = STA.Unparam_differentiator_linker(index_location, Endogenous, Exogenous, MSSP_model, time_set, tuple(Probability.keys()))
	# print('endo_diffed_S =', endo_diffed_S)
	# print('exo_diffed_S =', exo_diffed_S)
	
	SG_d = tuple(Probability.keys()), # Initial indistinguishable scenarios
	R_count_s = {key: () for key in Probability}
	S_tree_info = {}
	for time in time_set:
		S_tree_info[time] = {}
		new_S_ind_list = []
		for S_ind in SG_d:
			dfs_CoodStartEnd = STA.distinguisher_processor(time, S_ind, Differentiator, MSSP_model)
			# print("dfs_CoodStartEnd =", dfs_CoodStartEnd)
			
			R_count_s, S_tree_info, new_S_ind_list =\
				STA.Subproblem_generator(S_ind, time, endo_diffed_S, exo_diffed_S, Exogenous, new_S_ind_list, dfs_CoodStartEnd, R_count_s, S_tree_info)
			# print("R_count_s =", R_count_s)
			# print("S_tree_info =", S_tree_info)
			# print("new_S_ind_list =", new_S_ind_list)
		SG_d = tuple(new_S_ind_list)
	
	max_stages = max(len(v) for v in R_count_s.values()) + 1
	print('max_stages =', max_stages)
	
	total_realizations = sum(len(S_tree_info[t]) for t in S_tree_info)
	print("total_realizations:", total_realizations)

	current_directory = os.path.dirname(os.path.realpath(__file__))
	parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
	
	### Set output directory
	current_date = timer.strftime('%Y_%m%d_%Hh%Mmin', timer.localtime())
	output_directory = current_directory + '/Solutions_MSSP/' + str(optimization_model) + '/' + str(instance_name) + '_' + current_date + '/'
	os.makedirs(output_directory)
	
	### Move logfile ###
	if os.path.exists(str(parent_directory) +'/'+ solver_info['solver_option']['logfile']):
		shutil.move(str(parent_directory) +'/'+ solver_info['solver_option']['logfile'], output_directory) # Files are overwritten.
	
	### Output Solver results ###
	sol_results = str(optimization_model)+ '_sol_MSSP_' + str(instance_name)
	results.write(filename = os.path.join(output_directory, sol_results))
	
	### Output variables ###
	var_results = str(optimization_model)+ '_var_MSSP_' + str(instance_name)
	f_var = open(os.path.join(output_directory, var_results),	"w")
	f_var.write('Objective' + ' ' + str(Objective_value) + ' ' + 'computational_time' + ' ' + str(solution_time) + '\n')
	
	for var in Var_output:
		f_var.write(var.name + ' ' + var.name + ' ' + var.name + ' ' + var.name + ' ' + var.name + ' ' + var.name + ' ' + var.name + ' ' + var.name + ' ' + var.name + ' ' +  '\n')
		method1 = getattr(var, 'extract_values')()
		for coord in method1:
			f_var.write(var.name + ' ' + str(coord) + ' ' + str(method1[coord]) + '\n')
	f_var.close()
	
	### Output scenario tree information ###
	realization = str(optimization_model)+ '_realization_MSSP_' + str(instance_name)
	f_rea = open(os.path.join(output_directory, realization),	"w")
	f_rea.write('max_stages' + ' ' + str(max_stages) + ' ' + 'total_realizations' + ' ' + str(total_realizations) + '\n')
	
	for t in S_tree_info:
		if len(S_tree_info[t])>0:
			f_rea.write('time' + ' ' + str(t) + '\n')
		for before in S_tree_info[t]:
			f_rea.write('before realization' + ' ' + str(before) + '\n')
			f_rea.write('after realization' + ' ' + str(S_tree_info[t][before]) + '\n')
	f_rea.close()
	
	return Objective_value, solution_time

