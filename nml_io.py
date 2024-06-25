'''
IO for nml files

Based around nested dictionary structure, 
where each section (e.g., "raw_grid", "code_run_control") becomes a key in the outer dictionary, 
and the key-value pairs within each section become keys and values in the corresponding inner dictionaries
'''
import os

def format_bool(value):
    if value: return ".true."
    else: return ".false."

def format_float(value):
    abs_value = abs(value)
    if abs_value >= 1000 or abs_value < 0.001:
        return f"{value:.4e}"  # Exponential notation for 'gross' floats
    else:
        return f"{value:.4f}"  # Normal notation for 'nice' floats

def list_write_helper(value):
    # handles the parameter-side parenthesis for array quantities, i.e. schedule_cfl(1:2)
    if isinstance(value, list): return f'(1:{len(value)})'
    else: return ''
        
format_dict_write = { # Format specification for each of the possible types
    bool:   format_bool,
    str:    lambda x: f"'{x}'",
    int:    lambda x: f"{x}",
    float:  format_float,
    list:   lambda x: ", ".join(str(item) for item in x),
    tuple:  lambda x: ", ".join(str(item) for item in x),
}


def nml_write(nml_data, out_filename, n_fixedwidth = 40):

    os.makedirs(os.path.dirname(out_filename), exist_ok=True)
    
    with open(out_filename, 'w') as outfile:

        # for each block
        for block_name, block in nml_data.items():
            outfile.write(f'&{block_name}\n')

            # for each property in that block
            for property, value in block.items():
                prop_full = property + list_write_helper(value)
                if len(prop_full) > n_fixedwidth: raise Exception('Property name too long for my dumb fixed-with implementation. Make smarter or increase n_fixedwidth') 
                outfile.write('\t' + prop_full.ljust(n_fixedwidth) + ' = ' + format_dict_write[type(value)](value) + '\n')

            outfile.write('/\n\n')


def nml_read(filename):

    nested_dict = {}
    current_section = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('&'):
                section_name = line.strip('&')
                nested_dict[section_name] = {}
                current_section = section_name
            elif line.startswith('/'):
                current_section = None
            elif current_section:
                key, value = line.split('=', 1)
                key     = key.split('(', 1)[0].strip()
                value   = value.strip();

                # If string
                if value.startswith("'") and value.endswith("'"): 
                    nested_dict[current_section][key] = value.strip("'")

                # If bool
                elif value.startswith(".") and value.endswith("."): 
                    nested_dict[current_section][key] = value.strip(".").lower() == 'true'
                    
                # If array
                elif "," in value:
                    try: 
                        nested_dict[current_section][key] = [int(x) for x in value.split(',')]
                    except ValueError:
                        nested_dict[current_section][key] = [float(x) for x in value.split(',')]

                # If scalar
                else:
                    try: 
                        nested_dict[current_section][key] = int(value)
                    except ValueError:
                        nested_dict[current_section][key] = float(value)
         
    return nested_dict




















