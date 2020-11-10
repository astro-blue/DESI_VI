import os, sys, glob
import numpy as np

from astropy.io import fits
from astropy.table import Table, join, vstack
from astropy.io import fits

import pandas as pd
import fnmatch

import desispec.io

import matplotlib.pyplot as plt 


def read_individual_VI(VI_dir):
    
    #we will read all the *.csv files in the VI_dir. Change as needed.

    print('Reading all individual VI files in '+VI_dir)
    
    all_files = os.listdir(VI_dir)
    vi_files=[]

    pattern = "desi*.csv"
    for entry in all_files:
        if fnmatch.fnmatch(entry, pattern):
            vi_files.append(entry)

    vi = pd.read_csv(VI_dir + vi_files[0], delimiter = " , ", engine='python')

    for i in range(1,len(vi_files)):
        print(vi_files[i])
        vi2 = pd.read_csv(VI_dir + vi_files[i], delimiter = " , ", engine='python')
        vi = vi.append(vi2, ignore_index=True)
    
    return vi

def find_conflicts(vi_gp):
    vi_conflict = vi_gp.filter(lambda x: ( ( (x['VI_quality'].max()-x['VI_quality'].min()) >= 2) 
                       | ( (x['best redshift'].max() - x['best redshift'].min()) / (1+x['best redshift'].min()) > 0.0033 ) 
                       | (not all(i == x['best spectype'].iloc[0] for i in x['best spectype'])) )
                       & (x['VI_quality'].max() > 2)
                       & (len(x) >= 2)) #x is a group by TargetID)
    return vi_conflict


def prep_new_columns(vi):
    #make new column with best redshift estimate for each VI - take VI redshift if available, else take Redrock redshift. 
    #I am always assuming that the VI redshift, if provided, trumps over the Redrock redshift. 
    #print(1)
    vi['best redshift']=vi['VI_z']
    #print(2)
    vi.loc[vi['best redshift'].isnull(), 'best redshift'] = vi.loc[vi['best redshift'].isnull(), 'Redrock_z']
    #vi.loc[vi['best redshift']=='Target ', 'best redshift'] = 0 #catch someone who wrote in VI z field
    vi['best redshift'] = vi['best redshift'].astype(float)
    
    #make new column with best spectype estimate for each VI - take VI spectype if available, else take Redrock spectype 
    #I am always assuming that the VI redshift, if provided, trumps over the Redrock redshift. 
    vi['best spectype'] = vi['VI_spectype']
    vi.loc[vi['best spectype'].isnull(), 'best spectype'] = vi.loc[vi['best spectype'].isnull(), 'Redrock_spectype']
    
    #add new columns, holding the mean of the flags and the maximum difference in flag classification
    vi['vi_combined_flag'] = vi.groupby('TARGETID')['VI_quality'].transform('mean')
    vi['vi_diff'] = vi.groupby('TARGETID')['VI_quality'].transform(lambda x: ( x.max()-x.min()) )
    
    #add new column, difference in 'best redshift'
    vi['dz'] = vi.groupby('TARGETID')['best redshift'].transform(lambda x: ( (x.max() - x.min()) / (1+x.min()) ))
    #add new column with the mean of best redshift if they're within 0.0033*(1+z)
    vi.loc[vi.dz < 0.0033, 'vi_combined_z'] = vi.loc[vi.dz < 0.0033].groupby('TARGETID')['best redshift'].transform('mean')
    #keep as redrock z is difference is greater. These will be manually resolved if at least one of the inspectors flags a z as flag >2
    vi.loc[vi.dz >= 0.0033, 'vi_combined_z'] = vi.loc[vi.dz >= 0.0033, 'Redrock_z']
    
    #add new column, with all comments concatenated
    #this protects agains None in 'VI comment' field
    vi.loc[vi['VI_comment'].isnull(),'VI_comment']='--'
    vi['all VI comments'] = vi.groupby('TARGETID')['VI_comment'].transform(lambda x: '|'.join(x))
    
    #add new column, with the number of VI inspections for each object
    vi['N_VI'] = vi.groupby('TARGETID')['TARGETID'].transform('count')
    
    #add new column to hold comments from merger if needed
    vi['merger comment'] = 'none'
    
    return vi
