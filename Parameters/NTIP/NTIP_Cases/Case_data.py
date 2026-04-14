class T3S96(): # Case_1, 96 scenarios
	def __init__(self):

		###### Sets #####
		self.sets = {}
		self.sets['N'] = ['Chem_1', 'Chem_2', 'Chem_3'] # Chemical n
		self.sets['N_product'] = ['Chem_3'] # Product
		self.sets['N_feed'] = ['Chem_1', 'Chem_2'] # Raw material and intermediate
		self.sets['T'] = [1,2,3] # Time steps
		self.sets['I'] = ['Tech_1','Tech_2'] # Technologies
		self.sets['SG'] = [1,2,3] # Technology stages [1,2,3] = ['Lab','Pilot','Com']
		self.sets['I_PF'] = {'Tech_1':('Chem_3','Chem_1'), 'Tech_2':('Chem_3','Chem_2')} # Primary reactant/feedstock of technology i
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['MCst_n'] = {'Chem_1':724/2, 'Chem_2':845/2, 'Chem_3':1200} # Raw material cost [$/tonne]
		IR = 0.03 # Discount rate
		self.parameters['cd_t'] = {}
		for t in self.sets['T']:
			self.parameters['cd_t'][t] = (1 + IR) ** (1 - t) # Discounting Factor
		self.parameters['RD_i0'] = {'Tech_1':1,'Tech_2':5} # Initial R&D Investment
		self.parameters['XMax_i'] = {'Tech_1':6,'Tech_2':6} # Maximum allowable capacity Expansion at each time period
		self.parameters['RDMax'] = 10000 # Maximum research investment at each time period
		self.parameters['CC0_i'] = {'Tech_1':1,'Tech_2':1.4} # Initial capacity expansion cost for technology i
		self.parameters['CX_i0'] = {'Tech_1':1,'Tech_2':2.5} # Initial installed capacity of technology i
		self.parameters['CXMin_isg'] = {('Tech_1',1):1, ('Tech_1',2):1, ('Tech_1',3):1,
										('Tech_2',1):2.5, ('Tech_2',2):5, ('Tech_2',3):10} # Minimum capacity of stage sg for technology i
		self.parameters['gamma_innp'] = {('Tech_1','Chem_3','Chem_1'):0.55, ('Tech_2','Chem_3','Chem_2'):0.6} # Stoichiometric ratio between chemical n and n' in technology i
		self.parameters['Big_M'] = 100000
		self.parameters['Valpha'] = 1 # Research Threshold - The number of investments needed to realize Alpha
		self.parameters['Vbeta'] = 1 # Capacity Threshold - The number of expansions needed to realize Beta
		
		### Additional ###
		self.parameters['DeltaRDmin_i'] = {'Tech_1':1,'Tech_2':1} # Minimum investment required to count up the number of investments in research
		self.parameters['DeltaCXmin_i'] = {'Tech_1':1,'Tech_2':1} # Minimum expansion required to count up the number of expansions of capacity
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['alpha'] = {'Tech_1':{'certain':0}, 'Tech_2':{'Low':-0.20,'High':-0.18}}
		self.uncertain['beta'] = {'Tech_1':{'certain':0}, 'Tech_2':{'Low':-0.08,'High':-0.06}}
		self.uncertain['chi'] = {'Tech_1':{'certain':0.85}, 'Tech_2':{'Low':0.95,'High':0.98}} # Yield
		self.uncertain['demand'] = {1:{'certain':20}, 2:{'Low':23.5,'High':28}, 3:{'Low':22.1,'High':26}} # Only for chem 3
		self.uncertain['psi'] = {'Tech_1':{'2_CP':'2_CP'}, 'Tech_2':{'1_PA':'1_PA','2_PA':'2_PA','2_CP':'2_CP'}} # Project outcome
		
		##### Probability #####
		self.prob = {}
		self.prob['alpha_prob'] = {'Tech_1':{'certain':1}, 'Tech_2':{'Low':0.5,'High':0.5}}
		self.uncertain['beta_prob'] = {'Tech_1':{'certain':1}, 'Tech_2':{'Low':0.5,'High':0.5}}
		self.uncertain['chi_prob'] = {'Tech_1':{'certain':1}, 'Tech_2':{'Low':0.5,'High':0.5}} # Yield
		self.uncertain['demand_prob'] = {1:{'certain':1}, 2:{'Low':0.5,'High':0.5}, 3:{'Low':0.5,'High':0.5}} # Only for chem 3
		self.uncertain['psi_prob'] = {'Tech_1':{'2_CP':1}, 'Tech_2':{'1_PA':0.05,'2_PA':0.95*0.01,'2_CP':0.95*0.99}} # Probability of successs = {'Tech2':{'Lab':0.95,'Pilot':0.99}}

class T3S48(): # Case_1_one_undemand, 48 scenarios
	def __init__(self):

		###### Sets #####
		self.sets = {}
		self.sets['N'] = ['Chem_1', 'Chem_2', 'Chem_3'] # Chemical n
		self.sets['N_product'] = ['Chem_3'] # Product
		self.sets['N_feed'] = ['Chem_1', 'Chem_2'] # Raw material and intermediate
		self.sets['T'] = [1,2,3] # Time steps
		self.sets['I'] = ['Tech_1','Tech_2'] # Technologies
		self.sets['SG'] = [1,2,3] # Technology stages [1,2,3] = ['Lab','Pilot','Com']
		self.sets['I_PF'] = {'Tech_1':('Chem_3','Chem_1'), 'Tech_2':('Chem_3','Chem_2')} # Primary reactant/feedstock of technology i

		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['MCst_n'] = {'Chem_1':724/2, 'Chem_2':845/2, 'Chem_3':1200} # Raw material cost [$/tonne]
		IR = 0.03 # Discount rate
		self.parameters['cd_t'] = {}
		for t in self.sets['T']:
			self.parameters['cd_t'][t] = (1 + IR) ** (1 - t) # Discounting Factor
		self.parameters['RD_i0'] = {'Tech_1':1,'Tech_2':5} # Initial R&D Investment
		self.parameters['XMax_i'] = {'Tech_1':6,'Tech_2':6} # Maximum allowable capacity Expansion at each time period
		self.parameters['RDMax'] = 10000 # Maximum research investment at each time period
		self.parameters['CC0_i'] = {'Tech_1':1,'Tech_2':1.4} # Initial capacity expansion cost for technology i
		self.parameters['CX_i0'] = {'Tech_1':1,'Tech_2':2.5} # Initial installed capacity of technology i
		self.parameters['CXMin_isg'] = {('Tech_1',1):1, ('Tech_1',2):1, ('Tech_1',3):1,
										('Tech_2',1):2.5, ('Tech_2',2):5, ('Tech_2',3):10} # Minimum capacity of stage sg for technology i
		self.parameters['gamma_innp'] = {('Tech_1','Chem_3','Chem_1'):0.55, ('Tech_2','Chem_3','Chem_2'):0.6} # Stoichiometric ratio between chemical n and n' in technology i
		self.parameters['Big_M'] = 100000
		self.parameters['Valpha'] = 1 # Research Threshold - The number of investments needed to realize Alpha
		self.parameters['Vbeta'] = 1 # Capacity Threshold - The number of expansions needed to realize Beta
		
		### Additional ###
		self.parameters['DeltaRDmin_i'] = {'Tech_1':1,'Tech_2':1} # Minimum investment required to count up the number of investments in research
		self.parameters['DeltaCXmin_i'] = {'Tech_1':1,'Tech_2':1} # Minimum expansion required to count up the number of expansions of capacity
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['alpha'] = {'Tech_1':{'certain':0}, 'Tech_2':{'Low':-0.20,'High':-0.18}}
		self.uncertain['beta'] = {'Tech_1':{'certain':0}, 'Tech_2':{'Low':-0.08,'High':-0.06}}
		self.uncertain['chi'] = {'Tech_1':{'certain':0.85}, 'Tech_2':{'Low':0.95,'High':0.98}} # Yield
		self.uncertain['demand'] = {1:{'certain':20}, 2:{'certain':25.75}, 3:{'Low':22.1,'High':26}} # Only for chem 3
		self.uncertain['psi'] = {'Tech_1':{'2_CP':'2_CP'}, 'Tech_2':{'1_PA':'1_PA','2_PA':'2_PA','2_CP':'2_CP'}} # Project outcome
		
		##### Probability #####
		self.prob = {}
		self.prob['alpha_prob'] = {'Tech_1':{'certain':1}, 'Tech_2':{'Low':0.5,'High':0.5}}
		self.uncertain['beta_prob'] = {'Tech_1':{'certain':1}, 'Tech_2':{'Low':0.5,'High':0.5}}
		self.uncertain['chi_prob'] = {'Tech_1':{'certain':1}, 'Tech_2':{'Low':0.5,'High':0.5}} # Yield
		self.uncertain['demand_prob'] = {1:{'certain':1}, 2:{'certain':1}, 3:{'Low':0.5,'High':0.5}} # Only for chem 3
		self.uncertain['psi_prob'] = {'Tech_1':{'2_CP':1}, 'Tech_2':{'1_PA':0.05,'2_PA':0.95*0.01,'2_CP':0.95*0.99}} # Probability of successs = {'Tech2':{'Lab':0.95,'Pilot':0.99}}

class T3S24(): # 24 scenarios
	def __init__(self):

		###### Sets #####
		self.sets = {}
		self.sets['N'] = ['Chem_1', 'Chem_2', 'Chem_3'] # Chemical n
		self.sets['N_product'] = ['Chem_3'] # Product
		self.sets['N_feed'] = ['Chem_1', 'Chem_2'] # Raw material and intermediate
		self.sets['T'] = [1,2,3] # Time steps
		self.sets['I'] = ['Tech_1','Tech_2'] # Technologies
		self.sets['SG'] = [1,2,3] # Technology stages [1,2,3] = ['Lab','Pilot','Com']
		self.sets['I_PF'] = {'Tech_1':('Chem_3','Chem_1'), 'Tech_2':('Chem_3','Chem_2')} # Primary reactant/feedstock of technology i

		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['MCst_n'] = {'Chem_1':724/2, 'Chem_2':845/2, 'Chem_3':1200} # Raw material cost [$/tonne]
		IR = 0.03 # Discount rate
		self.parameters['cd_t'] = {}
		for t in self.sets['T']:
			self.parameters['cd_t'][t] = (1 + IR) ** (1 - t) # Discounting Factor
		self.parameters['RD_i0'] = {'Tech_1':1,'Tech_2':5} # Initial R&D Investment
		self.parameters['XMax_i'] = {'Tech_1':6,'Tech_2':6} # Maximum allowable capacity Expansion at each time period
		self.parameters['RDMax'] = 10000 # Maximum research investment at each time period
		self.parameters['CC0_i'] = {'Tech_1':1,'Tech_2':1.4} # Initial capacity expansion cost for technology i
		self.parameters['CX_i0'] = {'Tech_1':1,'Tech_2':2.5} # Initial installed capacity of technology i
		self.parameters['CXMin_isg'] = {('Tech_1',1):1, ('Tech_1',2):1, ('Tech_1',3):1,
										('Tech_2',1):2.5, ('Tech_2',2):5, ('Tech_2',3):10} # Minimum capacity of stage sg for technology i
		self.parameters['gamma_innp'] = {('Tech_1','Chem_3','Chem_1'):0.55, ('Tech_2','Chem_3','Chem_2'):0.6} # Stoichiometric ratio between chemical n and n' in technology i
		self.parameters['Big_M'] = 100000
		self.parameters['Valpha'] = 1 # Research Threshold - The number of investments needed to realize Alpha
		self.parameters['Vbeta'] = 1 # Capacity Threshold - The number of expansions needed to realize Beta
		
		### Additional ###
		self.parameters['DeltaRDmin_i'] = {'Tech_1':1,'Tech_2':1} # Minimum investment required to count up the number of investments in research
		self.parameters['DeltaCXmin_i'] = {'Tech_1':1,'Tech_2':1} # Minimum expansion required to count up the number of expansions of capacity

		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['alpha'] = {'Tech_1':{'certain':0}, 'Tech_2':{'Low':-0.20,'High':-0.18}}
		self.uncertain['beta'] = {'Tech_1':{'certain':0}, 'Tech_2':{'Low':-0.08,'High':-0.06}}
		self.uncertain['chi'] = {'Tech_1':{'certain':0.85}, 'Tech_2':{'Low':0.95,'High':0.98}} # Yield
		self.uncertain['demand'] = {1:{'certain':20}, 2:{'certain':25.75}, 3:{'certain':24.05}} # Only for chem 3
		self.uncertain['psi'] = {'Tech_1':{'2_CP':'2_CP'}, 'Tech_2':{'1_PA':'1_PA','2_PA':'2_PA','2_CP':'2_CP'}} # Project outcome
		
		##### Probability #####
		self.prob = {}
		self.prob['alpha_prob'] = {'Tech_1':{'certain':1}, 'Tech_2':{'Low':0.5,'High':0.5}}
		self.uncertain['beta_prob'] = {'Tech_1':{'certain':1}, 'Tech_2':{'Low':0.5,'High':0.5}}
		self.uncertain['chi_prob'] = {'Tech_1':{'certain':1}, 'Tech_2':{'Low':0.5,'High':0.5}} # Yield
		self.uncertain['demand_prob'] = {1:{'certain':1}, 2:{'certain':1}, 3:{'certain':1}} # Only for chem 3
		self.uncertain['psi_prob'] = {'Tech_1':{'2_CP':1}, 'Tech_2':{'1_PA':0.05,'2_PA':0.95*0.01,'2_CP':0.95*0.99}} # Probability of successs = {'Tech2':{'Lab':0.95,'Pilot':0.99}}

class T3S144(): # 144 scenarios
	def __init__(self):

		###### Sets #####
		self.sets = {}
		self.sets['N'] = ['Chem_1', 'Chem_2', 'Chem_3'] # Chemical n
		self.sets['N_product'] = ['Chem_3'] # Product
		self.sets['N_feed'] = ['Chem_1', 'Chem_2'] # Raw material and intermediate
		self.sets['T'] = [1,2,3] # Time steps
		self.sets['I'] = ['Tech_1','Tech_2'] # Technologies
		self.sets['SG'] = [1,2,3] # Technology stages [1,2,3] = ['Lab','Pilot','Com']
		self.sets['I_PF'] = {'Tech_1':('Chem_3','Chem_1'), 'Tech_2':('Chem_3','Chem_2')} # Primary reactant/feedstock of technology i
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['MCst_n'] = {'Chem_1':724/2, 'Chem_2':845/2, 'Chem_3':1200} # Raw material cost [$/tonne]
		IR = 0.03 # Discount rate
		self.parameters['cd_t'] = {}
		for t in self.sets['T']:
			self.parameters['cd_t'][t] = (1 + IR) ** (1 - t) # Discounting Factor
		self.parameters['RD_i0'] = {'Tech_1':1,'Tech_2':5} # Initial R&D Investment
		self.parameters['XMax_i'] = {'Tech_1':6,'Tech_2':6} # Maximum allowable capacity Expansion at each time period
		self.parameters['RDMax'] = 10000 # Maximum research investment at each time period
		self.parameters['CC0_i'] = {'Tech_1':1,'Tech_2':1.4} # Initial capacity expansion cost for technology i
		self.parameters['CX_i0'] = {'Tech_1':1,'Tech_2':2.5} # Initial installed capacity of technology i
		self.parameters['CXMin_isg'] = {('Tech_1',1):1, ('Tech_1',2):3, ('Tech_1',3):8,
										('Tech_2',1):2.5, ('Tech_2',2):5, ('Tech_2',3):10} # Minimum capacity of stage sg for technology i
		self.parameters['gamma_innp'] = {('Tech_1','Chem_3','Chem_1'):0.55, ('Tech_2','Chem_3','Chem_2'):0.6} # Stoichiometric ratio between chemical n and n' in technology i
		self.parameters['Big_M'] = 100000
		self.parameters['Valpha'] = 1 # Research Threshold - The number of investments needed to realize Alpha
		self.parameters['Vbeta'] = 1 # Capacity Threshold - The number of expansions needed to realize Beta
		
		### Additional ###
		self.parameters['DeltaRDmin_i'] = {'Tech_1':1,'Tech_2':1} # Minimum investment required to count up the number of investments in research
		self.parameters['DeltaCXmin_i'] = {'Tech_1':1,'Tech_2':1} # Minimum expansion required to count up the number of expansions of capacity
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['alpha'] = {'Tech_1':{'certain':0}, 'Tech_2':{'Low':-0.20,'High':-0.18}}
		self.uncertain['beta'] = {'Tech_1':{'certain':0}, 'Tech_2':{'Low':-0.08,'High':-0.06}}
		self.uncertain['chi'] = {'Tech_1':{'Low':0.8,'High':0.9}, 'Tech_2':{'certain':0.965}} # Yield
		self.uncertain['demand'] = {1:{'certain':20}, 2:{'certain':20}, 3:{'Low':22.1,'High':26}} # Only for chem 3
		self.uncertain['psi'] = {'Tech_1':{'1_PA':'1_PA','2_PA':'2_PA','2_CP':'2_CP'}, 'Tech_2':{'1_PA':'1_PA','2_PA':'2_PA','2_CP':'2_CP'}} # Project outcome
		
		##### Probability #####
		self.prob = {}
		self.prob['alpha_prob'] = {'Tech_1':{'certain':1}, 'Tech_2':{'Low':0.5,'High':0.5}}
		self.uncertain['beta_prob'] = {'Tech_1':{'certain':1}, 'Tech_2':{'Low':0.5,'High':0.5}}
		self.uncertain['chi_prob'] = {'Tech_1':{'Low':0.5,'High':0.5}, 'Tech_2':{'certain':1}} # Yield
		self.uncertain['demand_prob'] = {1:{'certain':1}, 2:{'certain':1}, 3:{'Low':0.5,'High':0.5}} # Only for chem 3
		self.uncertain['psi_prob'] = {'Tech_1':{'1_PA':0.02,'2_PA':0.98*0.01,'2_CP':0.98*0.99}, 'Tech_2':{'1_PA':0.05,'2_PA':0.95*0.01,'2_CP':0.95*0.99}} # Probability of successs = {'Tech2':{'Lab':0.95,'Pilot':0.99}}
