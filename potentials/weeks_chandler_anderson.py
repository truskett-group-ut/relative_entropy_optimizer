class Potential:
    #load in any default parameters needed
    def __init__(self, _):
        self.num_params = 4
        self.param_names = set(['d', 'epsilon', 'alpha', 'max_ur'])
        return None
    
    #initialize the state
    def SetParamsState(self, params_state):
        self.params_state = params_state
        if len(self.params_state) != self.num_params:
            raise AttributeError('Wrong number of parameters for weeks chandler anderson potential')
        return None
        
    #this is the actual potential
    def Potential(self, r, params_val):
        #load in the opt params
        d = float(params_val['d'])                   #particle diameter
        epsilon = float(params_val['epsilon'])       #how steep the wca repulsion should be
        alpha = float(params_val['alpha'])           #the exponent for the wca interaction
        max_ur = float(params_val['max_ur'])         #maximum value of the potential before leveling out
        #calculate the dimensionless potential (over k_B*T)
        alpha = max(0.001, alpha)
        if r <= d*(2.0**(1.0/alpha)):
            r = max(0.0001, r)
            ur = 4.0*epsilon*((d/r)**(2*alpha) - (d/r)**(alpha)) + epsilon
            if ur >= max_ur:
                ur = max_ur
        else:
            ur = 0.0
        return ur
    
    #holds some user defined defaults that may be desirable
    def DefaultParameters(self):
        return ({'d': False, 'epsilon': True, 'alpha': True, 'max_ur': False},
                {'d': 1.0, 'epsilon': 1.0, 'alpha': 6, 'max_ur': float(1e6)})