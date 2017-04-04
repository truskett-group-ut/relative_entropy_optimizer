from numpy import array, arange
import numdifftools as nd
import scipy.integrate as integrate
from scipy.interpolate import Akima1DInterpolator as Akima
from copy import deepcopy
import re

class RelativeEntropyUpdate:
    #nothing here yet
    def __init__(self):
        return None
    
    #load in a function that describes the interaction and current parameters
    def LoadPotential(self, pot, params_val):
        self.pot = pot
        self.params_val = params_val
        return None
    
    #yields the the derivative functions in r-space for any potential
    def GetDerivative(self, param_name):
        x_cur = self.params_val[param_name]
        dur = []
        params_val = deepcopy(self.params_val)
        del params_val[param_name]
        
        ur = lambda x: self.pot.Potential(self.r, dict(params_val.items() + [(param_name, x)]))
        dur = nd.Derivative(ur)
        return dur(x_cur)
    
    #read in tabulated data
    def GetRadialDistData(self, filename):
        f = open(filename, 'r')
        data = f.readlines()
        r = []
        gr = []
        num_re = r'^\s*([0-9eE\+\-\.]+)[,;\s]+([0-9eE\+\-\.]+)\.*'
        for line in data:
            match = re.match(num_re, line)
            if match:
                r.append(float(match.group(1)))
                gr.append(float(match.group(2)))
        f.close()
        return (1.0*array(r), 1.0*array(gr))
    
    #load the rdf from file and always make sure it is usable in case of user abuse
    def LoadRadialDistFuncs(self, filename_current, filename_target, spacing=0.005):
        #read in the data
        r, gr = self.GetRadialDistData(filename_current)
        r_tgt, gr_tgt = self.GetRadialDistData(filename_target)
        #sample according to an akima spline fit
        r_lower, r_upper = (max(r[0], r_tgt[0]), min(r[-1], r_tgt[-1]))
        self.r = arange(r_lower, r_upper, spacing)
        akima = Akima(r, gr)
        self.gr = akima.__call__(self.r, nu=0, extrapolate=None)
        akima = Akima(r_tgt, gr_tgt)
        self.gr_tgt = akima.__call__(self.r, nu=0, extrapolate=None)        
        return None
    
    #calculate update
    def CalcUpdate(self, learning_rate=0.01, dim=3):
        params_val_new = deepcopy(self.params_val)
        for param_name in self.pot.params_state:
            if self.pot.params_state[param_name]['opt']:
                dur = self.GetDerivative(param_name)
                update_integral = integrate.trapz(((self.r**(dim - 1))*(self.gr - self.gr_tgt)*dur), x=self.r)
                params_val_new[param_name] = params_val_new[param_name] + learning_rate*update_integral
                #check to make sure no constraint is violated
                if 'min' in self.pot.params_state[param_name]:
                    params_val_new[param_name] = max(params_val_new[param_name], self.pot.params_state[param_name]['min'])
                if 'max' in self.pot.params_state[param_name]:
                    params_val_new[param_name] = min(params_val_new[param_name], self.pot.params_state[param_name]['max'])
        conv_score = {'gradient': 0.0, 'rdf_diff': 0.0}
        for param_name in params_val_new:
            conv_score['gradient'] = conv_score['gradient'] + ((params_val_new[param_name] - self.params_val[param_name])/learning_rate)**2
        conv_score['gradient'] = conv_score['gradient']**(1.0/2.0)
        conv_score['rdf_diff'] = integrate.trapz(((self.r**(dim - 1))*(self.gr - self.gr_tgt)**2), x=self.r)
        return (params_val_new, conv_score)
    
    #calculate update
    #def CalcUpdate(self, learning_rate=0.01, dim=3, conv_crit='gradient'):
    #    params_val_new = deepcopy(self.params_val)
    #    for param_name in self.pot.params_state:
    #        if self.pot.params_state[param_name]['opt']:
    #            dur = self.GetDerivative(param_name)
    #            update_integral = integrate.trapz(((self.r**(dim - 1))*(self.gr - self.gr_tgt)*dur), x=self.r)
    #            params_val_new[param_name] = params_val_new[param_name] + learning_rate*update_integral
    #            #check to make sure no constraint is violated
    #            if 'min' in self.pot.params_state[param_name]:
    #                params_val_new[param_name] = max(params_val_new[param_name], self.pot.params_state[param_name]['min'])
    #            if 'max' in self.pot.params_state[param_name]:
    #                params_val_new[param_name] = min(params_val_new[param_name], self.pot.params_state[param_name]['max'])
    #    return params_val_new