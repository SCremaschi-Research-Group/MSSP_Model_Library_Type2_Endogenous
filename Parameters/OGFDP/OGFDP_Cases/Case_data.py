class WP6T15S3(): # The size and deliverability of F is uncertain, Example1_2004
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['WP'] = ['A','B','C','D','E','F']
		self.sets['PP'] = ['PP']
		self.sets['T'] = range(1,16) # 1,16
		
		##### Parameters #####
		self.parameters = {}
		self.parameters['shrink'] = 0.01
		self.parameters['M_wp'] = {'A':80, 'B':80, 'C':70, 'D':40, 'E':58, 'F':60}
		self.parameters['M_pp'] = {'PP':194}
		self.parameters['M_wpwp'] ={('A','A'):0,('A','B'):0,('A','C'):0,('A','D'):0,('A','E'):0,('A','F'):0,
									('B','A'):0,('B','B'):0,('B','C'):0,('B','D'):0,('B','E'):0,('B','F'):0,
									('C','A'):0,('C','B'):0,('C','C'):0,('C','D'):0,('C','E'):0,('C','F'):0,
									('D','A'):0,('D','B'):40,('D','C'):0,('D','D'):0,('D','E'):0,('D','F'):0,
									('E','A'):0,('E','B'):0,('E','C'):0,('E','D'):0,('E','E'):0,('E','F'):0,
									('F','A'):0,('F','B'):0,('F','C'):0,('F','D'):0,('F','E'):0,('F','F'):0}
		self.parameters['M_wppp'] = {('A','PP'):80,('B','PP'):120,('C','PP'):70,('D','PP'):40,('E','PP'):58,('F','PP'):60}
		self.parameters['FCC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Fixed capital cost for Well Platform
		self.parameters['FCC_pp'] = {'PP':30} # Fixed capital cost for Production Platform
		self.parameters['FCC_wpwp'] =  {('A','A'):0, ('A','B'):0, ('A','C'):0, ('A','D'):0, ('A','E'):0, ('A','F'):0,
										('B','A'):0, ('B','B'):0, ('B','C'):0, ('B','D'):0, ('B','E'):0, ('B','F'):0,
										('C','A'):0, ('C','B'):0, ('C','C'):0, ('C','D'):0, ('C','E'):0, ('C','F'):0,
										('D','A'):0, ('D','B'):10, ('D','C'):0, ('D','D'):0, ('D','E'):0, ('D','F'):0,
										('E','A'):0, ('E','B'):0, ('E','C'):0, ('E','D'):0, ('E','E'):0, ('E','F'):0,
										('F','A'):0, ('F','B'):0, ('F','C'):0, ('F','D'):0, ('F','E'):0, ('F','F'):0}
		self.parameters['FCC_wppp'] = {('A','PP'):5, ('B','PP'):15, ('C','PP'):15, ('D','PP'):23, ('E','PP'):10, ('F','PP'):20}
		self.parameters['VCC_wp'] = {'A':100, 'B':100, 'C':100, 'D':100, 'E':100, 'F':100} # Variable capital cost for Well Platform
		self.parameters['VCC_pp'] = {'PP':300} # Variable capital cost for Production Platform
		self.parameters['FOC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Fixed operating cost for Well Platform
		self.parameters['FOC_pp'] = {'PP':30} # # Fixed operating cost for Production Platform
		self.parameters['VOC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Variable operating cost for Well Platform
		self.parameters['VOC_pp'] = {'PP':30} # # Variable operating cost for Production Platform
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Size'] = {'A':{'Deterministic':400},'B':{'Deterministic':400},'C':{'Deterministic':350},
								'D':{'Deterministic':200},'E':{'Deterministic':290},'F':{'Low':130,'Medium':300,'High':470}}
		self.uncertain['Deliv'] = {'A':{'Deterministic':130},'B':{'Deterministic':200},'C':{'Deterministic':100},
								'D':{'Deterministic':100},'E':{'Deterministic':130},'F':{'Deterministic':120}}
		
		##### Probability #####
		self.uncertain['Size_prob'] = {'A':{'Deterministic':1},'B':{'Deterministic':1},'C':{'Deterministic':1},
								'D':{'Deterministic':1},'E':{'Deterministic':1},'F':{'Low':0.3,'Medium':0.4,'High':0.3}}
		self.uncertain['Deliv_prob'] = {'A':{'Deterministic':1},'B':{'Deterministic':1},'C':{'Deterministic':1},
								'D':{'Deterministic':1},'E':{'Deterministic':1},'F':{'Deterministic':1}}

class WP6T15S9(): # The size and deliverability of F is uncertain, Example2_2004
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['WP'] = ['A','B','C','D','E','F']
		self.sets['PP'] = ['PP']
		self.sets['T'] = range(1,16) # 1,16
		
		##### Parameters #####
		self.parameters = {}
		self.parameters['shrink'] = 0.01
		self.parameters['M_wp'] = {'A':80, 'B':80, 'C':70, 'D':40, 'E':58, 'F':60}
		self.parameters['M_pp'] = {'PP':194}
		self.parameters['M_wpwp'] ={('A','A'):0,('A','B'):0,('A','C'):0,('A','D'):0,('A','E'):0,('A','F'):0,
									('B','A'):0,('B','B'):0,('B','C'):0,('B','D'):0,('B','E'):0,('B','F'):0,
									('C','A'):0,('C','B'):0,('C','C'):0,('C','D'):0,('C','E'):0,('C','F'):0,
									('D','A'):0,('D','B'):40,('D','C'):0,('D','D'):0,('D','E'):0,('D','F'):0,
									('E','A'):0,('E','B'):0,('E','C'):0,('E','D'):0,('E','E'):0,('E','F'):0,
									('F','A'):0,('F','B'):0,('F','C'):0,('F','D'):0,('F','E'):0,('F','F'):0}
		self.parameters['M_wppp'] = {('A','PP'):80,('B','PP'):120,('C','PP'):70,('D','PP'):40,('E','PP'):58,('F','PP'):60}
		self.parameters['FCC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Fixed capital cost for Well Platform
		self.parameters['FCC_pp'] = {'PP':30} # Fixed capital cost for Production Platform
		self.parameters['FCC_wpwp'] =  {('A','A'):0, ('A','B'):0, ('A','C'):0, ('A','D'):0, ('A','E'):0, ('A','F'):0,
										('B','A'):0, ('B','B'):0, ('B','C'):0, ('B','D'):0, ('B','E'):0, ('B','F'):0,
										('C','A'):0, ('C','B'):0, ('C','C'):0, ('C','D'):0, ('C','E'):0, ('C','F'):0,
										('D','A'):0, ('D','B'):10, ('D','C'):0, ('D','D'):0, ('D','E'):0, ('D','F'):0,
										('E','A'):0, ('E','B'):0, ('E','C'):0, ('E','D'):0, ('E','E'):0, ('E','F'):0,
										('F','A'):0, ('F','B'):0, ('F','C'):0, ('F','D'):0, ('F','E'):0, ('F','F'):0}
		self.parameters['FCC_wppp'] = {('A','PP'):5, ('B','PP'):15, ('C','PP'):15, ('D','PP'):23, ('E','PP'):10, ('F','PP'):20}
		self.parameters['VCC_wp'] = {'A':100, 'B':100, 'C':100, 'D':100, 'E':100, 'F':100} # Variable capital cost for Well Platform
		self.parameters['VCC_pp'] = {'PP':300} # Variable capital cost for Production Platform
		self.parameters['FOC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Fixed operating cost for Well Platform
		self.parameters['FOC_pp'] = {'PP':30} # # Fixed operating cost for Production Platform
		self.parameters['VOC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Variable operating cost for Well Platform
		self.parameters['VOC_pp'] = {'PP':30} # # Variable operating cost for Production Platform
		
		self.parameters['size'] = {'A':400,'B':400,'C':350,'D':200,'E':290} #, 'F':250 
		self.parameters['deliverbility'] = {'A':130,'B':200,'C':100,'D':100,'E':130} # , 'F':120 
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Size'] = {'A':{'Deterministic':400},'B':{'Deterministic':400},'C':{'Deterministic':350},
								'D':{'Deterministic':200},'E':{'Deterministic':290},'F':{'Low':130,'Medium':300,'High':470}}
		self.uncertain['Deliv'] = {'A':{'Deterministic':130},'B':{'Deterministic':200},'C':{'Deterministic':100},
								'D':{'Deterministic':100},'E':{'Deterministic':130},'F':{'Low':80,'Medium':130,'High':180}}
		
		##### Probability #####
		self.uncertain['Size_prob'] = {'A':{'Deterministic':1},'B':{'Deterministic':1},'C':{'Deterministic':1},
								'D':{'Deterministic':1},'E':{'Deterministic':1},'F':{'Low':0.3,'Medium':0.4,'High':0.3}}
		self.uncertain['Deliv_prob'] = {'A':{'Deterministic':1},'B':{'Deterministic':1},'C':{'Deterministic':1},
								'D':{'Deterministic':1},'E':{'Deterministic':1},'F':{'Low':0.3,'Medium':0.4,'High':0.3}}

class WP6T15S27(): # The size and deliverability of D are uncertain. The size of E is uncertain. 27 scenarios
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['WP'] = ['A','B','C','D','E','F']
		self.sets['PP'] = ['PP']
		self.sets['T'] = range(1,16) # 1,16
		
		##### Parameters #####
		self.parameters = {}
		self.parameters['shrink'] = 0.01
		self.parameters['M_wp'] = {'A':80, 'B':80, 'C':50, 'D':64, 'E':70, 'F':50}
		self.parameters['M_pp'] = {'PP':197}
		self.parameters['M_wpwp'] ={('A','A'):0,('A','B'):0,('A','C'):0,('A','D'):0,('A','E'):0,('A','F'):0,
									('B','A'):0,('B','B'):0,('B','C'):0,('B','D'):0,('B','E'):0,('B','F'):0,
									('C','A'):0,('C','B'):0,('C','C'):0,('C','D'):0,('C','E'):0,('C','F'):0,
									('D','A'):0,('D','B'):64,('D','C'):0,('D','D'):0,('D','E'):0,('D','F'):0,
									('E','A'):0,('E','B'):0,('E','C'):0,('E','D'):0,('E','E'):0,('E','F'):0,
									('F','A'):0,('F','B'):0,('F','C'):0,('F','D'):0,('F','E'):0,('F','F'):0}
		self.parameters['M_wppp'] = {('A','PP'):80,('B','PP'):144,('C','PP'):50,('D','PP'):64,('E','PP'):70,('F','PP'):50}
		self.parameters['FCC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Fixed capital cost for Well Platform
		self.parameters['FCC_pp'] = {'PP':30} # Fixed capital cost for Production Platform
		self.parameters['FCC_wpwp'] =  {('A','A'):0, ('A','B'):0, ('A','C'):0, ('A','D'):0, ('A','E'):0, ('A','F'):0,
										('B','A'):0, ('B','B'):0, ('B','C'):0, ('B','D'):0, ('B','E'):0, ('B','F'):0,
										('C','A'):0, ('C','B'):0, ('C','C'):0, ('C','D'):0, ('C','E'):0, ('C','F'):0,
										('D','A'):0, ('D','B'):10, ('D','C'):0, ('D','D'):0, ('D','E'):0, ('D','F'):0,
										('E','A'):0, ('E','B'):0, ('E','C'):0, ('E','D'):0, ('E','E'):0, ('E','F'):0,
										('F','A'):0, ('F','B'):0, ('F','C'):0, ('F','D'):0, ('F','E'):0, ('F','F'):0}
		self.parameters['FCC_wppp'] = {('A','PP'):5, ('B','PP'):15, ('C','PP'):15, ('D','PP'):23, ('E','PP'):10, ('F','PP'):20}
		self.parameters['VCC_wp'] = {'A':100, 'B':100, 'C':100, 'D':100, 'E':100, 'F':100} # Variable capital cost for Well Platform
		self.parameters['VCC_pp'] = {'PP':300} # Variable capital cost for Production Platform
		self.parameters['FOC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Fixed operating cost for Well Platform
		self.parameters['FOC_pp'] = {'PP':30} # # Fixed operating cost for Production Platform
		self.parameters['VOC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Variable operating cost for Well Platform
		self.parameters['VOC_pp'] = {'PP':30} # # Variable operating cost for Production Platform
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Size'] = {'A':{'Deterministic':400},'B':{'Deterministic':400},'C':{'Deterministic':250},
								'D':{'Low':200,'Medium':320,'High':440},'E':{'Low':200,'Medium':350,'High':500},'F':{'Deterministic':250}}
		self.uncertain['Deliv'] = {'A':{'Deterministic':130},'B':{'Deterministic':200},'C':{'Deterministic':130},
								'D':{'Low':120,'Medium':150,'High':190},'E':{'Deterministic':130},'F':{'Deterministic':120}}
		
		##### Probability #####
		self.uncertain['Size_prob'] = {'A':{'Deterministic':1},'B':{'Deterministic':1},'C':{'Deterministic':1},
								'D':{'Low':0.3,'Medium':0.4,'High':0.3},'E':{'Low':0.3,'Medium':0.4,'High':0.3},'F':{'Deterministic':1}}
		self.uncertain['Deliv_prob'] = {'A':{'Deterministic':1},'B':{'Deterministic':1},'C':{'Deterministic':1},
								'D':{'Low':0.3,'Medium':0.4,'High':0.3},'E':{'Deterministic':1},'F':{'Deterministic':1}}

class WP6T15S81(): # The size and deliverability of D, E are uncertain, Example3_2004
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['WP'] = ['A','B','C','D','E','F']
		self.sets['PP'] = ['PP']
		self.sets['T'] = range(1,16) # 1,16
		
		##### Parameters #####
		self.parameters = {}
		self.parameters['shrink'] = 0.01
		self.parameters['M_wp'] = {'A':80, 'B':80, 'C':50, 'D':64, 'E':70, 'F':50}
		self.parameters['M_pp'] = {'PP':197}
		self.parameters['M_wpwp'] ={('A','A'):0,('A','B'):0,('A','C'):0,('A','D'):0,('A','E'):0,('A','F'):0,
									('B','A'):0,('B','B'):0,('B','C'):0,('B','D'):0,('B','E'):0,('B','F'):0,
									('C','A'):0,('C','B'):0,('C','C'):0,('C','D'):0,('C','E'):0,('C','F'):0,
									('D','A'):0,('D','B'):64,('D','C'):0,('D','D'):0,('D','E'):0,('D','F'):0,
									('E','A'):0,('E','B'):0,('E','C'):0,('E','D'):0,('E','E'):0,('E','F'):0,
									('F','A'):0,('F','B'):0,('F','C'):0,('F','D'):0,('F','E'):0,('F','F'):0}
		self.parameters['M_wppp'] = {('A','PP'):80,('B','PP'):144,('C','PP'):50,('D','PP'):64,('E','PP'):70,('F','PP'):50}
		self.parameters['FCC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Fixed capital cost for Well Platform
		self.parameters['FCC_pp'] = {'PP':30} # Fixed capital cost for Production Platform
		self.parameters['FCC_wpwp'] =  {('A','A'):0, ('A','B'):0, ('A','C'):0, ('A','D'):0, ('A','E'):0, ('A','F'):0,
										('B','A'):0, ('B','B'):0, ('B','C'):0, ('B','D'):0, ('B','E'):0, ('B','F'):0,
										('C','A'):0, ('C','B'):0, ('C','C'):0, ('C','D'):0, ('C','E'):0, ('C','F'):0,
										('D','A'):0, ('D','B'):10, ('D','C'):0, ('D','D'):0, ('D','E'):0, ('D','F'):0,
										('E','A'):0, ('E','B'):0, ('E','C'):0, ('E','D'):0, ('E','E'):0, ('E','F'):0,
										('F','A'):0, ('F','B'):0, ('F','C'):0, ('F','D'):0, ('F','E'):0, ('F','F'):0}
		self.parameters['FCC_wppp'] = {('A','PP'):5, ('B','PP'):15, ('C','PP'):15, ('D','PP'):23, ('E','PP'):10, ('F','PP'):20}
		self.parameters['VCC_wp'] = {'A':100, 'B':100, 'C':100, 'D':100, 'E':100, 'F':100} # Variable capital cost for Well Platform
		self.parameters['VCC_pp'] = {'PP':300} # Variable capital cost for Production Platform
		self.parameters['FOC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Fixed operating cost for Well Platform
		self.parameters['FOC_pp'] = {'PP':30} # # Fixed operating cost for Production Platform
		self.parameters['VOC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Variable operating cost for Well Platform
		self.parameters['VOC_pp'] = {'PP':30} # # Variable operating cost for Production Platform
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		
		self.uncertain['Size'] = {'A':{'Deterministic':400},'B':{'Deterministic':400},'C':{'Deterministic':250},
								'D':{'Low':200,'Medium':320,'High':440},'E':{'Low':200,'Medium':350,'High':500},'F':{'Deterministic':250}}
		self.uncertain['Deliv'] = {'A':{'Deterministic':130},'B':{'Deterministic':200},'C':{'Deterministic':130},
								'D':{'Low':120,'Medium':150,'High':190},'E':{'Low':100,'Medium':130,'High':160},'F':{'Deterministic':120}}

		##### Probability #####
		self.uncertain['Size_prob'] = {'A':{'Deterministic':1},'B':{'Deterministic':1},'C':{'Deterministic':1},
								'D':{'Low':0.3,'Medium':0.4,'High':0.3},'E':{'Low':0.3,'Medium':0.4,'High':0.3},'F':{'Deterministic':1}}
		self.uncertain['Deliv_prob'] = {'A':{'Deterministic':1},'B':{'Deterministic':1},'C':{'Deterministic':1},
								'D':{'Low':0.3,'Medium':0.4,'High':0.3},'E':{'Low':0.3,'Medium':0.4,'High':0.3},'F':{'Deterministic':1}}

class WP6T15S243():
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['WP'] = ['A','B','C','D','E','F']
		self.sets['PP'] = ['PP']
		self.sets['T'] = range(1,16) # 1,16
		
		##### Parameters #####
		self.parameters = {}
		self.parameters['shrink'] = 0.01
		self.parameters['M_wp'] = {'A':80, 'B':80, 'C':50, 'D':64, 'E':70, 'F':50}
		self.parameters['M_pp'] = {'PP':197}
		self.parameters['M_wpwp'] ={('A','A'):0,('A','B'):0,('A','C'):0,('A','D'):0,('A','E'):0,('A','F'):0,
									('B','A'):0,('B','B'):0,('B','C'):0,('B','D'):0,('B','E'):0,('B','F'):0,
									('C','A'):0,('C','B'):0,('C','C'):0,('C','D'):0,('C','E'):0,('C','F'):0,
									('D','A'):0,('D','B'):64,('D','C'):0,('D','D'):0,('D','E'):0,('D','F'):0,
									('E','A'):0,('E','B'):0,('E','C'):0,('E','D'):0,('E','E'):0,('E','F'):0,
									('F','A'):0,('F','B'):0,('F','C'):0,('F','D'):0,('F','E'):0,('F','F'):0}
		self.parameters['M_wppp'] = {('A','PP'):80,('B','PP'):144,('C','PP'):50,('D','PP'):64,('E','PP'):70,('F','PP'):50}
		self.parameters['FCC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Fixed capital cost for Well Platform
		self.parameters['FCC_pp'] = {'PP':30} # Fixed capital cost for Production Platform
		self.parameters['FCC_wpwp'] =  {('A','A'):0, ('A','B'):0, ('A','C'):0, ('A','D'):0, ('A','E'):0, ('A','F'):0,
										('B','A'):0, ('B','B'):0, ('B','C'):0, ('B','D'):0, ('B','E'):0, ('B','F'):0,
										('C','A'):0, ('C','B'):0, ('C','C'):0, ('C','D'):0, ('C','E'):0, ('C','F'):0,
										('D','A'):0, ('D','B'):10, ('D','C'):0, ('D','D'):0, ('D','E'):0, ('D','F'):0,
										('E','A'):0, ('E','B'):0, ('E','C'):0, ('E','D'):0, ('E','E'):0, ('E','F'):0,
										('F','A'):0, ('F','B'):0, ('F','C'):0, ('F','D'):0, ('F','E'):0, ('F','F'):0}
		self.parameters['FCC_wppp'] = {('A','PP'):5, ('B','PP'):15, ('C','PP'):15, ('D','PP'):23, ('E','PP'):10, ('F','PP'):20}
		self.parameters['VCC_wp'] = {'A':100, 'B':100, 'C':100, 'D':100, 'E':100, 'F':100} # Variable capital cost for Well Platform
		self.parameters['VCC_pp'] = {'PP':300} # Variable capital cost for Production Platform
		self.parameters['FOC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Fixed operating cost for Well Platform
		self.parameters['FOC_pp'] = {'PP':30} # # Fixed operating cost for Production Platform
		self.parameters['VOC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10} # Variable operating cost for Well Platform
		self.parameters['VOC_pp'] = {'PP':30} # # Variable operating cost for Production Platform
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		
		self.uncertain['Size'] = {'A':{'Deterministic':400},'B':{'Deterministic':400},'C':{'Deterministic':250},
								'D':{'Low':200,'Medium':320,'High':440},'E':{'Low':200,'Medium':350,'High':500},'F':{'Low':130,'Medium':300,'High':470}}
		self.uncertain['Deliv'] = {'A':{'Deterministic':130},'B':{'Deterministic':200},'C':{'Deterministic':130},
								'D':{'Low':120,'Medium':150,'High':190},'E':{'Low':100,'Medium':130,'High':160},'F':{'Deterministic':120}}

		##### Probability #####
		self.uncertain['Size_prob'] = {'A':{'Deterministic':1},'B':{'Deterministic':1},'C':{'Deterministic':1},
								'D':{'Low':0.3,'Medium':0.4,'High':0.3},'E':{'Low':0.3,'Medium':0.4,'High':0.3},'F':{'Low':0.3,'Medium':0.4,'High':0.3}}
		self.uncertain['Deliv_prob'] = {'A':{'Deterministic':1},'B':{'Deterministic':1},'C':{'Deterministic':1},
								'D':{'Low':0.3,'Medium':0.4,'High':0.3},'E':{'Low':0.3,'Medium':0.4,'High':0.3},'F':{'Deterministic':1}}

class WP7T15S243(): # The size and deliverability of D, E, G are uncertain, Example4modi_2004
	def __init__(self):
	
		##### Sets #####
		self.sets = {}
		self.sets['WP'] = ['A','B','C','D','E','F','G']
		self.sets['PP'] = ['PP']
		self.sets['T'] = range(1,16) # 1,16
		
		##### Parameters #####
		self.parameters = {}
		self.parameters['shrink'] = 0.01
		self.parameters['M_wp'] = {'A':88, 'B':82.4, 'C':50, 'D':58, 'E':56, 'F':50, 'G':40}
		self.parameters['M_pp'] = {'PP':212.2}
		self.parameters['M_wpwp'] ={('A','A'):0,('A','B'):0,('A','C'):0,('A','D'):0,('A','E'):0,('A','F'):0,('A','G'):0,
									('B','A'):0,('B','B'):0,('B','C'):0,('B','D'):0,('B','E'):0,('B','F'):0,('B','G'):0,
									('C','A'):0,('C','B'):0,('C','C'):0,('C','D'):0,('C','E'):0,('C','F'):0,('C','G'):0,
									('D','A'):0,('D','B'):58,('D','C'):0,('D','D'):0,('D','E'):0,('D','F'):0,('D','G'):0,
									('E','A'):0,('E','B'):0,('E','C'):0,('E','D'):0,('E','E'):0,('E','F'):0,('E','G'):0,
									('F','A'):0,('F','B'):0,('F','C'):0,('F','D'):0,('F','E'):0,('F','F'):0,('F','G'):0,
									('G','A'):0,('G','B'):40,('G','C'):0,('G','D'):0,('G','E'):0,('G','F'):0,('G','G'):0}
		self.parameters['M_wppp'] = {('A','PP'):88,('B','PP'):180.4,('C','PP'):50,('D','PP'):58,('E','PP'):56,('F','PP'):50,('G','PP'):40}
		self.parameters['FCC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10,'G':10} # Fixed capital cost for Well Platform
		self.parameters['FCC_pp'] = {'PP':30} # Fixed capital cost for Production Platform
		self.parameters['FCC_wpwp'] =  {('A','A'):0, ('A','B'):0, ('A','C'):0, ('A','D'):0, ('A','E'):0, ('A','F'):0, ('A','G'):0,
										('B','A'):0, ('B','B'):0, ('B','C'):0, ('B','D'):0, ('B','E'):0, ('B','F'):0, ('B','G'):0,
										('C','A'):0, ('C','B'):0, ('C','C'):0, ('C','D'):0, ('C','E'):0, ('C','F'):0, ('C','G'):0,
										('D','A'):0, ('D','B'):10, ('D','C'):0, ('D','D'):0, ('D','E'):0, ('D','F'):0, ('D','G'):0,
										('E','A'):0, ('E','B'):0, ('E','C'):0, ('E','D'):0, ('E','E'):0, ('E','F'):0, ('E','G'):0,
										('F','A'):0, ('F','B'):0, ('F','C'):0, ('F','D'):0, ('F','E'):0, ('F','F'):0, ('F','G'):0,
										('G','A'):0, ('G','B'):10, ('G','C'):0, ('G','D'):0, ('G','E'):0, ('G','F'):0, ('G','G'):0}
		self.parameters['FCC_wppp'] = {('A','PP'):5, ('B','PP'):15, ('C','PP'):15, ('D','PP'):23, ('E','PP'):10, ('F','PP'):20, ('G','PP'):23}
		self.parameters['VCC_wp'] = {'A':100, 'B':100, 'C':100, 'D':100, 'E':100, 'F':100, 'G':100} # Variable capital cost for Well Platform
		self.parameters['VCC_pp'] = {'PP':300} # Variable capital cost for Production Platform
		self.parameters['FOC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10,'G':10} # Fixed operating cost for Well Platform
		self.parameters['FOC_pp'] = {'PP':30} # # Fixed operating cost for Production Platform
		self.parameters['VOC_wp'] = {'A':10,'B':10,'C':10,'D':10,'E':10,'F':10,'G':10} # Variable operating cost for Well Platform
		self.parameters['VOC_pp'] = {'PP':30} # # Variable operating cost for Production Platform
		
		
		##### Uncertainty parameter #####
		self.uncertain = {}
		self.uncertain['Size'] = {'A':{'Deterministic':440},'B':{'Deterministic':412},'C':{'Deterministic':250},
								'D':{'Low':230,'Medium':290,'High':350},'E':{'Low':230,'Medium':280,'High':330},'F':{'Deterministic':250},'G':{'Low':150,'Medium':200,'High':250}}
		self.uncertain['Deliv'] = {'A':{'Deterministic':150},'B':{'Deterministic':200},'C':{'Deterministic':130},
								'D':{'Low':115,'Medium':135,'High':155},'E':{'Low':115,'Medium':125,'High':135},'F':{'Deterministic':120},'G':{'Deterministic':135}}
		##### Probability #####
		self.uncertain['Size_prob'] = {'A':{'Deterministic':1},'B':{'Deterministic':1},'C':{'Deterministic':1},
								'D':{'Low':0.3,'Medium':0.4,'High':0.3},'E':{'Low':0.3,'Medium':0.4,'High':0.3},'F':{'Deterministic':1},'G':{'Low':0.3,'Medium':0.4,'High':0.3}}
		self.uncertain['Deliv_prob'] = {'A':{'Deterministic':1},'B':{'Deterministic':1},'C':{'Deterministic':1},
								'D':{'Low':0.3,'Medium':0.4,'High':0.3},'E':{'Low':0.3,'Medium':0.4,'High':0.3},'F':{'Deterministic':1},'G':{'Deterministic':1}}