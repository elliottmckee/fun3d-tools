'''
Quick dumb driver script to spoof inputs and test things
'''

import itertools
import os
import copy

from nml_io import nml_write, nml_read


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

    
    base_dir = os.getcwd();
    template_nml = nml_read('fun3d.nml')
    project_name = template_nml['project']['project_rootname']

    # Traj specific data (outer loop)
    mach_vec = [0.3, 0.9, 1.5]
    re_vec = [22447372, 22447372, 22447372]

    # Angles to run (inner loop)
    angle_vec = list(itertools.product([-90, -85, -80], [0]))

    # Settings we want to modify (mainly mach dependant, must be same length as Traj points)
    # May run into issues with key uniqueness at some point, mainly w.r.t. plot/output variables, since will be same names across boundary and volume
    overrides_all = {'schedule_iteration': [[1, 10000], [1, 10000], [1, 10000]],
                  'schedule_cfl': [[1, 30], [1, 20], [1, 10]],
                  'schedule_cflturb': [[.25, 2.5], [.25, 2.5], [.25, 2.5]]}
    
    
    for traj_idx, (mach, Re) in enumerate(zip(mach_vec, re_vec)):
        for aoa, aos in angle_vec:

            # get clean template
            nml_data_curr = copy.deepcopy(template_nml)

            # gen case dir
            case_dir = os.path.join(base_dir, f'M{mach:.3f}', f'A{aoa:.3f}_B{aos:.3f}')
            os.makedirs(case_dir, exist_ok=True)

            # get case-specific overrides
            override = {key: value[traj_idx] for key, value in overrides_all.items()}
            override['mach_number'] = mach
            override['reynolds_number'] = Re
            override['angle_of_attack'] = aoa
            override['angle_of_yaw'] = aos

            # enact each override
            for section, properties in nml_data_curr.items():
                 for prop in properties.keys():
                     if prop in override: 
                        nml_data_curr[section][prop] = override[prop]

            # write nml
            nml_write(nml_data_curr, os.path.join(case_dir, 'fun3d.nml'))

            # write run script
            with open(os.path.join(case_dir, '_run_.sh'), 'w') as fid:
                for line in iter(TEMPLATE_RUN_FILE.splitlines()):
                    fid.write(eval(f"f'{line}'")+"\n")

            # write batch script
            with open(os.path.join(base_dir, '_run_batch_.sh'), 'w') as fid:
                fid.write(TEMPLATE_BATCH_FILE)
    










    




    
    

   
    

    
    




