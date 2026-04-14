class T10S4(): # 4 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [1,2,3] # Processes
		self.sets['IU'] = [1,2] # Processes with uncertain yield in the process network
		self.sets['K'] = [1,2,3,4,5,6,7,8,9,10] # Streams, 9, 10 are a vent for complete recourse
		self.sets['K126'] = [1,2,6]
		self.sets['K910'] = [9,10] # vents for complete recourse
		self.sets['STEP'] = [1,2,3] # Steps
		self.sets['Tend'] = 10 # End of time horizon

		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['FE'] = {1:1.5, 2:1.5, 3:1.5} # Fixed expansion cost for process i 
		self.parameters['VE'] = {1:0.3, 2:0.3, 3:0.3} # Variable expansion cost for process i
		self.parameters['FO'] = {1:0.2, 2:0.2, 3:0.2} # Fixed operating cost for process i
		self.parameters['VO']= {1:0.1, 2:0.1, 3:0, 4:0, 5:0, 6:0.4, 7:0, 8:0, 9:0, 10:0} # Variable operating cost for stream k, 9, 10 are a vent for complete recourse
		self.parameters['FIPP'] = {1:0.1, 2:0.1, 3:10000} # Fixed investment cost for pilot plant for process i
		self.parameters['FOPP'] = {1:0, 2:0, 3:2000} # Fixed operating cost for pilot plant for process i
		self.parameters['delta'] = 1 # Duration of time period t
		self.parameters['alpha'] = 1 # purchase price for final product
		self.parameters['beta'] = 0.6 # sales price for final product
		self.parameters['gamma'] = 0.1 # inventory cost for final product
		self.parameters['Big_M'] = 10000
		self.parameters['CARD'] =  1 # The number of sum of expansion and pilot allowed at t = 1
		self.parameters['theta'] = {3:0.7} # Yield of deterministic process
		self.parameters['d'] = {1:1, 2:2, 3:4, 4:8, 5:8, 6:6, 7:6, 8:6, 9:8, 10:8} # Demand for final product in t
		self.parameters['Wcap_inital'] = {1:0, 2:0, 3:3} # Initial capacity of process i
		self.parameters['UQE'] = {1:10, 2:10, 3:10} # Max limit of capacity expansion of process i, {1:10, 2:10, 3:10}
		self.parameters['LQE'] = {1:1, 2:1, 3:1} # Min limit of capacity expansion of process i
		self.parameters['Uoutflow'] = {1:10000, 2:10000, 3:10000} # Max limit of outflow of process i
		self.parameters['Loutflow'] = {1:0, 2:0, 3:0} # Min limit of outflow of process i
		
		##### Uncertain	parameters #####
		self.uncertain = {}
		self.uncertain['p_s'] = {}

class T10S16(): # Example1, 16 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [1,2,3] # Processes
		self.sets['IU'] = [1,2] # Processes with uncertain yield in the process network
		self.sets['K'] = [1,2,3,4,5,6,7,8,9,10] # Streams, 9, 10 are a vent for complete recourse
		self.sets['K126'] = [1,2,6]
		self.sets['K910'] = [9,10] # vents for complete recourse
		self.sets['STEP'] = [1,2,3] # Steps
		self.sets['Tend'] = 10 # End of time horizon

		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['FE'] = {1:1.5, 2:1.5, 3:1.5} # Fixed expansion cost for process i 
		self.parameters['VE'] = {1:0.3, 2:0.3, 3:0.3} # Variable expansion cost for process i
		self.parameters['FO'] = {1:0.2, 2:0.2, 3:0.2} # Fixed operating cost for process i
		self.parameters['VO']= {1:0.1, 2:0.1, 3:0, 4:0, 5:0, 6:0.4, 7:0, 8:0, 9:0, 10:0} # Variable operating cost for stream k, 9, 10 are a vent for complete recourse
		self.parameters['FIPP'] = {1:0.1, 2:0.1, 3:10000} # Fixed investment cost for pilot plant for process i
		self.parameters['FOPP'] = {1:0, 2:0, 3:2000} # Fixed operating cost for pilot plant for process i
		self.parameters['delta'] = 1 # Duration of time period t
		self.parameters['alpha'] = 1 # purchase price for final product
		self.parameters['beta'] = 0.6 # sales price for final product
		self.parameters['gamma'] = 0.1 # inventory cost for final product
		self.parameters['Big_M'] = 10000
		self.parameters['CARD'] =  1 # The number of sum of expansion and pilot allowed at t = 1
		self.parameters['theta'] = {3:0.7} # Yield of deterministic process
		self.parameters['d'] = {1:1, 2:2, 3:4, 4:8, 5:8, 6:6, 7:6, 8:6, 9:8, 10:8} # Demand for final product in t
		self.parameters['Wcap_inital'] = {1:0, 2:0, 3:3} # Initial capacity of process i
		self.parameters['UQE'] = {1:10, 2:10, 3:10} # Max limit of capacity expansion of process i, {1:10, 2:10, 3:10}
		self.parameters['LQE'] = {1:1, 2:1, 3:1} # Min limit of capacity expansion of process i
		self.parameters['Uoutflow'] = {1:10000, 2:10000, 3:10000} # Max limit of outflow of process i
		self.parameters['Loutflow'] = {1:0, 2:0, 3:0} # Min limit of outflow of process i
		
		##### Uncertain	parameters #####
		self.uncertain = {}
		self.uncertain['p_s'] = {}

