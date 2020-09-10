#!/usr/bin/env python
# coding: utf-8
import os, sys, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import fnmatch
import argparse
import re

#VI_check_dir = '/Users/uqtdavi1/Documents/programs/DESI/SV/VI_files/SV0/QSO/VI_check/VI_check_all_txt/'
VI_check_dir = ['/Users/tlan/Dropbox/Astro_Research/Projects_plots_notes/2020_DESI_visual_inspect/VI_v1_individual/BGS/individual_inspectors/VI_check/',
'/Users/tlan/Dropbox/Astro_Research/Projects_plots_notes/2020_DESI_visual_inspect/VI_v1_individual/LRG/individual_inspectors/VI_check/',
'/Users/tlan/Dropbox/Astro_Research/Projects_plots_notes/2020_DESI_visual_inspect/VI_v1_individual/ELG/individual_inspectors/VI_check/',
'/Users/tlan/Dropbox/Astro_Research/Projects_plots_notes/2020_DESI_visual_inspect/VI_v1_individual/QSO/individual_inspectors/VI_check_test/']
colors = ['g','r','b','black']
text = ['BGS','LRG','ELG','QSO']
plt.figure(figsize=(8,8))
plt.subplots_adjust(hspace=0.0)
for index, i_vi in enumerate(VI_check_dir):
	all_files = os.listdir(i_vi)
	name_id = []

	for i,file in enumerate(all_files):
		name_id.append(file[0:3])

	unique_id = list(set(name_id))
	n=len(unique_id)
	names = [None]*n #[None for _ in range(len(all_files))]
	zerr =np.zeros(n) # Error on redshifts
	qerr =np.zeros(n) # Error on qualities
	serr =np.zeros(n) # Error on spectype
	gerr =np.zeros(n) # Error on good redshifts
	terr =np.zeros(n) # Total number of errors (zerr+qerr+serr)
	total_vi = np.zeros(n)


	for i,file in enumerate(unique_id):
		names[i] = file
		f=open(i_vi+file+'_results.txt','r')
		ff=f.readlines()
		m = re.search('of(.+?)objects', ff[1])
		total_vi[i]=np.int(m.group(1))
	
		m = re.search('on(.+?)redshifts', ff[1])
		zerr[i]=np.int(m.group(1))
		m = re.search('redshifts,(.+?)qualities', ff[1])
		qerr[i]=np.int(m.group(1))
		m = re.search('and(.+?)spectypes', ff[1])
		serr[i]=np.int(m.group(1))
		m = re.search('=(.+?)\.', ff[2])
		gerr[i]=np.int(m.group(1))
		m = re.search('=(.+?)\.', ff[3])
		terr[i]=np.int(m.group(1))
		print(names[i], zerr[i], qerr[i], serr[i], gerr[i], terr[i])
		f.close()

	#d=pd.DataFrame(data=[names,zerr,qerr,serr,gerr,terr],columns=['names','zerr','qerr','serr','gerr','terr'])
	data={'names':names,'zerr':zerr,'qerr':qerr,'serr':serr,'gerr':gerr,'terr':terr,'total_vi':total_vi,'terr_frac':terr/total_vi}
	df = pd.DataFrame(data=data)
	ufsort=df.sort_values(by=['terr_frac'])
	plt.subplot(4,1,index+1)
	plt.hist(ufsort.terr_frac,bins=50,range=(0,0.6),color=colors[index])
	#plt.plot(ufsort.names,ufsort.gerr/ufsort.total_vi,'s',label='good redshifts',markersize=10)
	#plt.plot(ufsort.names,ufsort.zerr/ufsort.total_vi,'.',label='redshift',markersize=12)
	#plt.plot(ufsort.names,ufsort.qerr/ufsort.total_vi,'.',label='quality',markersize=12)
	#plt.plot(ufsort.names,ufsort.serr/ufsort.total_vi,'.',label='spectype',markersize=12)
	#plt.plot(ufsort.names,np.ones(len(ufsort.names))*0.05,':',label="5% error",markersize=10)
	plt.text(0.4,4.5,text[index],color=colors[index],fontsize=15)
	'''
	for i in range(0,len(index_order)):


		plt.text(i-0.2,data['terr_frac'][index_order[i]]+0.01, int(data['total_vi'][index_order[i]]),fontsize=10)	

	'''
	#plt.title('BGS - Percentage of disagreements of each type')
	plt.ylim(0,6.5)
	plt.xlim(-0.05,0.55)
	#plt.legend()
	#plt.savefig('QSO_VI_assess_inspectors.png', bbox_inches='tight')
plt.show()

