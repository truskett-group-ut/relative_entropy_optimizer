from importlib import import_module
import re

class Potential:
    #load in a list of potentials (names)
    def __init__(self, potential_specs):
        #initial checks on data
        self.potential_id_names = zip(*potential_specs)[0]
        for potential_id_name in self.potential_id_names:
            if re.search(r'\_', potential_id_name):
                raise AttributeError('Cannot have underscores in potential id name')
        if len(set(self.potential_id_names)) != len(self.potential_id_names):
            raise AttributeError('Each potential id name must be unique')
        #load in the modules
        self.potentials = {}   
        import_potential = lambda x: import_module(x)
        for potential_id_name, potential_type, init_params in potential_specs:
            self.potentials[potential_id_name] = import_potential(('potentials.' + potential_type)).Potential(init_params) 
        #set appropriate num_params
        self.num_params = sum([self.potentials[potential_id_name].num_params for potential_id_name in self.potentials])
        return None
    
    #initialize the state
    def SetParamsState(self, params_state):
        self.params_state = params_state
        if len(self.params_state) != self.num_params:
            raise AttributeError('Wrong number of parameters for combined interaction')
        return None
    
    #this is the actual potential
    def Potential(self, r, params_val):
        params_separated = {}
        for param in params_val:
            match = re.match(r'\s*([a-z0-9]+)\_\_([^\s]+)', param)
            potential_id_name = match.group(1)
            potential_param = match.group(2)
            if potential_id_name not in params_separated:
                params_separated[potential_id_name] = {}
            params_separated[potential_id_name][potential_param] = params_val[param]
        ur = 0.0    
        for potential_id_name in self.potentials:
            ur = ur + self.potentials[potential_id_name].Potential(r, params_separated[potential_id_name])
        return ur