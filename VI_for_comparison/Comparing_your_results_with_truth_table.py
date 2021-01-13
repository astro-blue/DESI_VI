#!/usr/bin/env python
# coding: utf-8
import os, sys, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import fnmatch
import argparse


'''
This is a light version of code to make comparison between your VI with the truth tables. 
This is used for self-testing. 

Please do compare your first 100 objects with the truth tables and make sure that 
your results are in reasonable agreements with the truth tables. 
(The disagreement rate < 15%)
'''

def compare_vi(VI_dir,VI_file,VI_truth_file,output_dir):
  VI_base = VI_file[:-4]  # Get rid of .csv at the end of the filename so we can add .png etc... for figures and output. 
  #print(VI_file)
  # Compare different visual inspections
  t = pd.read_csv(VI_dir+VI_truth_file) #truth (merged) file or file you want to compare to
  v = pd.read_csv(VI_dir+VI_file) #This should work for new prospect files

  # If the VI agreed with Redrock, insert the Redrock results into the VI column.  
  v.loc[pd.isna(v['VI_z']), 'VI_z'] = v.loc[pd.isna(v['VI_z']), 'Redrock_z']
  v['VI_z'] = v['VI_z'].astype(float)
  print('test')
  v.loc[pd.isna(v['VI_spectype']), 'VI_spectype'] = v.loc[pd.isna(v['VI_spectype']), 'Redrock_spectype']
  # Gather the results by TARGETID, put them all in g, including only those items the VI'er looked at.
  g = v.merge(t,how='inner',on='TARGETID')
  print(g)
  # Find the disagreements
  i_disagree_z = np.abs(g['VI_z']-g['best_z']) >=0.0033 
  i_disagree_class = abs(g['VI_quality']-g['best_quality']) >= 2  
  i_disagree_spectype = g['VI_spectype'] != g['best_spectype']

  i_good_bestz = g['best_quality'] >=2.5  # Choose only those redshifts that were given a quality >=2.5 in the merged results
  i_good_VIz   = g['VI_quality']   >=3.0  # Choose only those redshifts that were given a quality >=3 by the VI
  i_good_z = i_good_bestz | i_good_VIz

  i_disagree_all = i_disagree_class | i_disagree_z | i_disagree_spectype
  i_disagree_good = i_disagree_z & i_good_z
  #----------------
  # PRINT TO SCREEN
  print('\nOut of %s objects, you disagreed with the merged results on %s redshifts, %s qualities, and %s spectypes.'%(len(g['TARGETID']),sum(i_disagree_z),sum(i_disagree_class),sum(i_disagree_spectype)))
  print('\nNumber of redshift disagreements on high-quality redshifts out = %s (out of %s).' % (sum(i_disagree_good),sum(i_good_z)))
  print('\nTotal number of disagreements = %s.'%sum(i_disagree_all))
  print( g[['TARGETID','best_z','VI_z','best_quality','VI_quality','best_spectype','VI_spectype']][i_disagree_all])

  conflicts = ''
  for target in g['TARGETID'][i_disagree_all]:
    conflicts = conflicts+', '+str(target)
  print('\nLook at your disagreements by opening the Prospect notebook viewer https://github.com/desihub/prospect/blob/master/doc/nb/Prospect_targetid.ipynb in JupyterLab on NERSC (instructions here https://desi.lbl.gov/trac/wiki/Computing/JupyterAtNERSC) and cutting and pasting the following target list:')
  print(conflicts[2:])
  #---------------------------------------------------------------------------------------------------------------------------------------- 

  summaryfile = open(output_dir+VI_base+'_results.txt', "w") ####### PRINT OUTPUT TO FILE ########
  summaryfile.write('\nOut of %s objects, you disagreed with the merged results on %s redshifts, %s qualities, and %s spectypes.'%(len(g['TARGETID']),sum(i_disagree_z),sum(i_disagree_class),sum(i_disagree_spectype)))
  summaryfile.write('\nNumber of redshift disagreements on high-quality redshifts = %s (out of %s).'%(sum(i_disagree_good),sum(i_good_z)))
  summaryfile.write('\nTotal number of disagreements = %s.\n'%sum(i_disagree_all))
  if len(g['TARGETID'])>0:
    summaryfile.write('Fraction of disagreements [redshift, qualities, spectpes, all]= %s, %s, %s, %s.\n' % (sum(i_disagree_z)/len(g['TARGETID']),sum(i_disagree_class)/len(g['TARGETID']),sum(i_disagree_spectype)/len(g['TARGETID']),sum(i_disagree_all)/len(g['TARGETID'])))
    summaryfile.write('Fraction of disagreements for good redshift objects= %s.\n' % (sum(i_disagree_good)/sum(i_good_z)))
  
  g[['TARGETID','best_z','VI_z','best_quality','VI_quality','best_spectype','VI_spectype']][i_disagree_all].to_string(summaryfile)
  summaryfile.write('\n\nLook at your disagreements by opening the Prospect notebook viewer https://github.com/desihub/prospect/blob/master/doc/nb/Prospect_targetid.ipynb in JupyterLab on NERSC (instructions here https://desi.lbl.gov/trac/wiki/Computing/JupyterAtNERSC) and cutting and pasting the following target list:\n')
  summaryfile.write(conflicts[2:])
  summaryfile.close()
 

#------------------------------------------------------------------
# Run the comparison

VI_dir = '/Users/tlan/Dropbox/Astro_Research/Projects_plots_notes/2020_DESI_visual_inspect/SV1/ELG_80608/'
file='desi-vi_ELG_tile80608_nightdeep_1_TWL.csv' # your VI file
VI_truth_file='ELG_TWL_truth_80608_1.csv' # Insert the corresponding truth table
output_dir = VI_dir+'/test/'

if not os.path.exists(output_dir):
  os.makedirs(output_dir)

compare_vi(VI_dir,file,VI_truth_file,output_dir)