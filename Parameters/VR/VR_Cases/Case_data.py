class I3K7S8():
    def __init__(self):
        
        ##### Sets #####
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8] # Scenarios
        self.sets['J'] = [-3,-2,-1,0,1,2,3] # Depot (negative) + Start point (0) + Customers (positive)
        self.sets['K'] = [1,2,3,4,5,6,7] # Stages (I + R + 1)
        self.sets['I'] = [1,2,3] # Customers
        
        ##### Deterministic	parameters #####
        self.parameters = {}
        self.parameters['R'] = 3 # Returns to the depot R
        self.parameters['r_set'] = {(-1,-2),(-2,-3)} # Dummy to Dummy
        self.parameters['Q'] = 100 # Capacity of the vehicle
        self.parameters['f_jjp'] = {} # Travel cost from j to j'
        
        ##### Parameters for complete recouse #####
        self.parameters['Cp'] = 1000 # Purchase cost, this should be very high compared to travel cost
        
        ##### Uncertainty parameter #####
        self.uncertain = {}
        self.uncertain['d_js'] = {} # Uncertain demand
        
        ##### Probability #####
        self.uncertain['p_s'] = {} # Probability of scenario s

class I3K7S10():
    def __init__(self):
        
        ##### Sets #####
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8,9,10] # Scenarios
        self.sets['J'] = [-3,-2,-1,0,1,2,3] # Depot (negative) + Start point (0) + Customers (positive)
        self.sets['K'] = [1,2,3,4,5,6,7] # Stages (I + R + 1)
        self.sets['I'] = [1,2,3] # Customers
        
        ##### Deterministic	parameters #####        
        self.parameters = {}
        self.parameters['R'] = 3 # Returns to the depot R
        self.parameters['r_set'] = {(-1,-2),(-2,-3)} # Dummy to Dummy
        self.parameters['Q'] = 100 # Capacity of the vehicle
        self.parameters['f_jjp'] = {} # Travel cost from j to j'
        
        ##### Parameters for complete recouse #####
        self.parameters['Cp'] = 1000 # Purchase cost, this should be very high compared to travel cost
        
        ##### Uncertainty parameter #####
        self.uncertain = {}
        self.uncertain['d_js'] = {} # Uncertain demand
        
        ##### Probability #####
        self.uncertain['p_s'] = {} # Probability of scenario s

class I5K11S10():
    def __init__(self):
        
        ##### Sets #####
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8,9,10] # Scenarios
        self.sets['J'] = [-5,-4,-3,-2,-1,0,1,2,3,4,5] # Depot (negative) + Start point (0) + Customers (positive)
        self.sets['K'] = [1,2,3,4,5,6,7,8,9,10,11] # Stages (I + R + 1)
        self.sets['I'] = [1,2,3,4,5] # Customers
        
        ##### Deterministic	parameters #####
        self.parameters = {}
        self.parameters['R'] = 5 # Returns to the depot R
        self.parameters['r_set'] = {(-1,-2),(-2,-3),(-3,-4),(-4,-5)} # Dummy to Dummy
        self.parameters['Q'] = 100 # Capacity of the vehicle
        self.parameters['f_jjp'] = {} # Travel cost from j to j'
        
        ##### Parameters for complete recouse #####
        self.parameters['Cp'] = 1000 # Purchase cost, this should be very high compared to travel cost
        
        ##### Uncertainty parameter #####
        self.uncertain = {}
        self.uncertain['d_js'] = {} # Uncertain demand
        
        ##### Probability #####
        self.uncertain['p_s'] = {} # Probability of scenario s

class I7K15S10():
    def __init__(self):
        
        ##### Sets #####
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8,9,10] # Scenarios
        self.sets['J'] = [-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7] # Depot (negative) + Start point (0) + Customers (positive)
        self.sets['K'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] # Stages (I + R + 1)
        self.sets['I'] = [1,2,3,4,5,6,7] # Customers
        
        ##### Deterministic	parameters #####
        self.parameters = {}
        self.parameters['R'] = 7 # Returns to the depot R
        self.parameters['r_set'] = {(-1,-2),(-2,-3),(-3,-4),(-4,-5),(-5,-6),(-6,-7)} # Dummy to Dummy
        self.parameters['Q'] = 100 # Capacity of the vehicle
        self.parameters['f_jjp'] = {} # Travel cost from j to j'
        
        ##### Parameters for complete recouse #####
        self.parameters['Cp'] = 1000 # Purchase cost, this should be very high compared to travel cost
        
        ##### Uncertainty parameter #####
        self.uncertain = {}
        self.uncertain['d_js'] = {} # Uncertain demand
        
        ##### Probability #####
        self.uncertain['p_s'] = {} # Probability of scenario s

class I8K17S10():
    def __init__(self):
        
        ##### Sets #####
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8,9,10] # Scenarios
        self.sets['J'] = [-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8] # Depot (negative) + Start point (0) + Customers (positive)
        self.sets['K'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17] # Stages (I + R + 1)
        self.sets['I'] = [1,2,3,4,5,6,7,8] # Customers
        
        ##### Deterministic	parameters #####
        self.parameters = {}
        self.parameters['R'] = 8 # Returns to the depot R
        self.parameters['r_set'] = {(-1,-2),(-2,-3),(-3,-4),(-4,-5),(-5,-6),(-6,-7),(-7,-8)} # Dummy to Dummy
        self.parameters['Q'] = 100 # Capacity of the vehicle
        self.parameters['f_jjp'] = {} # Travel cost from j to j'
        
        ##### Parameters for complete recouse #####
        self.parameters['Cp'] = 1000 # Purchase cost, this should be very high compared to travel cost
        
        ##### Uncertainty parameter #####
        self.uncertain = {}
        self.uncertain['d_js'] = {} # Uncertain demand
        
        ##### Probability #####
        self.uncertain['p_s'] = {} # Probability of scenario s

class I9K19S10():
    def __init__(self):
        
        ##### Sets #####
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8,9,10] # Scenarios
        self.sets['J'] = [-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9] # Depot (negative) + Start point (0) + Customers (positive)
        self.sets['K'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19] # Stages (I + R + 1)
        self.sets['I'] = [1,2,3,4,5,6,7,8,9] # Customers
        
        ##### Deterministic	parameters #####
        self.parameters = {}
        self.parameters['R'] = 9 # Returns to the depot R
        self.parameters['r_set'] = {(-1,-2),(-2,-3),(-3,-4),(-4,-5),(-5,-6),(-6,-7),(-7,-8),(-8,-9)} # Dummy to Dummy
        self.parameters['Q'] = 100 # Capacity of the vehicle
        self.parameters['f_jjp'] = {} # Travel cost from j to j'
        
        ##### Parameters for complete recouse #####
        self.parameters['Cp'] = 1000 # Purchase cost, this should be very high compared to travel cost
        
        ##### Uncertainty parameter #####
        self.uncertain = {}
        self.uncertain['d_js'] = {} # Uncertain demand
        
        ##### Probability #####
        self.uncertain['p_s'] = {} # Probability of scenario s

class I10K21S10():
    def __init__(self):
        
        ##### Sets #####
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8,9,10] # Scenarios
        self.sets['J'] = [-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10] # Depot (negative) + Start point (0) + Customers (positive)
        self.sets['K'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21] # Stages (I + R + 1)
        self.sets['I'] = [1,2,3,4,5,6,7,8,9,10] # Customers
        
        ##### Deterministic	parameters #####
        self.parameters = {}
        self.parameters['R'] = 10 # Returns to the depot R
        self.parameters['r_set'] = {(-1,-2),(-2,-3),(-3,-4),(-4,-5),(-5,-6),(-6,-7),(-7,-8),(-8,-9),(-9,-10)} # Dummy to Dummy
        self.parameters['Q'] = 100 # Capacity of the vehicle
        self.parameters['f_jjp'] = {} # Travel cost from j to j'
        
        ##### Parameters for complete recouse #####
        self.parameters['Cp'] = 1000 # Purchase cost, this should be very high compared to travel cost
        
        ##### Uncertainty parameter #####
        self.uncertain = {}
        self.uncertain['d_js'] = {} # Uncertain demand
        
        ##### Probability #####
        self.uncertain['p_s'] = {} # Probability of scenario s