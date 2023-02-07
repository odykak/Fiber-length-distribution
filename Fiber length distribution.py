import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import glob
from statistics import mean
from statistics import stdev
from natsort import natsorted
from scipy.stats import norm

# Nature colors
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['0C5DA5', 'FF2C00', 'FF9500', '00B945', '845B97', '474747', '9e9e9e'])

# Font size. Dictionary taking numerous parameters.
plt.rcParams.update({'font.size' : 10})
plt.rcParams['axes.axisbelow'] = True

fibres=['80 μm','180 μm','200 μm','250 μm','500 μm','700 μm','1 mm']
graph=['a','b','c','d','e','f','g']
mean_fiber_length=[]
dev_fiber_length=[]

for index,fibre in enumerate(fibres):
    #Path to data. Full path if in different folder than this script is. My data files all with the Result prefix in their name, were located in folder names after the average, nominal, fibre length
    file_list = [i for i in glob.glob("Folder path/"+fibre+"/Results*")]
    #Sort in order of number appearing in front. Omit or adjust accordingly in case of different naming.
    file_list=natsorted(file_list)
    
    # Loading all the csv files to create a list of data frames
    data = [pd.read_csv(file) for file in file_list]
    
    #Concatanating all dataframes
    total=pd.concat([dataframe for dataframe in data],axis=0)
    
    mean_length=round(mean(total['Length']),3)
    dev_length=round(stdev(total['Length']),3)
    mean_fiber_length.append(mean_length)
    dev_fiber_length.append(dev_length)
    
    # mu, std = norm.fit(total['Length'])
    q1, q3 = total['Length'].quantile([0.75,0.25])
    h = 2*(q1-q3)*len(total['Length'])**(-1/3)
    bins = round((total['Length'].max()-total['Length'].min())/h)
    
    fig = plt.figure(figsize=(3.5,2.625))
    plt.hist(total['Length'],density=True,bins=bins,color='#1f77b4',edgecolor = 'black')#width=20,
    plt.grid(axis='y',linestyle='dashed', linewidth='0.3', color='grey',alpha=0.8)
    plt.xlabel('Fiber length (μm)')
    plt.ylabel('Normalized fiber count')# or count = # of fibers'
    plt.tick_params(length=3, width=0.5)# Bot left by default True if memory serves me. All change with =False though.

    mu, std = norm.fit(total['Length'])
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax,100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, '#FF9500', linewidth=2)
    print(round(mu,3),"±" ,round(std,3))
    
    ax=plt.gca()
    ax.text(0.02, 0.9, f'{graph[index]})',transform=ax.transAxes,fontsize=14, fontweight='bold')
