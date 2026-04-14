class N11E5T12S4():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['Omega_E'] = [1,2,3,4,5] # two-year epochs (total 10 years)
		self.sets['Omega_N'] = [1,2,3,4,5,6,7,8,9,10,11] # Buses
		self.sets['Omega_O'] = [1,2] # Conventional investment alternatives
		self.sets['Omega_L'] = ['1_2','2_3','3_4','3_5','5_6','6_7','6_8','8_9','9_10','9_11'] # Lines
		self.sets['Omega_T'] = [1,2,3,4,5,6,7,8,9,10,11,12] # Demand periods
		self.sets['Omega_G'] = [1,2] # all generation units and substation (typo?)
		self.sets['Omega_DG'] = [1] # DG units, indexed g*
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD'] = 50 # investment cost for DSR (Demand Side Response), (￡/bus)
		self.parameters['gammaL_o'] = {1:80, 2:120} # Investment cost for line upgrade with o, (￡/line)
		IR = 0.02 # Discount rate
		self.parameters['rI_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['rI_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['ro_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['ro_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['kappaL_o'] = {1:1, 2:1} # Time required for the upgraded line to become operational corresponding to o
		self.parameters['kappaD'] = 0 # Time for commissioning DSR scheme
		self.parameters['Q_o'] = {1:50, 2:100} # Capacity addition by upgrading line corresponding to o, kW
		self.parameters['Dmax_n'] = {1:0,2:25,3:0,4:25,5:25,6:0,7:25,8:25,9:0,10:25,11:0} # Max load can be shifted at bus n, kW
		self.parameters['L_e'] = {1:60,2:90,3:100,4:110,5:115} # Peak load at growing buses corresponding to e, kW
		self.parameters['GB'] = [5,8] # Buses where peak load grows
		self.parameters['NGB'] = [2,4,7,10] # Buses where peak load does not grow
		self.parameters['PeakTime'] = [1,2,6] # time at peak Load in Omega_T
		self.parameters['OffR'] = 0.5 # Off-peak ratio to peak time
		self.parameters['delta'] = 6 # Length of demand periods where power shifts must balance
		self.parameters['w'] = 1 # weighing of time period
		self.parameters['zeta_g'] = {1:1, 2:1} # Max output (%) of g, zeta = 1 if g refers to main power source
		self.parameters['Kwind_e'] = {1:0,2:50,3:60,4:70,5:60} # Capacity of DG wind unit (g=1, g*=1), kW
		self.parameters['Kmain_e'] = {1:10000,2:10000,3:10000,4:10000,5:10000} # Installed capacity of main generator (g=2), kW
		self.parameters['Fini_l'] = {'1_2':360,'2_3':360,'3_4':80,'3_5':240,'5_6':240,'6_7':80,'6_8':120,'8_9':80,'9_10':80,'9_11':80} # Initial capacity of line l, kW
		self.parameters['Connection_ng'] = {(1,2):1,(11,1):1}
		self.parameters['Connection_nl'] = {(1,'1_2'):-1,(2,'1_2'):1,(2,'2_3'):-1,(3,'2_3'):1,(3,'3_4'):-1,(3,'3_5'):-1,(4,'3_4'):1,(5,'3_5'):1,(5,'5_6'):-1,
											(6,'5_6'):1,(6,'6_7'):-1,(6,'6_8'):-1,(7,'6_7'):1,(8,'6_8'):1,(8,'8_9'):-1,(9,'8_9'):1,(9,'9_10'):-1,(9,'9_11'):1,(10,'9_10'):1,(11,'9_11'):-1}
		self.parameters['cDSR'] = 10*0.001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		self.parameters['cDG'] = 100*0.001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		
		##### Parameters for complete recouse #####
		self.parameters['cDR'] = 10000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['f_n'] = {1:{1:0}, 2:{1:0.2}, 3:{1:0}, 4:{1:0.2},5:{1:0.5,2:0.1},6:{1:0},7:{1:0.2},8:{1:0.5,2:0.1},9:{1:0},10:{1:0.2},11:{1:0}} # Consumer participations
		
		##### Probability #####
		self.uncertain['f_n_prob'] = {1:{1:1}, 2:{1:1}, 3:{1:1}, 4:{1:1},5:{1:0.7,2:0.3},6:{1:1},7:{1:1},8:{1:0.7,2:0.3},9:{1:1},10:{1:1},11:{1:1}}
		

class N11E5T720S4():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['Omega_E'] = [1,2,3,4,5] # two-year epochs (total 10 years)
		self.sets['Omega_N'] = [1,2,3,4,5,6,7,8,9,10,11] # Buses
		self.sets['Omega_O'] = [1,2] # Conventional investment alternatives
		self.sets['Omega_L'] = ['1_2','2_3','3_4','3_5','5_6','6_7','6_8','8_9','9_10','9_11'] # Lines
		self.sets['Omega_T'] = list(range(1,720+1)) # Demand periods
		self.sets['Omega_G'] = [1,2] # all generation units and substation (typo?)
		self.sets['Omega_DG'] = [1] # DG units, indexed g*
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD'] = 50 # investment cost for DSR (Demand Side Response), (￡/bus)
		self.parameters['gammaL_o'] = {1:80, 2:120} # Investment cost for line upgrade with o, (￡/line)
		IR = 0.02 # Discount rate
		self.parameters['rI_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['rI_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['ro_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['ro_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['kappaL_o'] = {1:1, 2:1} # Time required for the upgraded line to become operational corresponding to o
		self.parameters['kappaD'] = 0 # Time for commissioning DSR scheme
		self.parameters['Q_o'] = {1:50, 2:100} # Capacity addition by upgrading line corresponding to o, kW
		self.parameters['Dmax_n'] = {1:0,2:25,3:0,4:25,5:25,6:0,7:25,8:25,9:0,10:25,11:0} # Max load can be shifted at bus n, kW
		self.parameters['L_e'] = {1:60,2:90,3:100,4:110,5:115} # Peak load at growing buses corresponding to e, kW
		self.parameters['GB'] = [5,8] # Buses where peak load grows
		self.parameters['NGB'] = [2,4,7,10] # Buses where peak load does not grow
		self.parameters['PeakTime'] = [8,9,10,11,12,13,14,15,16,17] # time at peak Load in Omega_T
		self.parameters['OffR'] = 0.5 # Off-peak ratio to peak time
		self.parameters['delta'] = 24 # Length of demand periods where power shifts must balance
		self.parameters['w'] = 1 # weighing of time period
		self.parameters['zeta_g'] = {1:1, 2:1} # Max output (%) of g, zeta = 1 if g refers to main power source
		self.parameters['Kwind_e'] = {1:0,2:50,3:60,4:70,5:60} # Capacity of DG wind unit (g=1, g*=1), kW
		self.parameters['Kmain_e'] = {1:10000,2:10000,3:10000,4:10000,5:10000} # Installed capacity of main generator (g=2), kW
		self.parameters['Fini_l'] = {'1_2':360,'2_3':360,'3_4':80,'3_5':240,'5_6':240,'6_7':80,'6_8':120,'8_9':80,'9_10':80,'9_11':80} # Initial capacity of line l, kW
		self.parameters['Connection_ng'] = {(1,2):1,(11,1):1}
		self.parameters['Connection_nl'] = {(1,'1_2'):-1,(2,'1_2'):1,(2,'2_3'):-1,(3,'2_3'):1,(3,'3_4'):-1,(3,'3_5'):-1,(4,'3_4'):1,(5,'3_5'):1,(5,'5_6'):-1,
											(6,'5_6'):1,(6,'6_7'):-1,(6,'6_8'):-1,(7,'6_7'):1,(8,'6_8'):1,(8,'8_9'):-1,(9,'8_9'):1,(9,'9_10'):-1,(9,'9_11'):1,(10,'9_10'):1,(11,'9_11'):-1}
		self.parameters['cDSR'] = 10*0.000001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		self.parameters['cDG'] = 100*0.001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		
		##### Parameters for complete recouse #####
		self.parameters['cDR'] = 10000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['f_n'] = {1:{1:0}, 2:{1:0.2}, 3:{1:0}, 4:{1:0.2},5:{1:0.5,2:0.1},6:{1:0},7:{1:0.2},8:{1:0.5,2:0.1},9:{1:0},10:{1:0.2},11:{1:0}} # Consumer participations
		
		##### Probability #####
		self.uncertain['f_n_prob'] = {1:{1:1}, 2:{1:1}, 3:{1:1}, 4:{1:1},5:{1:0.7,2:0.3},6:{1:1},7:{1:1},8:{1:0.7,2:0.3},9:{1:1},10:{1:1},11:{1:1}}

class N11E5T1440S4():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['Omega_E'] = [1,2,3,4,5] # two-year epochs (total 10 years)
		self.sets['Omega_N'] = [1,2,3,4,5,6,7,8,9,10,11] # Buses
		self.sets['Omega_O'] = [1,2] # Conventional investment alternatives
		self.sets['Omega_L'] = ['1_2','2_3','3_4','3_5','5_6','6_7','6_8','8_9','9_10','9_11'] # Lines
		self.sets['Omega_T'] = list(range(1,1440+1)) # Demand periods
		self.sets['Omega_G'] = [1,2] # all generation units and substation (typo?)
		self.sets['Omega_DG'] = [1] # DG units, indexed g*
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD'] = 50 # investment cost for DSR (Demand Side Response), (￡/bus)
		self.parameters['gammaL_o'] = {1:80, 2:120} # Investment cost for line upgrade with o, (￡/line)
		IR = 0.02 # Discount rate
		self.parameters['rI_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['rI_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['ro_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['ro_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['kappaL_o'] = {1:1, 2:1} # Time required for the upgraded line to become operational corresponding to o
		self.parameters['kappaD'] = 0 # Time for commissioning DSR scheme
		self.parameters['Q_o'] = {1:50, 2:100} # Capacity addition by upgrading line corresponding to o, kW
		self.parameters['Dmax_n'] = {1:0,2:25,3:0,4:25,5:25,6:0,7:25,8:25,9:0,10:25,11:0} # Max load can be shifted at bus n, kW
		self.parameters['L_e'] = {1:60,2:90,3:100,4:110,5:115} # Peak load at growing buses corresponding to e, kW
		self.parameters['GB'] = [5,8] # Buses where peak load grows
		self.parameters['NGB'] = [2,4,7,10] # Buses where peak load does not grow
		self.parameters['PeakTime'] = [8,9,10,11,12,13,14,15,16,17] # time at peak Load in Omega_T
		self.parameters['OffR'] = 0.5 # Off-peak ratio to peak time
		self.parameters['delta'] = 24 # Length of demand periods where power shifts must balance
		self.parameters['w'] = 1 # weighing of time period
		self.parameters['zeta_g'] = {1:1, 2:1} # Max output (%) of g, zeta = 1 if g refers to main power source
		self.parameters['Kwind_e'] = {1:0,2:50,3:60,4:70,5:60} # Capacity of DG wind unit (g=1, g*=1), kW
		self.parameters['Kmain_e'] = {1:10000,2:10000,3:10000,4:10000,5:10000} # Installed capacity of main generator (g=2), kW
		self.parameters['Fini_l'] = {'1_2':360,'2_3':360,'3_4':80,'3_5':240,'5_6':240,'6_7':80,'6_8':120,'8_9':80,'9_10':80,'9_11':80} # Initial capacity of line l, kW
		self.parameters['Connection_ng'] = {(1,2):1,(11,1):1}
		self.parameters['Connection_nl'] = {(1,'1_2'):-1,(2,'1_2'):1,(2,'2_3'):-1,(3,'2_3'):1,(3,'3_4'):-1,(3,'3_5'):-1,(4,'3_4'):1,(5,'3_5'):1,(5,'5_6'):-1,
											(6,'5_6'):1,(6,'6_7'):-1,(6,'6_8'):-1,(7,'6_7'):1,(8,'6_8'):1,(8,'8_9'):-1,(9,'8_9'):1,(9,'9_10'):-1,(9,'9_11'):1,(10,'9_10'):1,(11,'9_11'):-1}
		self.parameters['cDSR'] = 10*0.000001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		self.parameters['cDG'] = 100*0.001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		
		##### Parameters for complete recouse #####
		self.parameters['cDR'] = 10000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['f_n'] = {1:{1:0}, 2:{1:0.2}, 3:{1:0}, 4:{1:0.2},5:{1:0.5,2:0.1},6:{1:0},7:{1:0.2},8:{1:0.5,2:0.1},9:{1:0},10:{1:0.2},11:{1:0}} # Consumer participations
		
		##### Probability #####
		self.uncertain['f_n_prob'] = {1:{1:1}, 2:{1:1}, 3:{1:1}, 4:{1:1},5:{1:0.7,2:0.3},6:{1:1},7:{1:1},8:{1:0.7,2:0.3},9:{1:1},10:{1:1},11:{1:1}}

class N11E5T2160S4():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['Omega_E'] = [1,2,3,4,5] # two-year epochs (total 10 years)
		self.sets['Omega_N'] = [1,2,3,4,5,6,7,8,9,10,11] # Buses
		self.sets['Omega_O'] = [1,2] # Conventional investment alternatives
		self.sets['Omega_L'] = ['1_2','2_3','3_4','3_5','5_6','6_7','6_8','8_9','9_10','9_11'] # Lines
		self.sets['Omega_T'] = list(range(1,2160+1)) # Demand periods
		self.sets['Omega_G'] = [1,2] # all generation units and substation (typo?)
		self.sets['Omega_DG'] = [1] # DG units, indexed g*
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD'] = 50 # investment cost for DSR (Demand Side Response), (￡/bus)
		self.parameters['gammaL_o'] = {1:80, 2:120} # Investment cost for line upgrade with o, (￡/line)
		IR = 0.02 # Discount rate
		self.parameters['rI_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['rI_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['ro_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['ro_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['kappaL_o'] = {1:1, 2:1} # Time required for the upgraded line to become operational corresponding to o
		self.parameters['kappaD'] = 0 # Time for commissioning DSR scheme
		self.parameters['Q_o'] = {1:50, 2:100} # Capacity addition by upgrading line corresponding to o, kW
		self.parameters['Dmax_n'] = {1:0,2:25,3:0,4:25,5:25,6:0,7:25,8:25,9:0,10:25,11:0} # Max load can be shifted at bus n, kW
		self.parameters['L_e'] = {1:60,2:90,3:100,4:110,5:115} # Peak load at growing buses corresponding to e, kW
		self.parameters['GB'] = [5,8] # Buses where peak load grows
		self.parameters['NGB'] = [2,4,7,10] # Buses where peak load does not grow
		self.parameters['PeakTime'] = [8,9,10,11,12,13,14,15,16,17] # time at peak Load in Omega_T
		self.parameters['OffR'] = 0.5 # Off-peak ratio to peak time
		self.parameters['delta'] = 24 # Length of demand periods where power shifts must balance
		self.parameters['w'] = 1 # weighing of time period
		self.parameters['zeta_g'] = {1:1, 2:1} # Max output (%) of g, zeta = 1 if g refers to main power source
		self.parameters['Kwind_e'] = {1:0,2:50,3:60,4:70,5:60} # Capacity of DG wind unit (g=1, g*=1), kW
		self.parameters['Kmain_e'] = {1:10000,2:10000,3:10000,4:10000,5:10000} # Installed capacity of main generator (g=2), kW
		self.parameters['Fini_l'] = {'1_2':360,'2_3':360,'3_4':80,'3_5':240,'5_6':240,'6_7':80,'6_8':120,'8_9':80,'9_10':80,'9_11':80} # Initial capacity of line l, kW
		self.parameters['Connection_ng'] = {(1,2):1,(11,1):1}
		self.parameters['Connection_nl'] = {(1,'1_2'):-1,(2,'1_2'):1,(2,'2_3'):-1,(3,'2_3'):1,(3,'3_4'):-1,(3,'3_5'):-1,(4,'3_4'):1,(5,'3_5'):1,(5,'5_6'):-1,
											(6,'5_6'):1,(6,'6_7'):-1,(6,'6_8'):-1,(7,'6_7'):1,(8,'6_8'):1,(8,'8_9'):-1,(9,'8_9'):1,(9,'9_10'):-1,(9,'9_11'):1,(10,'9_10'):1,(11,'9_11'):-1}
		self.parameters['cDSR'] = 10*0.000001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		self.parameters['cDG'] = 100*0.001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		
		##### Parameters for complete recouse #####
		self.parameters['cDR'] = 10000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['f_n'] = {1:{1:0}, 2:{1:0.2}, 3:{1:0}, 4:{1:0.2},5:{1:0.5,2:0.1},6:{1:0},7:{1:0.2},8:{1:0.5,2:0.1},9:{1:0},10:{1:0.2},11:{1:0}} # Consumer participations
		
		##### Probability #####
		self.uncertain['f_n_prob'] = {1:{1:1}, 2:{1:1}, 3:{1:1}, 4:{1:1},5:{1:0.7,2:0.3},6:{1:1},7:{1:1},8:{1:0.7,2:0.3},9:{1:1},10:{1:1},11:{1:1}}

class N11E5T2880S4():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['Omega_E'] = [1,2,3,4,5] # two-year epochs (total 10 years)
		self.sets['Omega_N'] = [1,2,3,4,5,6,7,8,9,10,11] # Buses
		self.sets['Omega_O'] = [1,2] # Conventional investment alternatives
		self.sets['Omega_L'] = ['1_2','2_3','3_4','3_5','5_6','6_7','6_8','8_9','9_10','9_11'] # Lines
		self.sets['Omega_T'] = list(range(1,2880+1)) # Demand periods
		self.sets['Omega_G'] = [1,2] # all generation units and substation (typo?)
		self.sets['Omega_DG'] = [1] # DG units, indexed g*
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD'] = 50 # investment cost for DSR (Demand Side Response), (￡/bus)
		self.parameters['gammaL_o'] = {1:80, 2:120} # Investment cost for line upgrade with o, (￡/line)
		IR = 0.02 # Discount rate
		self.parameters['rI_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['rI_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['ro_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['ro_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['kappaL_o'] = {1:1, 2:1} # Time required for the upgraded line to become operational corresponding to o
		self.parameters['kappaD'] = 0 # Time for commissioning DSR scheme
		self.parameters['Q_o'] = {1:50, 2:100} # Capacity addition by upgrading line corresponding to o, kW
		self.parameters['Dmax_n'] = {1:0,2:25,3:0,4:25,5:25,6:0,7:25,8:25,9:0,10:25,11:0} # Max load can be shifted at bus n, kW
		self.parameters['L_e'] = {1:60,2:90,3:100,4:110,5:115} # Peak load at growing buses corresponding to e, kW
		self.parameters['GB'] = [5,8] # Buses where peak load grows
		self.parameters['NGB'] = [2,4,7,10] # Buses where peak load does not grow
		self.parameters['PeakTime'] = [8,9,10,11,12,13,14,15,16,17] # time at peak Load in Omega_T
		self.parameters['OffR'] = 0.5 # Off-peak ratio to peak time
		self.parameters['delta'] = 24 # Length of demand periods where power shifts must balance
		self.parameters['w'] = 1 # weighing of time period
		self.parameters['zeta_g'] = {1:1, 2:1} # Max output (%) of g, zeta = 1 if g refers to main power source
		self.parameters['Kwind_e'] = {1:0,2:50,3:60,4:70,5:60} # Capacity of DG wind unit (g=1, g*=1), kW
		self.parameters['Kmain_e'] = {1:10000,2:10000,3:10000,4:10000,5:10000} # Installed capacity of main generator (g=2), kW
		self.parameters['Fini_l'] = {'1_2':360,'2_3':360,'3_4':80,'3_5':240,'5_6':240,'6_7':80,'6_8':120,'8_9':80,'9_10':80,'9_11':80} # Initial capacity of line l, kW
		self.parameters['Connection_ng'] = {(1,2):1,(11,1):1}
		self.parameters['Connection_nl'] = {(1,'1_2'):-1,(2,'1_2'):1,(2,'2_3'):-1,(3,'2_3'):1,(3,'3_4'):-1,(3,'3_5'):-1,(4,'3_4'):1,(5,'3_5'):1,(5,'5_6'):-1,
											(6,'5_6'):1,(6,'6_7'):-1,(6,'6_8'):-1,(7,'6_7'):1,(8,'6_8'):1,(8,'8_9'):-1,(9,'8_9'):1,(9,'9_10'):-1,(9,'9_11'):1,(10,'9_10'):1,(11,'9_11'):-1}
		self.parameters['cDSR'] = 10*0.000001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		self.parameters['cDG'] = 100*0.001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		
		##### Parameters for complete recouse #####
		self.parameters['cDR'] = 10000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['f_n'] = {1:{1:0}, 2:{1:0.2}, 3:{1:0}, 4:{1:0.2},5:{1:0.5,2:0.1},6:{1:0},7:{1:0.2},8:{1:0.5,2:0.1},9:{1:0},10:{1:0.2},11:{1:0}} # Consumer participations
		
		##### Probability #####
		self.uncertain['f_n_prob'] = {1:{1:1}, 2:{1:1}, 3:{1:1}, 4:{1:1},5:{1:0.7,2:0.3},6:{1:1},7:{1:1},8:{1:0.7,2:0.3},9:{1:1},10:{1:1},11:{1:1}}

class N11E5T3600S4():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['Omega_E'] = [1,2,3,4,5] # two-year epochs (total 10 years)
		self.sets['Omega_N'] = [1,2,3,4,5,6,7,8,9,10,11] # Buses
		self.sets['Omega_O'] = [1,2] # Conventional investment alternatives
		self.sets['Omega_L'] = ['1_2','2_3','3_4','3_5','5_6','6_7','6_8','8_9','9_10','9_11'] # Lines
		self.sets['Omega_T'] = list(range(1,3600+1)) # Demand periods
		self.sets['Omega_G'] = [1,2] # all generation units and substation (typo?)
		self.sets['Omega_DG'] = [1] # DG units, indexed g*
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD'] = 50 # investment cost for DSR (Demand Side Response), (￡/bus)
		self.parameters['gammaL_o'] = {1:80, 2:120} # Investment cost for line upgrade with o, (￡/line)
		IR = 0.02 # Discount rate
		self.parameters['rI_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['rI_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['ro_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['ro_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['kappaL_o'] = {1:1, 2:1} # Time required for the upgraded line to become operational corresponding to o
		self.parameters['kappaD'] = 0 # Time for commissioning DSR scheme
		self.parameters['Q_o'] = {1:50, 2:100} # Capacity addition by upgrading line corresponding to o, kW
		self.parameters['Dmax_n'] = {1:0,2:25,3:0,4:25,5:25,6:0,7:25,8:25,9:0,10:25,11:0} # Max load can be shifted at bus n, kW
		self.parameters['L_e'] = {1:60,2:90,3:100,4:110,5:115} # Peak load at growing buses corresponding to e, kW
		self.parameters['GB'] = [5,8] # Buses where peak load grows
		self.parameters['NGB'] = [2,4,7,10] # Buses where peak load does not grow
		self.parameters['PeakTime'] = [8,9,10,11,12,13,14,15,16,17] # time at peak Load in Omega_T
		self.parameters['OffR'] = 0.5 # Off-peak ratio to peak time
		self.parameters['delta'] = 24 # Length of demand periods where power shifts must balance
		self.parameters['w'] = 1 # weighing of time period
		self.parameters['zeta_g'] = {1:1, 2:1} # Max output (%) of g, zeta = 1 if g refers to main power source
		self.parameters['Kwind_e'] = {1:0,2:50,3:60,4:70,5:60} # Capacity of DG wind unit (g=1, g*=1), kW
		self.parameters['Kmain_e'] = {1:10000,2:10000,3:10000,4:10000,5:10000} # Installed capacity of main generator (g=2), kW
		self.parameters['Fini_l'] = {'1_2':360,'2_3':360,'3_4':80,'3_5':240,'5_6':240,'6_7':80,'6_8':120,'8_9':80,'9_10':80,'9_11':80} # Initial capacity of line l, kW
		self.parameters['Connection_ng'] = {(1,2):1,(11,1):1}
		self.parameters['Connection_nl'] = {(1,'1_2'):-1,(2,'1_2'):1,(2,'2_3'):-1,(3,'2_3'):1,(3,'3_4'):-1,(3,'3_5'):-1,(4,'3_4'):1,(5,'3_5'):1,(5,'5_6'):-1,
											(6,'5_6'):1,(6,'6_7'):-1,(6,'6_8'):-1,(7,'6_7'):1,(8,'6_8'):1,(8,'8_9'):-1,(9,'8_9'):1,(9,'9_10'):-1,(9,'9_11'):1,(10,'9_10'):1,(11,'9_11'):-1}
		self.parameters['cDSR'] = 10*0.000001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		self.parameters['cDG'] = 100*0.001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		
		##### Parameters for complete recouse #####
		self.parameters['cDR'] = 1000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['f_n'] = {1:{1:0}, 2:{1:0.2}, 3:{1:0}, 4:{1:0.2},5:{1:0.5,2:0.1},6:{1:0},7:{1:0.2},8:{1:0.5,2:0.1},9:{1:0},10:{1:0.2},11:{1:0}} # Consumer participations
		
		##### Probability #####
		self.uncertain['f_n_prob'] = {1:{1:1}, 2:{1:1}, 3:{1:1}, 4:{1:1},5:{1:0.7,2:0.3},6:{1:1},7:{1:1},8:{1:0.7,2:0.3},9:{1:1},10:{1:1},11:{1:1}}

class N11E5T4320S4():
	def __init__(self):
		
		### Sets ###
		self.sets = {}
		self.sets['Omega_E'] = [1,2,3,4,5] # two-year epochs (total 10 years)
		self.sets['Omega_N'] = [1,2,3,4,5,6,7,8,9,10,11] # Buses
		self.sets['Omega_O'] = [1,2] # Conventional investment alternatives
		self.sets['Omega_L'] = ['1_2','2_3','3_4','3_5','5_6','6_7','6_8','8_9','9_10','9_11'] # Lines
		self.sets['Omega_T'] = list(range(1,4320+1)) # Demand periods
		self.sets['Omega_G'] = [1,2] # all generation units and substation (typo?)
		self.sets['Omega_DG'] = [1] # DG units, indexed g*
		
		### Parameters ###
		self.parameters = {}
		self.parameters['gammaD'] = 50 # investment cost for DSR (Demand Side Response), (￡/bus)
		self.parameters['gammaL_o'] = {1:80, 2:120} # Investment cost for line upgrade with o, (￡/line)
		IR = 0.02 # Discount rate
		self.parameters['rI_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['rI_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['ro_e'] = {}
		for e in self.sets['Omega_E']:
			self.parameters['ro_e'][e] = (1 + IR) ** (1 - e) # Discounting Factor
		self.parameters['kappaL_o'] = {1:1, 2:1} # Time required for the upgraded line to become operational corresponding to o
		self.parameters['kappaD'] = 0 # Time for commissioning DSR scheme
		self.parameters['Q_o'] = {1:50, 2:100} # Capacity addition by upgrading line corresponding to o, kW
		self.parameters['Dmax_n'] = {1:0,2:25,3:0,4:25,5:25,6:0,7:25,8:25,9:0,10:25,11:0} # Max load can be shifted at bus n, kW
		self.parameters['L_e'] = {1:60,2:90,3:100,4:110,5:115} # Peak load at growing buses corresponding to e, kW
		self.parameters['GB'] = [5,8] # Buses where peak load grows
		self.parameters['NGB'] = [2,4,7,10] # Buses where peak load does not grow
		self.parameters['PeakTime'] = [8,9,10,11,12,13,14,15,16,17] # time at peak Load in Omega_T
		self.parameters['OffR'] = 0.5 # Off-peak ratio to peak time
		self.parameters['delta'] = 24 # Length of demand periods where power shifts must balance
		self.parameters['w'] = 1 # weighing of time period
		self.parameters['zeta_g'] = {1:1, 2:1} # Max output (%) of g, zeta = 1 if g refers to main power source
		self.parameters['Kwind_e'] = {1:0,2:50,3:60,4:70,5:60} # Capacity of DG wind unit (g=1, g*=1), kW
		self.parameters['Kmain_e'] = {1:10000,2:10000,3:10000,4:10000,5:10000} # Installed capacity of main generator (g=2), kW
		self.parameters['Fini_l'] = {'1_2':360,'2_3':360,'3_4':80,'3_5':240,'5_6':240,'6_7':80,'6_8':120,'8_9':80,'9_10':80,'9_11':80} # Initial capacity of line l, kW
		self.parameters['Connection_ng'] = {(1,2):1,(11,1):1}
		self.parameters['Connection_nl'] = {(1,'1_2'):-1,(2,'1_2'):1,(2,'2_3'):-1,(3,'2_3'):1,(3,'3_4'):-1,(3,'3_5'):-1,(4,'3_4'):1,(5,'3_5'):1,(5,'5_6'):-1,
											(6,'5_6'):1,(6,'6_7'):-1,(6,'6_8'):-1,(7,'6_7'):1,(8,'6_8'):1,(8,'8_9'):-1,(9,'8_9'):1,(9,'9_10'):-1,(9,'9_11'):1,(10,'9_10'):1,(11,'9_11'):-1}
		self.parameters['cDSR'] = 10*0.000001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		self.parameters['cDG'] = 100*0.001 # ￡/MWh? should be ￡/MW. From ￡/MW to ￡/kW
		
		##### Parameters for complete recouse #####
		self.parameters['cDR'] = 10000
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['f_n'] = {1:{1:0}, 2:{1:0.2}, 3:{1:0}, 4:{1:0.2},5:{1:0.5,2:0.1},6:{1:0},7:{1:0.2},8:{1:0.5,2:0.1},9:{1:0},10:{1:0.2},11:{1:0}} # Consumer participations
		
		##### Probability #####
		self.uncertain['f_n_prob'] = {1:{1:1}, 2:{1:1}, 3:{1:1}, 4:{1:1},5:{1:0.7,2:0.3},6:{1:1},7:{1:1},8:{1:0.7,2:0.3},9:{1:1},10:{1:1},11:{1:1}}