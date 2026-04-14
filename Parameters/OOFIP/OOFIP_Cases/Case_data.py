class F3FPSO3T10S2(): # 3 fields, 3 FPSO, 9 connections, 1 tier, and 2 scenarios with uncertain oil deliverability, water-oil ratio, and gas-oil ratio
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['F'] = [1,2,3] # field site
		self.sets['FPSO'] = [1,2,3] # Floating Production Storage and Offloading facilities
		self.sets['rf'] = [1] # ringfence
		self.sets['F_rf'] = {1:[1,2,3]} # Fields f in a ringfence rf
		self.sets['F_fpso'] = {1:[1,2,3], 2:[1,2,3], 3:[1,2,3]} # Fields f connected to FPSO fpso
		self.sets['I'] = [1] # tier i for progressive production sharing agreements
		self.sets['T'] = list(range(1,11))
		self.sets['T1'] = [1] # Time set for initial NACs
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['FC_ffpso'] = {(1,1):18, (1,2):21, (1,3):36,
										(2,1):26, (2,2):21, (2,3):20,
										(3,1):19, (3,2):11, (3,3):27} # Fixed cost for installing the connection between field f and FPSO fpso
		self.parameters['FCwell_f'] = {1:40, 2:40, 3:40} # Fixed cost for drilling a well in field f
		self.parameters['FCFPSO_fpso'] = {1:200, 2:200, 3:200} # Fixed capital cost for installing FPSO fpso
		self.parameters['VCliq_fpso'] = {1:1.5, 2:1.5, 3:1.5} # Variable capital cost for installing or expanding the liquid (oil and water) capacity of FPSO
		self.parameters['VCgas_fpso'] = {1:1.6, 2:1.5, 3:1.5} # Variable capital cost for installing or expanding the gas capacity of FPSO
		self.parameters['OCliq_rf'] = {1:0.2} # Operating cost for unit liquid produced in ringfence rf
		self.parameters['OCgas_rf'] = {1:0.1} # Operating cost for unit gas produced in ringfence rf
		self.parameters['ftax_rf'] = {1:0.1} # Income tax rate for ringfence rf
		self.parameters['fPO_rfi'] = {(1,1):0.5} # Profit oil fraction in tier i for ringfence rf
		self.parameters['fCR_rf'] = {1:0.3} # Cost recovery ceiling fraction for ring fence rf
		self.parameters['Loil_rfi'] = {(1,1):0} # Lower threshold for profit oil in tier i for ringfence rf
		self.parameters['Uoil_rfi'] = {(1,1):10000} # Upper threshold for profit oil in tier i for ringfence rf
		self.parameters['alpha'] = 20 # Selling price of oil
		self.parameters['l1'] = 3 # Lead time for initial installation of a FPSO facility
		self.parameters['l2'] = 1 # Lead time for expansion of a FPSO facility
		self.parameters['Uoil_fpso'] = {1:500, 2:500, 3:500} # Installation capacity for oil in FPSO
		self.parameters['Uliq_fpso'] = {1:500, 2:500, 3:500} # Installation capacity for liquid in FPSO
		self.parameters['Ugas_fpso'] = {1:500, 2:500, 3:500} # Installation capacity for gas in FPSO
		self.parameters['myu'] = 0.9 # Expanded capacity must be less than myu*Installed capacity
		self.parameters['UIwell'] = 7 # The number of wells that can be drilled over all fields at t
		self.parameters['UNwell_f'] = {1:10,2:10,3:10} # The number of wells that can be drilled at field f
		self.parameters['epsilon'] = 0.02 # Required oil production percentage to judge field f has started production
		
		self.parameters['a_oil_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter a's for oil deliverability
		self.parameters['b_oil_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter b's for oil deliverability
		self.parameters['c_oil_ffpso'] = {(1,1):-14.5,(1,2):-15,(1,3):-15.5,(2,1):-10.5,(2,2):-11,(2,3):-11.5,(3,1):-7.5,(3,2):-8,(3,3):-8.5} # Model parameter c's for oil deliverability
		self.parameters['d_oil_ffpso'] = {(1,1):14.5,(1,2):15,(1,3):15.5,(2,1):10.5,(2,2):11,(2,3):11.5,(3,1):7.5,(3,2):8,(3,3):8.5} # Model parameter d's for oil deliverability
		self.parameters['a_wor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter a's for water-oil ratio
		self.parameters['b_wor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter b's for water-oil ratio
		self.parameters['c_wor_ffpso'] = {(1,1):1,(1,2):1.2,(1,3):1.4,(2,1):2.3,(2,2):2.5,(2,3):2.7,(3,1):3.8,(3,2):4,(3,3):4.2} # Model parameter c's for water-oil ratio
		self.parameters['d_wor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter d's for water-oil ratio
		self.parameters['a_gor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter a's for gas-oil ratio
		self.parameters['b_gor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter b's for gas-oil ratio
		self.parameters['c_gor_ffpso'] = {(1,1):0.15,(1,2):0.1,(1,3):0.1,(2,1):0.1,(2,2):0.3,(2,3):0,(3,1):0.2,(3,2):0.2,(3,3):-0.05} # Model parameter c's for gas-oil ratio
		self.parameters['d_gor_ffpso'] = {(1,1):0.65,(1,2):0.75,(1,3):0.85,(2,1):0.8,(2,2):0.7,(2,3):0.9,(3,1):0.75,(3,2):0.8,(3,3):0.95} # Model parameter d's for gas-oil ratio
		
		DR = 0.02 # Discount rate
		self.parameters['dis_t'] = {}
		for t in self.sets['T']:
			self.parameters['dis_t'][t] = (1 + DR) ** (1 - t) # Discount Factor
		self.parameters['delta'] = 1 # number of days in a time period t
		# self.parameters['Big_M'] = 100000
		# self.parameters['Big_U'] = 100000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['FieldSize'] = {1:{1:57,2:403}, 2:{1:320}, 3:{1:500}} # Uncertain recoverable oil volume (field size)
		self.uncertain['alpha_o_fs'] = {(1,1):0.75,(1,2):1.25,
										(2,1):1,(2,2):1,
										(3,1):1,(3,2):1} # Uncertainty of oil deliverability
		self.uncertain['alpha_wc_fs'] = {(1,1):0.75,(1,2):1.25,
										(2,1):1,(2,2):1,
										(3,1):1,(3,2):1} # Uncertainty of water-oil ratio
		self.uncertain['alpha_gc_fs'] = {(1,1):0.75,(1,2):1.25,
										(2,1):1,(2,2):1,
										(3,1):1,(3,2):1} # Uncertainty of gas-oil ratio
		self.uncertain['N1_f'] = {1:3, 2:0, 3:0} # Required number of wells to reveal uncertainty
		self.uncertain['N2_f'] = {1:1, 2:0, 3:0} # Required years of production to reveal uncertainty
		
		##### Probability #####
		self.uncertain['FieldSize_prob'] = {1:{1:0.5,2:0.5}, 2:{1:1}, 3:{1:1}}

class F3FPSO3T10S4(): # Case1, i.e, 3 fields, 3 FPSO, 9 connections, 1 tier, and 4 scenarios with uncertain oil deliverability, water-oil ratio, and gas-oil ratio
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['F'] = [1,2,3] # field site
		self.sets['FPSO'] = [1,2,3] # Floating Production Storage and Offloading facilities
		self.sets['rf'] = [1] # ringfence
		self.sets['F_rf'] = {1:[1,2,3]} # Fields f in a ringfence rf
		self.sets['F_fpso'] = {1:[1,2,3], 2:[1,2,3], 3:[1,2,3]} # Fields f connected to FPSO fpso
		self.sets['I'] = [1] # tier i for progressive production sharing agreements
		self.sets['T'] = list(range(1,11))
		self.sets['T1'] = [1] # Time set for initial NACs
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['FC_ffpso'] = {(1,1):18, (1,2):21, (1,3):36,
										(2,1):26, (2,2):21, (2,3):20,
										(3,1):19, (3,2):11, (3,3):27} # Fixed cost for installing the connection between field f and FPSO fpso
		self.parameters['FCwell_f'] = {1:40, 2:40, 3:40} # Fixed cost for drilling a well in field f
		self.parameters['FCFPSO_fpso'] = {1:200, 2:200, 3:200} # Fixed capital cost for installing FPSO fpso
		self.parameters['VCliq_fpso'] = {1:1.5, 2:1.5, 3:1.5} # Variable capital cost for installing or expanding the liquid (oil and water) capacity of FPSO
		self.parameters['VCgas_fpso'] = {1:1.6, 2:1.5, 3:1.5} # Variable capital cost for installing or expanding the gas capacity of FPSO
		self.parameters['OCliq_rf'] = {1:0.2} # Operating cost for unit liquid produced in ringfence rf
		self.parameters['OCgas_rf'] = {1:0.1} # Operating cost for unit gas produced in ringfence rf
		self.parameters['ftax_rf'] = {1:0.1} # Income tax rate for ringfence rf
		self.parameters['fPO_rfi'] = {(1,1):0.5} # Profit oil fraction in tier i for ringfence rf
		self.parameters['fCR_rf'] = {1:0.3} # Cost recovery ceiling fraction for ring fence rf
		self.parameters['Loil_rfi'] = {(1,1):0} # Lower threshold for profit oil in tier i for ringfence rf
		self.parameters['Uoil_rfi'] = {(1,1):10000} # Upper threshold for profit oil in tier i for ringfence rf
		self.parameters['alpha'] = 20 # Selling price of oil
		self.parameters['l1'] = 3 # Lead time for initial installation of a FPSO facility, 3
		self.parameters['l2'] = 1 # Lead time for expansion of a FPSO facility
		self.parameters['Uoil_fpso'] = {1:500, 2:500, 3:500} # Installation capacity for oil in FPSO
		self.parameters['Uliq_fpso'] = {1:500, 2:500, 3:500} # Installation capacity for liquid in FPSO
		self.parameters['Ugas_fpso'] = {1:500, 2:500, 3:500} # Installation capacity for gas in FPSO
		self.parameters['myu'] = 0.9 # Expanded capacity must be less than myu*Installed capacity
		self.parameters['UIwell'] = 7 # The number of wells that can be drilled over all fields at t
		self.parameters['UNwell_f'] = {1:10,2:10,3:10} # The number of wells that can be drilled at field f
		self.parameters['epsilon'] = 0.02 # Required oil production percentage to judge field f has started production
		
		self.parameters['a_oil_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter a's for oil deliverability
		self.parameters['b_oil_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter b's for oil deliverability
		self.parameters['c_oil_ffpso'] = {(1,1):-14.5,(1,2):-15,(1,3):-15.5,(2,1):-10.5,(2,2):-11,(2,3):-11.5,(3,1):-7.5,(3,2):-8,(3,3):-8.5} # Model parameter c's for oil deliverability
		self.parameters['d_oil_ffpso'] = {(1,1):14.5,(1,2):15,(1,3):15.5,(2,1):10.5,(2,2):11,(2,3):11.5,(3,1):7.5,(3,2):8,(3,3):8.5} # Model parameter d's for oil deliverability
		self.parameters['a_wor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter a's for water-oil ratio
		self.parameters['b_wor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter b's for water-oil ratio
		self.parameters['c_wor_ffpso'] = {(1,1):1,(1,2):1.2,(1,3):1.4,(2,1):2.3,(2,2):2.5,(2,3):2.7,(3,1):3.8,(3,2):4,(3,3):4.2} # Model parameter c's for water-oil ratio
		self.parameters['d_wor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter d's for water-oil ratio
		self.parameters['a_gor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter a's for gas-oil ratio
		self.parameters['b_gor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter b's for gas-oil ratio
		self.parameters['c_gor_ffpso'] = {(1,1):0.15,(1,2):0.1,(1,3):0.1,(2,1):0.1,(2,2):0.3,(2,3):0,(3,1):0.2,(3,2):0.2,(3,3):-0.05} # Model parameter c's for gas-oil ratio
		self.parameters['d_gor_ffpso'] = {(1,1):0.65,(1,2):0.75,(1,3):0.85,(2,1):0.8,(2,2):0.7,(2,3):0.9,(3,1):0.75,(3,2):0.8,(3,3):0.95} # Model parameter d's for gas-oil ratio
		
		DR = 0.02 # Discount rate
		self.parameters['dis_t'] = {}
		for t in self.sets['T']:
			self.parameters['dis_t'][t] = (1 + DR) ** (1 - t) # Discount Factor
		self.parameters['delta'] = 1 # number of days in a time period t
		# self.parameters['Big_M'] = 100000
		# self.parameters['Big_U'] = 100000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['FieldSize'] = {1:{1:57,2:403}, 2:{1:80,2:560}, 3:{1:500}} # Uncertain recoverable oil volume (field size), {1:57,2:403}
		self.uncertain['alpha_o_fs'] = {(1,1):0.75,(1,2):0.75,(1,3):1.25,(1,4):1.25,
										(2,1):0.75,(2,2):1.25,(2,3):0.75,(2,4):1.25,
										(3,1):1,(3,2):1,(3,3):1,(3,4):1} # Uncertainty of oil deliverability
		self.uncertain['alpha_wc_fs'] = {(1,1):0.75,(1,2):0.75,(1,3):1.25,(1,4):1.25,
										(2,1):0.75,(2,2):1.25,(2,3):0.75,(2,4):1.25,
										(3,1):1,(3,2):1,(3,3):1,(3,4):1} # Uncertainty of water-oil ratio
		self.uncertain['alpha_gc_fs'] = {(1,1):0.75,(1,2):0.75,(1,3):1.25,(1,4):1.25,
										(2,1):0.75,(2,2):1.25,(2,3):0.75,(2,4):1.25,
										(3,1):1,(3,2):1,(3,3):1,(3,4):1} # Uncertainty of gas-oil ratio
		self.uncertain['N1_f'] = {1:3, 2:4, 3:0} # Required number of wells to reveal uncertainty
		self.uncertain['N2_f'] = {1:1, 2:1, 3:0} # Required years of production to reveal uncertainty
		
		##### Probability #####
		self.uncertain['FieldSize_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:1}}

class F3FPSO3T10S8(): # 3 fields, 3 FPSO, 9 connections, 1 tier, and 8 scenarios with uncertain oil deliverability, water-oil ratio, and gas-oil ratio
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['F'] = [1,2,3] # field site
		self.sets['FPSO'] = [1,2,3] # Floating Production Storage and Offloading facilities
		self.sets['rf'] = [1] # ringfence
		self.sets['F_rf'] = {1:[1,2,3]} # Fields f in a ringfence rf
		self.sets['F_fpso'] = {1:[1,2,3], 2:[1,2,3], 3:[1,2,3]} # Fields f connected to FPSO fpso
		self.sets['I'] = [1] # tier i for progressive production sharing agreements
		self.sets['T'] = list(range(1,11))
		self.sets['T1'] = [1] # Time set for initial NACs
		
		##### Deterministic	parameters #####
		self.parameters = {}
		self.parameters['FC_ffpso'] = {(1,1):18, (1,2):21, (1,3):36,
										(2,1):26, (2,2):21, (2,3):20,
										(3,1):19, (3,2):11, (3,3):27} # Fixed cost for installing the connection between field f and FPSO fpso
		self.parameters['FCwell_f'] = {1:40, 2:40, 3:40} # Fixed cost for drilling a well in field f
		self.parameters['FCFPSO_fpso'] = {1:200, 2:200, 3:200} # Fixed capital cost for installing FPSO fpso
		self.parameters['VCliq_fpso'] = {1:1.5, 2:1.5, 3:1.5} # Variable capital cost for installing or expanding the liquid (oil and water) capacity of FPSO
		self.parameters['VCgas_fpso'] = {1:1.6, 2:1.5, 3:1.5} # Variable capital cost for installing or expanding the gas capacity of FPSO
		self.parameters['OCliq_rf'] = {1:0.2} # Operating cost for unit liquid produced in ringfence rf
		self.parameters['OCgas_rf'] = {1:0.1} # Operating cost for unit gas produced in ringfence rf
		self.parameters['ftax_rf'] = {1:0.1} # Income tax rate for ringfence rf
		self.parameters['fPO_rfi'] = {(1,1):0.5} # Profit oil fraction in tier i for ringfence rf
		self.parameters['fCR_rf'] = {1:0.3} # Cost recovery ceiling fraction for ring fence rf
		self.parameters['Loil_rfi'] = {(1,1):0} # Lower threshold for profit oil in tier i for ringfence rf
		self.parameters['Uoil_rfi'] = {(1,1):10000} # Upper threshold for profit oil in tier i for ringfence rf
		self.parameters['alpha'] = 20 # Selling price of oil
		self.parameters['l1'] = 3 # Lead time for initial installation of a FPSO facility, 3
		self.parameters['l2'] = 1 # Lead time for expansion of a FPSO facility
		self.parameters['Uoil_fpso'] = {1:500, 2:500, 3:500} # Installation capacity for oil in FPSO
		self.parameters['Uliq_fpso'] = {1:500, 2:500, 3:500} # Installation capacity for liquid in FPSO
		self.parameters['Ugas_fpso'] = {1:500, 2:500, 3:500} # Installation capacity for gas in FPSO
		self.parameters['myu'] = 0.9 # Expanded capacity must be less than myu*Installed capacity
		self.parameters['UIwell'] = 10 # The number of wells that can be drilled over all fields at t
		self.parameters['UNwell_f'] = {1:17,2:17,3:17} # The number of wells that can be drilled at field f
		self.parameters['epsilon'] = 0.02 # Required oil production percentage to judge field f has started production
		
		self.parameters['a_oil_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter a's for oil deliverability
		self.parameters['b_oil_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter b's for oil deliverability
		self.parameters['c_oil_ffpso'] = {(1,1):-14.5,(1,2):-15,(1,3):-15.5,(2,1):-10.5,(2,2):-11,(2,3):-11.5,(3,1):-7.5,(3,2):-8,(3,3):-8.5} # Model parameter c's for oil deliverability
		self.parameters['d_oil_ffpso'] = {(1,1):14.5,(1,2):15,(1,3):15.5,(2,1):10.5,(2,2):11,(2,3):11.5,(3,1):7.5,(3,2):8,(3,3):8.5} # Model parameter d's for oil deliverability
		self.parameters['a_wor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter a's for water-oil ratio
		self.parameters['b_wor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter b's for water-oil ratio
		self.parameters['c_wor_ffpso'] = {(1,1):1,(1,2):1.2,(1,3):1.4,(2,1):2.3,(2,2):2.5,(2,3):2.7,(3,1):3.8,(3,2):4,(3,3):4.2} # Model parameter c's for water-oil ratio
		self.parameters['d_wor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter d's for water-oil ratio
		self.parameters['a_gor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter a's for gas-oil ratio
		self.parameters['b_gor_ffpso'] = {(1,1):0,(1,2):0,(1,3):0,(2,1):0,(2,2):0,(2,3):0,(3,1):0,(3,2):0,(3,3):0} # Model parameter b's for gas-oil ratio
		self.parameters['c_gor_ffpso'] = {(1,1):0.15,(1,2):0.1,(1,3):0.1,(2,1):0.1,(2,2):0.3,(2,3):0,(3,1):0.2,(3,2):0.2,(3,3):-0.05} # Model parameter c's for gas-oil ratio
		self.parameters['d_gor_ffpso'] = {(1,1):0.65,(1,2):0.75,(1,3):0.85,(2,1):0.8,(2,2):0.7,(2,3):0.9,(3,1):0.75,(3,2):0.8,(3,3):0.95} # Model parameter d's for gas-oil ratio
		
		DR = 0.02 # Discount rate
		self.parameters['dis_t'] = {}
		for t in self.sets['T']:
			self.parameters['dis_t'][t] = (1 + DR) ** (1 - t) # Discount Factor
		self.parameters['delta'] = 1 # number of days in a time period t
		# self.parameters['Big_M'] = 100000
		# self.parameters['Big_U'] = 100000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['FieldSize'] = {1:{1:57,2:403}, 2:{1:80,2:560}, 3:{1:125,2:875}} # Uncertain recoverable oil volume (field size), {1:57,2:403}
		
		self.uncertain['alpha_o_fs'] = {(1,1):0.75,(1,2):0.75,(1,3):0.75,(1,4):0.75,(1,5):1.25,(1,6):1.25,(1,7):1.25,(1,8):1.25,
										(2,1):0.75,(2,2):0.75,(2,3):1.25,(2,4):1.25,(2,5):0.75,(2,6):0.75,(2,7):1.25,(2,8):1.25,
										(3,1):0.75,(3,2):1.25,(3,3):0.75,(3,4):1.25,(3,5):0.75,(3,6):1.25,(3,7):0.75,(3,8):1.25} # Uncertainty of oil deliverability
		self.uncertain['alpha_wc_fs'] = {(1,1):0.75,(1,2):0.75,(1,3):0.75,(1,4):0.75,(1,5):1.25,(1,6):1.25,(1,7):1.25,(1,8):1.25,
										(2,1):0.75,(2,2):0.75,(2,3):1.25,(2,4):1.25,(2,5):0.75,(2,6):0.75,(2,7):1.25,(2,8):1.25,
										(3,1):0.75,(3,2):1.25,(3,3):0.75,(3,4):1.25,(3,5):0.75,(3,6):1.25,(3,7):0.75,(3,8):1.25} # Uncertainty of water-oil ratio
		self.uncertain['alpha_gc_fs'] = {(1,1):0.75,(1,2):0.75,(1,3):0.75,(1,4):0.75,(1,5):1.25,(1,6):1.25,(1,7):1.25,(1,8):1.25,
										(2,1):0.75,(2,2):0.75,(2,3):1.25,(2,4):1.25,(2,5):0.75,(2,6):0.75,(2,7):1.25,(2,8):1.25,
										(3,1):0.75,(3,2):1.25,(3,3):0.75,(3,4):1.25,(3,5):0.75,(3,6):1.25,(3,7):0.75,(3,8):1.25} # Uncertainty of gas-oil ratio
		self.uncertain['N1_f'] = {1:3, 2:4, 3:4} # Required number of wells to reveal uncertainty
		self.uncertain['N2_f'] = {1:1, 2:1, 3:1} # Required years of production to reveal uncertainty
		
		##### Probability #####
		self.uncertain['FieldSize_prob'] = {1:{1:0.5,2:0.5}, 2:{1:0.5,2:0.5}, 3:{1:0.5,2:0.5}}
