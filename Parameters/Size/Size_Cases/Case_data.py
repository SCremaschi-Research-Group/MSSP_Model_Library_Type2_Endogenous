class I3T3S8():
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['I'] = [1,2,3]
		self.sets['T'] = range(1,4)
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['rho'] = 0.008 # unit penalty cost
		self.parameters['sigma'] = 453 # set-up cost for any size
		self.parameters['c_t'] = {1:30000,2:30000,3:30000} # Total production capacity
		self.parameters['M'] =  30000 # Maximum production for size i at t in s
		
		##### Parameters for complete recouse #####
		self.parameters['Cpu'] = 1000 # Purchase cost, this should be very high compared to other costs
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Cpr_i'] = {1:{1:0.48,2:0.52}, 2:{1:0.5,2:0.54}, 3:{1:0.54}} # Unit production costs
		self.uncertain['D_t'] = {1:{1:7500}, 2:{1:5000,2:10000}} # Demand. Same demand after t = 2
		self.uncertain['t_realization'] = 2
		
		##### Probability #####
		self.uncertain['Cpr_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:1}}
		self.uncertain['D_t_prob'] = {1:{1:1}, 2:{1:0.5,2:0.5}}

class I3T3S16():
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['I'] = [1,2,3]
		self.sets['T'] = range(1,4)
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['rho'] = 0.008 # unit penalty cost
		self.parameters['sigma'] = 453 # set-up cost for any size
		self.parameters['c_t'] = {1:30000,2:30000,3:30000} # Total production capacity
		self.parameters['M'] =  30000 # Maximum production for size i at t in s
		
		##### Parameters for complete recouse #####
		self.parameters['Cpu'] = 1000 # Purchase cost, this should be very high compared to other costs
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Cpr_i'] = {1:{1:0.48,2:0.52}, 2:{1:0.5,2:0.54}, 3:{1:0.54}} # Unit production costs
		self.uncertain['D_t'] = {1:{1:5000,2:10000}, 2:{1:5000,2:10000}} # Demand. Same demand after t = 2
		self.uncertain['t_realization'] = 2
		
		##### Probability #####
		self.uncertain['Cpr_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:1}}
		self.uncertain['D_t_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}}

class I3T3S32():
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['I'] = [1,2,3]
		self.sets['T'] = range(1,4)
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['rho'] = 0.008 # unit penalty cost
		self.parameters['sigma'] = 453 # set-up cost for any size
		self.parameters['c_t'] = {1:30000,2:30000,3:30000} # Total production capacity
		self.parameters['M'] =  30000 # Maximum production for size i at t in s
		
		##### Parameters for complete recouse #####
		self.parameters['Cpu'] = 1000 # Purchase cost, this should be very high compared to other costs
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Cpr_i'] = {1:{1:0.48,2:0.52}, 2:{1:0.5,2:0.54}, 3:{1:0.52,2:0.56}} # Unit production costs
		self.uncertain['D_t'] = {1:{1:5000,2:10000}, 2:{1:5000,2:10000}} # Demand. Same demand after t = 2
		self.uncertain['t_realization'] = 2
		
		##### Probability #####
		self.uncertain['Cpr_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:0.5,2:0.5}}
		self.uncertain['D_t_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}}

class I3T3S64():
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['I'] = [1,2,3]
		self.sets['T'] = range(1,4)
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['rho'] = 0.008 # unit penalty cost
		self.parameters['sigma'] = 453 # set-up cost for any size
		self.parameters['c_t'] = {1:30000,2:30000,3:30000} # Total production capacity
		self.parameters['M'] =  30000 # Maximum production for size i at t in s
		
		##### Parameters for complete recouse #####
		self.parameters['Cpu'] = 1000 # Purchase cost, this should be very high compared to other costs
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Cpr_i'] = {1:{1:0.48,2:0.52}, 2:{1:0.5,2:0.54}, 3:{1:0.52,2:0.56}} # Unit production costs
		self.uncertain['D_t'] = {1:{1:5000,2:10000}, 2:{1:5000,2:10000}, 3:{1:5000,2:10000}} # Demand.
		self.uncertain['t_realization'] = 3
		
		##### Probability #####
		self.uncertain['Cpr_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:0.5,2:0.5}}
		self.uncertain['D_t_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:0.5,2:0.5}}

class I3T4S128():
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['I'] = [1,2,3]
		self.sets['T'] = range(1,5)
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['rho'] = 0.008 # unit penalty cost
		self.parameters['sigma'] = 453 # set-up cost for any size
		self.parameters['c_t'] = {1:30000,2:30000,3:30000,4:30000} # Total production capacity
		self.parameters['M'] =  30000 # Maximum production for size i at t in s
		
		##### Parameters for complete recouse #####
		self.parameters['Cpu'] = 1000 # Purchase cost, this should be very high compared to other costs
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Cpr_i'] = {1:{1:0.48,2:0.52}, 2:{1:0.5,2:0.54}, 3:{1:0.52,2:0.56}} # Unit production costs
		self.uncertain['D_t'] = {1:{1:5000,2:10000}, 2:{1:5000,2:10000}, 3:{1:5000,2:10000}, 4:{1:5000,2:10000}} # Demand.
		self.uncertain['t_realization'] = 4
		
		##### Probability #####
		self.uncertain['Cpr_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:0.5,2:0.5}}
		self.uncertain['D_t_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:0.5,2:0.5}, 4:{1:0.5,2:0.5}}

class I4T4S256():
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['I'] = [1,2,3,4]
		self.sets['T'] = range(1,5)
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['rho'] = 0.008 # unit penalty cost
		self.parameters['sigma'] = 453 # set-up cost for any size
		self.parameters['c_t'] = {1:40000,2:40000,3:40000,4:40000} # Total production capacity
		self.parameters['M'] =  40000 # Maximum production for size i at t in s
		
		##### Parameters for complete recouse #####
		self.parameters['Cpu'] = 1000 # Purchase cost, this should be very high compared to other costs
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Cpr_i'] = {1:{1:0.48,2:0.52}, 2:{1:0.5,2:0.54}, 3:{1:0.52,2:0.56}, 4:{1:0.54,2:0.58}} # Unit production costs
		self.uncertain['D_t'] = {1:{1:5000,2:10000}, 2:{1:5000,2:10000}, 3:{1:5000,2:10000}, 4:{1:5000,2:10000}} # Demand.
		self.uncertain['t_realization'] = 4
		
		##### Probability #####
		self.uncertain['Cpr_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:0.5,2:0.5}, 4:{1:0.5,2:0.5}}
		self.uncertain['D_t_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:0.5,2:0.5}, 4:{1:0.5,2:0.5}}