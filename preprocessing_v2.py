# MJ 2024/05/10 Preprocessing data set loaded from load_dataset.py
# Neccessary step before visualisation

# Libraries
from load_dataset import all_x, all_y, all_z
import numpy as np
from pylab import *

# Initialising vars ---------------------------------------------
# Import data from load_dataset
x = np.array(all_x)
y = np.array(all_y)
z = np.array(all_z)      
# Make outlying data NaN, Downsampling profiles where over-dense, Removing outliers made into NaNm Might reduce point cloud size
num_profiles = len(x) 
# Removing outliers made into NaNm Might reduce point cloud size   
num_rows = len(x[0])     #Number of data points in a profile
# Make outlying data NaN
z_nans = []     #List of lists of indices which have NaNs in Z
# Downsampling profiles where over-dense
y_avg = []



### Yet to go through the rest of these vars, and state which functions they feature in
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
# List of rows to remove
rows_remove = []
# Initialising vars ---------------------------------------------

# Make outlying data NaN ----------------------------------------
# Replacing all values less than <a specified value dependent on which strip analysed> in z as NaN, as well as their x and y counterparts
# Not doing if statement, so quicker with "z[profile][z[profile] < 218] = NaN"
# NaN's only seen for z 
# Unsure how to find out number for x and y
for profile in range(len(z)):
    z[profile][z[profile] < 218] = NaN      # 218 (for real strip) #150 for wooden. Soft code this as enhancement goal
    profile += 1

# Where there is a NaN in z, the x and y values for this coordinate are also made NaN
for profile in range(num_profiles):
    z_nans.append(np.where(np.isnan(z[profile])))   # Get indices of NaN values for current profile
    for indices_z_nans in range(len(z_nans[profile])):
        x[profile, indices_z_nans] = NaN    # Replace x value with NaN due to corresponding z value also being NaN
        y[profile, indices_z_nans] = NaN
# Make outlying data NaN ----------------------------------------


# Downsampling profiles where over-dense ------------------------
# Average the y values, so each singular profile in one distinct line
for profile in range(num_profiles):
    y_avg.append(np.nansum(y[profile])/len(y[profile]))  # Should obtain 1x326 array
profile = 0     # Required for if-statement
profile_count = 0       # Required for while-statement
while(profile_count<num_profiles-1):
    profile_distance.append(abs(y_avg[profile_count] - y_avg[profile_count+1]))    # Distance between current profile and next
    if (profile_count > 0):     # Don't donwsample for first profile
        # Interesting experiment would be to determine threshold of acceptable profile density 
        if ((profile_distance[profile_count-1])<0.025 and profile_distance[profile_count]<0.025 and (profile_distance[profile_count-1]+profile_distance[profile_count])<0.05):
            z[profile_count][:] = NaN       # Ideally, corresponding x and y values also be made NaN (and y_avg values for completeness)
            x[profile_count][:] = NaN
            y[profile_count][:] = NaN
            # Updating the profile distance, as this is an iterative algo over whole set of profiles
            profile_distance[profile_count] = profile_distance[profile_count] + profile_distance[profile_count-1]
            print("Distances updated")
    profile_count += 1
# Downsampling profiles where over-dense ------------------------


# Removing outliers and downsampled data, which was made into NaN. This might reduce point cloud size. ----------------------------
# Based on condition, find indices true when condition applied
# Indices (for x, y, and z) remove elements synchronously
x = array(x)
y = array(y)
z = array(z)

# Gets indices, for each profile separately, which are NaNs
for profile in range(num_profiles):
    if(np.all(~np.isnan(z[profile][:])) == True):          # If there is not one NaN in a profile, the we mark don't care in indices_temp with NaN
        indices_temp = NaN
    else:
        indices_temp = np.array(np.where(np.isnan(z[profile][:])==1)).astype(int16)     # If there are indices which are NaN in a profile, we note down those indices
    np.array(indices.append(np.array(indices_temp).astype(int16)))      # Collect the indices, which are not a number and those which are a number (marked as do-not care (NaN))

# Counts the number of NaNs for each point across all profiles
indice_profile = []
for profile in range(num_profiles):
    indice_profile = indices[profile]   # Ideally wouldn't need this but need to find way to retrieve value from 2D numpy array
    for point in range(num_rows):       # Iterate through all the possible points, which could be NaN, per profile in z matrix
        indice_count[point] += np.count_nonzero(indice_profile[0]==point)

# Calculating percentage of NaNs per row
# A high percentage of NaN's indicates uninsightful data- i.e., we it has little/no value)
for point in range(num_rows):
    percent_nans.append(100*indice_count[point]/num_profiles)

# Determine which rows to remove
for point in range(num_rows):
    if(percent_nans[point] > 75.0): rows_remove.append(point)       # Interesting experiment would be to investigate threshold of NaN's which dicates whether row is removed

# Removes row if large number NaNs present (i.e. data not useful)
for profile in range(num_profiles):
    np.array(x_reduced.append(np.array(np.delete(x[profile],rows_remove))))
    np.array(y_reduced.append(np.array(np.delete(y[profile],rows_remove))))
    np.array(z_reduced.append(np.array(np.delete(z[profile],rows_remove))))

reduced_num_profiles = len(x_reduced)
reduced_num_rows = size(x_reduced[0])

print(len(x_reduced))
print(size(x_reduced[0]))

print(len(y_reduced))
print(size(y_reduced[0]))

print(len(z_reduced))
print(size(z_reduced[0]))
print("Outlying data removed")
# Removing Now all outliers made into NaN, can reduce point cloud size ----------------------------

# Create functions for pre-processing steps to improve reability for users glancing over code/light refamiliarisaiton

print("End of preprocessing")


# Temporary plotting to check post-preprocessing visualisations -----------------------------------
if 1:
    import matplotlib.pyplot as plt
    #Replotting
    plt.style.use('ggplot')
    plt.ion()   #Turns interactive mode on
    #Create 3D scatter figure
    #plt.figure()    #Initialise figure
    #fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(projection='3d')
    print("Created figure\n")


    #Adding labels, title, etc.
    ax1.set_xlabel('x (mm)', fontsize=10, rotation=0)
    ax1.set_ylabel('y (mm)', fontsize=10, rotation=0) 
    ax1.set_zlabel('z (mm)', fontsize=10, rotation=0)
    ax1.set_title('3D scan of a pantograph carbon strip')

    ax1.set_xlim(0, -80)
    ax1.set_ylim(0, 750)
    ax1.set_zlim(125, 300)
    plot1 = ax1.scatter(x[:][:], y[:][:], z[:][:], s=0.025, depthshade=True)
# Temporary plotting to check post-preprocessing visualisations -----------------------------------