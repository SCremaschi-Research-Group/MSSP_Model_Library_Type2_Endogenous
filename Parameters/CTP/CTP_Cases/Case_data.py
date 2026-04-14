class I2J3T12S16():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['I'] = [1,2] # drugs
		self.sets['J'] = [1,2,3] # Clinical trials
		self.sets['T'] = [1,2,3,4,5,6,7,8,9,10,11,12] # Time periods
		self.sets['R'] = [1,2] # Resource types
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD_i'] = {1:44,2:56} # Penalty for reduced active patent life
		self.parameters['gammaL_i'] = {1:19.2,2:19.6} # Penalty for late completion of j = 3 of drug i
		self.parameters['tau_ij'] = {(1,1):2,(1,2):4,(1,3):4,(2,1):2,(2,2):3,(2,3):5} # Duration of trial j for drug i
		self.parameters['revmax_i'] = {1:3100,2:3250}
		self.parameters['n_t'] = {1:0.025,2:0.025,3:0.025,4:0.025,5:0.025,6:0.025,7:0.025,8:0.025,9:0.025,10:0.025,11:0.025,12:0.025} # interest rate for a period
		self.parameters['c_ij'] = {(1,1):10,(1,2):90,(1,3):220,(2,1):10,(2,2):80,(2,3):200} # Cost of trial (i,j)
		self.parameters['rho_ijr'] = {(1,1,1):1,(1,1,2):1,(1,2,1):1,(1,2,2):2,(1,3,1):2,(1,3,2):3,
									(2,1,1):1,(2,1,2):1,(2,2,1):2,(2,2,2):1,(2,3,1):2,(2,3,2):3} # Resource requirements of trial (i,j) for resource type r
		self.parameters['rhomax_r'] = {1:2,2:3} # Availability of resource type r

		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['FP'] = ['F','P'] # Outcome of a trial
		
		##### Probability #####
		self.uncertain['phat_ij'] = {(1,1):0.3,(1,2):0.5,(1,3):0.8,(2,1):0.4,(2,2):0.6,(2,3):0.8}

class I3J3T12S64():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['I'] = [1,2,3] # drugs
		self.sets['J'] = [1,2,3] # Clinical trials
		self.sets['T'] = [1,2,3,4,5,6,7,8,9,10,11,12] # Time periods
		self.sets['R'] = [1,2] # Resource types
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD_i'] = {1:44,2:56,3:52} # Penalty for reduced active patent life
		self.parameters['gammaL_i'] = {1:19.2,2:19.6,3:20.0} # Penalty for late completion of j = 3 of drug i
		self.parameters['tau_ij'] = {(1,1):2,(1,2):4,(1,3):4,(2,1):2,(2,2):3,(2,3):5,(3,1):2,(3,2):3,(3,3):4} # Duration of trial j for drug i
		self.parameters['revmax_i'] = {1:3100,2:3250,3:3300}
		self.parameters['n_t'] = {1:0.025,2:0.025,3:0.025,4:0.025,5:0.025,6:0.025,7:0.025,8:0.025,9:0.025,10:0.025,11:0.025,12:0.025} # interest rate for a period
		self.parameters['c_ij'] = {(1,1):10,(1,2):90,(1,3):220,(2,1):10,(2,2):80,(2,3):200,(3,1):10,(3,2):90,(3,3):180} # Cost of trial (i,j)
		self.parameters['rho_ijr'] = {(1,1,1):1,(1,1,2):1,(1,2,1):1,(1,2,2):2,(1,3,1):2,(1,3,2):3,
									(2,1,1):1,(2,1,2):1,(2,2,1):2,(2,2,2):1,(2,3,1):2,(2,3,2):3,
									(3,1,1):1,(3,1,2):1,(3,2,1):1,(3,2,2):1,(3,3,1):2,(3,3,2):3} # Resource requirements of trial (i,j) for resource type r
		self.parameters['rhomax_r'] = {1:2,2:3} # Availability of resource type r

		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['FP'] = ['F','P'] # Outcome of a trial
		
		##### Probability #####
		self.uncertain['phat_ij'] = {(1,1):0.3,(1,2):0.5,(1,3):0.8,(2,1):0.4,(2,2):0.6,(2,3):0.8,(3,1):0.3,(3,2):0.6,(3,3):0.9}

class I4J3T6S256():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['I'] = [1,2,3,4] # drugs
		self.sets['J'] = [1,2,3] # Clinical trials
		self.sets['T'] = [1,2,3,4,5,6] # Time periods
		self.sets['R'] = [1,2] # Resource types
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD_i'] = {1:22,2:28,3:26,4:24} # Penalty for reduced active patent life
		self.parameters['gammaL_i'] = {1:19.2,2:19.6,3:20.0,4:19.4} # Penalty for late completion of j = 3 of drug i
		self.parameters['tau_ij'] = {(1,1):1,(1,2):1,(1,3):3,(2,1):1,(2,2):2,(2,3):2,(3,1):1,(3,2):1,(3,3):3,(4,1):1,(4,2):2,(4,3):2} # Duration of trial j for drug i
		self.parameters['revmax_i'] = {1:3100,2:3250,3:3300,4:3000}
		self.parameters['n_t'] = {1:0.025,2:0.025,3:0.025,4:0.025,5:0.025,6:0.025} # interest rate for a period
		self.parameters['c_ij'] = {(1,1):10,(1,2):90,(1,3):220,(2,1):10,(2,2):80,(2,3):200,(3,1):10,(3,2):90,(3,3):180,(4,1):10,(4,2):100,(4,3):170} # Cost of trial (i,j)
		self.parameters['rho_ijr'] = {(1,1,1):1,(1,1,2):1,(1,2,1):1,(1,2,2):2,(1,3,1):2,(1,3,2):3,
									(2,1,1):1,(2,1,2):1,(2,2,1):2,(2,2,2):1,(2,3,1):2,(2,3,2):3,
									(3,1,1):1,(3,1,2):1,(3,2,1):1,(3,2,2):1,(3,3,1):2,(3,3,2):3,
									(4,1,1):1,(4,1,2):1,(4,2,1):1,(4,2,2):2,(4,3,1):2,(4,3,2):3} # Resource requirements of trial (i,j) for resource type r
		self.parameters['rhomax_r'] = {1:4,2:3} # Availability of resource type r

		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['FP'] = ['F','P'] # Outcome of a trial
		
		##### Probability #####
		self.uncertain['phat_ij'] = {(1,1):0.3,(1,2):0.5,(1,3):0.8,(2,1):0.4,(2,2):0.6,(2,3):0.8,(3,1):0.3,(3,2):0.6,(3,3):0.9,(4,1):0.4,(4,2):0.6,(4,3):0.8}

class I4J3T12S256():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['I'] = [1,2,3,4] # drugs
		self.sets['J'] = [1,2,3] # Clinical trials
		self.sets['T'] = [1,2,3,4,5,6,7,8,9,10,11,12] # Time periods
		self.sets['R'] = [1,2] # Resource types
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD_i'] = {1:22,2:28,3:26,4:24} # Penalty for reduced active patent life
		self.parameters['gammaL_i'] = {1:19.2,2:19.6,3:20.0,4:19.4} # Penalty for late completion of j = 3 of drug i
		self.parameters['tau_ij'] = {(1,1):1,(1,2):1,(1,3):3,(2,1):1,(2,2):2,(2,3):2,(3,1):1,(3,2):1,(3,3):3,(4,1):1,(4,2):2,(4,3):2} # Duration of trial j for drug i
		self.parameters['revmax_i'] = {1:3100,2:3250,3:3300,4:3000}
		self.parameters['n_t'] = {1:0.025,2:0.025,3:0.025,4:0.025,5:0.025,6:0.025,7:0.025,8:0.025,9:0.025,10:0.025,11:0.025,12:0.025} # interest rate for a period
		self.parameters['c_ij'] = {(1,1):10,(1,2):90,(1,3):220,(2,1):10,(2,2):80,(2,3):200,(3,1):10,(3,2):90,(3,3):180,(4,1):10,(4,2):100,(4,3):170} # Cost of trial (i,j)
		self.parameters['rho_ijr'] = {(1,1,1):1,(1,1,2):1,(1,2,1):1,(1,2,2):2,(1,3,1):2,(1,3,2):3,
									(2,1,1):1,(2,1,2):1,(2,2,1):2,(2,2,2):1,(2,3,1):2,(2,3,2):3,
									(3,1,1):1,(3,1,2):1,(3,2,1):1,(3,2,2):1,(3,3,1):2,(3,3,2):3,
									(4,1,1):1,(4,1,2):1,(4,2,1):1,(4,2,2):2,(4,3,1):2,(4,3,2):3} # Resource requirements of trial (i,j) for resource type r
		self.parameters['rhomax_r'] = {1:4,2:3} # Availability of resource type r

		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['FP'] = ['F','P'] # Outcome of a trial
		
		##### Probability #####
		self.uncertain['phat_ij'] = {(1,1):0.3,(1,2):0.5,(1,3):0.8,(2,1):0.4,(2,2):0.6,(2,3):0.8,(3,1):0.3,(3,2):0.6,(3,3):0.9,(4,1):0.4,(4,2):0.6,(4,3):0.8}

class I5J3T6S1024():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['I'] = [1,2,3,4,5] # drugs
		self.sets['J'] = [1,2,3] # Clinical trials
		self.sets['T'] = [1,2,3,4,5,6] # Time periods
		self.sets['R'] = [1,2] # Resource types
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD_i'] = {1:22,2:28,3:26,4:24,5:24} # Penalty for reduced active patent life
		self.parameters['gammaL_i'] = {1:19.2,2:19.6,3:20.0,4:19.4,5:19.6} # Penalty for late completion of j = 3 of drug i
		self.parameters['tau_ij'] = {(1,1):1,(1,2):1,(1,3):3,(2,1):1,(2,2):2,(2,3):2,(3,1):1,(3,2):1,(3,3):3,(4,1):1,(4,2):2,(4,3):2,(5,1):1,(5,2):2,(5,3):3} # Duration of trial j for drug i
		self.parameters['revmax_i'] = {1:3100,2:3250,3:3300,4:3000,5:3150}
		self.parameters['n_t'] = {1:0.025,2:0.025,3:0.025,4:0.025,5:0.025,6:0.025} # interest rate for a period
		self.parameters['c_ij'] = {(1,1):10,(1,2):90,(1,3):220,(2,1):10,(2,2):80,(2,3):200,(3,1):10,(3,2):90,(3,3):180,(4,1):10,(4,2):100,(4,3):170,(5,1):10,(5,2):70,(5,3):210} # Cost of trial (i,j)
		self.parameters['rho_ijr'] = {(1,1,1):1,(1,1,2):1,(1,2,1):1,(1,2,2):2,(1,3,1):2,(1,3,2):3,
									(2,1,1):1,(2,1,2):1,(2,2,1):2,(2,2,2):1,(2,3,1):2,(2,3,2):3,
									(3,1,1):1,(3,1,2):1,(3,2,1):1,(3,2,2):1,(3,3,1):2,(3,3,2):3,
									(4,1,1):1,(4,1,2):1,(4,2,1):1,(4,2,2):2,(4,3,1):2,(4,3,2):3,
									(5,1,1):1,(5,1,2):1,(5,2,1):1,(5,2,2):1,(5,3,1):2,(5,3,2):3} # Resource requirements of trial (i,j) for resource type r
		self.parameters['rhomax_r'] = {1:4,2:3} # Availability of resource type r

		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['FP'] = ['F','P'] # Outcome of a trial
		
		##### Probability #####
		self.uncertain['phat_ij'] = {(1,1):0.3,(1,2):0.5,(1,3):0.8,(2,1):0.4,(2,2):0.6,(2,3):0.8,(3,1):0.3,(3,2):0.6,(3,3):0.9,(4,1):0.4,(4,2):0.6,(4,3):0.8,(5,1):0.35,(5,2):0.50,(5,3):0.90}

class I5J3T12S1024():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['I'] = [1,2,3,4,5] # drugs
		self.sets['J'] = [1,2,3] # Clinical trials
		self.sets['T'] = [1,2,3,4,5,6,7,8,9,10,11,12] # Time periods
		self.sets['R'] = [1,2] # Resource types
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD_i'] = {1:22,2:28,3:26,4:24,5:24} # Penalty for reduced active patent life
		self.parameters['gammaL_i'] = {1:19.2,2:19.6,3:20.0,4:19.4,5:19.6} # Penalty for late completion of j = 3 of drug i
		self.parameters['tau_ij'] = {(1,1):1,(1,2):1,(1,3):3,(2,1):1,(2,2):2,(2,3):2,(3,1):1,(3,2):1,(3,3):3,(4,1):1,(4,2):2,(4,3):2,(5,1):1,(5,2):2,(5,3):3} # Duration of trial j for drug i
		self.parameters['revmax_i'] = {1:3100,2:3250,3:3300,4:3000,5:3150}
		self.parameters['n_t'] = {1:0.025,2:0.025,3:0.025,4:0.025,5:0.025,6:0.025,7:0.025,8:0.025,9:0.025,10:0.025,11:0.025,12:0.025} # interest rate for a period
		self.parameters['c_ij'] = {(1,1):10,(1,2):90,(1,3):220,(2,1):10,(2,2):80,(2,3):200,(3,1):10,(3,2):90,(3,3):180,(4,1):10,(4,2):100,(4,3):170,(5,1):10,(5,2):70,(5,3):210} # Cost of trial (i,j)
		self.parameters['rho_ijr'] = {(1,1,1):1,(1,1,2):1,(1,2,1):1,(1,2,2):2,(1,3,1):2,(1,3,2):3,
									(2,1,1):1,(2,1,2):1,(2,2,1):2,(2,2,2):1,(2,3,1):2,(2,3,2):3,
									(3,1,1):1,(3,1,2):1,(3,2,1):1,(3,2,2):1,(3,3,1):2,(3,3,2):3,
									(4,1,1):1,(4,1,2):1,(4,2,1):1,(4,2,2):2,(4,3,1):2,(4,3,2):3,
									(5,1,1):1,(5,1,2):1,(5,2,1):1,(5,2,2):1,(5,3,1):2,(5,3,2):3} # Resource requirements of trial (i,j) for resource type r
		self.parameters['rhomax_r'] = {1:4,2:3} # Availability of resource type r

		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['FP'] = ['F','P'] # Outcome of a trial
		
		##### Probability #####
		self.uncertain['phat_ij'] = {(1,1):0.3,(1,2):0.5,(1,3):0.8,(2,1):0.4,(2,2):0.6,(2,3):0.8,(3,1):0.3,(3,2):0.6,(3,3):0.9,(4,1):0.4,(4,2):0.6,(4,3):0.8,(5,1):0.35,(5,2):0.50,(5,3):0.90}
