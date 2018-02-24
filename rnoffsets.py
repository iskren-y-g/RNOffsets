import argparse
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Initialize variables
#box_max=22.; min_sep=9.; n_pos=int(30)    # Maximum x,y size of dither box. Minimum separation between offsets within the dither box. Number of offsets

parser = argparse.ArgumentParser()
parser.add_argument("--n_pos", type=int, default=15,help="Number of offsets")
parser.add_argument("--box_max", type=float, default=22.,help="Maximum size of dither box")
parser.add_argument("--min_sep", type=float, default=9.,help="Minimum separation between consecutive offsets box_max")
parser.add_argument("--connect", type=str,default='Y',help="Connect with line the offsetsin each group?")
args = parser.parse_args()
if args.n_pos:
    n_pos=args.n_pos
if args.box_max:
    box_max=args.box_max
if args.min_sep:
    min_sep=args.min_sep
if args.connect:
    connect=args.connect

x_off=0.0;y_off=0.0; x1=0.0; x2=0.0;x3=0.0; y1=0.0; y2=0.0;y3=0.0; dist1=0.0; dist2=0.0; dist12=0.0   # Initialisation of variables
i=int(0) # Counter for the non repetive random offsets
k=int(0)   # Counter for the last offset

# Initialize the data frame
offset_file=pd.DataFrame(columns=['x_off','y_off','ni'])

if min_sep/box_max>.55:
    print('\nError! The requested min_sep/box_max %.2f is too high! Re-run with ratio lower than ~0.55\n' % (min_sep/box_max))
    raise SystemExit
elif min_sep/box_max<=.55 and min_sep/box_max>=.45:
    print('\nWarning! The requested min_sep/box_max %.2f is too high and program might be stuck. Ctrl+C and re-run with lower ratio than ~0.4\n' % (min_sep/box_max))

for offset in range(1,n_pos+1,1):
    i=i+1; k=k+1      # Initializing the counters 
    if i==1:    # For the first offset, in each group of 3 offsets
        if k>=3:    # If not the very first offset, generate new random positions, calculate the distance and repeat until the while condition is fullfilled
            x_off=np.random.uniform(-1000,1000,1)*(box_max*.5)/1000.
            y_off=np.random.uniform(-1000,1000,1)*(box_max*.5)/1000.
            if np.sign(x1)==np.sign(x_off) : x_off=-1*x_off
            dist1=np.sqrt((x_off-x1)**2+(y_off-y1)**2)
            while dist1<=min_sep:
                x_off=np.random.uniform(-1000,1000,1)*(box_max*.5)/1000.
                y_off=np.random.uniform(-1000,1000,1)*(box_max*.5)/1000.
                if np.sign(y1)==np.sign(y_off) : y_off=-1*y_off
                dist1=np.sqrt((x_off-x1)**2+(y_off-y1)**2)#; print('Trying new offsets 1')
            x1=x_off;y1=y_off   # Assign the new offset positions tio the temp variables
        else:   # For the very first offset, do nothing
            x1=x_off;y1=y_off
    if i==2:    # For the 2nd offset in the group of 3, generate new offset positions, and repeat while the condition is fullfilled
        x_off=np.random.uniform(-1000,1000,1)*(box_max*.5)/1000.
        y_off=np.random.uniform(-1000,1000,1)*(box_max*.5)/1000.
        if np.sign(x1)==np.sign(x_off) : x_off=-1*x_off
        dist1=np.sqrt((x_off-x1)**2+(y_off-y1)**2)
        while dist1<=min_sep:
            x_off=np.random.uniform(-1000,1000,1)*(box_max*.5)/1000.
            y_off=np.random.uniform(-1000,1000,1)*(box_max*.5)/1000.
            if np.sign(y1)==np.sign(y_off) : y_off=-1*y_off
            dist1=np.sqrt((x_off-x1)**2+(y_off-y1)**2)#; print('Trying new offsets 2')
        x2=x_off;y2=y_off
    if i==3:
        x_off=np.random.uniform(-1000,1000,1)*(box_max*.5)/1000.
        y_off=np.random.uniform(-1000,1000,1)*(box_max*.5)/1000.#; print(x_off,y_off)
        dist1=np.sqrt((x_off-x1)**2+(y_off-y1)**2)
        dist2=np.sqrt((x_off-x2)**2+(y_off-y2)**2)
        dist12=np.sqrt((x1-x2)**2+(y1-y2)**2)
        while dist1<=min_sep or dist2<=min_sep or dist12<=min_sep:
            x_off=np.random.uniform(-1000,1000,1)*(box_max*.5)/1000.
            y_off=np.random.uniform(-1000,1000,1)*(box_max*.5)/1000.#; print(x_off,y_off)
            dist1=np.sqrt((x_off-x1)**2+(y_off-y1)**2)#; print('Trying new offsets 3')
            dist2=np.sqrt((x_off-x2)**2+(y_off-y2)**2)
            dist12=np.sqrt((x1-x2)**2+(y1-y2)**2)
    if offset==1: print('#No. offset\tx\ty\tDist1\tDist2\tDist3')
    print('%d\t\t%5.2f\t%5.2f\t%5.2f\t%5.2f\t%5.2f%4d' % (offset,x_off,y_off,dist1,dist2,dist12,i))
    if offset==1: 
        offset_file=offset_file.append({'x_off': float(x_off), 'y_off': abs(float(y_off)), 'ni': int(i)}, ignore_index=True)
    else:
        offset_file=offset_file.append({'x_off': float(x_off), 'y_off': float(y_off), 'ni': int(i)}, ignore_index=True)
    if i==3: x1=x_off;y1=y_off;i=0
offset_file.to_csv('temp.off',columns=['x_off','y_off'], sep=';', float_format='%.2f',header=False,index=False)

# Scatter plot of all
#plt.rcParams["font.family"] = "serif"; plt.rcParams["font.size"] = 11
plt.figure(figsize=plt.figaspect(1.))
plt.xlabel('$\Delta$ X [arcsec]'); plt.ylabel('$\Delta$ Y [arcsec]')
plt.xlim(-(box_max*.5),(box_max*.5));plt.ylim(-(box_max*.5),(box_max*.5))
lim_max=int(round(box_max*.5+2))
plt.xticks(range(-lim_max,lim_max,2)); plt.yticks(range(-lim_max,lim_max,2))
plt.scatter(offset_file['x_off'],offset_file['y_off'], s=28, facecolors='none', edgecolors='b',label='')
plt.vlines(0,-11,11, linestyles='--', colors='lightgray')
plt.plot(np.linspace(-11,11,200),np.linspace(-1e-3,1e-3,200), color='lightgray', linestyle='dashed',label='')

# Connect with lines the offsets in each offset group
if connect=='Y':
    i=0;k=0; temp_x=[];temp_y=[]
    for xi_pos,yi_pos,ni_pos in zip(offset_file.x_off,offset_file.y_off,offset_file.ni):
        plt.annotate(str(int(ni_pos)),xy=(xi_pos,yi_pos))
        i=i+1
        if i<=3:
            temp_x.append(xi_pos); temp_y.append(yi_pos)
        if i==3: k=k+1
        if i==3: plt.plot(temp_x,temp_y,'-', linewidth=2, label='Grp'+str(int(k)))
        if i==3: i=0; temp_x=[]; temp_y=[]
    plt.legend(frameon=False,ncol=3)

plt.tight_layout()
plt.show()