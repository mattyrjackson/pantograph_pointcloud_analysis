# Point Cloud visualisation 
#Use program once all CSV files produced from scan


#Not sure for reason of this (see Matplotlib scatter plot 3D)
#~mpl_toolkits.mplot3d.axes3d.Axes3D.scatter
#import matplotlib
#print (matplotlib.get_backend())

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from pylab import *
import time
from os.path import exists


plt.style.use('ggplot')

dir = 'C:\\Users\\User\\Documents\\University\\5th_Year\\FYP\\Carbon_Sliding_Strip\\Practical\\Sensors\\Triangulation sensor\\scanCONTROL Windows SDK 4.1.1\\C++ SDK (+python bindings)\\examples\\CmmTrigger\\326_profiles_03_02_23'   #fab_wooden_1'  #fab_wooden_2   #real_strip_2'  #326_profiles_03_02_23'
os.chdir(dir)	#.chdir() changes current working directory to specified path


#Determining number CSV files to read
file_num_max = 0
for files in os.listdir(dir):
    if files.endswith('.csv'):
            file_num_max += 1
print("Number of CSV files to read: ")
print(file_num_max)

            
#Import data
print("Importing x,z,y data from all the CSV files")
print("\n")

tstart = time.time()  #For profiling

file_num = 1


#Buffers
all_x = []
all_y = []
all_z = []

plt.ion()   #Turns interactive mode on


#Create 3D scatter figure
#plt.figure()    #Initialise figure
#fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
print("Created figure\n")


#Adding labels, title, etc.
ax.set_xlabel('x (mm)', fontsize=10, rotation=0)
ax.set_ylabel('y (mm)', fontsize=10, rotation=0) 
ax.set_zlabel('z (mm)', fontsize=10, rotation=0)
ax.set_title('3D scan of a pantograph carbon strip')


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
        print('File' + my_CSV_file + 'does not exist')


def all_data(all_x, all_y, all_z):
    return all_x, all_y, all_z


#Create 3D scatter plot
plot1 = ax.scatter(all_x[:][:], all_y[:][:], all_z[:][:], s=0.025)
#Plot 3D scatter
plt.show()
print("Plotted scatter\n")


print("About to finish PC_vis")
print(type(x))

