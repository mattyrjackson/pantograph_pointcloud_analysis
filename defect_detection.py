#Processing stage

import PC_visualisation_large_buffer
import preprocessing
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
#Plot zooming
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


reduced_num_profiles = preprocessing.reduced_num_profiles   #As dataset reduced in preprocessing
reduced_num_rows = preprocessing.reduced_num_rows

z_avg = []
z_new = []
y_new = []

z_above_diff = []
#above_curve_threshold = 0.25 #mm

edge_buffer = 100

y_first_half = []
z_first_half = []
y_second_half = []
z_second_half = []

z_diff_first_half = []
z_diff_second_half = []
min_distance_from_curve = float32(0.01)    #(mm)

max_distance_from_curve = float32(2.5)    #(mm)
z_max_first_half = []
z_max_second_half = []

z_new_first_half = []
z_new_second_half = []

y_new_exact = []
z_new_exact = []

z_mins_first_half = []
z_mins_second_half = []
z_max_diff_first_half = []
z_max_diff_second_half = []
depth_threshold = 2.75     #(mm)

y_zoom_first_half = []
z_zoom_first_half = []
y_zoom_second_half = []
z_zoom_second_half = []

zoom_first_half = 1
zoom_second_half = 1

#Import data from previous stage
x_reduced = array(preprocessing.x_reduced)
y_reduced = array(preprocessing.y_reduced)
z_reduced = array(preprocessing.z_reduced)

x_fitted_1 = []
x_fitted_2 = []


#y, z fitted curve---------------------------------------------------------------------------------------------------------------------------
#Don't need x as working in y, z 2D (side) view

#y avg
y_avg = array(preprocessing.y_avg)

#z avg
profile = 0
for profile in range(reduced_num_profiles):
    """May not obtain a 1x326 array as ignores NaN's
    Unlikely as preprocessing removes rows with high percentage of NaN's.
    and to get a whole row profile of NaN's in z direction would mean measuring table
    which means it has a high percentage of NaN's, so should be removed
    but code is kept until proven redundant."""
    z_avg.append(np.nansum(z_reduced[profile])/np.count_nonzero(~np.isnan(z_reduced[profile])))  

#If any zeroes or NaN's are still present: Preventing zeros and NaN's infiltrating curve
#Assumes one of the next 9 z_avg values is >0 or ~NaN
profile = 0
for profile in range(reduced_num_profiles):
    if (z_avg[profile]==0.0 or np.isnan(z_avg[profile])):
        if (z_avg[profile+1] != 0.0 and ~np.isnan(z_avg[profile+1])):
            z_avg[profile] = z_avg[profile+1]
            y_avg[profile] = y_avg[profile+1]
        elif (z_avg[profile+2] != 0.0 and ~np.isnan(z_avg[profile+2])):
            z_avg[profile] = z_avg[profile+2]
            y_avg[profile] = y_avg[profile+2]
        elif (z_avg[profile+3] != 0.0 and ~np.isnan(z_avg[profile+3])):
            z_avg[profile] = z_avg[profile+3]
            y_avg[profile] = y_avg[profile+3]
        elif (z_avg[profile+4] != 0.0 and ~np.isnan(z_avg[profile+4])):
            z_avg[profile] = z_avg[profile+4]
            y_avg[profile] = y_avg[profile+4]
        elif (z_avg[profile+5] != 0.0 and ~np.isnan(z_avg[profile+5])):
            z_avg[profile] = z_avg[profile+5]
            y_avg[profile] = y_avg[profile+5]
        elif (z_avg[profile+6] != 0.0 and ~np.isnan(z_avg[profile+6])):
            z_avg[profile] = z_avg[profile+6]
            y_avg[profile] = y_avg[profile+6]
        elif (z_avg[profile+7] != 0.0 and ~np.isnan(z_avg[profile+7])):
            z_avg[profile] = z_avg[profile+7]
            y_avg[profile] = y_avg[profile+7]
        elif (z_avg[profile+8] != 0.0 and ~np.isnan(z_avg[profile+8])):
            z_avg[profile] = z_avg[profile+8]
            y_avg[profile] = y_avg[profile+8]
        elif (z_avg[profile+9] != 0.0 and ~np.isnan(z_avg[profile+9])):
            z_avg[profile] = z_avg[profile+9]
            y_avg[profile] = y_avg[profile+9]


#Fitted smoothed curve----------------
#Fitting data to curve
#This is our golden curve
p = np.polyfit(y_avg, z_avg, 5)     # 5 chosen as degree of the fitting polynomial as a higher degree is more accurate, witout being overly so
f = np.poly1d(p)

#These are our points for the fitted curve
point=0     # One point per profile for fitted curve
for point in range(reduced_num_profiles-1):     # "-1" required as the next profile is used to calculate the line
    y_new.append(np.linspace(y_avg[point], y_avg[point+1], num=1))      #y_new and z_new 1x325. option "num" is number of samples to generate (1 is enough)
    z_new.append(f(y_new[point]))
    x_fitted_1.append(1)        # First fitted curve will be at x=1mm (in 3D space)
    x_fitted_2.append(1.1017)  # Next fitted curve will be 0.1017mm (4 d.p.) offset from first fitted curve
                               # 0.1017mm was the avg distance between points in 3 randomly chosen CSV files for x
#Fitted curve generated from reduced_num_profiles-1 many profiles, adding in last one as copy of 2nd to last profile
y_new.append(y_new[reduced_num_profiles-2][:])      #"-2" as we start from index zero in an array and want to copy the 2nd to last element
z_new.append(z_new[reduced_num_profiles-2][:])
x_fitted_1.append(1)
x_fitted_2.append(1.1017)
#-------------------------------------


#Will likely remove
#Redundant as fitted smooth curve is all that is required
"""#Exact curve--------------------------
p_exact = np.polyfit(y_avg, z_avg, 1)
f_exact = np.poly1d(p_exact)
point=0
for point in range(reduced_num_profiles-1):
    y_new_exact.append(np.linspace(y_avg[point], y_avg[point+1], 1))      #y_new and z_new 1x325
    z_new_exact.append(f(y_new_exact[point]))
    
#Same reason as in fitted smooth curve
y_new_exact.append(y_new[reduced_num_profiles-2][:])    
z_new_exact.append(z_new[reduced_num_profiles-2][:])
#-------------------------------------"""

#Removed due to complexity and redundancy
#Kept in-case further development required
"""
#Removing above fitted curve outlying data-------------------------
profile = 0
point = 0
for profile in range(reduced_num_profiles):      
    z_above_diff.append(z_reduced[profile][:] - z_new_exact[profile][:])
    
profile = 0
point = 0
for profile in range(reduced_num_profiles):
    if(any(z_above_diff[profile][:] > above_curve_threshold)):
        above_indices_temp = np.array(np.where(~np.isnan(z_above_diff[profile][:] > above_curve_threshold))).astype(int16)
    else:
        above_indices_temp = np.array([])
    for point in range(len(above_indices_temp)):
        z_reduced[profile][above_indices_temp[point]] = NaN     #Note, due to using fitted curve, misses last profile (due to averaging in z_new_exact)
#------------------------------------------------------------------
"""


#Creating figure for 1st side view
fig1 = plt.figure()
ax1 = fig1.add_subplot()
#Fitted curve for first side view
plot1 = ax1.plot(y_new[:], z_new[:], color='blue')

#Creating figure for 2nd side view
fig2 = plt.figure()
ax2 = fig2.add_subplot()
#Fitted curve for second side view
plot2 = ax2.plot(y_new[:], z_new[:], color='blue')
#-----------------------------------------------------------------------------------------------------------------------------

#Overlaying first side view---------------------------------------------------------------------------------------------------
#Creating buffer for second cross-section
profile = 0
for profile in range(reduced_num_profiles):
    y_first_half.append(y_reduced[profile][:edge_buffer])   #The first edge_buffer many rows from the strips' edge 
    z_first_half.append(z_reduced[profile][:edge_buffer])
#-----------------------------------------------------------------------------------------------------------------------------

#Overlaying second side view--------------------------------------------------------------------------------------------------
#Creating buffer for second cross-section
profile = 0
for profile in range(reduced_num_profiles):
    y_second_half.append(y_reduced[profile][reduced_num_rows-edge_buffer:reduced_num_rows])     #The last edge_buffer many rows, finishing at the strips' edge
    z_second_half.append(z_reduced[profile][reduced_num_rows-edge_buffer:reduced_num_rows])
#-----------------------------------------------------------------------------------------------------------------------------


#Defect detection-------------------------------------------------------------------------------------------------------------
#1. Detecting defect features
#2. Use coordinates encompassing each feature
#3. Plot each half of the cross section with zoomed areas to the defect features

#Find minimum z per profile
profile = 0
for profile in range(reduced_num_profiles):
    z_mins_first_half.append(np.nanmin(z_first_half[profile]))
    z_mins_second_half.append(np.nanmin(z_second_half[profile]))

#First half
profile = 0
profiles_checked = 0
crack_detected = 0
for profile in range(reduced_num_profiles):
    if((z_new[profile][0] - z_mins_first_half[profile]) > depth_threshold):
        print(z_new[profile][0] - z_mins_first_half[profile])
        y_zoom_first_half.append(y_avg[profile])
        z_zoom_first_half.append(z_mins_first_half[profile])
        z_zoom_first_half.append(z_new[profile][0])
        #crack_detected = 1
    #else:
        #if(z_zoom_first_half==[]):
        #    print("There are no cracks")
        #elif(profiles_checked in range(10) and crack_detected):
        #    print("The first set of coordinates taken are outliers")
        #else:
y_max_first_half = np.max(y_zoom_first_half)
y_min_first_half = np.min(y_zoom_first_half)
z_max_first_half = np.max(z_zoom_first_half)
z_min_first_half = np.min(z_zoom_first_half)

if (y_max_first_half == y_min_first_half or y_zoom_first_half == []):
    y_max_first_half = NaN
    y_min_first_half = NaN
    zoom_first_half = 0
    
if (z_max_first_half == z_min_first_half or z_zoom_first_half == []):
    z_max_first_half = NaN
    z_min_first_half = NaN
    
print(y_max_first_half)
print(y_min_first_half)
print(z_max_first_half)
print(z_min_first_half)
            #profile = reduced_num_profiles
            #break       #If the threshold is no longer being passed then this marks the end of the crack

#Second half
profile = 0
for profile in range(reduced_num_profiles):
    if((z_new[profile][0] - z_mins_second_half[profile]) > depth_threshold):
        y_zoom_second_half.append(y_avg[profile])
        z_zoom_second_half.append(z_mins_second_half[profile])
        z_zoom_second_half.append(z_new[profile][0])
    #else:
        #if(z_zoom_second_half==[]):
            #print("There are no cracks")
        #else:
y_max_second_half = np.max(y_zoom_second_half)
y_min_second_half = np.min(y_zoom_second_half)
z_max_second_half = np.max(z_zoom_second_half)
z_min_second_half = np.min(z_zoom_second_half)
            #profile = reduced_num_profiles
            #break       #Unsure how break works

if (y_max_second_half == y_min_second_half or y_zoom_second_half == []):
    y_max_second_half = NaN
    y_min_second_half = NaN
    zoom_second_half = 0 

if (z_max_second_half == z_min_second_half or z_zoom_second_half == []):
    z_max_second_half = NaN
    z_min_second_half = NaN
    
print(y_max_second_half)
print(y_min_second_half)
print(z_max_second_half)
print(z_min_second_half)

    #2D side plot, manually zooming to defects---------------(first half)-----------------------
    #Adding labels, title, etc.
if (zoom_first_half==1):
    ax1.set_xlabel('y (mm)', fontsize=10, rotation=0)
    ax1.set_ylabel('z (mm)', fontsize=10, rotation=0) 
    ax1.set_title('2D side profile of a pantograph carbon strip')

    
    #Zooming in to defects
    ax_inset1 = inset_axes(ax1, 2.5, 2.5, loc='lower center')
    ax_inset1.scatter(y_first_half, z_first_half)
    ax_inset1.scatter(y_new, z_new)
    ax_inset1.set_xlim(y_min_first_half, y_max_first_half)  
    ax_inset1.set_ylim(z_min_first_half, z_max_first_half)      #Actually z but for 2D purposes we call z y and y x
    #Draws box around zoomed area and lines connecting box to actual
    mark_inset(ax1, ax_inset1, loc1=1, loc2=2)

#Changes z-axis range in plot for more realistic curvature of strip
ax1.set_xlim(left=0, right=750, emit=True, auto=False)
ax1.set_ylim(bottom=130, top=240, emit=True, auto=False)
plot3 = ax1.scatter(y_first_half[:][:], z_first_half[:][:], s=0.025)
#-------------------------------------------------------------------------------------------

#2D side plot, manually zooming to defects---------------(second half)-----------------------
#Adding labels, title, etc.
if (zoom_second_half==1):
    ax2.set_xlabel('y (mm)', fontsize=10, rotation=0)
    ax2.set_ylabel('z (mm)', fontsize=10, rotation=0) 
    ax2.set_title('2D side profile of a pantograph carbon strip')

    
    #Zooming in to defects
    ax_inset2 = inset_axes(ax2, 2.5, 2.5, loc='lower center')
    ax_inset2.scatter(y_second_half, z_second_half)
    ax_inset2.scatter(y_new, z_new)
    ax_inset2.set_xlim(y_min_second_half-5, y_max_second_half+5)  
    ax_inset2.set_ylim(z_min_second_half, z_max_second_half)      #Actually z but for 2D purposes we call z y and y x
    #Draws box around zoomed area and lines connecting box to actual
    mark_inset(ax2, ax_inset2, loc1=1, loc2=2)

#Changes z-axis range in plot for more realistic curvature of strip
ax2.set_xlim(left=0, right=750, emit=True, auto=False)
ax2.set_ylim(bottom=130, top=240, emit=True, auto=False)
plot4 = ax2.scatter(y_second_half[:][:], z_second_half[:][:], s=0.025)
    #-------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------


#Plotting all figures--------------------------------------------------------------------------------------------------------------                     
plt.show()  #Show all plots in this program
#----------------------------------------------------------------------------------------------------------------------------------


