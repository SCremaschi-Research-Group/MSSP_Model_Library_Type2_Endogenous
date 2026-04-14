class K4R1T5S2(): # 1 uncertain technology, 5 time periods, 2 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['K'] = [1,2,3,4] # Technology k
		# self.sets['J'] = [1] # Resource j
		self.sets['R'] = [1] # Uncertain technology k
		self.sets['I'] = [1,2,3] # Capacity expansion permissible point i
		self.sets['T'] = [1,2,3,4,5] # Time periods t
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['HtSize'] = 24 # Operational scheduling intervals (24 days per year?)
		self.parameters['Cbark0'] = 5000 # Initial installed capacity (common for all process k)
		self.parameters['Deltabar_ki'] = {(1,1):4247, (1,2):4741, (1,3):4602,
										(2,1):4465, (2,2):4014, (2,3):4622,
										(3,1):4762, (3,2):4571, (3,3):4692,
										(4,1):4869, (4,2):4632, (4,3):4167} # Incremental capacity for technology k from point i-1 to i
		self.parameters['bdist_kt'] = {(1,1):18, (1,2):12, (1,3):18, (1,4):15, (1,5):15,
										(2,1):13, (2,2):16, (2,3):10, (2,4):16, (2,5):13,
										(3,1):13, (3,2):13, (3,3):12, (3,4):16, (3,5):19,
										(4,1):14, (4,2):18, (4,3):13, (4,4):19, (4,5):16} # Budget distribution for technology k
		self.parameters['n_t'] = {1:365, 2:365, 3:365, 4:365, 5:365} # Frequency of representative day in each t
		self.parameters['DetInt_ki'] = {(2,1):21766875000, (2,2):17159850000, (2,3):17563600000,
										(3,1):19048000000, (3,2):12341700000, (3,3):10697760000,
										(4,1):15824250000, (4,2):5211000000,  (4,3):3125250000} # Deterministic integral for process k from point i-1 to i
		DR = 0.04 # Discount rate
		self.parameters['alpha_t'] = {}
		for t in self.sets['T']:
			self.parameters['alpha_t'][t] = (1 + DR) ** (1 - t) # Discount Factor
		self.parameters['n'] = 365 # Frequency of representative day
		self.parameters['beta'] = (4,5) # Uniform distribution of the production cost
		self.parameters['gamma'] = 30*10**3 # Purchase/unmet demand cost
		self.parameters['d1bardist'] = 1.1 # Initial demand coefficient
		self.parameters['dTbardist'] = 0.6 # Final demand coefficient
		self.parameters['DemDistInh'] = (0.8,1.15) # Uniform distribution for demand in each h
		self.parameters['Omega_k'] = {1:100, 2:100, 3:100, 4:100} # Capacity per unit of technology k
		self.parameters['UT_k'] = {1:6, 2:6, 3:6, 4:6} # Minimum up-time of technology k
		self.parameters['DT_k'] = {1:2, 2:2, 3:2, 4:2} # Minimum down-time of technology k
		self.parameters['eta'] = 1 # Availability parameter
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		
		##### Probability #####
		self.prob = {}

class K4R1T5S4(): # 1 uncertain technology, 5 time periods, 4 scenarios
	def __init__(self):

		###### Sets #####
		self.sets = {}
		self.sets['K'] = [1,2,3,4] # Technology k
		# self.sets['J'] = [1] # Resource j
		self.sets['R'] = [1] # Uncertain technology k
		self.sets['I'] = [1,2,3] # Capacity expansion permissible point i
		self.sets['T'] = [1,2,3,4,5] # Time periods t
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['HtSize'] = 24 # Operational scheduling intervals (24 days per year?)
		self.parameters['Cbark0'] = 5000 # Initial installed capacity (common for all process k)
		self.parameters['Deltabar_ki'] = {(1,1):4247, (1,2):4741, (1,3):4602,
										(2,1):4465, (2,2):4014, (2,3):4622,
										(3,1):4762, (3,2):4571, (3,3):4692,
										(4,1):4869, (4,2):4632, (4,3):4167} # Incremental capacity for technology k from point i-1 to i
		self.parameters['bdist_kt'] = {(1,1):18, (1,2):12, (1,3):18, (1,4):15, (1,5):15,
										(2,1):13, (2,2):16, (2,3):10, (2,4):16, (2,5):13,
										(3,1):13, (3,2):13, (3,3):12, (3,4):16, (3,5):19,
										(4,1):14, (4,2):18, (4,3):13, (4,4):19, (4,5):16} # Budget distribution for technology k
		self.parameters['n_t'] = {1:365, 2:365, 3:365, 4:365, 5:365} # Frequency of representative day in each t
		self.parameters['DetInt_ki'] = {(2,1):21766875000, (2,2):17159850000, (2,3):17563600000,
										(3,1):19048000000, (3,2):12341700000, (3,3):10697760000,
										(4,1):15824250000, (4,2):5211000000,  (4,3):3125250000} # Deterministic integral for process k from point i-1 to i
		DR = 0.04 # Discount rate
		self.parameters['alpha_t'] = {}
		for t in self.sets['T']:
			self.parameters['alpha_t'][t] = (1 + DR) ** (1 - t) # Discount Factor
		self.parameters['n'] = 365 # Frequency of representative day
		self.parameters['beta'] = (4,5) # Uniform distribution of the production cost
		self.parameters['gamma'] = 30*10**3 # Purchase/unmet demand cost
		self.parameters['d1bardist'] = 1.1 # Initial demand coefficient
		self.parameters['dTbardist'] = 0.6 # Final demand coefficient
		self.parameters['DemDistInh'] = (0.8,1.15) # Uniform distribution for demand in each h
		self.parameters['Omega_k'] = {1:100, 2:100, 3:100, 4:100} # Capacity per unit of technology k
		self.parameters['UT_k'] = {1:6, 2:6, 3:6, 4:6} # Minimum up-time of technology k
		self.parameters['DT_k'] = {1:2, 2:2, 3:2, 4:2} # Minimum down-time of technology k
		self.parameters['eta'] = 1 # Availability parameter
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		
		##### Probability #####
		self.prob = {}

class K4R1T5S8(): # 1 uncertain technology, 5 time periods, 8 scenarios
	def __init__(self):

		###### Sets #####
		self.sets = {}
		self.sets['K'] = [1,2,3,4] # Technology k
		# self.sets['J'] = [1] # Resource j
		self.sets['R'] = [1] # Uncertain technology k
		self.sets['I'] = [1,2,3] # Capacity expansion permissible point i
		self.sets['T'] = [1,2,3,4,5] # Time periods t
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['HtSize'] = 24 # Operational scheduling intervals (24 days per year?)
		self.parameters['Cbark0'] = 5000 # Initial installed capacity (common for all process k)
		self.parameters['Deltabar_ki'] = {(1,1):4247, (1,2):4741, (1,3):4602,
										(2,1):4465, (2,2):4014, (2,3):4622,
										(3,1):4762, (3,2):4571, (3,3):4692,
										(4,1):4869, (4,2):4632, (4,3):4167} # Incremental capacity for technology k from point i-1 to i
		self.parameters['bdist_kt'] = {(1,1):18, (1,2):12, (1,3):18, (1,4):15, (1,5):15,
										(2,1):13, (2,2):16, (2,3):10, (2,4):16, (2,5):13,
										(3,1):13, (3,2):13, (3,3):12, (3,4):16, (3,5):19,
										(4,1):14, (4,2):18, (4,3):13, (4,4):19, (4,5):16} # Budget distribution for technology k
		self.parameters['n_t'] = {1:365, 2:365, 3:365, 4:365, 5:365} # Frequency of representative day in each t
		self.parameters['DetInt_ki'] = {(2,1):21766875000, (2,2):17159850000, (2,3):17563600000,
										(3,1):19048000000, (3,2):12341700000, (3,3):10697760000,
										(4,1):15824250000, (4,2):5211000000,  (4,3):3125250000} # Deterministic integral for process k from point i-1 to i
		# (4,1):19000000000, (4,2):12000000000,  (4,3):10000000000
		DR = 0.04 # Discount rate
		self.parameters['alpha_t'] = {}
		for t in self.sets['T']:
			self.parameters['alpha_t'][t] = (1 + DR) ** (1 - t) # Discount Factor
		self.parameters['n'] = 365 # Frequency of representative day
		self.parameters['beta'] = (4,5) # Uniform distribution of the production cost
		self.parameters['gamma'] = 30*10**3 # Purchase/unmet demand cost
		self.parameters['d1bardist'] = 1.1 # Initial demand coefficient
		self.parameters['dTbardist'] = 0.6 # Final demand coefficient
		self.parameters['DemDistInh'] = (0.8,1.15) # Uniform distribution for demand in each h
		self.parameters['Omega_k'] = {1:100, 2:100, 3:100, 4:100} # Capacity per unit of technology k
		self.parameters['UT_k'] = {1:6, 2:6, 3:6, 4:6} # Minimum up-time of technology k
		self.parameters['DT_k'] = {1:2, 2:2, 3:2, 4:2} # Minimum down-time of technology k
		self.parameters['eta'] = 1 # Availability parameter
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		
		##### Probability #####
		self.prob = {}

class K4R1T5S12(): # 1 uncertain technology, 5 time periods, 12 scenarios
	def __init__(self):

		###### Sets #####
		self.sets = {}
		self.sets['K'] = [1,2,3,4] # Technology k
		# self.sets['J'] = [1] # Resource j
		self.sets['R'] = [1] # Uncertain technology k
		self.sets['I'] = [1,2,3] # Capacity expansion permissible point i
		self.sets['T'] = [1,2,3,4,5] # Time periods t
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['HtSize'] = 24 # Operational scheduling intervals (24 days per year?)
		self.parameters['Cbark0'] = 5000 # Initial installed capacity (common for all process k)
		self.parameters['Deltabar_ki'] = {(1,1):4247, (1,2):4741, (1,3):4602,
										(2,1):4465, (2,2):4014, (2,3):4622,
										(3,1):4762, (3,2):4571, (3,3):4692,
										(4,1):4869, (4,2):4632, (4,3):4167} # Incremental capacity for technology k from point i-1 to i
		self.parameters['bdist_kt'] = {(1,1):18, (1,2):12, (1,3):18, (1,4):15, (1,5):15,
										(2,1):13, (2,2):16, (2,3):10, (2,4):16, (2,5):13,
										(3,1):13, (3,2):13, (3,3):12, (3,4):16, (3,5):19,
										(4,1):14, (4,2):18, (4,3):13, (4,4):19, (4,5):16} # Budget distribution for technology k
		self.parameters['n_t'] = {1:365, 2:365, 3:365, 4:365, 5:365} # Frequency of representative day in each t
		self.parameters['DetInt_ki'] = {(2,1):21766875000, (2,2):17159850000, (2,3):17563600000,
										(3,1):19048000000, (3,2):12341700000, (3,3):10697760000,
										(4,1):15824250000, (4,2):5211000000,  (4,3):3125250000} # Deterministic integral for process k from point i-1 to i
		DR = 0.04 # Discount rate
		self.parameters['alpha_t'] = {}
		for t in self.sets['T']:
			self.parameters['alpha_t'][t] = (1 + DR) ** (1 - t) # Discount Factor
		self.parameters['n'] = 365 # Frequency of representative day
		self.parameters['beta'] = (4,5) # Uniform distribution of the production cost
		self.parameters['gamma'] = 30*10**3 # Purchase/unmet demand cost
		self.parameters['d1bardist'] = 1.1 # Initial demand coefficient
		self.parameters['dTbardist'] = 0.6 # Final demand coefficient
		self.parameters['DemDistInh'] = (0.8,1.15) # Uniform distribution for demand in each h
		self.parameters['Omega_k'] = {1:100, 2:100, 3:100, 4:100} # Capacity per unit of technology k
		self.parameters['UT_k'] = {1:6, 2:6, 3:6, 4:6} # Minimum up-time of technology k
		self.parameters['DT_k'] = {1:2, 2:2, 3:2, 4:2} # Minimum down-time of technology k
		self.parameters['eta'] = 1 # Availability parameter
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		
		##### Probability #####
		self.prob = {}

class K4R2T5S16(): # 2 uncertain technology, 5 time periods, 16 scenarios
	def __init__(self):

		###### Sets #####
		self.sets = {}
		self.sets['K'] = [1,2,3,4] # Technology k
		# self.sets['J'] = [1] # Resource j
		self.sets['R'] = [1,4] # Uncertain technology k
		self.sets['I'] = [1,2,3] # Capacity expansion permissible point i
		self.sets['T'] = [1,2,3,4,5] # Time periods t
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['HtSize'] = 24 # Operational scheduling intervals (24 days per year?)
		self.parameters['Cbark0'] = 5000 # Initial installed capacity (common for all process k)
		self.parameters['Deltabar_ki'] = {(1,1):4247, (1,2):4741, (1,3):4602,
										(2,1):4465, (2,2):4014, (2,3):4622,
										(3,1):4762, (3,2):4571, (3,3):4692,
										(4,1):4869, (4,2):4632, (4,3):4167} # Incremental capacity for technology k from point i-1 to i
		self.parameters['bdist_kt'] = {(1,1):18, (1,2):12, (1,3):18, (1,4):15, (1,5):15,
										(2,1):13, (2,2):16, (2,3):10, (2,4):16, (2,5):13,
										(3,1):13, (3,2):13, (3,3):12, (3,4):16, (3,5):19,
										(4,1):14, (4,2):18, (4,3):13, (4,4):19, (4,5):16} # Budget distribution for technology k
		self.parameters['n_t'] = {1:365, 2:365, 3:365, 4:365, 5:365} # Frequency of representative day in each t
		self.parameters['DetInt_ki'] = {(2,1):21766875000, (2,2):17159850000, (2,3):17563600000,
										(3,1):19048000000, (3,2):12341700000, (3,3):10697760000} # Deterministic integral for process k from point i-1 to i
		
		DR = 0.04 # Discount rate
		self.parameters['alpha_t'] = {}
		for t in self.sets['T']:
			self.parameters['alpha_t'][t] = (1 + DR) ** (1 - t) # Discount Factor
		self.parameters['n'] = 365 # Frequency of representative day
		self.parameters['beta'] = (4,5) # Uniform distribution of the production cost
		self.parameters['gamma'] = 30*10**3 # Purchase/unmet demand cost
		self.parameters['d1bardist'] = 1.1 # Initial demand coefficient
		self.parameters['dTbardist'] = 0.6 # Final demand coefficient
		self.parameters['DemDistInh'] = (0.8,1.15) # Uniform distribution for demand in each h
		self.parameters['Omega_k'] = {1:100, 2:100, 3:100, 4:100} # Capacity per unit of technology k
		self.parameters['UT_k'] = {1:6, 2:6, 3:6, 4:6} # Minimum up-time of technology k
		self.parameters['DT_k'] = {1:2, 2:2, 3:2, 4:2} # Minimum down-time of technology k
		self.parameters['eta'] = 1 # Availability parameter
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		
		##### Probability #####
		self.prob = {}
