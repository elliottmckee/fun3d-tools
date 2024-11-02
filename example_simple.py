''' 
very simple example showing:
    - reading in template nml
    - changing some values
    - writing out "rendered" nml
'''

import itertools
import os
import copy
import json

from nml_io import nml_write, nml_read


if __name__ == '__main__':

    # read in template file
    nml_dict = nml_read('resource/fun3d_test.nml')

    # modify some stuff
    nml_dict['reference_physical_properties']['mach_number']        = 3.0
    nml_dict['reference_physical_properties']['angle_of_attack']    = 5.0
    nml_dict['nonlinear_solver_parameters']['schedule_cfl(1:2)']    = [1, 10000]

    # just using this to "pretty-print" the nested dictionary structure
    print(json.dumps(nml_dict, indent=4))

    # write "rendered"/modified nml file
    nml_write(nml_dict, 'fun3d_rendered.nml')