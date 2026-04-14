class I2T5S16():
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['Tend'] = 5
		self.sets['I'] = [1,2]
		
		##### Parameters #####
		self.parameters = {}
		self.parameters['B'] = {1:2, 2:2, 3:2, 4:2, 5:2}
		# self.parameters['B'] = {1:3, 2:3, 3:3, 4:3, 5:3} # AEEV gets infeasible if budget is 3
		self.parameters['delta_i'] = {1:5, 2:2} # implementation time
		self.parameters['f'] = {1:0.2, 2:0.1} # fixed activity cost
		self.parameters['r'] =  0.05 # discount factor
		self.parameters['D_i'] =  {1:[2],2:[2]} # Dependant, valid when j>i
		self.parameters['theta_theta'] =  {1:1, 2:1.5} # threshold investment for certain resource requirement theta
		self.parameters['theta_Z'] = {1:1.5, 2:2.5} # threshold investment for initial performance assessment Z^
		self.parameters['Ztilda'] =  {1:{'minmin':0,'minmax':0,'maxmax':0},2:{'minmin':0,'minmax':0.5,'maxmax':1}} # 2:{'minmin':-0.5,'minmax':-1.5,'maxmax':-3}}# 
		self.parameters['Big_M'] =  10000 # Additional parameter
		
		##### Uncertainty Information #####
		self.Uncertain = {}
		self.Uncertain['theta'] = {1:{'min':2,'max':4}, 2:{'min':3,'max':5}}
		self.Uncertain['Zhat'] = {1:{'min':1.5,'max':4.5}, 2:{'min':1,'max':3.5}}
		
		self.Uncertain['theta_prob'] = {1:{'min':0.35,'max':0.65}, 2:{'min':0.3,'max':0.7}}
		# self.Uncertain['Zhat_prob'] = {1:{'min':0.6,'max':0.4}, 2:{'min':0.4,'max':0.6}}
		self.Uncertain['Z_prob'] = {1:{'min':0.6*0.8+0.4*0.3,'max':0.6*0.2+0.4*0.7}, 2:{'min':0.4*0.8+0.6*0.3,'max':0.4*0.2+0.6*0.7}}
		# self.Uncertain['Z_prob'] = {1:{'min':0.6,'max':0.4}, 2:{'min':0.4,'max':0.6}} # Before correction

class I2T10S16():
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['Tend'] = 10
		self.sets['I'] = [1,2]
		
		##### Parameters #####
		self.parameters = {}
		self.parameters['B'] = {1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2, 8:2, 9:2, 10:2}
		self.parameters['delta_i'] = {1:5, 2:2} # implementation time
		self.parameters['f'] = {1:0.2, 2:0.1} # fixed activity cost
		self.parameters['r'] =  0.05 # discount factor
		self.parameters['D_i'] =  {1:[2],2:[2]} # Dependant, valid when j>i
		self.parameters['theta_theta'] = {1:1, 2:1.5} # threshold investment for certain resource requirement theta
		self.parameters['theta_Z'] = {1:1.5, 2:2.5} # threshold investment for initial performance assessment Z^
		self.parameters['Ztilda'] =  {1:{'minmin':0,'minmax':0,'maxmax':0}, 2:{'minmin':0,'minmax':0.5,'maxmax':1}}
		self.parameters['Big_M'] =  10000 # Additional parameter
		
		##### Uncertainty Information #####
		self.Uncertain = {}
		self.Uncertain['theta'] = {1:{'min':2,'max':4}, 2:{'min':3,'max':5}}
		self.Uncertain['Zhat'] = {1:{'min':1.5,'max':4.5}, 2:{'min':1,'max':3.5}}
		
		self.Uncertain['theta_prob'] = {1:{'min':0.35,'max':0.65}, 2:{'min':0.3,'max':0.7}}
		# self.Uncertain['Zhat_prob'] = {1:{'min':0.6,'max':0.4}, 2:{'min':0.4,'max':0.6}}
		self.Uncertain['Z_prob'] = {1:{'min':0.6*0.8+0.4*0.3,'max':0.6*0.2+0.4*0.7}, 2:{'min':0.4*0.8+0.6*0.3,'max':0.4*0.2+0.6*0.7}}

class I3T5S64():
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['Tend'] = 5
		self.sets['I'] = [1,2,3]
		
		##### Parameters #####
		self.parameters = {}
		self.parameters['B'] = {1:3, 2:3, 3:3, 4:3, 5:3}
		self.parameters['delta_i'] = {1:5, 2:2, 3:3} # implementation time
		self.parameters['f'] = {1:0.2, 2:0.1, 3:0.3} # fixed activity cost
		self.parameters['r'] =  0.05 # discount factor
		self.parameters['D_i'] =  {1:[1],2:[3],3:[3]} # Dependant, valid when j>i
		self.parameters['theta_theta'] =  {1:1, 2:1.5, 3:2.5} # threshold investment for certain resource requirement theta
		self.parameters['theta_Z'] = {1:1.5, 2:2.5, 3:3.5} # threshold investment for initial performance assessment Z^
		self.parameters['Ztilda'] =  {1:{'minmin':0,'minmax':0,'maxmax':0}, 2:{'minmin':-0.5,'minmax':-1.5,'maxmax':-3}, 3:{'minmin':0,'minmax':0,'maxmax':0}}
		self.parameters['Big_M'] =  10000 # Additional parameter
		
		##### Uncertainty Information #####
		self.Uncertain = {}

		self.Uncertain['theta'] = {1:{'min':2,'max':4}, 2:{'min':3,'max':5}, 3:{'min':4,'max':6}}
		self.Uncertain['Zhat'] = {1:{'min':1.5,'max':4.5}, 2:{'min':1,'max':3.5}, 3:{'min':1.5,'max':4.5}}
		
		self.Uncertain['theta_prob'] = {1:{'min':0.35,'max':0.65}, 2:{'min':0.3,'max':0.7}, 3:{'min':0.5,'max':0.5}}
		# self.Uncertain['Zhat_prob'] = {1:{'min':0.6,'max':0.4}, 2:{'min':0.4,'max':0.6}, 3:{'min':0.14,'max':0.86}}
		self.Uncertain['Z_prob'] = {1:{'min':0.6*0.8+0.4*0.3,'max':0.6*0.2+0.4*0.7}, 2:{'min':0.4*0.8+0.6*0.3,'max':0.4*0.2+0.6*0.7}, 3:{'min':0.14*0.8+0.86*0.3,'max':0.14*0.2+0.86*0.7}}

class I3T10S64():
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['Tend'] = 10
		self.sets['I'] = [1,2,3]
		
		##### Parameters #####
		self.parameters = {}
		self.parameters['B'] = {1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3, 10:3} # 
		self.parameters['delta_i'] = {1:5, 2:2, 3:3} # implementation time
		self.parameters['f'] = {1:0.2, 2:0.1, 3:0.3} # fixed activity cost
		self.parameters['r'] =  0.05 # discount factor
		self.parameters['D_i'] =  {1:[1],2:[3],3:[3]} # Dependant, valid when j>i
		self.parameters['theta_theta'] =  {1:1, 2:1.5, 3:2.5} # threshold investment for certain resource requirement theta
		self.parameters['theta_Z'] = {1:1.5, 2:2.5, 3:3.5} # threshold investment for initial performance assessment Z^
		self.parameters['Ztilda'] =  {1:{'minmin':0,'minmax':0,'maxmax':0}, 2:{'minmin':-0.5,'minmax':-1.5,'maxmax':-3}, 3:{'minmin':0,'minmax':0,'maxmax':0}}
		self.parameters['Big_M'] =  10000 # Additional parameter
		
		##### Uncertainty Information #####
		self.Uncertain = {}
		self.Uncertain['theta'] = {1:{'min':2,'max':4}, 2:{'min':3,'max':5}, 3:{'min':4,'max':6}}
		self.Uncertain['Zhat'] = {1:{'min':1.5,'max':4.5}, 2:{'min':1,'max':3.5}, 3:{'min':1.5,'max':4.5}}
		
		self.Uncertain['theta_prob'] = {1:{'min':0.35,'max':0.65}, 2:{'min':0.3,'max':0.7}, 3:{'min':0.5,'max':0.5}}
		# self.Uncertain['Zhat_prob'] = {1:{'min':0.6,'max':0.4}, 2:{'min':0.4,'max':0.6}, 3:{'min':0.14,'max':0.86}}
		self.Uncertain['Z_prob'] = {1:{'min':0.6*0.8+0.4*0.3,'max':0.6*0.2+0.4*0.7}, 2:{'min':0.4*0.8+0.6*0.3,'max':0.4*0.2+0.6*0.7}, 3:{'min':0.14*0.8+0.86*0.3,'max':0.14*0.2+0.86*0.7}}

class I4T5S128():
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['Tend'] = 5
		self.sets['I'] = [1,2,3,4]
		
		##### Parameters #####
		self.parameters = {}
		self.parameters['B'] = {1:4, 2:4, 3:4, 4:4, 5:4} # budget
		self.parameters['delta_i'] = {1:5, 2:2, 3:3, 4:3} # implementation time
		self.parameters['f'] = {1:0.2, 2:0.1, 3:0.3, 4:0.2} # fixed activity cost
		self.parameters['r'] =  0.05 # discount factor
		self.parameters['D_i'] =  {1:[1], 2:[3], 3:[3], 4:[4]} # Dependant, valid when j>i
		self.parameters['theta_theta'] =  {1:1, 2:1.5, 3:2.5, 4:0.5} # threshold investment for certain resource requirement theta
		self.parameters['theta_Z'] = {1:1.5, 2:2.5, 3:3.5, 4:1.5} # threshold investment for initial performance assessment Z^
		self.parameters['Ztilda'] =  {1:{'minmin':0,'minmax':0,'maxmax':0}, 2:{'minmin':-0.5,'minmax':-1.5,'maxmax':-3},
										3:{'minmin':0,'minmax':0,'maxmax':0}, 4:{'minmin':0,'minmax':0,'maxmax':0}}
		self.parameters['Big_M'] =  10000 # Additional parameter
		
		##### Uncertainty Information #####
		self.Uncertain = {}

		self.Uncertain['theta'] = {1:{'min':2,'max':4}, 2:{'min':3,'max':5}, 3:{'min':4,'max':6}, 4:{'min':2,'max':6}}
		self.Uncertain['Zhat'] = {1:{'min':1.5,'max':4.5}, 2:{'min':1,'max':3.5}, 3:{'min':1.5,'max':4.5}, 4:{'deterministic':2.485}}

		self.Uncertain['theta_prob'] = {1:{'min':0.35,'max':0.65}, 2:{'min':0.3,'max':0.7}, 3:{'min':0.5,'max':0.5}, 4:{'min':0.4,'max':0.6}}
		# self.Uncertain['Zhat_prob'] = {1:{'min':0.6,'max':0.4}, 2:{'min':0.4,'max':0.6}, 3:{'min':0.14,'max':0.86}, 4:{'min':0.225,'max':0.775}}
		self.Uncertain['Z_prob'] = {1:{'min':0.6*0.8+0.4*0.3,'max':0.6*0.2+0.4*0.7}, 2:{'min':0.4*0.8+0.6*0.3,'max':0.4*0.2+0.6*0.7}, 
									3:{'min':0.14*0.8+0.86*0.3,'max':0.14*0.2+0.86*0.7}, 4:{'deterministic':1}}