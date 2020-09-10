import pandas as pd
import fnmatch
import argparse
import os
VI_dir     = '/Users/tlan/Dropbox/Astro_Research/Projects_plots_notes/2020_DESI_visual_inspect/VI_v1_individual/QSO/'

pattern = "*.csv"

all_files = os.listdir(VI_dir)
vi_id=[]
for entry in all_files:
	if fnmatch.fnmatch(entry, pattern):
  		vi_id.append(entry[-7:-4]) 
  		
unique_id = list(set(vi_id))
VI_output = VI_dir+'individual_inspectors/'
#unique_id = ['TWL']

for i_id in unique_id:
	pattern = "desi*"+i_id+".csv"	
	vi_files=[]
	file_count = 0
	for entry in all_files:
		if fnmatch.fnmatch(entry, pattern):
			if file_count==0:
				base_file = pd.read_csv(VI_dir+entry,delimiter = " , ", engine='python')
				print('1')
			else:	
				new_file = pd.read_csv(VI_dir+entry,delimiter = " , ", engine='python')
				base_file = base_file.append(new_file)
			file_count+=1
	
	base_file.to_csv(VI_output+i_id+'.csv')
 		