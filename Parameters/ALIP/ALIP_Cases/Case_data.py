class I3T12S4(): # Well_1, 4 scenarios
	def __init__(self):
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [5,6,7] # potential ALMs. 5: Gas Lift (GL), 6: Electrical Submersible Pump (ESP), 7: Sucker Rod Pump (SRP) 
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['T_end'] = 12 # End of the time horizon (months). Change T_end to change problem size.
		self.parameters['Pg'] = 6*30
		self.parameters['Po'] = 100*30
		self.parameters['Png'] = 50*30
		self.parameters['WI'] = 0.7 # Working interest
		self.parameters['MARR'] = 0.01 # Minimum acceptable rate of return
		self.parameters['FT'] = 0.3 # Federal tax rate
		self.parameters['b'] = 0.6357 # Decline exponent constant, which determines the pruduction rate curve after installing an ALM.
		self.parameters['D'] = 0.0507 # Nominal decline rate, which determines the pruduction rate curve after installing an ALM.
		self.parameters['LT'] = 0.2 # Local tax
		self.parameters['RT'] = 0.2 # Royalties
		self.parameters['Qg1'] = 800 # Initial gas flowrate
		self.parameters['Qo1'] = 20 # Initial oil flowrate
		self.parameters['Qng1'] = 500 # Initial natural gas flowrate
		self.parameters['n'] = 5 # Straight-line n-year depreciation model
		self.parameters['Cm_i'] = {5:5000, 6:2000, 7:1200} # Maintenance cost of ALM i
		self.parameters['Co_i'] = {5:129000, 6:250000, 7:160000} # Equipment and installation cost of ALM i
		self.parameters['Ce_i'] = {5:54000, 6:170000, 7:110000} # Equipment cost of ALM i
		self.parameters['LFR_LB_i'] = {5:0, 6:200, 7:300} # Lower limit for the liquid flowrate (LFR) of ALM i
		self.parameters['LFR_UB_i'] = {5:800, 6:800, 7:700} # Upper limit for the liquid flowrate (LFR) of ALM i
		
		##### Parameters for complete recouse #####
		self.parameters['CLIM'] = 10000000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Qrc_i'] = {5:{'Certain':0.98}, 6:{'High':1.26,'Low':0.84}, 7:{'High':1.296,'Low':0.864}} # Possible flow rate change ratio when ALM i is installed
		# self.uncertain['Qrc_i'] = {5:{'Certain':1.06}, 6:{'High':1.3,'Low':0.95}, 7:{'High':1.5,'Low':0.9}} # Possible flow rate change ratio when ALM i is installed
		# 5:{'High':1.176,'Low':0.784}
		##### Probability #####
		self.prob = {}
		self.prob['Qrc_i_prob'] = {5:{'Certain':1.0}, 6:{'High':0.5,'Low':0.5}, 7:{'High':0.5,'Low':0.5}} # Possible flow rate change ratio when ALM i is installed

class I3T16S4(): # Well_1, 4 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [5,6,7] # potential ALMs. 5: Gas Lift (GL), 6: Electrical Submersible Pump (ESP), 7: Sucker Rod Pump (SRP) 
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['T_end'] = 16 # End of the time horizon (months). Change T_end to change problem size.
		self.parameters['Pg'] = 6*30
		self.parameters['Po'] = 100*30
		self.parameters['Png'] = 50*30
		self.parameters['WI'] = 0.7 # Working interest
		self.parameters['MARR'] = 0.01 # Minimum acceptable rate of return
		self.parameters['FT'] = 0.3 # Federal tax rate
		self.parameters['b'] = 0.6357 # Decline exponent constant, which determines the pruduction rate curve after installing an ALM.
		self.parameters['D'] = 0.0507 # Nominal decline rate, which determines the pruduction rate curve after installing an ALM.
		self.parameters['LT'] = 0.2 # Local tax
		self.parameters['RT'] = 0.2 # Royalties
		self.parameters['Qg1'] = 800 # Initial gas flowrate
		self.parameters['Qo1'] = 20 # Initial oil flowrate
		self.parameters['Qng1'] = 500 # Initial natural gas flowrate
		self.parameters['n'] = 5 # Straight-line n-year depreciation model
		self.parameters['Cm_i'] = {5:5000, 6:2000, 7:1200} # Maintenance cost of ALM i
		self.parameters['Co_i'] = {5:129000, 6:250000, 7:160000} # Equipment and installation cost of ALM i
		self.parameters['Ce_i'] = {5:54000, 6:170000, 7:110000} # Equipment cost of ALM i
		self.parameters['LFR_LB_i'] = {5:0, 6:200, 7:300} # Lower limit for the liquid flowrate (LFR) of ALM i
		self.parameters['LFR_UB_i'] = {5:800, 6:800, 7:700} # Upper limit for the liquid flowrate (LFR) of ALM i
		
		##### Parameters for complete recouse #####
		self.parameters['CLIM'] = 10000000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Qrc_i'] = {5:{'Certain':0.98}, 6:{'High':1.26,'Low':0.84}, 7:{'High':1.296,'Low':0.864}} # Possible flow rate change ratio when ALM i is installed
		# self.uncertain['Qrc_i'] = {5:{'Certain':1.06}, 6:{'High':1.3,'Low':0.95}, 7:{'High':1.5,'Low':0.9}} # Possible flow rate change ratio when ALM i is installed
		# 5:{'High':1.176,'Low':0.784}
		##### Probability #####
		self.prob = {}
		self.prob['Qrc_i_prob'] = {5:{'Certain':1.0}, 6:{'High':0.5,'Low':0.5}, 7:{'High':0.5,'Low':0.5}} # Possible flow rate change ratio when ALM i is installed

class I3T20S4(): # Well_1, 4 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [5,6,7] # potential ALMs. 5: Gas Lift (GL), 6: Electrical Submersible Pump (ESP), 7: Sucker Rod Pump (SRP) 
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['T_end'] = 20 # End of the time horizon (months). Change T_end to change problem size.
		self.parameters['Pg'] = 6*30
		self.parameters['Po'] = 100*30
		self.parameters['Png'] = 50*30
		self.parameters['WI'] = 0.7 # Working interest
		self.parameters['MARR'] = 0.01 # Minimum acceptable rate of return
		self.parameters['FT'] = 0.3 # Federal tax rate
		self.parameters['b'] = 0.6357 # Decline exponent constant, which determines the pruduction rate curve after installing an ALM.
		self.parameters['D'] = 0.0507 # Nominal decline rate, which determines the pruduction rate curve after installing an ALM.
		self.parameters['LT'] = 0.2 # Local tax
		self.parameters['RT'] = 0.2 # Royalties
		self.parameters['Qg1'] = 800 # Initial gas flowrate
		self.parameters['Qo1'] = 20 # Initial oil flowrate
		self.parameters['Qng1'] = 500 # Initial natural gas flowrate
		self.parameters['n'] = 5 # Straight-line n-year depreciation model
		self.parameters['Cm_i'] = {5:5000, 6:2000, 7:1200} # Maintenance cost of ALM i
		self.parameters['Co_i'] = {5:129000, 6:250000, 7:160000} # Equipment and installation cost of ALM i
		self.parameters['Ce_i'] = {5:54000, 6:170000, 7:110000} # Equipment cost of ALM i
		self.parameters['LFR_LB_i'] = {5:0, 6:200, 7:300} # Lower limit for the liquid flowrate (LFR) of ALM i
		self.parameters['LFR_UB_i'] = {5:800, 6:800, 7:700} # Upper limit for the liquid flowrate (LFR) of ALM i
		
		##### Parameters for complete recouse #####
		self.parameters['CLIM'] = 10000000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Qrc_i'] = {5:{'Certain':0.98}, 6:{'High':1.26,'Low':0.84}, 7:{'High':1.296,'Low':0.864}} # Possible flow rate change ratio when ALM i is installed
		# self.uncertain['Qrc_i'] = {5:{'Certain':1.06}, 6:{'High':1.3,'Low':0.95}, 7:{'High':1.5,'Low':0.9}} # Possible flow rate change ratio when ALM i is installed
		# 5:{'High':1.176,'Low':0.784}
		##### Probability #####
		self.prob = {}
		self.prob['Qrc_i_prob'] = {5:{'Certain':1.0}, 6:{'High':0.5,'Low':0.5}, 7:{'High':0.5,'Low':0.5}} # Possible flow rate change ratio when ALM i is installed

class I3T24S4(): # Well_1, 4 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [5,6,7] # potential ALMs. 5: Gas Lift (GL), 6: Electrical Submersible Pump (ESP), 7: Sucker Rod Pump (SRP) 
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['T_end'] = 24 # End of the time horizon (months). Change T_end to change problem size.
		self.parameters['Pg'] = 6*30
		self.parameters['Po'] = 100*30
		self.parameters['Png'] = 50*30
		self.parameters['WI'] = 0.7 # Working interest
		self.parameters['MARR'] = 0.01 # Minimum acceptable rate of return
		self.parameters['FT'] = 0.3 # Federal tax rate
		self.parameters['b'] = 0.6357 # Decline exponent constant, which determines the pruduction rate curve after installing an ALM.
		self.parameters['D'] = 0.0507 # Nominal decline rate, which determines the pruduction rate curve after installing an ALM.
		self.parameters['LT'] = 0.2 # Local tax
		self.parameters['RT'] = 0.2 # Royalties
		self.parameters['Qg1'] = 800 # Initial gas flowrate
		self.parameters['Qo1'] = 20 # Initial oil flowrate
		self.parameters['Qng1'] = 500 # Initial natural gas flowrate
		self.parameters['n'] = 5 # Straight-line n-year depreciation model
		self.parameters['Cm_i'] = {5:5000, 6:2000, 7:1200} # Maintenance cost of ALM i
		self.parameters['Co_i'] = {5:129000, 6:250000, 7:160000} # Equipment and installation cost of ALM i
		self.parameters['Ce_i'] = {5:54000, 6:170000, 7:110000} # Equipment cost of ALM i
		self.parameters['LFR_LB_i'] = {5:0, 6:200, 7:300} # Lower limit for the liquid flowrate (LFR) of ALM i
		self.parameters['LFR_UB_i'] = {5:800, 6:800, 7:700} # Upper limit for the liquid flowrate (LFR) of ALM i
		
		##### Parameters for complete recouse #####
		self.parameters['CLIM'] = 10000000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Qrc_i'] = {5:{'Certain':0.98}, 6:{'High':1.26,'Low':0.84}, 7:{'High':1.296,'Low':0.864}} # Possible flow rate change ratio when ALM i is installed
		# self.uncertain['Qrc_i'] = {5:{'Certain':1.06}, 6:{'High':1.3,'Low':0.95}, 7:{'High':1.5,'Low':0.9}} # Possible flow rate change ratio when ALM i is installed
		# 5:{'High':1.176,'Low':0.784}
		##### Probability #####
		self.prob = {}
		self.prob['Qrc_i_prob'] = {5:{'Certain':1.0}, 6:{'High':0.5,'Low':0.5}, 7:{'High':0.5,'Low':0.5}} # Possible flow rate change ratio when ALM i is installed

class I3T28S4(): # Well_1, 4 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [5,6,7] # potential ALMs. 5: Gas Lift (GL), 6: Electrical Submersible Pump (ESP), 7: Sucker Rod Pump (SRP) 
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['T_end'] = 28 # End of the time horizon (months). Change T_end to change problem size.
		self.parameters['Pg'] = 6*30
		self.parameters['Po'] = 100*30
		self.parameters['Png'] = 50*30
		self.parameters['WI'] = 0.7 # Working interest
		self.parameters['MARR'] = 0.01 # Minimum acceptable rate of return
		self.parameters['FT'] = 0.3 # Federal tax rate
		self.parameters['b'] = 0.6357 # Decline exponent constant, which determines the pruduction rate curve after installing an ALM.
		self.parameters['D'] = 0.0507 # Nominal decline rate, which determines the pruduction rate curve after installing an ALM.
		self.parameters['LT'] = 0.2 # Local tax
		self.parameters['RT'] = 0.2 # Royalties
		self.parameters['Qg1'] = 800 # Initial gas flowrate
		self.parameters['Qo1'] = 20 # Initial oil flowrate
		self.parameters['Qng1'] = 500 # Initial natural gas flowrate
		self.parameters['n'] = 5 # Straight-line n-year depreciation model
		self.parameters['Cm_i'] = {5:5000, 6:2000, 7:1200} # Maintenance cost of ALM i
		self.parameters['Co_i'] = {5:129000, 6:250000, 7:160000} # Equipment and installation cost of ALM i
		self.parameters['Ce_i'] = {5:54000, 6:170000, 7:110000} # Equipment cost of ALM i
		self.parameters['LFR_LB_i'] = {5:0, 6:200, 7:300} # Lower limit for the liquid flowrate (LFR) of ALM i
		self.parameters['LFR_UB_i'] = {5:800, 6:800, 7:700} # Upper limit for the liquid flowrate (LFR) of ALM i
		
		##### Parameters for complete recouse #####
		self.parameters['CLIM'] = 10000000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Qrc_i'] = {5:{'Certain':0.98}, 6:{'High':1.26,'Low':0.84}, 7:{'High':1.296,'Low':0.864}} # Possible flow rate change ratio when ALM i is installed
		# self.uncertain['Qrc_i'] = {5:{'Certain':1.06}, 6:{'High':1.3,'Low':0.95}, 7:{'High':1.5,'Low':0.9}} # Possible flow rate change ratio when ALM i is installed
		# 5:{'High':1.176,'Low':0.784}
		##### Probability #####
		self.prob = {}
		self.prob['Qrc_i_prob'] = {5:{'Certain':1.0}, 6:{'High':0.5,'Low':0.5}, 7:{'High':0.5,'Low':0.5}} # Possible flow rate change ratio when ALM i is installed

class I3T32S4(): # Well_1, 4 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [5,6,7] # potential ALMs. 5: Gas Lift (GL), 6: Electrical Submersible Pump (ESP), 7: Sucker Rod Pump (SRP) 
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['T_end'] = 32 # End of the time horizon (months). Change T_end to change problem size.
		self.parameters['Pg'] = 6*30
		self.parameters['Po'] = 100*30
		self.parameters['Png'] = 50*30
		self.parameters['WI'] = 0.7 # Working interest
		self.parameters['MARR'] = 0.01 # Minimum acceptable rate of return
		self.parameters['FT'] = 0.3 # Federal tax rate
		self.parameters['b'] = 0.6357 # Decline exponent constant, which determines the pruduction rate curve after installing an ALM.
		self.parameters['D'] = 0.0507 # Nominal decline rate, which determines the pruduction rate curve after installing an ALM.
		self.parameters['LT'] = 0.2 # Local tax
		self.parameters['RT'] = 0.2 # Royalties
		self.parameters['Qg1'] = 800 # Initial gas flowrate
		self.parameters['Qo1'] = 20 # Initial oil flowrate
		self.parameters['Qng1'] = 500 # Initial natural gas flowrate
		self.parameters['n'] = 5 # Straight-line n-year depreciation model
		self.parameters['Cm_i'] = {5:5000, 6:2000, 7:1200} # Maintenance cost of ALM i
		self.parameters['Co_i'] = {5:129000, 6:250000, 7:160000} # Equipment and installation cost of ALM i
		self.parameters['Ce_i'] = {5:54000, 6:170000, 7:110000} # Equipment cost of ALM i
		self.parameters['LFR_LB_i'] = {5:0, 6:200, 7:300} # Lower limit for the liquid flowrate (LFR) of ALM i
		self.parameters['LFR_UB_i'] = {5:800, 6:800, 7:700} # Upper limit for the liquid flowrate (LFR) of ALM i
		
		##### Parameters for complete recouse #####
		self.parameters['CLIM'] = 10000000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Qrc_i'] = {5:{'Certain':0.98}, 6:{'High':1.26,'Low':0.84}, 7:{'High':1.296,'Low':0.864}} # Possible flow rate change ratio when ALM i is installed
		# self.uncertain['Qrc_i'] = {5:{'Certain':1.06}, 6:{'High':1.3,'Low':0.95}, 7:{'High':1.5,'Low':0.9}} # Possible flow rate change ratio when ALM i is installed
		# 5:{'High':1.176,'Low':0.784}
		##### Probability #####
		self.prob = {}
		self.prob['Qrc_i_prob'] = {5:{'Certain':1.0}, 6:{'High':0.5,'Low':0.5}, 7:{'High':0.5,'Low':0.5}} # Possible flow rate change ratio when ALM i is installed

class I3T12S8(): # Well_1, 8 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [5,6,7] # potential ALMs. 5: Gas Lift (GL), 6: Electrical Submersible Pump (ESP), 7: Sucker Rod Pump (SRP) 
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['T_end'] = 12 # End of the time horizon (months). Change T_end to change problem size.
		self.parameters['Pg'] = 6*30
		self.parameters['Po'] = 100*30
		self.parameters['Png'] = 50*30
		self.parameters['WI'] = 0.7 # Working interest
		self.parameters['MARR'] = 0.01 # Minimum acceptable rate of return
		self.parameters['FT'] = 0.3 # Federal tax rate
		self.parameters['b'] = 0.6357 # Decline exponent constant, which determines the pruduction rate curve after installing an ALM.
		self.parameters['D'] = 0.0507 # Nominal decline rate, which determines the pruduction rate curve after installing an ALM.
		self.parameters['LT'] = 0.2 # Local tax
		self.parameters['RT'] = 0.2 # Royalties
		self.parameters['Qg1'] = 800 # Initial gas flowrate
		self.parameters['Qo1'] = 20 # Initial oil flowrate
		self.parameters['Qng1'] = 500 # Initial natural gas flowrate
		# self.parameters['DownholeSeparator'] =1
		self.parameters['n'] = 5 # Straight-line n-year depreciation model
		self.parameters['Cm_i'] = {5:5000, 6:2000, 7:1200} # Maintenance cost of ALM i
		self.parameters['Co_i'] = {5:129000, 6:250000, 7:160000} # Equipment and installation cost of ALM i
		self.parameters['Ce_i'] = {5:54000, 6:170000, 7:110000} # Equipment cost of ALM i
		self.parameters['LFR_LB_i'] = {5:0, 6:0, 7:300} # Lower limit for the liquid flowrate (LFR) of ALM i
		self.parameters['LFR_UB_i'] = {5:1000, 6:1000, 7:1000} # Upper limit for the liquid flowrate (LFR) of ALM i
		
		##### Parameters for complete recouse #####
		self.parameters['CLIM'] = 10000000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Qrc_i'] = {5:{'High':1.176,'Low':0.784}, 6:{'High':1.26,'Low':0.84}, 7:{'High':1.296,'Low':0.864}} # Possible flow rate change ratio when ALM i is installed
		# 5:{'High':1.5,'Low':0.55}
		##### Probability #####
		self.prob = {}
		self.prob['Qrc_i_prob'] = {5:{'High':0.5,'Low':0.5}, 6:{'High':0.5,'Low':0.5}, 7:{'High':0.5,'Low':0.5}} # Possible flow rate change ratio when ALM i is installed

class I3T16S8(): # Well_1, 8 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [5,6,7] # potential ALMs. 5: Gas Lift (GL), 6: Electrical Submersible Pump (ESP), 7: Sucker Rod Pump (SRP) 
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['T_end'] = 16 # End of the time horizon (months). Change T_end to change problem size.
		self.parameters['Pg'] = 6*30
		self.parameters['Po'] = 100*30
		self.parameters['Png'] = 50*30
		self.parameters['WI'] = 0.7 # Working interest
		self.parameters['MARR'] = 0.01 # Minimum acceptable rate of return
		self.parameters['FT'] = 0.3 # Federal tax rate
		self.parameters['b'] = 0.6357 # Decline exponent constant, which determines the pruduction rate curve after installing an ALM.
		self.parameters['D'] = 0.0507 # Nominal decline rate, which determines the pruduction rate curve after installing an ALM.
		self.parameters['LT'] = 0.2 # Local tax
		self.parameters['RT'] = 0.2 # Royalties
		self.parameters['Qg1'] = 800 # Initial gas flowrate
		self.parameters['Qo1'] = 20 # Initial oil flowrate
		self.parameters['Qng1'] = 500 # Initial natural gas flowrate
		self.parameters['n'] = 5 # Straight-line n-year depreciation model
		self.parameters['Cm_i'] = {5:5000, 6:2000, 7:1200} # Maintenance cost of ALM i
		self.parameters['Co_i'] = {5:129000, 6:250000, 7:160000} # Equipment and installation cost of ALM i
		self.parameters['Ce_i'] = {5:54000, 6:170000, 7:110000} # Equipment cost of ALM i
		self.parameters['LFR_LB_i'] = {5:0, 6:0, 7:300} # Lower limit for the liquid flowrate (LFR) of ALM i
		self.parameters['LFR_UB_i'] = {5:1000, 6:1000, 7:1000} # Upper limit for the liquid flowrate (LFR) of ALM i
		
		##### Parameters for complete recouse #####
		self.parameters['CLIM'] = 10000000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Qrc_i'] = {5:{'High':1.176,'Low':0.784}, 6:{'High':1.26,'Low':0.84}, 7:{'High':1.296,'Low':0.864}} # Possible flow rate change ratio when ALM i is installed
		# 5:{'High':1.5,'Low':0.55}
		##### Probability #####
		self.prob = {}
		self.prob['Qrc_i_prob'] = {5:{'High':0.5,'Low':0.5}, 6:{'High':0.5,'Low':0.5}, 7:{'High':0.5,'Low':0.5}} # Possible flow rate change ratio when ALM i is installed

class I3T20S8(): # Well_1, 8 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [5,6,7] # potential ALMs. 5: Gas Lift (GL), 6: Electrical Submersible Pump (ESP), 7: Sucker Rod Pump (SRP) 
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['T_end'] = 20 # End of the time horizon (months). Change T_end to change problem size.
		self.parameters['Pg'] = 6*30
		self.parameters['Po'] = 100*30
		self.parameters['Png'] = 50*30
		self.parameters['WI'] = 0.7 # Working interest
		self.parameters['MARR'] = 0.01 # Minimum acceptable rate of return
		self.parameters['FT'] = 0.3 # Federal tax rate
		self.parameters['b'] = 0.6357 # Decline exponent constant, which determines the pruduction rate curve after installing an ALM.
		self.parameters['D'] = 0.0507 # Nominal decline rate, which determines the pruduction rate curve after installing an ALM.
		self.parameters['LT'] = 0.2 # Local tax
		self.parameters['RT'] = 0.2 # Royalties
		self.parameters['Qg1'] = 800 # Initial gas flowrate
		self.parameters['Qo1'] = 20 # Initial oil flowrate
		self.parameters['Qng1'] = 500 # Initial natural gas flowrate
		# self.parameters['DownholeSeparator'] =1
		self.parameters['n'] = 5 # Straight-line n-year depreciation model
		self.parameters['Cm_i'] = {5:5000, 6:2000, 7:1200} # Maintenance cost of ALM i
		self.parameters['Co_i'] = {5:129000, 6:250000, 7:160000} # Equipment and installation cost of ALM i
		self.parameters['Ce_i'] = {5:54000, 6:170000, 7:110000} # Equipment cost of ALM i
		self.parameters['LFR_LB_i'] = {5:0, 6:0, 7:300} # Lower limit for the liquid flowrate (LFR) of ALM i
		self.parameters['LFR_UB_i'] = {5:1000, 6:1000, 7:1000} # Upper limit for the liquid flowrate (LFR) of ALM i
		
		##### Parameters for complete recouse #####
		self.parameters['CLIM'] = 10000000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Qrc_i'] = {5:{'High':1.176,'Low':0.784}, 6:{'High':1.26,'Low':0.84}, 7:{'High':1.296,'Low':0.864}} # Possible flow rate change ratio when ALM i is installed
		# 5:{'High':1.5,'Low':0.55}
		##### Probability #####
		self.prob = {}
		self.prob['Qrc_i_prob'] = {5:{'High':0.5,'Low':0.5}, 6:{'High':0.5,'Low':0.5}, 7:{'High':0.5,'Low':0.5}} # Possible flow rate change ratio when ALM i is installed

class I3T24S8(): # Well_1, 8 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [5,6,7] # potential ALMs. 5: Gas Lift (GL), 6: Electrical Submersible Pump (ESP), 7: Sucker Rod Pump (SRP) 
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['T_end'] = 24 # End of the time horizon (months). Change T_end to change problem size.
		self.parameters['Pg'] = 6*30
		self.parameters['Po'] = 100*30
		self.parameters['Png'] = 50*30
		self.parameters['WI'] = 0.7 # Working interest
		self.parameters['MARR'] = 0.01 # Minimum acceptable rate of return
		self.parameters['FT'] = 0.3 # Federal tax rate
		self.parameters['b'] = 0.6357 # Decline exponent constant, which determines the pruduction rate curve after installing an ALM.
		self.parameters['D'] = 0.0507 # Nominal decline rate, which determines the pruduction rate curve after installing an ALM.
		self.parameters['LT'] = 0.2 # Local tax
		self.parameters['RT'] = 0.2 # Royalties
		self.parameters['Qg1'] = 800 # Initial gas flowrate
		self.parameters['Qo1'] = 20 # Initial oil flowrate
		self.parameters['Qng1'] = 500 # Initial natural gas flowrate
		# self.parameters['DownholeSeparator'] =1
		self.parameters['n'] = 5 # Straight-line n-year depreciation model
		self.parameters['Cm_i'] = {5:5000, 6:2000, 7:1200} # Maintenance cost of ALM i
		self.parameters['Co_i'] = {5:129000, 6:250000, 7:160000} # Equipment and installation cost of ALM i
		self.parameters['Ce_i'] = {5:54000, 6:170000, 7:110000} # Equipment cost of ALM i
		self.parameters['LFR_LB_i'] = {5:0, 6:0, 7:300} # Lower limit for the liquid flowrate (LFR) of ALM i
		self.parameters['LFR_UB_i'] = {5:1000, 6:1000, 7:1000} # Upper limit for the liquid flowrate (LFR) of ALM i
		
		##### Parameters for complete recouse #####
		self.parameters['CLIM'] = 10000000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Qrc_i'] = {5:{'High':1.176,'Low':0.784}, 6:{'High':1.26,'Low':0.84}, 7:{'High':1.296,'Low':0.864}} # Possible flow rate change ratio when ALM i is installed
		# 5:{'High':1.5,'Low':0.55}
		##### Probability #####
		self.prob = {}
		self.prob['Qrc_i_prob'] = {5:{'High':0.5,'Low':0.5}, 6:{'High':0.5,'Low':0.5}, 7:{'High':0.5,'Low':0.5}} # Possible flow rate change ratio when ALM i is installed

class I3T28S8(): # Well_1, 8 scenarios
	def __init__(self):
		
		###### Sets #####
		self.sets = {}
		self.sets['I'] = [5,6,7] # potential ALMs. 5: Gas Lift (GL), 6: Electrical Submersible Pump (ESP), 7: Sucker Rod Pump (SRP) 
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['T_end'] = 28 # End of the time horizon (months). Change T_end to change problem size.
		self.parameters['Pg'] = 6*30
		self.parameters['Po'] = 100*30
		self.parameters['Png'] = 50*30
		self.parameters['WI'] = 0.7 # Working interest
		self.parameters['MARR'] = 0.01 # Minimum acceptable rate of return
		self.parameters['FT'] = 0.3 # Federal tax rate
		self.parameters['b'] = 0.6357 # Decline exponent constant, which determines the pruduction rate curve after installing an ALM.
		self.parameters['D'] = 0.0507 # Nominal decline rate, which determines the pruduction rate curve after installing an ALM.
		self.parameters['LT'] = 0.2 # Local tax
		self.parameters['RT'] = 0.2 # Royalties
		self.parameters['Qg1'] = 800 # Initial gas flowrate
		self.parameters['Qo1'] = 20 # Initial oil flowrate
		self.parameters['Qng1'] = 500 # Initial natural gas flowrate
		self.parameters['n'] = 5 # Straight-line n-year depreciation model
		self.parameters['Cm_i'] = {5:5000, 6:2000, 7:1200} # Maintenance cost of ALM i
		self.parameters['Co_i'] = {5:129000, 6:250000, 7:160000} # Equipment and installation cost of ALM i
		self.parameters['Ce_i'] = {5:54000, 6:170000, 7:110000} # Equipment cost of ALM i
		self.parameters['LFR_LB_i'] = {5:0, 6:0, 7:300} # Lower limit for the liquid flowrate (LFR) of ALM i
		self.parameters['LFR_UB_i'] = {5:1000, 6:1000, 7:1000} # Upper limit for the liquid flowrate (LFR) of ALM i
		
		##### Parameters for complete recouse #####
		self.parameters['CLIM'] = 10000000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Qrc_i'] = {5:{'High':1.176,'Low':0.784}, 6:{'High':1.26,'Low':0.84}, 7:{'High':1.296,'Low':0.864}} # Possible flow rate change ratio when ALM i is installed
		# 5:{'High':1.5,'Low':0.55}
		##### Probability #####
		self.prob = {}
		self.prob['Qrc_i_prob'] = {5:{'High':0.5,'Low':0.5}, 6:{'High':0.5,'Low':0.5}, 7:{'High':0.5,'Low':0.5}} # Possible flow rate change ratio when ALM i is installed
