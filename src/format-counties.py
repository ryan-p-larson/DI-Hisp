
# coding: utf-8

# In[18]:

# Libraries & directories
import pandas as pd


# In[19]:

dirData = '../data/'
dirDataExt = dirData + 'external/'

dirCensus = dirDataExt + 'census/'


# In[20]:

# 1990s first
f1992 = dirCensus + 'crhia92.txt'

# 1992's Census is fixed width and weird -> columns and names
f1992Cols = [(0,6), (6,40), (40, 51), (51, 60), (60, 69), (69, 78), (78, 86), (86, 96), (96, 104), (105, 114)]
f1992ColNames = ['FIPS', 'County Name', 'Total Population', 'White', 'White - Hispanic', 'White - non hispanic', 'Black', 'American Indian & Native Alaskan', 'Asian & Pacific Islander', 'Hispanic']

# The file has 8 rows of metadata
# use cols and header, set header to none for custom cols
df1992 = pd.read_fwf(f1992, skiprows=16, colspecs=f1992Cols,
                     header=None, names=f1992ColNames, index_col=False, 
                     nrows=99)

# Calc the percentage
df1992['hisp_perc'] = (df1992['Hispanic'] / df1992['Total Population']) * 100


# In[21]:

# 1996 next
f1996 = dirCensus + 'crhia96.txt'

f1996Cols = [(0,6), (6,40), (40, 51), (51, 60), (60, 69), (69, 78), (78, 86), (86, 96), (96, 105), (105, 115)]

# Reuse the 1990 cols & names
df1996 = pd.read_fwf(f1996, skiprows=16, colspecs=f1996Cols,
                     header=None, names=f1992ColNames, index_col=False, 
                    nrows=99)

# Calc the percentage
df1996['hisp_perc'] = (df1996['Hispanic'] / df1996['Total Population']) * 100


# In[22]:

df1996.head()


# In[23]:

# 2000
f2000s = dirCensus + 'CO-EST00INT-SEXRACEHISP.csv'

df2000s = pd.read_csv(f2000s, dtype={'COUNTY':str}, encoding = 'iso-8859-1')


# In[24]:

# filtering...
# SEX = 0 [total]
# RACE = 0 [all races combined]
# ORIGIN = {0:'Total', 1:'Not Hispanic', 2:'Hispanic'}

# State=19 at the end

filt2000s = df2000s[['STATE', 'COUNTY', 'CTYNAME', 'SEX', 'ORIGIN', 'RACE', 'POPESTIMATE2000', 'POPESTIMATE2004', 'POPESTIMATE2008']][(df2000s.STATE == 19)]
filt2000s.head()


# In[25]:

# 2000

# Create another filtered dataframe with only the 2000's info
hisp2000 = filt2000s[['CTYNAME', 'COUNTY', 'SEX', 'ORIGIN', 'RACE', 'POPESTIMATE2000']]

# create the final dataframe
# rename column to hispanic population
df2000 = hisp2000[['CTYNAME', 'COUNTY', 'POPESTIMATE2000']][(hisp2000.SEX == 0) & (hisp2000.RACE == 0) & (hisp2000.ORIGIN == 2)].rename(columns={'POPESTIMATE2000': 'hisp_pop'}) 

# Add column, but use the indexes to assign value
df2000['total_pop'] = hisp2000['POPESTIMATE2000'][(hisp2000.SEX == 0) & (hisp2000.RACE == 0) & (hisp2000.ORIGIN == 0)].values

# Finally, create the percentage
df2000['hisp_perc'] = (df2000['hisp_pop'] / df2000['total_pop']) * 100


# In[26]:

# 2004

# Create another filtered dataframe with only the 2000's info
hisp2004 = filt2000s[['CTYNAME', 'COUNTY', 'SEX', 'ORIGIN', 'RACE', 'POPESTIMATE2004']]

# rename column to hispanic population
df2004 = hisp2004[['CTYNAME', 'COUNTY', 'POPESTIMATE2004']][(hisp2004.SEX == 0) & (hisp2004.RACE == 0) & (hisp2004.ORIGIN == 2)].rename(columns={'POPESTIMATE2004': 'hisp_pop'}) 

# Add column, but use the indexes to assign value
df2004['total_pop'] = hisp2004['POPESTIMATE2004'][(hisp2004.SEX == 0) & (hisp2004.RACE == 0) & (hisp2004.ORIGIN == 0)].values

# Finally, create the percentage
df2004['hisp_perc'] = (df2004['hisp_pop'] / df2004['total_pop']) * 100


# In[27]:

# 2008

# Create another filtered dataframe with only the 2000's info
hisp2008 = filt2000s[['CTYNAME', 'COUNTY', 'SEX', 'ORIGIN', 'RACE', 'POPESTIMATE2008']]

# rename column to hispanic population
df2008 = hisp2008[['CTYNAME', 'COUNTY', 'POPESTIMATE2008']][(hisp2008.SEX == 0) & (hisp2008.RACE == 0) & (hisp2008.ORIGIN == 2)].rename(columns={'POPESTIMATE2008': 'hisp_pop'}) 

# Add column, but use the indexes to assign value
df2008['total_pop'] = hisp2008['POPESTIMATE2008'][(hisp2008.SEX == 0) & (hisp2008.RACE == 0) & (hisp2008.ORIGIN == 0)].values

# Finally, create the percentage
df2008['hisp_perc'] = (df2008['hisp_pop'] / df2008['total_pop']) * 100


# In[28]:

df2008.head()


# In[29]:

# 2012

f2012 = dirCensus + 'CC-EST2012-ALLDATA-19.csv'

df2012 = pd.read_csv(f2012, dtype={'COUNTY':str})

# 2012 file has ALL counties, we'll need to filter down
# YEAR = 8 [2015 estimate]
# AGEGRP = 0 [Total]
df2012 = df2012[(df2012.YEAR == 5) & (df2012.AGEGRP == 0)]

# add total hispanic population
df2012['hisp_pop'] = df2012.H_MALE + df2012.H_FEMALE

# And calculate the percentage
df2012['hisp_perc'] = (df2012.hisp_pop / df2012.TOT_POP) * 100


# In[30]:

# Canonical dataframe

# Create a dataframe from 2010 and keep only the vars we want
dfCanonical = df2008[['CTYNAME', 'COUNTY', 'hisp_perc']].rename(columns={'hisp_perc':'hisp_perc2008'})

# Assign and rename percentages calculated from previous dataframes
dfCanonical['hisp_perc2004'] = df2004['hisp_perc']
dfCanonical['hisp_perc2000'] = df2000['hisp_perc']

# indices mismatch, just use values as all are in order
dfCanonical['hisp_perc1996'] = df1996['hisp_perc'].values
dfCanonical['hisp_perc1992'] = df1992['hisp_perc'].values
dfCanonical['hisp_perc2012'] = df2012['hisp_perc'].values


dfCanonical.head()


# In[31]:

# write out to a csv
fCanonical = dirData + 'processed/populations/ia-hisp-counties.csv'
dfCanonical.to_csv(fCanonical, float_format='%.3f', index=False)


# In[ ]:



