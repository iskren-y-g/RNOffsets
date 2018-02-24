import numpy as np
import pandas as pd

# Initialize variables
r_max=22.; min_sep=9.; n_pos=int(30)    # Maximum x,y size of dither box. Minimum separation between offsets within the dither box. Number of offsets

x_off=0.0;y_off=0.0; x1=0.0; x2=0.0;x3=0.0; y1=0.0; y2=0.0;y3=0.0; dist1=0.0; dist2=0.0; dist12=0.0   # Initialisation of variables
i=int(0) # Counter for the non repetive random offsets
k=int(0)   # Counter for the last offset

# Initialize the data frame
offset_file=pd.DataFrame(columns=['x_off','y_off'])

if min_sep/r_max>.55:
    print('\nError! The requested min_sep/r_max %.2f is too high! Re-run with ratio lower than ~0.55\n' % (min_sep/r_max))
    raise SystemExit
elif min_sep/r_max<=.55 and min_sep/r_max>=.45:
    print('\nWarning! The requested min_sep/r_max %.2f is too high and program might be stuck. Ctrl+C and re-run with lower ratio than ~0.4\n' % (min_sep/r_max))

for offset in range(1,n_pos+1,1):
    i=i+1; k=k+1      # Initializing the counters 
    if i==1:    # For the first offset, in each group of 3 offsets
        if k>=3:    # If not the very first offset, generate new random positions, calculate the distance and repeat until the while condition is fullfilled
            x_off=np.random.uniform(-1000,1000,1)*(r_max/np.sqrt(6))/1000.
            y_off=np.random.uniform(-1000,1000,1)*(r_max/np.sqrt(6))/1000.
            if np.sign(x1)==np.sign(x_off) : x_off=-1*x_off
#            if np.sign(y1)==np.sign(y_off) : y_off=-1*y_off
            dist1=np.sqrt((x_off-x1)**2+(y_off-y1)**2)
            while dist1<=min_sep:
                x_off=np.random.uniform(-1000,1000,1)*(r_max/np.sqrt(6))/1000.
                y_off=np.random.uniform(-1000,1000,1)*(r_max/np.sqrt(6))/1000.
 #               if np.sign(x1)==np.sign(x_off) : x_off=-1*x_off
                if np.sign(y1)==np.sign(y_off) : y_off=-1*y_off
                dist1=np.sqrt((x_off-x1)**2+(y_off-y1)**2)#; print('Trying new offsets 1')
            x1=x_off;y1=y_off   # Assign the new offset positions tio the temp variables
        else:   # For the very first offset, do nothing
            x1=x_off;y1=y_off
    if i==2:    # For the 2nd offset in the group of 3, generate new offset positions, and repeat while the condition is fullfilled
        x_off=np.random.uniform(-1000,1000,1)*(r_max/np.sqrt(6))/1000.
        y_off=np.random.uniform(-1000,1000,1)*(r_max/np.sqrt(6))/1000.
        if np.sign(x1)==np.sign(x_off) : x_off=-1*x_off
#        if np.sign(y1)==np.sign(y_off) : y_off=-1*y_off
        dist1=np.sqrt((x_off-x1)**2+(y_off-y1)**2)
        while dist1<=min_sep:
            x_off=np.random.uniform(-1000,1000,1)*(r_max/np.sqrt(6))/1000.
            y_off=np.random.uniform(-1000,1000,1)*(r_max/np.sqrt(6))/1000.
#            if np.sign(x1)==np.sign(x_off) : x_off=-1*x_off
            if np.sign(y1)==np.sign(y_off) : y_off=-1*y_off
            dist1=np.sqrt((x_off-x1)**2+(y_off-y1)**2)#; print('Trying new offsets 2')
        x2=x_off;y2=y_off
    if i==3:
        x_off=np.random.uniform(-1000,1000,1)*(r_max/np.sqrt(6))/1000.
        y_off=np.random.uniform(-1000,1000,1)*(r_max/np.sqrt(6))/1000.#; print(x_off,y_off)
#        if np.sign(x2)==np.sign(x_off) : x_off=-1*x_off
#        if np.sign(y2)==np.sign(y_off) : y_off=-1*y_off
        dist1=np.sqrt((x_off-x1)**2+(y_off-y1)**2)
        dist2=np.sqrt((x_off-x2)**2+(y_off-y2)**2)
        dist12=np.sqrt((x1-x2)**2+(y1-y2)**2)
        while dist1<=min_sep or dist2<=min_sep or dist12<=min_sep:
            x_off=np.random.uniform(-1000,1000,1)*(r_max/np.sqrt(6))/1000.
            y_off=np.random.uniform(-1000,1000,1)*(r_max/np.sqrt(6))/1000.#; print(x_off,y_off)
#            if np.sign(x2)==np.sign(x_off) : x_off=-1*x_off
#            if np.sign(y2)==np.sign(y_off) : y_off=-1*y_off
            dist1=np.sqrt((x_off-x1)**2+(y_off-y1)**2)#; print('Trying new offsets 3')
            dist2=np.sqrt((x_off-x2)**2+(y_off-y2)**2)
            dist12=np.sqrt((x1-x2)**2+(y1-y2)**2)
        x1=x_off;y1=y_off
        i=0
    if offset==1: print('#No. offset\tx\ty\tDist1\tDist2\tDist3')
    print('%d\t\t%5.2f\t%5.2f\t%5.2f\t%5.2f\t%5.2f' % (offset,x_off,y_off,dist1,dist2,dist12))
    if offset==1: 
        offset_file=offset_file.append({'x_off': float(x_off), 'y_off': abs(float(y_off))}, ignore_index=True)
    else:
        offset_file=offset_file.append({'x_off': float(x_off), 'y_off': float(y_off)}, ignore_index=True)
offset_file.to_csv('temp.off',sep=';', float_format='%.2f',header=False,index=False)
