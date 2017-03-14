from numpy import tanh, pi

class Potential():
    #load in any default parameters needed
    def __init__(self, _):
        self.num_params = 4
        self.param_names = set(['rho_p', 'd_p', 'd', 'w'])
        return None
    
    #initialize the state
    def SetParamsState(self, params_state):
        self.params_state = params_state
        if len(self.params_state) != self.num_params:
            raise AttributeError('Wrong number of parameters for depletion potential')
        return None
        
    #this is the actual potential
    def Potential(self, r, params_val):
        #load in the opt params
        rho_p = float(params_val['rho_p'])  #polymer concentration
        d_p = float(params_val['d_p'])      #polymer diameter
        d = float(params_val['d'])          #particle diameter
        w = float(params_val['w'])          #how fast to smooth the linearly extrapolated core region to zero
        #calculate the dimensionless potential (over k_B*T)
        if r < d:
            R_d = d/2.0 + d_p/2.0
            ur0 = -1.0*(rho_p/d**3)*((4.0*pi/3.0)*(R_d**3 - (3.0/4.0)*d*R_d**2 + (1.0/16.0)*d**3)) 
            dur0 = -1.0*(rho_p/d**3)*((4.0*pi/3.0)*(-1.0*(3.0/4.0)*R_d**2 + (3.0/16.0)*d**2)) 
            ur = ur0 + dur0*(r - d)
        elif d <= r and r < d + d_p:
            R_d = d/2.0 + d_p/2.0
            ur = -1.0*(rho_p/d**3)*((4.0*pi/3.0)*(R_d**3 - (3.0/4.0)*r*R_d**2 + (1.0/16.0)*r**3))    
        else:
            ur = 0.0
        #smooth
        ur = 0.5*(1.0 + tanh(w*(r - d)))*ur
        return ur
    
    #holds some user defined defaults that may be desirable
    def DefaultParameters(self):
        return ({'rho_p': True, 'd_p': True, 'd': False, 'w': False},
                {'rho_p': 0.1, 'd_p': 0.2, 'd': 1.0, 'w': 50.0})