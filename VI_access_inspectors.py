#!/usr/bin/env python
# coding: utf-8
import os, sys, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import fnmatch
import argparse
import re

VI_check_dir = '/Users/tlan/Dropbox/Astro_Research/Projects_plots_notes/2020_DESI_visual_inspect/VI_v1_individual/QSO/VI_check_all_single/'

all_files = os.listdir(VI_check_dir)
n=len(all_files)
names = [None]*n #[None for _ in range(len(all_files))]
zerr =np.zeros(n) # Error on redshifts
qerr =np.zeros(n) # Error on qualities
serr =np.zeros(n) # Error on spectype
gerr =np.zeros(n) # Error on good redshifts
terr =np.zeros(n) # Total number of errors (zerr+qerr+serr)
total_vi = np.zeros(n)
for i,file in enumerate(all_files):
	names[i] = file[-15:-12]
	f=open(VI_check_dir+file,'r')
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
	print(names[i], zerr[i], qerr[i], serr[i], gerr[i], terr[i],total_vi[i])
	f.close()

#d=pd.DataFrame(data=[names,zerr,qerr,serr,gerr,terr],columns=['names','zerr','qerr','serr','gerr','terr'])
data={'names':names,'zerr':zerr,'qerr':qerr,'serr':serr,'gerr':gerr,'terr':terr,'terr_frac':np.array(terr)*1.0/total_vi}
df = pd.DataFrame(data=data)
users = np.unique(df['names'].tolist())
nusers = len(users)

usermean={'names':users,'zerr':np.zeros(nusers),'qerr':np.zeros(nusers),'serr':np.zeros(nusers),'gerr':np.zeros(nusers),'terr':np.zeros(nusers),'terr_frac':np.zeros(nusers)}
uf = pd.DataFrame(data=usermean)

print(df.loc[df.names==users[0], ['names','zerr','qerr','serr','gerr','terr']])
for user in users:
	print(df.loc[df.names==user, ['names','zerr','qerr','serr','gerr','terr','terr_frac']])
	for choice in ['zerr','qerr','serr','gerr','terr','terr_frac']:
		uf.loc[uf.names==user,choice] = df.loc[df.names==user, choice].mean()

	#print(df.loc[df.names==users[0], ['names','zerr','qerr','serr','gerr','terr']].mean())
ufsort=uf.sort_values(by=['terr_frac'])
print(uf.sort_values(by=['terr_frac']))

plt.ion()
plt.figure(figsize=(10,5))
plt.plot(ufsort.names,ufsort.terr/0.5,'o',label='total (r+q+s)')
plt.plot(ufsort.names,ufsort.gerr/0.5,'s',label='good redshifts')
plt.plot(ufsort.names,ufsort.zerr/0.5,'.',label='redshift')
plt.plot(ufsort.names,ufsort.qerr/0.5,'.',label='quality')
plt.plot(ufsort.names,ufsort.serr/0.5,'.',label='spectype')
plt.plot(ufsort.names,np.ones(nusers)*5.0,':',label="5% error")
plt.title('Percentage of disagreements of each type')
plt.legend()
#plt.savefig('VI_assess_inspectors.png', bbox_inches='tight')
#plt.show()
#plt.close()