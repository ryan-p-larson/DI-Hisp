
# coding: utf-8

# In[1]:

# Libraries & directories
import pandas as pd


# In[2]:

dirData = 'data/'
dirDataExt = dirData + 'external/'

dirCensus = dirDataExt + 'census/'


# In[3]:

# 1990s first
f1990 = dirCensus + 'crhia90.txt'

# 1990's Census is fixed width and weird -> columns and names
f1990Cols = [(0,6), (6,40), (40, 51), (51, 60), (60, 69), (69, 78), (78, 86), (86, 96), (96, 104), (105, 114)]
f1990ColNames = ['FIPS', 'County Name', 'Total Population', 'White', 'White - Hispanic', 'White - non hispanic', 'Black', 'American Indian & Native Alaskan', 'Asian & Pacific Islander', 'Hispanic']

# The file has 8 rows of metadata
# use cols and header, set header to none for custom cols
df1990 = pd.read_fwf(f1990, skiprows=16, colspecs=f1990Cols,
                     header=None, names=f1990ColNames, index_col=False,
                     nrows=99)

# Calc the percentage
df1990['hisp_perc'] = df1990['Hispanic'] / df1990['Total Population']


# In[4]:

df1990.head()


# In[5]:

# 1995 next
f1995 = dirCensus + 'crhia95.txt'

f1995Cols = f1900Cols = [(0,6), (6,40), (40, 51), (51, 60), (60, 69), (69, 78), (78, 86), (86, 96), (96, 105), (105, 115)]

# Reuse the 1990 cols & names
df1995 = pd.read_fwf(f1995, skiprows=16, colspecs=f1995Cols,
                     header=None, names=f1990ColNames, index_col=False,
                    nrows=99)

# Calc the percentage
df1995['hisp_perc'] = df1995['Hispanic'] / df1995['Total Population']


# In[6]:

df1995.head()


# In[10]:

# 2000
f2000s = dirCensus + 'CO-EST00INT-SEXRACEHISP.csv'

df2000s = pd.read_csv(f2000s, dtype={'COUNTY':str}, encoding = 'iso-8859-1')


# In[11]:

# filtering...
# SEX = 0 [total]
# RACE = 0 [all races combined]
# ORIGIN = {0:'Total', 1:'Not Hispanic', 2:'Hispanic'}

# State=19 at the end

filt2000s = df2000s[['STATE', 'COUNTY', 'CTYNAME', 'SEX', 'ORIGIN', 'RACE', 'POPESTIMATE2000', 'POPESTIMATE2005', 'POPESTIMATE2010']][(df2000s.STATE == 19)]
filt2000s.head()


# In[12]:

# 2000

# Create another filtered dataframe with only the 2000's info
hisp2000 = filt2000s[['CTYNAME', 'COUNTY', 'SEX', 'ORIGIN', 'RACE', 'POPESTIMATE2000']]

# create the final dataframe
# rename column to hispanic population
df2000 = hisp2000[['CTYNAME', 'COUNTY', 'POPESTIMATE2000']][(hisp2000.SEX == 0) & (hisp2000.RACE == 0) & (hisp2000.ORIGIN == 2)].rename(columns={'POPESTIMATE2000': 'hisp_pop'})

# Add column, but use the indexes to assign value
df2000['total_pop'] = hisp2000['POPESTIMATE2000'][(hisp2000.SEX == 0) & (hisp2000.RACE == 0) & (hisp2000.ORIGIN == 0)].values

# Finally, create the percentage
df2000['hisp_perc'] = df2000['hisp_pop'] / df2000['total_pop']


# In[13]:

# 2005

# Create another filtered dataframe with only the 2000's info
hisp2005 = filt2000s[['CTYNAME', 'COUNTY', 'SEX', 'ORIGIN', 'RACE', 'POPESTIMATE2005']]

# rename column to hispanic population
df2005 = hisp2005[['CTYNAME', 'COUNTY', 'POPESTIMATE2005']][(hisp2005.SEX == 0) & (hisp2005.RACE == 0) & (hisp2005.ORIGIN == 2)].rename(columns={'POPESTIMATE2005': 'hisp_pop'})

# Add column, but use the indexes to assign value
df2005['total_pop'] = hisp2005['POPESTIMATE2005'][(hisp2005.SEX == 0) & (hisp2005.RACE == 0) & (hisp2005.ORIGIN == 0)].values

# Finally, create the percentage
df2005['hisp_perc'] = df2005['hisp_pop'] / df2005['total_pop']


# In[14]:

# 2010

# Create another filtered dataframe with only the 2000's info
hisp2010 = filt2000s[['CTYNAME', 'COUNTY', 'SEX', 'ORIGIN', 'RACE', 'POPESTIMATE2010']]

# rename column to hispanic population
df2010 = hisp2010[['CTYNAME', 'COUNTY', 'POPESTIMATE2010']][(hisp2010.SEX == 0) & (hisp2010.RACE == 0) & (hisp2010.ORIGIN == 2)].rename(columns={'POPESTIMATE2010': 'hisp_pop'})

# Add column, but use the indexes to assign value
df2010['total_pop'] = hisp2010['POPESTIMATE2010'][(hisp2010.SEX == 0) & (hisp2010.RACE == 0) & (hisp2010.ORIGIN == 0)].values

# Finally, create the percentage
df2010['hisp_perc'] = df2010['hisp_pop'] / df2010['total_pop']


# In[15]:

df2010.head()


# In[24]:

# 2015

f2015 = dirCensus + 'CC-EST2015-ALLDATA-19.csv'

df2015 = pd.read_csv(f2015, dtype={'COUNTY':str})

# 2015 file has ALL counties, we'll need to filter down
# YEAR = 8 [2015 estimate]
# AGEGRP = 0 [Total]
df2015 = df2015[(df2015.YEAR == 8) & (df2015.AGEGRP == 0)]

# add total hispanic population
df2015['hisp_pop'] = df2015.apply(lambda x: x.H_MALE + x.H_FEMALE, axis=1)

# And calculate the percentage
df2015['hisp_perc'] = df2015.hisp_pop / df2015.TOT_POP


# In[25]:

df2015.head()


# In[27]:

# Canonical dataframe

# Create a dataframe from 2010 and keep only the vars we want
dfCanonical = df2010[['CTYNAME', 'COUNTY', 'hisp_perc']].rename(columns={'hisp_perc':'hisp_perc2010'})

# Assign and rename percentages calculated from previous dataframes
dfCanonical['hisp_perc2005'] = df2005['hisp_perc']
dfCanonical['hisp_perc2000'] = df2000['hisp_perc']

# indices mismatch, just use values as all are in order
dfCanonical['hisp_perc1995'] = df1995['hisp_perc'].values
dfCanonical['hisp_perc1990'] = df1990['hisp_perc'].values
dfCanonical['hisp_perc2015'] = df2015['hisp_perc'].values


dfCanonical.head()


# In[29]:

# write out to a csv
fCanonical = dirData + 'processed/populations/ia-hisp-counties.csv'
dfCanonical.to_csv(fCanonical, float_format='%.3f', index=False)


# In[ ]:
