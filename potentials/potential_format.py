class PotentialName:
    #load in any default parameters needed
    def __init__(self):
        self.num_params_opt = ?
        self.num_params_fixed = ?
        return None
        
    #this is the actual potential
    def Potential(self, r, params_opt, params_fixed):
        #calculate ur at a given r using functional form and the inputs...
        return ur
        
    def DefaultParameters(self):
        #generate defaults
        return (params_opt, params_fixed)