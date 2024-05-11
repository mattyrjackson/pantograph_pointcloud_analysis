# MJ 2024/05/10 Load dataset

# Libraries
import time
import os
from os.path import exists
import pandas as pd
import numpy as np
from pylab import *

# Location of dataset
dir = 'C:\\Users\\User\\Documents\\University\\5th_Year\\FYP\\Carbon_Sliding_Strip\\Practical\\Sensors\\Triangulation sensor\\scanCONTROL Windows SDK 4.1.1\\C++ SDK (+python bindings)\\examples\\CmmTrigger\\326_profiles_03_02_23'   #fab_wooden_1  #fab_wooden_2   #real_strip_2  #326_profiles_03_02_23
os.chdir(dir)	#.chdir() changes current working directory to specified path

# Determine number CSV files to read
def num_csvs(dir):
    file_num_max = 0
    for files in os.listdir(dir):
        if files.endswith('.csv'):
            file_num_max += 1
    print("Number of CSV files to read: ")
    print(file_num_max)
    return file_num_max
       
# Import data ---------------------------------------------------
print("Importing x,z,y data from all the CSV files")
print("\n")
# Determine when profile captured, for ordering
tstart = time.time()  
# Buffers
all_x = []
all_y = []
all_z = []

def load_data(file_num_max, dir):
    file_num = 1
    for tstart in range(file_num_max):
        my_CSV_file = "test" + str(file_num) + ".csv"
        file_exists = exists(dir)

        if (file_exists == 1):
            #Reading data from CSV file
            x=pd.read_csv(my_CSV_file, usecols=['X'])
            y=pd.read_csv(my_CSV_file, usecols=['Y'])
            z=pd.read_csv(my_CSV_file, usecols=['Z'])

            #Converting data to float32
            x = x.to_numpy()[:, 0]
            x = x.astype(float32)
        
            y = y.to_numpy()[:, 0]
            y = y.astype(float32)

            z = z.to_numpy()[:, 0]
            z = z.astype(float32)

    
            all_x.append(x)     #Append current files' data to the buffer
            all_y.append(y) 
            all_z.append(z)

            file_num += 1
        else:
            print('File' + my_CSV_file + 'does not exist. Please check your dataset.')
            break
    return all_x, all_y, all_z
# Import data --------------------------------------------------

# Calling functions for loading of data
file_num_max = num_csvs(dir)   # Determine number CSV files to read
all_x, all_y, all_z = load_data(file_num_max, dir)
