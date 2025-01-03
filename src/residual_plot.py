import os
import re

import matplotlib.pyplot as plt
import pandas as pd


def extract_variable_names(file_path):
    '''get variable names available from fun3d dat file'''
    # Read only the first few lines to get the variable names
    with open(file_path, 'r') as file:
        # Read the first two lines (TITLE and VARIABLES)
        lines = [file.readline().strip() for _ in range(2)]
    
    # Extract the variable names from the second line
    variables_line = lines[1]
    variables = re.findall(r'"(.*?)"', variables_line)
    
    return variables


def parse_dat(filename):
    '''parses fun3d dat file to pandas dataframe'''
    var_names = extract_variable_names(filename)
    df = pd.read_csv(filename, skiprows=2, header=0, names=var_names, sep='\s+')
    return df


def residual_plot(filename):
    '''plots all residuals for a given fun3d dat file'''

    print('current file: ', filename)
    df = parse_dat(filename)

    print('Wall Time', df['Wall Time'])
    
    # plot all residuals
    plt.figure(figsize=(10, 6)) 

    for col in df.columns:
        if col.startswith('R_'):
            plt.plot(df['Iteration'], df[col], label=col)

    plt.yscale('log')
    plt.xlabel('Iteration')
    plt.ylabel('Values (log scale)')
    plt.title('Plot of R_1, R_2, ... against Iteration')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    
    # plot body forces
    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    c_labels = ['C_x', 'C_y', 'C_z']
    colors = ['b', 'g', 'r']

    for ax, label, color in zip(axs, c_labels, colors):
        ax.plot(df['Iteration'], df[label], label=label, color=color)
        ax.set_ylabel(f'{label} Values')
        ax.set_title(f'{label} against Iteration')
        ax.grid(True)

    axs[-1].set_xlabel('Iteration')  # Set xlabel for the last subplot
    plt.tight_layout()


    # plot body moments
    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    c_labels = ['C_M_x', 'C_M_y', 'C_M_z']
    colors = ['b', 'g', 'r']

    for ax, label, color in zip(axs, c_labels, colors):
        ax.plot(df['Iteration'], df[label], label=label, color=color)
        ax.set_ylabel(f'{label} Values')
        ax.set_title(f'{label} against Iteration')
        ax.grid(True)

    axs[-1].set_xlabel('Iteration')  # Set xlabel for the last subplot
    plt.tight_layout()
    plt.show()
    return


def get_subdirectories(directory):
    # Get a list of all entries in the directory
    entries = os.listdir(directory)
    
    # Filter out the subdirectories
    subdirs = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry))]
    subdirs = [os.path.join(directory, entry) for entry in entries if os.path.isdir(os.path.join(directory, entry))]
    
    return subdirs




if __name__ == '__main__':


    # plot single result
    # residual_plot('/home/emckee/projects/fun3d/meatrocket_r3/T0.699_M0.634/A0.000_B0.000/meat_rocket_hist.dat')
  

    # plot directory of results
    base_dir = '/home/emckee/projects/fun3d/meatrocket_r3/';
    dirs_raw = get_subdirectories(base_dir)
    dirs_raw.sort()
    suf = '/A0.000_B0.000/meat_rocket_hist.dat'
    dirs_proc = [direc + suf for direc in dirs_raw]

    for dir_curr in dirs_proc:
        residual_plot(dir_curr)

    