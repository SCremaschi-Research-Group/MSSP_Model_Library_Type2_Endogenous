class I3T6S8():
    def __init__(self):
        
        ### Sets ###
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8] # Scenarios
        self.sets['I'] = [1,2,3] # Aggregates
        
        ### Parameters ###
        self.parameters = {}
        self.parameters['Precedence'] = {1:[], 2:[], 3:[1]} # Aggregate precedence, j must be mined before i
        
        ### Parameter generator ###
        self.make = {}
        self.make['p_s'] =  {} # Probability
        self.make['c1_t'] =  {} # Revenue of sold metal
        self.make['cmng_t'] =  {} # Cost for rock mining
        self.make['cproc_t'] =  {} # Cost for rock processing
        self.make['P_ave'] = 33 # Rock processing capacity
        self.make['M_ave'] = 33 # Rock mining capacity
        
        ##### Parameters for complete recouse #####
        self.parameters['CMadd'] = 10000

class I3T10S10():
    def __init__(self):
        
        ### Sets ###
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8,9,10] # Scenarios
        self.sets['I'] = [1,2,3] # Aggregates
        
        ### Parameters ###
        self.parameters = {}
        self.parameters['a0'] = 100 # To simplify, set a0 = 100
        self.parameters['Precedence'] = {1:[], 2:[], 3:[1]} # Aggregate precedence, j must be mined before i
        
        ### Parameter generator ###
        self.make = {}
        self.make['p_s'] =  {} # Probability
        self.make['c1_t'] =  {} # Revenue of sold metal
        self.make['cmng_t'] =  {} # Cost for rock mining
        self.make['cproc_t'] =  {} # Cost for rock processing
        self.make['P_ave'] = 33 # Rock processing capacity
        self.make['M_ave'] = 33 # Rock mining capacity
        
        ##### Parameters for complete recouse #####
        self.parameters['CMadd'] = 10000

class I20T10S10():
    def __init__(self):
        
        ### Sets ###
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8,9,10] # Scenarios
        self.sets['I'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20] # Aggregates
        
        ### Parameters ###
        self.parameters = {}
        self.parameters['Precedence'] = {1:[], 2:[], 3:[1,4], 4:[], 5:[], 6:[1], 7:[2], 8:[3], 9:[4], 10:[5], 11:[6], 12:[7], 13:[8], 14:[9], 15:[10], 16:[11], 17:[12], 18:[13], 19:[14], 20:[15]} # Aggregate precedence, j must be mined before i
        
        ### Parameter generator ###
        self.make = {}
        self.make['p_s'] =  {} # Probability
        self.make['c1_t'] =  {} # Revenue of sold metal
        self.make['cmng_t'] =  {} # Cost for rock mining
        self.make['cproc_t'] =  {} # Cost for rock processing
        self.make['P_ave'] = 220 # Rock processing capacity
        self.make['M_ave'] = 220 # Rock mining capacity
        
        ##### Parameters for complete recouse #####
        self.parameters['CMadd'] = 10000

class I40T10S10():
    def __init__(self):
        
        ### Sets ###
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8,9,10] # Scenarios
        self.sets['I'] = list(range(1,40+1)) # Aggregates
        
        ### Parameters ###
        self.parameters = {}
        self.parameters['Precedence'] = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[],
                                        11:[1], 12:[2], 13:[3], 14:[4], 15:[5], 16:[6], 17:[7], 18:[8], 19:[9], 20:[10],
                                        21:[11], 22:[12], 23:[13], 24:[14], 25:[15], 26:[16], 27:[17], 28:[18], 29:[19], 30:[20],
                                        31:[21], 32:[22], 33:[23], 34:[24], 35:[25], 36:[26], 37:[27], 38:[28], 39:[29], 40:[30]} # Aggregate precedence, j must be mined before i
        
        ### Parameter generator ###
        self.make = {}
        self.make['p_s'] =  {} # Probability
        self.make['c1_t'] =  {} # Revenue of sold metal
        self.make['cmng_t'] =  {} # Cost for rock mining
        self.make['cproc_t'] =  {} # Cost for rock processing
        self.make['P_ave'] = 440 # Rock processing capacity
        self.make['M_ave'] = 440 # Rock mining capacity
        
        ##### Parameters for complete recouse #####
        self.parameters['CMadd'] = 10000

class I60T10S10():
    def __init__(self):
        
        ### Sets ###
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8,9,10] # Scenarios
        self.sets['I'] = list(range(1,60+1)) # Aggregates
        
        ### Parameters ###
        self.parameters = {}
        self.parameters['Precedence'] = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[],
                                        11:[1], 12:[2], 13:[3], 14:[4], 15:[5], 16:[6], 17:[7], 18:[8], 19:[9], 20:[10],
                                        21:[11], 22:[12], 23:[13], 24:[14], 25:[15], 26:[16], 27:[17], 28:[18], 29:[19], 30:[20],
                                        31:[21], 32:[22], 33:[23], 34:[24], 35:[25], 36:[26], 37:[27], 38:[28], 39:[29], 40:[30],
                                        41:[31], 42:[32], 43:[33], 44:[34], 45:[35], 46:[36], 47:[37], 48:[38], 49:[39], 50:[40],
                                        51:[41], 52:[42], 53:[43], 54:[44], 55:[45], 56:[46], 57:[47], 58:[48], 59:[49], 60:[50]} # Aggregate precedence, j must be mined before i
        
        ### Parameter generator ###
        self.make = {}
        self.make['p_s'] =  {} # Probability
        self.make['c1_t'] =  {} # Revenue of sold metal
        self.make['cmng_t'] =  {} # Cost for rock mining
        self.make['cproc_t'] =  {} # Cost for rock processing
        self.make['P_ave'] = 660 # Rock processing capacity
        self.make['M_ave'] = 660 # Rock mining capacity
        
        ##### Parameters for complete recouse #####
        self.parameters['CMadd'] = 10000

class I80T10S10():
    def __init__(self):
        
        ### Sets ###
        self.sets = {}
        self.sets['S'] = [1,2,3,4,5,6,7,8,9,10] # Scenarios
        self.sets['I'] = list(range(1,80+1)) # Aggregates
        
        ### Parameters ###
        self.parameters = {}
        self.parameters['Precedence'] = {1:[], 2:[], 3:[1,4], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[],
                                        11:[1], 12:[2], 13:[3], 14:[4], 15:[5], 16:[6], 17:[7], 18:[8], 19:[9], 20:[10],
                                        21:[11], 22:[12], 23:[13], 24:[14], 25:[15], 26:[16], 27:[17], 28:[18], 29:[19], 30:[20],
                                        31:[21], 32:[22], 33:[23], 34:[24], 35:[25], 36:[26], 37:[27], 38:[28], 39:[29], 40:[30],
                                        41:[31], 42:[32], 43:[33], 44:[34], 45:[35], 46:[36], 47:[37], 48:[38], 49:[39], 50:[40],
                                        51:[41], 52:[42], 53:[43], 54:[44], 55:[45], 56:[46], 57:[47], 58:[48], 59:[49], 60:[50],
                                        61:[51], 62:[52], 63:[53], 64:[54], 65:[55], 66:[56], 67:[57], 68:[58], 69:[59], 70:[60],
                                        71:[61], 72:[62], 73:[63], 74:[64], 75:[65], 76:[66], 77:[67], 78:[68], 79:[69], 80:[70]} # Aggregate precedence, j must be mined before i
        
        ### Parameter generator ###
        self.make = {}
        self.make['p_s'] =  {} # Probability
        self.make['c1_t'] =  {} # Revenue of sold metal
        self.make['cmng_t'] =  {} # Cost for rock mining
        self.make['cproc_t'] =  {} # Cost for rock processing
        self.make['P_ave'] = 880 # Rock processing capacity
        self.make['M_ave'] = 880 # Rock mining capacity
        
        ##### Parameters for complete recouse #####
        self.parameters['CMadd'] = 10000
