# fun3d-tools
pythonic interface for interacting with the NASA FUN3D CFD solver.

# motivation
every toolchain I have used previously for interacting with FUN3D has been overcomplicated, bloated, and chock-full of workflow-specific assumptions that break if you have to off-road at all.

the tools here aim to be a bedrock to build such complex tools using a simple, minimal, general, and straightforward interface for working with fun3d files.

# disclaimer
this is a WIP, as I am building up functionality incrementally, as needed, during my own CFD excursions.

# functionality

## nml I/O
_FUN3D nml files are effectively just nested dictionaries, lets treat them as such._
- nml_read() allows you to read a .nml file to this dict format
- nml_write() allows you to write this dict format to a .nml file

Whatever you have to do between those two points is up to you.

I primarily use this to read in a "template" .nml file, and just modify the bits as needed. You could also make fun3d .nml's from scratch using this, but this seems circuitous.

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

**output:**
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


### additional examples
- [example_simple.py](https://github.com/elliottmckee/fun3d-tools/blob/main/example_simple.py)
- [example_advanced.py](https://github.com/elliottmckee/fun3d-tools/blob/main/example_advanced.py)


## input types reference
| input type  | .nml example | fun3d-tools type |
| ------------- | ------------- | ------------- |
| string  | ```project_rootname = 'AIM9X_SIDEWINDER'```  | ```<class 'str'>``` |
| scalar  | ```area_reference = 1.00```                  | ```<class 'float'>```<br>```<class 'int'>```<br>```...``` |
| array-explicit  | ```schedule_cfl(1:2) = 0.1, 5.0```  | ```<class 'list'> of length n``` |
| array-implicit-assign-all  | ```wall_temperature(:) = 1.05```<br>```wall_temp_flag(:) = .true.```  | ```<class 'list'> of length 1``` |












## residual plotting
[residual_plot.py]([https://github.com/elliottmckee/fun3d-tools/blob/main/example_simple.py](https://github.com/elliottmckee/fun3d-tools/blob/main/residual_plot.py)) simply plots all the residuals available, given a FUN3D case .dat file.

