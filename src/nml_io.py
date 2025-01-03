'''
IO for fun3d nml files

Based around nested dictionary structure, 
where each section (e.g., "raw_grid", "code_run_control") becomes a key in the outer dictionary, 
and the key-value pairs within each section become keys and values in the corresponding inner dictionaries

TODO:
- Ideally clean up handling of lists vs. non-lists
'''

import os


def format_bool(value):
    if value: return ".true."
    else: return ".false."

def format_float(value):
    abs_value = abs(value)
    if abs_value >= 1000 or abs_value < 0.001:
        return f"{value:.6e}"  # Exponential notation for 'gross' floats
    else:
        return f"{value:.6f}"  # Normal notation for 'nice' floats

def format_list(values):
    # TODO: Simplify this with a loop or something please 
    # this also doesn't tie into format_dict_write below automagically
    
    if all(isinstance(x, bool) for x in values):
        # bool
        return ", ".join(format_bool(x) for x in values)

    elif all(isinstance(x, int) for x in values):
        # int
        return ", ".join(str(x) for x in values)

    elif all(isinstance(x, float) for x in values):
        # float
        return ", ".join(str(x) for x in values)

    else:
        raise Exception('Issue with list. Check for incorrect/inconsistent types?')

format_dict_write = { # Format specification for each of the possible types
    bool:   format_bool,
    str:    lambda x: f"'{x}'",
    int:    lambda x: f"{x}",
    float:  format_float,
    list:   format_list,
    tuple:  lambda x: ", ".join(str(item) for item in x),
}

def _value_parse(value):
    # common parser/map for fun3d input values -> python datatypes 
    
    if value.startswith("'") and value.endswith("'"): 
        # is string
        return value.strip("'")

    elif value.startswith(".") and value.endswith("."): 
        # is bool
        return value.strip(".").lower() == 'true'
        
    else:
        # assume scalar
        try: return int(value)
        except ValueError: return float(value) 



def nml_write(nml_data, out_filename, n_fixedwidth = 40, overwrite=False):

    open_flag = 'x'
    if overwrite:
        open_flag = 'w'

    if '/' in out_filename:
        os.makedirs(os.path.dirname(out_filename), exist_ok=True)
    
    with open(out_filename, open_flag) as outfile:

        # for each block
        for block_name, block in nml_data.items():
            outfile.write(f'&{block_name}\n')

            # for each property in that block
            for property, value in block.items():

                if isinstance(value, list):
                    # is array, so need to add parenthesis to LHS of = statement
                    if len(value) == 1:
                        property = property + '(:)'
                    else:
                        property = property + f'(1:{len(value)})'

                if len(property) > n_fixedwidth: raise Exception('Property name too long for my dumb fixed-with implementation. Make smarter or increase n_fixedwidth') 
                outfile.write('\t' + property.ljust(n_fixedwidth) + ' = ' + format_dict_write[type(value)](value) + '\n')

            outfile.write('/\n\n')



def nml_read(filename):
    # this could probably be done better with recursion... but dont know if fun3d needs more depth than supported here?

    nml_dict = {}
    current_section = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            
            # find start of section
            if line.startswith('&'):
                section_name = line.strip('&')
                nml_dict[section_name] = {}
                current_section = section_name
            
            # find end of section
            elif line.startswith('/'):
                current_section = None
            
            # while in a section
            elif current_section:
                key, value = line.split('=', 1)
                key     = key.strip()
                value   = value.strip();

                if ":" in key:
                    # is array
                    key = key.split('(')[0]
                    nml_dict[current_section][key] = [_value_parse(x) for x in value.split(',')]
                else: 
                    nml_dict[current_section][key] = _value_parse(value)

    return nml_dict





















