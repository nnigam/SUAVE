# compute_aircraft_lift.py
# 
# Created:  Anil V., Dec 2013
# Modified: Anil, Trent, Tarik, Feb 2014 
# Modified: Anil  April 2014 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import SUAVE
# suave imports

from SUAVE.Structure import Data
from SUAVE.Attributes import Units

from SUAVE.Attributes.Results import Result
#from SUAVE import Vehicle
from SUAVE.Components.Wings import Wing
from SUAVE.Components.Fuselages import Fuselage
from SUAVE.Components.Propulsors import Turbofan
from SUAVE.Geometry.Two_Dimensional.Planform import wing_planform
from SUAVE.Geometry.Two_Dimensional.Planform import fuselage_planform

#from SUAVE.Attributes.Aerodynamics.Aerodynamics_Surrogate import Aerodynamics_Surrogate
#from SUAVE.Attributes.Aerodynamics.Aerodynamics_Surrogate import Interpolation
from SUAVE.Attributes.Aerodynamics.Aerodynamics_1d_Surrogate import Aerodynamics_1d_Surrogate
from SUAVE.Methods.Aerodynamics.Drag import compute_aircraft_drag



from SUAVE.Attributes.Aerodynamics.Configuration   import Configuration
from SUAVE.Attributes.Aerodynamics.Conditions      import Conditions
from SUAVE.Attributes.Aerodynamics.Geometry        import Geometry


from SUAVE.Methods.Aerodynamics.Lift.weissenger_vortex_lattice import weissinger_vortex_lattice
#from SUAVE.Methods.Aerodynamics.Lift import compute_aircraft_lift
#from SUAVE.Methods.Aerodynamics.Drag import compute_aircraft_drag


# python imports
import os, sys, shutil
from copy import deepcopy
from warnings import warn

# package imports
import numpy as np
import scipy as sp


# ----------------------------------------------------------------------
#  The Function
# ----------------------------------------------------------------------

def compute_aircraft_lift(conditions,configuration,geometry=None):
    """ SUAVE.Methods.Aerodynamics.compute_aircraft_lift(conditions,configuration,geometry)
        computes the lift associated with an aircraft 
        
        Inputs:
            conditions - data dictionary with fields:
                mach_number - float or 1D array of freestream mach numbers
                angle_of_attack - floar or 1D array of angle of attacks
                
            configuration - data dictionary with fields:
                surrogate_models.lift_coefficient - a callable function or class 
                    with inputs of angle of attack and outputs of lift coefficent
                fuselage_lift_correction - the correction to fuselage contribution to lift
                    
            geometry - Not used
            
        
        Outputs:
            CL - float or 1D array of lift coefficients of the total aircraft
        
        Updates:
            conditions.lift_breakdown - stores results here
            
        Assumptions:
            surrogate model returns total incompressible lift due to wings
            prandtl-glaurert compressibility correction on this
            fuselage contribution to lift correction as a factor
        
    """    
   
    # unpack
    fus_correction = configuration.fuselage_lift_correction
    Mc             = conditions.freestream.mach_number
    AoA            = conditions.aerodynamics.angle_of_attack
    
    # the lift surrogate model for wings only
    wings_lift_model = configuration.surrogate_models.lift_coefficient
    
    # pack for interpolate
    X_interp = AoA
    
    # interpolate
    wings_lift = wings_lift_model(X_interp)

    #print('lift')
    #print(wings_lift)
    #print('AoA')
    #print(X_interp*180/np.pi)
    
    # compressibility correction
    compress_corr = 1./(np.sqrt(1.-Mc**2.))
    
    # correct lift
    wings_lift_comp = wings_lift * compress_corr
    
    # total lift, accounting one fuselage
    aircraft_lift_total = wings_lift_comp * fus_correction 
    
    # store results
    lift_results = Result(
        total                = aircraft_lift_total ,
        incompressible_wings = wings_lift          ,
        compressible_wings   = wings_lift_comp     ,
        compressibility_correction_factor = compress_corr  ,
        fuselage_correction_factor        = fus_correction ,
    )
    conditions.aerodynamics.lift_breakdown.update( lift_results )    #update
    
    conditions.aerodynamics.lift_coefficient= aircraft_lift_total

    return aircraft_lift_total

if __name__ == '__main__':   
    #test()
    raise RuntimeError , 'module test failed, not implemented'