# MJ 2024/05/10 Preprocessing data set loaded from load_dataset.py
# Neccessary step before visualisation

# Libraries
from load_dataset import all_x, all_y, all_z

# Initialising vars ---------------------------------------------
# Import data from load_dataset
x = np.array(PC_visualisation_large_buffer.all_x)
y = np.array(PC_visualisation_large_buffer.all_y)
z = np.array(PC_visualisation_large_buffer.all_z)
profile = 0     #Number of columns
row = 0         
num_rows = len(x[0])     #Number of data points in a profile
num_profiles = len(x) 
z_nans = []     #List of lists of indices which have NaNs in Z
p = 0
y_avg = []
profile_count = 0
profile_distance =  []
# For point cloud reduction
indices = []
indices_temp = array([])
# Initialise indice count
indice_count = array([])
indice_count = np.zeros(1280)
# Calc % nans per row
percent_nans = []
# Reduced x, y, z arrays
x_reduced = []
y_reduced = []
z_reduced = []
#List of rows to remove
rows_remove = []
# Initialising vars ---------------------------------------------

