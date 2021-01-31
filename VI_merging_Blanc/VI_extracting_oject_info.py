import os, sys, glob
import numpy as np
import inspect
from astropy.io import fits
from astropy.table import Table, join, vstack
from astropy.io import fits
import pandas as pd
import fnmatch
import matplotlib.pyplot as plt 
import re
from datetime import datetime
from pytz import timezone
from VI_merge_functions_v2 import *
pd.options.display.max_colwidth = 150

on_nersc = True
if on_nersc:
  import desispec.io
  import desispec

#--------------------------------------------------------------------------------------------------
# USER DEFINED INPUTS BELOW ARE "tiles", "nights", and "subset"; and importantly "output_name".
#--------------------------------------------------------------------------------------------------
if on_nersc:  
  # Set to directory with all the VI files to merge
  VI_dir = os.environ['HOME']+'/projects/VI_files/SV1/BGS/'
else:
  VI_dir = '/Users/uqtdavi1/Documents/programs/DESI/SV/VI_files/SV0/Blanc/BGS/'

# Here you need to choose the tiles on which your objects were observed
tiledir   = '/global/cfs/cdirs/desi/spectro/redux/blanc/tiles/'
tiles = ['80609']
nights = ['20201223']
petals = ['0','1','2','3','4', '5', '6' ,'7', '8', '9']
#subset = "_15_"  # YOU WANT TO CHANGE THIS EACH TIME, it defines "pattern" below.  Set to "" to use all.
#output_name = "desi-vi_BGS_tile"+tiles[0]+"_nightdeep"+subset+"merged"
file_name = 'desi-vi_QSO_tile80609_nightdeep_merged_all'
vi = pd.read_csv(VI_dir+file_name+'.csv', delimiter = ",", engine='python', keep_default_na=False)
vi['TILEID']=tiles[0]
if on_nersc:
  vi = add_auxiliary_data(vi,tiledir,tiles,nights,petals)

vi = vi[['TARGETID','Redrock_z', 'best_z', 'best_quality', 'Redrock_spectype', 'best_spectype', 'all_VI_issues', 'all_VI_comments', 'merger_comment','N_VI','DELTACHI2', 'ZWARN', 'ZERR','TARGET_RA','TARGET_DEC','FIBER','FLUX_G', 'FLUX_R', 'FLUX_Z','FIBERFLUX_G', 'FIBERFLUX_R', 'FIBERFLUX_Z', 'EBV','TILEID']]

output_filename = filename+'_ADDING_object_info.csv'
vi.to_csv(VI_dir+output_filename,index=False)