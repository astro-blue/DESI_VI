import numpy as np
import pandas as pd

v = pd.read_csv('desi-vi_ELG_tile80608_nightdeep_1_TWL.csv') #This should work for new prospect files
v.loc[pd.isna(v['VI_z']), 'VI_z'] = v.loc[pd.isna(v['VI_z']), 'Redrock_z']
v.loc[pd.isna(v['VI_spectype']), 'VI_spectype'] = v.loc[pd.isna(v['VI_spectype']), 'Redrock_spectype']


v['best_quality']=v['VI_quality']
v['best_spectype']=v['VI_spectype']
v['best_z']=v['VI_z']
del v['VI_z']
del v['VI_quality']
del v['VI_spectype']
#v.drop(columns=['VI_z','VI_quality','VI_spectype'],axis=1)
v.to_csv('ELG_TWL_truth.csv',index=False)
#v['VI_z'].fillna(9.99)
# If the VI agreed with Redrock, insert the Redrock results into the VI column.  
#v['VI_z']
#v.loc[pd.isna(v['VI_z']), 'VI_z'] = v.loc[pd.isna(v['VI_z']), 'Redrock_z']
#v['VI_z'] = v['VI_z'].astype(float)
