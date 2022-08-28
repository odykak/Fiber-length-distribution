# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 17:26:49 2022

@author: KO
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import glob
import os
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from io import StringIO
from statistics import mean
from statistics import stdev
from natsort import natsorted
from scipy.stats import norm

#Appearance stuff (colors, font size etc)

#My colors
# mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5'])
#                                                       0sangre,   1neptune,  2pumpkin,  3clover,   4denim,    5cocoa,    6cumin,    7berry3

# mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['#e41a1c','#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#dede00'])

# Nature colors
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['0C5DA5', 'FF2C00', 'FF9500', '00B945', '845B97', '474747', '9e9e9e'])

#Seaborn colors
# colors=sns.color_palette("rocket",3)

# Font size. Dictionary taking numerous parameters.
plt.rcParams.update({'font.size' : 10})
plt.rcParams['axes.axisbelow'] = True

# Gets current working directory (cwd)
# cwd=os.getcwd()

# Working directory. Pick where you want to save your stuff
wd=r"Your working directory"

# # Creates a folder to store the graphs inside the cwd
 mesa= wd + '/Fibers length distribution/'
 if not os.path.exists(mesa):
     os.makedirs(mesa)
        
#Data should be in folders named as in list called "ines"
ines=['0.18 mm','0.2 mm','0.25 mm','0.5 mm','0.7 mm','1 mm']
graph=['a','b','c','d','e','f']
mean_fiber_length=[]
dev_fiber_length=[]

for index,ina in enumerate(ines):
    #Path to data. Full path if in different folder than this script is. Otherwise *files common name part*".
    file_list = [i for i in glob.glob("path to file/"+ina+"/Results*")]
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
   
    mu, std = norm.fit(total['Length'])
    
    bins=13
    fig = plt.figure(figsize=(3.5,2.625))
    plt.hist(total['Length'],bins=bins,color='#1f77b4',density=True,edgecolor = 'black')
    plt.grid(axis='y',linestyle='dashed', linewidth='0.3', color='grey',alpha=0.8)
    plt.xlabel('Fiber length (μm)')
    plt.ylabel('Normalized fiber count')
    plt.title(f'{ines[index]} nominal length',fontsize=12)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax,100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, '#FF9500', linewidth=1)
    print(round(mu,3),"±" ,round(std,3))
    
    ax=plt.gca()
    ax.text(0.02, 0.9, f'{graph[index]})',transform=ax.transAxes,fontsize=14, fontweight='bold')

    # plt.savefig(mesa+f'{ines[index]}'+'.png', dpi=300,bbox_inches="tight",) #pad_inches=0.05
