
# coding: utf-8

# In[1]:

# Libraries & directories
import pandas as pd


# In[2]:

dirData = 'data/'
dirDataExt = dirData + 'external/'

dirCensusTracts = dirDataExt + 'census-tracts/'


# In[22]:

# read in the tract file

# list of columns to read in, too messy otherwise
#
# vc43 = race; total population
# vc87 estimate; hispanic and latino total population
tractCols = ['GEO.id2', 'GEO.display-label', 'HC01_VC87', 'HC01_VC88', 'HC03_VC88']
tracts = pd.read_csv(dirCensusTracts + 'ACS_14_5YR_DP05.csv', index_col=False, usecols=tractCols, skiprows=[1])

#rename columns for our sanity
tractRename = dict(zip(tractCols, ['FIPS', 'Name',  'total_pop', 'hisp_pop', 'hisp_perc']))
tracts.rename(columns=tractRename, inplace=True)


# In[23]:

tracts.head()


# In[24]:

tracts.to_csv(dirData + 'processed/populations/ia-tracts-2014.csv', index=False)


# In[ ]:
