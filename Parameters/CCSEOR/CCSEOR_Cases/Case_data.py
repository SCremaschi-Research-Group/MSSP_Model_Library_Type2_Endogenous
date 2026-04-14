class I6R6T30S2(): # 6 reservoirs, 30 time periods, 6 time segments, 2 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [1,2,3,4,5,6] # Depleted oil reservoirs i
		self.sets['L'] = [1] # Different types l of pipes for primary pipelines
		self.sets['K'] = [1] # Different types k of pipes for secondary pipelines
		self.sets['T'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30] # Time periods t
		self.sets['R'] = [1,2,3,4,5,6] # Planning segments r of the time horizon T
		self.sets['R_i'] = {1:[2],2:[1,2,3],3:[2,3],4:[1,2,3],5:[1,2,3],6:[1,2,3]} # The planning segments r in which secondary pipelines can be established for reservoir i at the beginning
		
		# ##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['Fmax_t'] = {1:15,2:15,3:15,4:15,5:15,6:15,7:15,8:15,9:15,10:15,
									11:25,12:25,13:25,14:25,15:25,16:25,17:25,18:25,19:25,20:25,
									21:25,22:25,23:25,24:25,25:25,26:25,27:25,28:25,29:25,30:25} # Maximum CO2 flow (Mt) that can be supplied by the CO2 source
		self.parameters['d'] = 150 # The length (km) of primary pipeline that connects the CO2 common source to the branching point
		self.parameters['dp_i'] = {1:50, 2:30, 3:70, 4:100, 5:45, 6:60} # The length (km) of secondary pipeline from the branching point to reservoir i
		self.parameters['umin_l'] = {1:0} # The minimum flow (Mt) that can be transferred through the primary pipeline l
		self.parameters['umax_l'] = {1:25} # The maximum flow (Mt) that can be transferred through the primary pipeline l
		self.parameters['wmin_k'] = {1:1} # The minimum flow (Mt) that can be transferred through the secondary pipeline k
		self.parameters['wmax_k'] = {1:10} # The maximum flow (Mt) that can be transferred through the secondary pipeline k
		self.parameters['g_l'] = {1:95} # The fixed costs (M$) of a primary pipeline l
		self.parameters['gp_ik'] = {(1,1):95, (2,1):95, (3,1):95, (4,1):95, (5,1):95, (6,1):95} # The fixed costs (M$) of a secondary pipeline k to a reservoir i
		self.parameters['h_l'] = {1:0.25} # The variable costs (M$/(Mt*km)) to transfer CO2 through a primary pipeline l
		self.parameters['hp_ik'] = {(1,1):0.25, (2,1):0.25, (3,1):0.25, (4,1):0.25, (5,1):0.25, (6,1):0.25} # The variable costs (M$/(Mt*km)) to transfer CO2 through a secondary pipeline k to a reservoir i
		self.parameters['e_i'] = {1:20, 2:15, 3:15, 4:10, 5:10, 6:15} # The operation of reservoir i lasts e_i periods
		self.parameters['fmin_i'] = {1:1, 2:1, 3:1, 4:1, 5:1, 6:1} # The lower bound, an economically affordable minimum level, of the CO2 amount injected into i
		self.parameters['fmax_i'] = {1:5, 2:7, 3:8, 4:10, 5:9, 6:7} # The upper bound, the injection capacity of reservoir i, of the CO2 amount injected into i
		self.parameters['alpha_i'] = {1:0.5, 2:0.9, 3:0.95, 4:0.85, 5:0.8, 6:0.75} # The portion of the total injected CO2 in reservoir i that is sequestered in it (unit-less)
		self.parameters['c_i'] = {1:100, 2:150, 3:75, 4:200, 5:200, 6:150} # The total capacity of reservoir i (Mt)
		self.parameters['v_i'] = {1:80, 2:80, 3:80, 4:80, 5:80, 6:80} # The value of oil recovered from reservoir i (M$/Mbbls)
		self.parameters['b'] = 15 # The credit of CO2 sequestered in reservoirs (M$/Mt)
		rho = 0.1 # Interest rate
		self.parameters['beta_t'] = {}
		for t in self.sets['T']:
			self.parameters['beta_t'][t] = (1 + rho)**(-t) # The coefficient used in calculating the NPV ≠ Discount Factor

		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['thetamax_m'] = {1:{1:(5.35,0.82),2:(3.75,0.94)}, 2:{1:(1.6,0.855)}, 3:{1:(0.9,0.94)}, 
										4:{1:(4.375,0.91)}, 5:{1:(3,0.93)}, 6:{1:(1.4,0.92)}} # i:{SrNo:(thetamax_i,m_i)}, 5,6 are deterministic
		
		##### Probability #####
		self.prob = {}
		self.uncertain['thetamax_m_prob'] = {1:{1:0.5,2:0.5}, 2:{1:1}, 3:{1:1}, 4:{1:1}, 5:{1:1}, 6:{1:1}} # i:{SrNo:probability} (equal probability)

class I6R6T30S4(): # 6 reservoirs, 30 time periods, 6 time segments, 4 scenarios, Case2SM4
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [1,2,3,4,5,6] # Depleted oil reservoirs i
		self.sets['L'] = [1] # Different types l of pipes for primary pipelines
		self.sets['K'] = [1] # Different types k of pipes for secondary pipelines
		self.sets['T'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30] # Time periods t
		self.sets['R'] = [1,2,3,4,5,6] # Planning segments r of the time horizon T
		self.sets['R_i'] = {1:[2],2:[1,2,3],3:[2,3],4:[1,2,3],5:[1,2,3],6:[1,2,3]} # The planning segments r in which secondary pipelines can be established for reservoir i at the beginning
		
		# ##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['Fmax_t'] = {1:15,2:15,3:15,4:15,5:15,6:15,7:15,8:15,9:15,10:15,
									11:25,12:25,13:25,14:25,15:25,16:25,17:25,18:25,19:25,20:25,
									21:25,22:25,23:25,24:25,25:25,26:25,27:25,28:25,29:25,30:25} # Maximum CO2 flow (Mt) that can be supplied by the CO2 source
		self.parameters['d'] = 150 # The length (km) of primary pipeline that connects the CO2 common source to the branching point
		self.parameters['dp_i'] = {1:50, 2:30, 3:70, 4:100, 5:45, 6:60} # The length (km) of secondary pipeline from the branching point to reservoir i
		self.parameters['umin_l'] = {1:0} # The minimum flow (Mt) that can be transferred through the primary pipeline l
		self.parameters['umax_l'] = {1:25} # The maximum flow (Mt) that can be transferred through the primary pipeline l
		self.parameters['wmin_k'] = {1:1} # The minimum flow (Mt) that can be transferred through the secondary pipeline k
		self.parameters['wmax_k'] = {1:10} # The maximum flow (Mt) that can be transferred through the secondary pipeline k
		self.parameters['g_l'] = {1:95} # The fixed costs (M$) of a primary pipeline l
		self.parameters['gp_ik'] = {(1,1):95, (2,1):95, (3,1):95, (4,1):95, (5,1):95, (6,1):95} # The fixed costs (M$) of a secondary pipeline k to a reservoir i
		self.parameters['h_l'] = {1:0.25} # The variable costs (M$/(Mt*km)) to transfer CO2 through a primary pipeline l
		self.parameters['hp_ik'] = {(1,1):0.25, (2,1):0.25, (3,1):0.25, (4,1):0.25, (5,1):0.25, (6,1):0.25} # The variable costs (M$/(Mt*km)) to transfer CO2 through a secondary pipeline k to a reservoir i
		self.parameters['e_i'] = {1:20, 2:15, 3:15, 4:10, 5:10, 6:15} # The operation of reservoir i lasts e_i periods
		self.parameters['fmin_i'] = {1:1, 2:1, 3:1, 4:1, 5:1, 6:1} # The lower bound, an economically affordable minimum level, of the CO2 amount injected into i
		self.parameters['fmax_i'] = {1:5, 2:7, 3:8, 4:10, 5:9, 6:7} # The upper bound, the injection capacity of reservoir i, of the CO2 amount injected into i
		self.parameters['alpha_i'] = {1:0.5, 2:0.9, 3:0.95, 4:0.85, 5:0.8, 6:0.75} # The portion of the total injected CO2 in reservoir i that is sequestered in it (unit-less)
		self.parameters['c_i'] = {1:100, 2:150, 3:75, 4:200, 5:200, 6:150} # The total capacity of reservoir i (Mt)
		self.parameters['v_i'] = {1:80, 2:80, 3:80, 4:80, 5:80, 6:80} # The value of oil recovered from reservoir i (M$/Mbbls)
		self.parameters['b'] = 15 # The credit of CO2 sequestered in reservoirs (M$/Mt)
		rho = 0.1 # Interest rate
		self.parameters['beta_t'] = {}
		for t in self.sets['T']:
			self.parameters['beta_t'][t] = (1 + rho)**(-t) # The coefficient used in calculating the NPV ≠ Discount Factor

		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['thetamax_m'] = {1:{1:(5.35,0.82),2:(3.75,0.94)}, 2:{1:(0.75,0.75),2:(2.45,0.96)}, 3:{1:(0.9,0.94)}, 
										4:{1:(4.375,0.91)}, 5:{1:(3,0.93)}, 6:{1:(1.4,0.92)}} # i:{SrNo:(thetamax_i,m_i)}, 3,4,5,6 are deterministic
		
		##### Probability #####
		self.prob = {}
		self.uncertain['thetamax_m_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:1}, 4:{1:1}, 5:{1:1}, 6:{1:1}} # i:{SrNo:probability} (equal probability)

class I6R6T30S8(): # 6 reservoirs, 30 time periods, 6 time segments, 8 scenarios, Case2SM8
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [1,2,3,4,5,6] # Depleted oil reservoirs i
		self.sets['L'] = [1] # Different types l of pipes for primary pipelines
		self.sets['K'] = [1] # Different types k of pipes for secondary pipelines
		self.sets['T'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30] # Time periods t
		self.sets['R'] = [1,2,3,4,5,6] # Planning segments r of the time horizon T
		self.sets['R_i'] = {1:[2],2:[1,2,3],3:[2,3],4:[1,2,3],5:[1,2,3],6:[1,2,3]} # The planning segments r in which secondary pipelines can be established for reservoir i at the beginning
		# 1:[2]
		# ##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['Fmax_t'] = {1:15,2:15,3:15,4:15,5:15,6:15,7:15,8:15,9:15,10:15,
									11:25,12:25,13:25,14:25,15:25,16:25,17:25,18:25,19:25,20:25,
									21:25,22:25,23:25,24:25,25:25,26:25,27:25,28:25,29:25,30:25} # Maximum CO2 flow (Mt) that can be supplied by the CO2 source
		self.parameters['d'] = 150 # The length (km) of primary pipeline that connects the CO2 common source to the branching point
		self.parameters['dp_i'] = {1:50, 2:30, 3:70, 4:100, 5:45, 6:60} # The length (km) of secondary pipeline from the branching point to reservoir i
		self.parameters['umin_l'] = {1:0} # The minimum flow (Mt) that can be transferred through the primary pipeline l
		self.parameters['umax_l'] = {1:25} # The maximum flow (Mt) that can be transferred through the primary pipeline l
		self.parameters['wmin_k'] = {1:1} # The minimum flow (Mt) that can be transferred through the secondary pipeline k
		self.parameters['wmax_k'] = {1:10} # The maximum flow (Mt) that can be transferred through the secondary pipeline k
		self.parameters['g_l'] = {1:95} # The fixed costs (M$) of a primary pipeline l
		self.parameters['gp_ik'] = {(1,1):95, (2,1):95, (3,1):95, (4,1):95, (5,1):95, (6,1):95} # The fixed costs (M$) of a secondary pipeline k to a reservoir i
		self.parameters['h_l'] = {1:0.25} # The variable costs (M$/(Mt*km)) to transfer CO2 through a primary pipeline l
		self.parameters['hp_ik'] = {(1,1):0.25, (2,1):0.25, (3,1):0.25, (4,1):0.25, (5,1):0.25, (6,1):0.25} # The variable costs (M$/(Mt*km)) to transfer CO2 through a secondary pipeline k to a reservoir i
		self.parameters['e_i'] = {1:20, 2:15, 3:15, 4:10, 5:10, 6:15} # The operation of reservoir i lasts e_i periods
		self.parameters['fmin_i'] = {1:1, 2:1, 3:1, 4:1, 5:1, 6:1} # The lower bound, an economically affordable minimum level, of the CO2 amount injected into i
		self.parameters['fmax_i'] = {1:5, 2:7, 3:8, 4:10, 5:9, 6:7} # The upper bound, the injection capacity of reservoir i, of the CO2 amount injected into i
		self.parameters['alpha_i'] = {1:0.5, 2:0.9, 3:0.95, 4:0.85, 5:0.8, 6:0.75} # The portion of the total injected CO2 in reservoir i that is sequestered in it (unit-less)
		self.parameters['c_i'] = {1:100, 2:150, 3:75, 4:200, 5:200, 6:150} # The total capacity of reservoir i (Mt)
		self.parameters['v_i'] = {1:80, 2:80, 3:80, 4:80, 5:80, 6:80} # The value of oil recovered from reservoir i (M$/Mbbls)
		self.parameters['b'] = 15 # The credit of CO2 sequestered in reservoirs (M$/Mt)
		rho = 0.1 # Interest rate
		self.parameters['beta_t'] = {}
		for t in self.sets['T']:
			self.parameters['beta_t'][t] = (1 + rho)**(-t) # The coefficient used in calculating the NPV ≠ Discount Factor

		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['thetamax_m'] = {1:{1:(5.35,0.82),2:(3.75,0.94)}, 2:{1:(0.75,0.75),2:(2.45,0.96)}, 3:{1:(0.45,0.91),2:(1.35,0.97)}, 
										4:{1:(4.375,0.91)}, 5:{1:(3,0.93)}, 6:{1:(1.4,0.92)}} # i:{SrNo:(thetamax_i,m_i)}, 5,6 are deterministic
		
		##### Probability #####
		self.prob = {}
		self.uncertain['thetamax_m_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:0.5,2:0.5}, 4:{1:1}, 5:{1:1}, 6:{1:1}} # i:{SrNo:probability} (equal probability)

class I6R6T30S12(): # 6 reservoirs, 30 time periods, 6 time segments, 12 scenarios, Case2SM12
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [1,2,3,4,5,6] # Depleted oil reservoirs i
		self.sets['L'] = [1] # Different types l of pipes for primary pipelines
		self.sets['K'] = [1] # Different types k of pipes for secondary pipelines
		self.sets['T'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30] # Time periods t
		self.sets['R'] = [1,2,3,4,5,6] # Planning segments r of the time horizon T
		self.sets['R_i'] = {1:[2],2:[1,2,3],3:[2,3],4:[1,2,3],5:[1,2,3],6:[1,2,3]} # The planning segments r in which secondary pipelines can be established for reservoir i at the beginning
		
		# ##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['Fmax_t'] = {1:15,2:15,3:15,4:15,5:15,6:15,7:15,8:15,9:15,10:15,
									11:25,12:25,13:25,14:25,15:25,16:25,17:25,18:25,19:25,20:25,
									21:25,22:25,23:25,24:25,25:25,26:25,27:25,28:25,29:25,30:25} # Maximum CO2 flow (Mt) that can be supplied by the CO2 source
		self.parameters['d'] = 150 # The length (km) of primary pipeline that connects the CO2 common source to the branching point
		self.parameters['dp_i'] = {1:50, 2:30, 3:70, 4:100, 5:45, 6:60} # The length (km) of secondary pipeline from the branching point to reservoir i
		self.parameters['umin_l'] = {1:0} # The minimum flow (Mt) that can be transferred through the primary pipeline l
		self.parameters['umax_l'] = {1:25} # The maximum flow (Mt) that can be transferred through the primary pipeline l
		self.parameters['wmin_k'] = {1:1} # The minimum flow (Mt) that can be transferred through the secondary pipeline k
		self.parameters['wmax_k'] = {1:10} # The maximum flow (Mt) that can be transferred through the secondary pipeline k
		self.parameters['g_l'] = {1:95} # The fixed costs (M$) of a primary pipeline l
		self.parameters['gp_ik'] = {(1,1):95, (2,1):95, (3,1):95, (4,1):95, (5,1):95, (6,1):95} # The fixed costs (M$) of a secondary pipeline k to a reservoir i
		self.parameters['h_l'] = {1:0.25} # The variable costs (M$/(Mt*km)) to transfer CO2 through a primary pipeline l
		self.parameters['hp_ik'] = {(1,1):0.25, (2,1):0.25, (3,1):0.25, (4,1):0.25, (5,1):0.25, (6,1):0.25} # The variable costs (M$/(Mt*km)) to transfer CO2 through a secondary pipeline k to a reservoir i
		self.parameters['e_i'] = {1:20, 2:15, 3:15, 4:10, 5:10, 6:15} # The operation of reservoir i lasts e_i periods
		self.parameters['fmin_i'] = {1:1, 2:1, 3:1, 4:1, 5:1, 6:1} # The lower bound, an economically affordable minimum level, of the CO2 amount injected into i
		self.parameters['fmax_i'] = {1:5, 2:7, 3:8, 4:10, 5:9, 6:7} # The upper bound, the injection capacity of reservoir i, of the CO2 amount injected into i
		self.parameters['alpha_i'] = {1:0.5, 2:0.9, 3:0.95, 4:0.85, 5:0.8, 6:0.75} # The portion of the total injected CO2 in reservoir i that is sequestered in it (unit-less)
		self.parameters['c_i'] = {1:100, 2:150, 3:75, 4:200, 5:200, 6:150} # The total capacity of reservoir i (Mt)
		self.parameters['v_i'] = {1:80, 2:80, 3:80, 4:80, 5:80, 6:80} # The value of oil recovered from reservoir i (M$/Mbbls)
		self.parameters['b'] = 15 # The credit of CO2 sequestered in reservoirs (M$/Mt)
		rho = 0.1 # Interest rate
		self.parameters['beta_t'] = {}
		for t in self.sets['T']:
			self.parameters['beta_t'][t] = (1 + rho)**(-t) # The coefficient used in calculating the NPV ≠ Discount Factor

		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['thetamax_m'] = {1:{1:(5.35,0.82),2:(4.55,0.88),3:(3.75,0.94)} , 2:{1:(0.75,0.75),2:(2.45,0.96)}, 3:{1:(0.9,0.94)}, 
										4:{1:(2.5,0.84),2:(6.25,0.98)}, 5:{1:(3,0.93)}, 6:{1:(1.4,0.92)}} # i:{SrNo:(thetamax_i,m_i)}, 5,6 are deterministic
		
		##### Probability #####
		self.prob = {}
		self.uncertain['thetamax_m_prob'] = {1:{1:1/3,2:1/3,3:1/3}, 2:{1:0.5,2:0.5}, 3:{1:1}, 4:{1:0.5,2:0.5}, 5:{1:1}, 6:{1:1}} # i:{SrNo:probability} (equal probability)
