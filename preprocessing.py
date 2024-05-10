#Read in all_x, all_y, all_z
#import_dir = 'C:\Users\User\Documents\University\5th_Year\FYP\Carbon Sliding Strip\Practical\Data analysis and visualisation\PC_visualisation_large_buffer' 

import PC_visualisation_large_buffer
#from PC_visualisation_large_buffer import all_x
#from PC_visualisation_large_buffer import all_y
#from PC_visualisation_large_buffer import all_z


import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import statistics



#Import data from previous stage
x = np.array(PC_visualisation_large_buffer.all_x)
y = np.array(PC_visualisation_large_buffer.all_y)
z = np.array(PC_visualisation_large_buffer.all_z)

print("Just imported data for preprocessing ")

profile = 0     #Number of columns
row = 0         
num_rows = len(x[0])     #Number of data points in a profile
num_profiles = len(x) 
z_nans = []     #List of lists of indices which have NaNs in Z

p = 0
y_avg = []
profile_count = 0
profile_distance =  []

#For point cloud reduction
indices = []
indices_temp = array([])
#Initialising the indice count
indice_count = array([])
indice_count = np.zeros(1280)
#Calc % nans per row
percent_nans = []

#Reduced x, y, z arrays
x_reduced = []
y_reduced = []
z_reduced = []

#List of rows to remove
rows_remove = []

#Deleting the coors would produce non-rectangular maxtrices, making it impossible to plot
"""for list in z:
    print("Profile is: ", profile)
    row = 0
    for i in range(num_rows-1):
        print("Row is: ", row)"""

"""all_z is a array of arrays
        row is the element number within the profile array
        which is in the z array
        if z[profile][row]<200:     
            #z[profile].pop(row)
            #y[profile].pop(row)
            #x[profile].pop(row)
            np.delete(x[profile], row, 0)       #Unsure how last option (axis) works
            np.delete(y[profile], row, 0)
            print(np.delete(z[profile], row, 0))

            #When an element is popped, the size of the array changes
            if (row == 0): row = 0
            elif (row > 0): row -= 1
        else: 
            row += 1
    profile += 1"""

"""Replacing all values less than 200 in z as NaN, as well as their x and y counterparts
#for list in z:
    #print("Profile is: ", profile)
    #row = 0

    #for i in range(num_rows-1):
        #print("Row is: ", row)

        #The if method takes too long
        #if z[profile][row]<200:   
            #x[profile][row] = NaN
            #y[profile][row] = NaN
            #z[profile][row] = NaN

        #row += 1"""

#Replotting
plt.style.use('ggplot')
plt.ion()   #Turns interactive mode on


#Removing outlying data------------------------------------------------------------------------------------
    
#Create 3D scatter figure
#plt.figure()    #Initialise figure
#fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
fig1 = plt.figure()
ax1 = fig1.add_subplot(projection='3d')
print("Created 1st preprocessed figure\n")

#Adding labels, title, etc.
ax1.set_xlabel('x (mm)', fontsize=10, rotation=0)
ax1.set_ylabel('y (mm)', fontsize=10, rotation=0) 
ax1.set_zlabel('z (mm)', fontsize=10, rotation=0)
ax1.set_title('3D scan of a pantograph carbon strip')

#Replacing all values less than 200 in z as NaN, as well as their x and y counterparts
#Not doing if statement, so quicker
#But point only has NaN for z 
#Unsure how to find out number for x and y
profile = 0
for list in z:
    z[profile][z[profile] < 218] = NaN      #218 (for real strip) #150 for wooden
    profile += 1

#Where there is a NaN in z, the x and y values for this coordinate are also made NaN
profile = 0
indices_z_nans = 0
for profile in range(num_profiles):
    z_nans.append(np.where(np.isnan(z[profile])))   #Get indices of NaN values for current profile
    for indices_z_nans in range(len(z_nans[profile])):
        x[profile, indices_z_nans] = NaN    #Replace x value with NaN due to corresponding z value also being NaN
        y[profile, indices_z_nans] = NaN

            
ax1.set_xlim(0, -80)
ax1.set_ylim(0, 750)
ax1.set_zlim(125, 300)
plot1 = ax1.scatter(x[:][:], y[:][:], z[:][:], s=0.025, depthshade=True)
#---------------------------------------------------------------------------------------------------------------

#3D scatter figure for downsampling-----------------------------------------------------------------------------
fig2 = plt.figure()
ax2 = fig2.add_subplot(projection='3d')
print("Created 2nd preprocessed figure\n")

#Adding labels, title, etc.
ax2.set_xlabel('x (mm)', fontsize=10, rotation=0)
ax2.set_ylabel('y (mm)', fontsize=10, rotation=0) 
ax2.set_zlabel('z (mm)', fontsize=10, rotation=0)
ax2.set_title('3D scan of a pantograph carbon strip')


#Downsampling
profile = 0
for profile in range(num_profiles):
    y_avg.append(np.nansum(y[profile])/len(y[profile]))  #Should obtain 1x326 array
    profile += 1

while(profile_count<num_profiles-1):
    profile_distance.append(abs(y_avg[profile_count] - y_avg[profile_count+1]))    #Distance between current profile and next

    if (profile_count > 0):
        if ((profile_distance[profile_count-1])<0.025 and profile_distance[profile_count]<0.025 and (profile_distance[profile_count-1]+profile_distance[profile_count])<0.05):
            z[profile_count][:] = NaN       # Shouldn't corresponding x and y values also be made NaN (and y_avg values for completeness)
            
            #Updating the profile distance
            profile_distance[profile_count] = profile_distance[profile_count] + profile_distance[profile_count-1]
            print("Distances updated")
            
    profile_count += 1

ax2.set_xlim(0, -80)
ax2.set_ylim(0, 750)
ax2.set_zlim(125, 300)
plot2 = ax2.scatter(x[:][:], y[:][:], z[:][:], s=0.025)
#----------------------------------------------------------------------------------------------------------

#Now all outliers made into NaN, can reduce point cloud size-----------------------------------------------
#Based on condition, find indices true when condition applied
#Indices (for x, y, and z) remove elements synchronously
x = array(x)
y = array(y)
z = array(z)

#Gets indices for each profile which are NaNs
profile = 0
for profile in range(num_profiles):
    if(np.all(~np.isnan(z[profile][:])) == True):          #If there are no NaNs in a profile, the indices for this profile are set to NaN
        indices_temp = NaN
    else:
        indices_temp = np.array(np.where(np.isnan(z[profile][:])==1)).astype(int16)
    np.array(indices.append(np.array(indices_temp).astype(int16)))

#Counts the number of NaNs for each point across all profiles
profile = 0
point = 0
indice_profile = []
for profile in range(num_profiles):
    indice_profile = indices[profile]   #Ideally wouldn't need this but need to find way to retrieve value from 2D numpy array
    for point in range(num_rows):       #Iterate through all the possible points that could be NaN, per profile in z matrix
        indice_count[point] += np.count_nonzero(indice_profile[0]==point)

#Calculating percentage of NaNs per row
point = 0
for point in range(num_rows):
    percent_nans.append(100*indice_count[point]/num_profiles)

#Determine which rows to remove
point = 0
for point in range(num_rows):
    if(percent_nans[point] > 75.0): rows_remove.append(point)

#Removes row if large number NaNs present (i.e. data not useful)
profile = 0
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


#Plotting result of final preprocessed stage
fig3 = plt.figure()
ax3 = fig3.add_subplot(projection='3d')
print("Created 3rd preprocessed figure\n")
#Adding labels, title, etc.
ax3.set_xlabel('x (mm)', fontsize=10, rotation=0)
ax3.set_ylabel('y (mm)', fontsize=10, rotation=0) 
ax3.set_zlabel('z (mm)', fontsize=10, rotation=0)
ax3.set_title('3D scan of a pantograph carbon strip')
ax3.set_xlim(0,-80)
ax3.set_ylim(0, 750)
ax3.set_zlim(125, 300)
plot3 = ax3.scatter(x_reduced[:][:], y_reduced[:][:], z_reduced[:][:], s=0.025)
#------------------------------------------------------------------------------------------------------------

print("End of preprocessing")

#Plot 3D scatter---------------------------------------------------------------------------------------------
plt.show()
print("Plotted scatter graphs\n")
