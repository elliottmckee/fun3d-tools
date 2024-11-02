# fun3d-tools
Pythonic interface for interacting with the NASA FUN3D CFD solver.

# motivation
In my professional career, every set of tools I have used for interacting with FUN3D have been far too overcomplicated, bloated, and chock-full of workflow-specific assumptions that break if you have to off-road at all.

All the tools here aim to be simple, minimal, general, and straightforward. 

# functionality

## nml I/O
FUN3D nml files are effectively just nested dictionaries, lets treat them as such.

This allows you to very simply read in "template" .nml files and write out a modified/"rendered" .nml files. Whatever you have to do between those two points is up to you.

You can also make fun3d .nml's from scratch using this, but this seems circuitous. 

### examples
- [example_simple.py](https://github.com/elliottmckee/fun3d-tools/blob/main/example_simple.py)
- [example_advanced.py](https://github.com/elliottmckee/fun3d-tools/blob/main/example_advanced.py)

### demo ([example_simple.py](https://github.com/elliottmckee/fun3d-tools/blob/main/example_simple.py))
```python
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
```

```
{
    "project": {
        "project_rootname": "fun3d_test_nml"
    },
    "raw_grid": {
        "grid_format": "aflr3",
        "data_format": "ascii"
    },
    "reference_physical_properties": {
        "mach_number": 3.0,
        "reynolds_number": 36055000.0,
        "angle_of_attack": 5.0,
        "angle_of_yaw": 0,
        "temperature": 267.5863,
        "temperature_units": "Kelvin"
    },
...
```





## residual plotting
[residual_plot.py]([https://github.com/elliottmckee/fun3d-tools/blob/main/example_simple.py](https://github.com/elliottmckee/fun3d-tools/blob/main/residual_plot.py)) simply plots all the residuals available, given a FUN3D case .dat file.

