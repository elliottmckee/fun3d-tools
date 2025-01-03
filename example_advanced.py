'''
Quick, kinda clunky, but more practical example
'''

import itertools
import os
import copy
import json

from src.nml_io import nml_write, nml_read


TEMPLATE_RUN_FILE = '''
# symlink things
ln -s ../../{project_name}.ugrid {project_name}.ugrid 
ln -s ../../{project_name}.mapbc {project_name}.mapbc 

# run
mpirun -n 6 nodet_mpi
'''

TEMPLATE_BATCH_FILE = '''
#!/bin/bash
base_dir=$(pwd)

# Find all directories containing _run_.sh scripts
directories=$(find . -type f -name "*_run_.sh" -exec dirname {} \; | sort -u)
# echo "$directories"

# Loop over each directory, run, cd back
for dir in $directories; do
    echo "Running case: $dir"
    cd $dir
    sh _run_.sh
    cd $base_dir
done
'''


if __name__ == '__main__':

    # TODO: The final implementation should ideally consist of 2 things- 
    #           1. the main dictionary of substitutions
    #           2. a set of rule-based settings. i.e. if M>3 use X, else Y
    
    cfd_base_dir = 'cfd_cases';
    template_nml = nml_read('resource/fun3d_test.nml')
    project_name = template_nml['project']['project_rootname']

    # Traj specific data (outer loop, these all must have same length)
    outerloop_dict = {  'reference_physical_properties': {  'mach_number':              [0.3,           0.9,        1.5],
                                                            'reynolds_number':          [22447372,      52447372,   82447372]},
                        'nonlinear_solver_parameters': {    'schedule_iteration':       [[1, 10000],    [1, 10000], [1, 10000]],
                                                            'schedule_cfl':             [[1, 30],       [1, 20],    [1, 10]],
                                                            'schedule_cflturb':         [[.1, 3.0],       [.1, 2.0],    [.1, 1.0]]}
                    }

    # AoA, Aos to run (inner loop)
    aoa_vec = [0, 5, 10]
    aos_vec = [-5, 0, 5]
    angle_vec = list(itertools.product(aoa_vec, aos_vec))


    for traj_idx in range( len(outerloop_dict['reference_physical_properties']['mach_number']) ):
        for aoa, aos in angle_vec:

            # gen case directory
            mach_curr = outerloop_dict['reference_physical_properties']['mach_number'][traj_idx]
            case_dir = os.path.join(cfd_base_dir, f'M{mach_curr:.3f}', f'A{aoa:.3f}_B{aos:.3f}')
            os.makedirs(case_dir, exist_ok=True)

            # get clean template
            nml_data_curr = copy.deepcopy(template_nml)

            # enact case-specific values
            for section, properties in outerloop_dict.items():
                for prop in properties.keys():
                    nml_data_curr[section][prop] = outerloop_dict[section][prop][traj_idx]

            # write nml
            nml_write(nml_data_curr, os.path.join(case_dir, 'fun3d.nml'), overwrite=True)

            # write run script
            with open(os.path.join(case_dir, '_run_.sh'), 'w') as fid:
                for line in iter(TEMPLATE_RUN_FILE.splitlines()):
                    fid.write(eval(f"f'{line}'")+"\n")

    # write batch script
    with open(os.path.join(cfd_base_dir, '_run_batch_.sh'), 'w') as fid:
        fid.write(TEMPLATE_BATCH_FILE)
    










    




    
    

   
    

    
    




