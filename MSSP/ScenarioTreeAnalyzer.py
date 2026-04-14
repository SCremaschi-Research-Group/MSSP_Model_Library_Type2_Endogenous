import numpy as np
import itertools
import collections

def tupler(Endo_input):
	# This function converts the elements in the sets of here-and-now decision variables, wait-and-see decision variables, differentiator variables, and differentiator sets to tuples. 
	# This process allows for the unified processing of different types of sets. The original sets can be tuples, lists, integers, or strings.
	
	# Differentiator sets
	for un_dict in Endo_input:
		if un_dict['Differentiator']['diff_set'] != None:
			for s_sp in un_dict['Differentiator']['diff_set']:
				coords = ()
				for coord in un_dict['Differentiator']['diff_set'][s_sp]:
					tupled_coord = ()
					if isinstance(coord, int) == True or isinstance(coord, str) == True: 
						tupled_coord += (coord,)
					elif isinstance(coord, list) == True:
						tupled_coord += tuple(coord)
					elif isinstance(coord, tuple) == True:
						tupled_coord += coord
					else:
						raise TypeError('The element type in sets must be int, str, tuple, or list. For example, D[s,sp] = [1,2,3], D[s,sp] = [(1,2)]')
					coords += (tupled_coord,)
				un_dict['Differentiator']['diff_set'][s_sp] = tuple(coords)
		# print('Endo_input =', Endo_input)
	
	return Endo_input

def input_data_processor(Differentiator, model):
	
	index_location = {}
	### Endogenous part ###
	index_location['DF'] = {}
	for df in Differentiator:
		index_location['DF'][df.name] = {}
		index_location['DF'][df.name]['t_index'] = Differentiator[df]['t_index']
		index_location['DF'][df.name]['s_index'] = Differentiator[df]['s_index']
	# print('index_location =', index_location)
	
	coord_length = {}
	coord_length['DF'] = {}
	for df in Differentiator:
		method1 = getattr(model, df.name)
		for index in method1:
			coord_length['DF'][df.name] = len(index)
			break
	# print('coord_length =', coord_length)

	return index_location, coord_length

def Complete_uncertainty_info(Endo_input, Exo_input, coord_length):
	
	### Endogenous part ###
	Endogenous = {}
	for un_dict in Endo_input:
		un_name = un_dict['param'].name
		Endogenous[un_name] = un_dict
		Endogenous[un_name]['param'] = un_dict['param'].extract_values()
		if Endogenous[un_name]['Differentiator']['variable'] != None:
			Endogenous[un_name]['Differentiator']['coord_len'] = coord_length['DF'][Endogenous[un_name]['Differentiator']['variable'].name]
	
	### Exogenous part ###
	Exogenous = {}
	for un_dict in Exo_input:
		un_name = un_dict['param'].name
		Exogenous[un_name] = un_dict
		Exogenous[un_name]['param'] = un_dict['param'].extract_values()
	
	return Endogenous, Exogenous

def Unparam_differentiator_linker(index_location, Endogenous, Exogenous, model, T, S):
	
	### Endogenous part ###
	index_info = {}
	diff_coords = {}
	coord_treated_s = {}
	difference_set = {}
	collected_S = {}
	i_collector = {} 
	for un_name in Endogenous:
		if Endogenous[un_name]['Differentiator']['diff_set'] != None:
		
			### Link differentiating, time, scenario, other indexes to the coordinates
			index_info[un_name] = {}
			for loc in range(0,Endogenous[un_name]['Differentiator']['coord_len']):
				if loc in Endogenous[un_name]['Differentiator']['diff_index']:
					index_info[un_name][loc] = 'Dssp'
				elif loc == index_location['DF'][Endogenous[un_name]['Differentiator']['variable'].name]['t_index']:
					index_info[un_name][loc] = 'time'
				elif loc == index_location['DF'][Endogenous[un_name]['Differentiator']['variable'].name]['s_index']:
					index_info[un_name][loc] = 'scenario'
				else:
					index_info[un_name][loc] = 'other'
			# print('index_info =', index_info)
			
			### Collect all differentiating coordinates without 'other' index
			diff_coords[un_name] = tuple(set(tuple(itertools.chain.from_iterable(Endogenous[un_name]['Differentiator']['diff_set'].values()))))
			# print('diff_coords =', diff_coords)
			
			### Collect scenarios related to differentiating coordinates
			coord_treated_s[un_name] = {}
			difference_set[un_name] = {} # New from GKDA!!!
			for coord in diff_coords[un_name]:
				coord_treated_s[un_name][coord] = [ssp for ssp in Endogenous[un_name]['Differentiator']['diff_set'] if coord in Endogenous[un_name]['Differentiator']['diff_set'][ssp]]
			# print(coord_treated_s)
			for coord in coord_treated_s[un_name]:
				coord_treated_s[un_name][coord] = tuple(sorted(tuple(set(tuple(itertools.chain.from_iterable(coord_treated_s[un_name][coord]))))))
				difference_set[un_name][coord] = {} # New from GKDA!!!
				if len(set(S) - set(coord_treated_s[un_name][coord])) > 0: # New from GKDA!!!
					difference_set[un_name][coord] = tuple(sorted(tuple(set(S) - set(coord_treated_s[un_name][coord])))) # New from GKDA!!!
			# print('coord_treated_s', coord_treated_s)
			
			### Link coord without 'other' to scenarios differenciated
			collected_S[un_name] = {}
			for coord in diff_coords[un_name]:
				collected_S[un_name][coord] = {}
				counter = 0
				s_rest = tuple(coord_treated_s[un_name][coord])
				while len(s_rest) > 0:
					s_collector = ()
					s_rest_collector = ()
					# print('s_rest =', s_rest)
					if len(s_rest) == 1: 
						s_collector += s_rest
					s = s_rest[0] # for s in s_rest:
					for sp in s_rest:
						if s!=sp and (s,sp) in Endogenous[un_name]['Differentiator']['diff_set']: # Changed while working for CTP:
							if len(s_collector) == 0: # Base scenario
								s_collector += (s,)
							if coord not in Endogenous[un_name]['Differentiator']['diff_set'][s,sp]: # and s in s_collector:
								s_collector += (sp,)
							else:
								s_rest_collector += (sp,)
					collected_S[un_name][coord]['S'+str(counter)] = s_collector
					# print('collected_S =', collected_S)
					s_rest = s_rest_collector
					# print('s_rest =', s_rest)
					counter += 1
				# print('collected_S =', collected_S)
			# print('collected_S =', collected_S)
			
			### collected_S backchecker ### Suppressed to reduce the computational time!
			for coord in coord_treated_s[un_name]:
				len_counter = 0
				for S_group in collected_S[un_name][coord]:
					len_counter += len(collected_S[un_name][coord][S_group])
					# print('Check overlap ', len(set(collected_S[un_name][coord][S_group])), len(collected_S[un_name][coord][S_group]))
					if len(set(collected_S[un_name][coord][S_group])) != len(collected_S[un_name][coord][S_group]):
						raise ValueError('Differentiator liker is not working properly.')
				# print('Check the number of scenario ', len_counter, len(coord_treated_s[un_name][coord]))
				if len_counter != len(coord_treated_s[un_name][coord]):
					raise ValueError('Differentiator liker is not working properly.')
			
			i_collector[un_name] = {}
			var_name = Endogenous[un_name]['Differentiator']['variable'].name
			method1 = getattr(model, var_name)
			for coord_AEEV in method1: # DF_GKDA[var_name]['sets']: 
				i_Dssp = ()
				i = ()
				i += (var_name,)
				for loc in index_info[un_name]:
					if index_info[un_name][loc] == 'Dssp':
						i_Dssp += (coord_AEEV[loc],)
						i += (coord_AEEV[loc],)
					elif index_info[un_name][loc] == 'other':
						i += (coord_AEEV[loc],)
				if i_Dssp not in i_collector[un_name]:
					i_collector[un_name][i_Dssp] = () # []
				if i not in i_collector[un_name][i_Dssp]:
					i_collector[un_name][i_Dssp] += (i,) # .append(i)
	
	for un_name in difference_set: # New from GKDA!!!
		for coord in difference_set[un_name]: # New from GKDA!!!
			if len(difference_set[un_name][coord])>0: # New from GKDA!!!
				collected_S[un_name][coord]['S_lack'] = difference_set[un_name][coord] # New from GKDA!!!
	
	# print('index_info =', index_info)
	# print('diff_coords =', diff_coords)
	# print('coord_treated_s', coord_treated_s)
	# print('difference_set', difference_set) # New from GKDA!!!
	# print('collected_S', collected_S)
	# print('i_collector =', i_collector)
	
	item_linker = {}
	for un_name in i_collector:
		item_linker[un_name] = {}
		for tupled_i_Dssp in i_collector[un_name]:
			if tupled_i_Dssp in diff_coords[un_name]:
				item_linker[un_name][tupled_i_Dssp] = i_collector[un_name][tupled_i_Dssp]
	# print('item_linker =', item_linker)
	
	# Back check
	for un_name in item_linker:
		if len(item_linker[un_name]) != len(diff_coords[un_name]):
			print('item_linker =', item_linker)
			print('diff_coords =', diff_coords)
			raise KeyError('Differentiator linker is not working properly')
	
	endo_diffed_S = {}
	for un_name in item_linker:
		for tupled_i_Dssp in item_linker[un_name]:
			for i in item_linker[un_name][tupled_i_Dssp]:
				if i not in endo_diffed_S:
					endo_diffed_S[i] = {}
				endo_diffed_S[i][un_name] = collected_S[un_name][tupled_i_Dssp]
	# print('endo_diffed_S =', endo_diffed_S)
	
	### Exogenous part ###
	exo_diffed_S = {}
	for un_name in Exogenous:
		for t in T:
			exo_diffed_S[t] = {}
			# Collect scenarios with the same outcomes
			for index_exo in Exogenous[un_name]['param']:
				if index_exo[Exogenous[un_name]['t_index']] == t:
					before_t_s_deletion = list(index_exo)
					
					# del listed_index_exo[Exogenous[un_name]['s_index']]
					dellist = lambda items,indices: [item for idx,item in enumerate(items) if idx not in indices]
					del_idx = [Exogenous[un_name]['t_index'], Exogenous[un_name]['s_index']] # Remove indexes for time and scenario
					listed_index_exo = dellist(before_t_s_deletion, del_idx)
					
					index_exo_WO_s = tuple(listed_index_exo)
					if index_exo_WO_s not in exo_diffed_S[t]:
						exo_diffed_S[t][index_exo_WO_s] = {}
						exo_diffed_S[t][index_exo_WO_s][un_name] = {}
					if Exogenous[un_name]['param'][index_exo] not in exo_diffed_S[t][index_exo_WO_s][un_name]:
						# exo_diffed_S[t][index_exo_WO_s][un_name][Exogenous[un_name]['param'][index_exo]] = []
						exo_diffed_S[t][index_exo_WO_s][un_name][Exogenous[un_name]['param'][index_exo]] = ()
					else:
						pass
					if index_exo[Exogenous[un_name]['s_index']] not in exo_diffed_S[t][index_exo_WO_s][un_name][Exogenous[un_name]['param'][index_exo]]:
						# exo_diffed_S[t][index_exo_WO_s][un_name][Exogenous[un_name]['param'][index_exo]].append(index_exo[Exogenous[un_name]['s_index']])
						exo_diffed_S[t][index_exo_WO_s][un_name][Exogenous[un_name]['param'][index_exo]] += (index_exo[Exogenous[un_name]['s_index']],)
			# print('exo_diffed_S =', exo_diffed_S)
			# Leave collected scenarios in tuples if there is uncertainty realization
			for index_exo_WO_s in exo_diffed_S[t]:
				for un_name in exo_diffed_S[t][index_exo_WO_s]:
					if len(exo_diffed_S[t][index_exo_WO_s][un_name]) >= 2: # If there is uncertainty realization
						pass
					else:
						exo_diffed_S[t][index_exo_WO_s][un_name] = {}
	# print('exo_diffed_S =', exo_diffed_S)
	return endo_diffed_S, exo_diffed_S

def distinguisher_processor(time, S_ind, Differentiator, model):
	
	dfs_CoodStartEnd = ()
	
	def nest_func(time, Differentiator, dfs_CoodStartEnd):
		listed_index = list(index)
		
		dellist = lambda items,indices: [item for idx,item in enumerate(items) if idx not in indices]
		del_idx = [Differentiator[df]['t_index'], Differentiator[df]['s_index']] # Remove indexes for time and scenario
		index_WO_ts = dellist(listed_index, del_idx)
		
		# df_CoodTime = (df.name, *index_WO_ts)
		df_CoodStartEnd = {}
		df_CoodStartEnd['COORDS'] = (df.name, *index_WO_ts)
		df_CoodStartEnd['time'] = time
		### Append ###
		# dfs_CoodTime += (df_CoodTime,)
		# print(df_CoodStartEnd)
		# print(dfs_CoodStartEnd)
		
		if df_CoodStartEnd not in dfs_CoodStartEnd: 
			dfs_CoodStartEnd += (df_CoodStartEnd,)
		# if len(dfs_CoodStartEnd) == 0: 
		# 	dfs_CoodStartEnd += (df_CoodStartEnd,)
		# else:
		# 	if df_CoodStartEnd not in dfs_CoodStartEnd:
		# 		raise ValueError('MSSP solution has not satisfied scenario indistinguishability.')
		return dfs_CoodStartEnd

	for df in Differentiator:
		method1 = getattr(model, df.name)
		if 'trigger_GT' in Differentiator[df]:
			for index in method1:
				if time == index[Differentiator[df]['t_index']] and index[Differentiator[df]['s_index']] in S_ind:
					if method1[index].value != None and method1[index].value > Differentiator[df]['trigger_GT']:
						dfs_CoodStartEnd = nest_func(time, Differentiator, dfs_CoodStartEnd)
		elif 'trigger_LT' in Differentiator[df]:
			for index in method1:
				if time == index[Differentiator[df]['t_index']] and index[Differentiator[df]['s_index']] in S_ind:
					if method1[index].value != None and method1[index].value < Differentiator[df]['trigger_LT']:
						dfs_CoodStartEnd = nest_func(time, Differentiator, dfs_CoodStartEnd)
		else:
			raise KeyError('Specify the trigger value of differentiator variable(s). For example, {"trigger_GT":0.8}')
	
	# print(dfs_CoodStartEnd)
	
	return dfs_CoodStartEnd

def Subproblem_generator(S_ind, time, endo_diffed_S, exo_diffed_S, Exogenous, new_S_ind_list, dfs_CoodStartEnd, R_count_s, S_tree_info):
	
	### If there are started items, pick up the COORDS. ###
	started_items = []
	for monitored in dfs_CoodStartEnd: # df_monitor[time][sub_p]:
		if monitored['time'] == time:
			started_items.append(monitored['COORDS'])
	started_items = tuple(started_items)
	# print("started_items =", started_items)
	
	realized_scenario = {}
	### Endogenous part ###
	for i in started_items:
		if i in endo_diffed_S:
			realized_scenario[i] = {}
			for un_name in endo_diffed_S[i]:
				realized_scenario[i][un_name] = {}
				for S_group in endo_diffed_S[i][un_name]:
					distinguished_S = []
					for s in S_ind:
						if s in endo_diffed_S[i][un_name][S_group]:
							distinguished_S.append(s)
					if len(distinguished_S)>=1:
						realized_scenario[i][un_name][S_group] = tuple(distinguished_S)
	# print("realized_scenario =", realized_scenario)
	
	### Exogenous part ###
	if Exogenous != dict():
		for exo_coord in exo_diffed_S[time]:
			if exo_coord not in realized_scenario:
				realized_scenario[exo_coord] = {}
				for un_name in exo_diffed_S[time][exo_coord]:
					realized_scenario[exo_coord][un_name] = exo_diffed_S[time][exo_coord][un_name]
	# print("realized_scenario =", realized_scenario)
	
	##### Consider intersection #####
	S_extractor = [set(S_ind)] # [set(sub_p_UnParam[time][sub_p][0])] # Initial extractor = all scenarios
	for i in realized_scenario:
		intersections = []
		for un_name in realized_scenario[i]:
			if len(realized_scenario[i][un_name]) >=1:
				for s_set in S_extractor:
					# print(s_set)
					for outcome in realized_scenario[i][un_name]:
						# print(outcome)
						intersection = s_set & set(realized_scenario[i][un_name][outcome]) # Extract intersection of sets
						# print(intersection)
						if intersection != set() and intersection not in intersections: # if intersection is not empty set
							intersections.append(intersection)
							# print(intersections)
				S_extractor = intersections
				# print(S_extractor)
	# print("S_extractor =", S_extractor)
	realized_S = S_extractor
	# print('realized_S =', realized_S, 'before realization =', sub_p_UnParam[time][sub_p][0])
	
	### Tupler and carry over all indistinguishable scenarios ###
	tupled_realized_S = ()
	for S in realized_S:
		tupled_realized_S += (tuple(S),)
		if len(S) > 1:
			new_S_ind_list.append(tuple(S))
	
	##### Realization checker #####
	if len(realized_S) > 1: # If there are multiple sets of S, realization occurs.
		Realization_checker = True
	else:
		Realization_checker = False
	
	if Realization_checker == True:
		S_tree_info[time][S_ind] = tupled_realized_S
		for s in S_ind:
			R_count_s[s] += (time,)
	
	return R_count_s, S_tree_info, new_S_ind_list
