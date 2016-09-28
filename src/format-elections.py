
# coding: utf-8

# In[1]:

# Libraries
import pandas as pd


# In[2]:

# directories
dirData = '../data/'

dirDataExt = dirData + 'external/'
dirElection = dirDataExt + 'election/'

dirDataProc = dirData + 'processed/'


# ## 2012
# 
# All numbers are in thousands.

# In[3]:

f2012 = pd.read_csv(dirElection + 'Table04b(2012).csv', 
                    skiprows=3, na_values=['(B)', '-'])
f2012['State'].fillna(method='ffill', inplace=True)


# In[4]:

df2012Iowa = f2012[f2012['State'] == 'IOWA']


# In[5]:

# Population
# Registration
# Percent voted
formatted2012DF = df2012Iowa[['Race and Hispanic origin', 'Total Population', 'Total Citizen Population', 
                      'Total registered', 'Percent registered\n(Total)', 'Percent registered\n(Citizen)',
                     'Total voted', 'Percent voted\n(Total)', 'Percent voted\n(Citizen)']]


# ## 2008

# In[6]:

# from 2008 table 04b. Formatting is weirddddd
f2008 = pd.read_csv(dirElection + 'Table 04b(2008).csv', header=5, na_values=['(B)','-']) 


# In[7]:

df2008Ia = f2008.iloc[193:204]
df2008Ia['Race and Hispanic origin'] = df2008Ia['State, sex, race, and Hispanic origin'].apply(lambda x: x.replace('.', ''))


# In[8]:

formatted2008DF = df2008Ia[['Race and Hispanic origin', 'Total Population', 'Total Citizen Population', 
                      'Total Registered', 'Total Voted', 'Percent registered (Total 18+)', 
                    'Percent registered (Citizen 18+)', 'Percent voted (Total 18+)', 'Percent voted (Citizen 18+)']]


# ## 2004

# In[9]:

# same formatting as 2008
f2004 = pd.read_csv(dirElection + 'Table 04b(2008).csv', header=5, na_values=['(B)', '-'])

# extract just iowa
df2004Ia = f2004.iloc[193:204]

#fix race col
df2004Ia['Race and Hispanic origin'] = df2004Ia['State, sex, race, and Hispanic origin'].apply(lambda x: x[1:])


# In[10]:

# filter the columns
formatted2004DF = df2004Ia[['Race and Hispanic origin', 'Total Population', 'Total Citizen Population', 
                      'Total Registered', 'Percent registered (Total 18+)', 'Percent registered (Citizen 18+)',
                     'Total Voted', 'Percent voted (Total 18+)', 'Percent voted (Citizen 18+)']]


# ## 2000

# In[11]:

cols2000 = ['Race', 'Population 18 and over', 'Total Citizen', 'Percent Citizen', 'Confidence Interval', 
            'Total Registered', 'Percent Registered 18+', 'Confidence Interval', 
            'Total Voted', 'Percent Voted 18+', 'Confidence interval']

f2000 = pd.read_excel(dirElection + 'tab04a(2000).xls', header=None, skiprows=10, names=cols2000, 
                      index=False, na_values=['(B)', '-'])


# In[12]:

df2000Ia = f2000.iloc[144:153]

# filter columns
formatted2000DF = df2000Ia[['Race', 'Population 18 and over', 'Total Citizen', 'Percent Citizen',
                           'Total Registered', 'Percent Registered 18+', 'Total Voted', 'Percent Voted 18+']]

# drop the API row
formatted2000DF.dropna(subset=['Total Registered'], inplace=True)


# Create a new column so that the DF is normalized to the others
formatted2000DF['Citizen Registered %'] = (formatted2000DF['Total Registered'] / formatted2000DF['Total Citizen']) * 100
formatted2000DF['Citizen Voted %'] = (formatted2000DF['Total Voted'] / formatted2000DF['Total Citizen']) * 100


# In[13]:

formatted2000DF = formatted2000DF[['Race', 'Population 18 and over', 'Total Citizen', 'Total Registered',
            'Percent Registered 18+', 'Citizen Registered %', 'Total Voted',
             'Percent Voted 18+', 'Citizen Voted %']]


# ## 1996
# 
# Fixed width format...

# In[14]:

# 96 was too weird with fixed width format, so I calculated by hand

f1996 = pd.read_csv(dirElection + '96-extract.csv')
f1996.head()


# In[15]:

# read the row #'s you need to extract


# ## Column Renaming

# In[16]:

col2012 = ['Race and Hispanic origin', 'Total Population', 'Total Citizen Population', 
            'Total registered', 'Percent registered\n(Total)', 'Percent registered\n(Citizen)',
            'Total voted', 'Percent voted\n(Total)', 'Percent voted\n(Citizen)']
col2008 = ['Race and Hispanic origin', 'Total Population', 'Total Citizen Population', 
            'Total Registered', 'Percent registered (Total 18+)', 'Percent registered (Citizen 18+)',
            'Total Voted', 'Percent voted (Total 18+)', 'Percent voted (Citizen 18+)']
col2004 = ['Race and Hispanic origin', 'Total Population', 'Total Citizen Population', 
            'Total Registered', 'Percent registered (Total 18+)', 'Percent registered (Citizen 18+)',
            'Total Voted', 'Percent voted (Total 18+)', 'Percent voted (Citizen 18+)']
col2000 = ['Race', 'Population 18 and over', 'Total Citizen', 'Total Registered',
            'Percent Registered 18+', 'Citizen Registered %', 'Total Voted',
             'Percent Voted 18+', 'Citizen Voted %']
           
#col1996

normalCols = ['Race', 'Total Population', 'Citizen Population', 'Registered Population', 
             'Total Registered %', 'Citizen Registered %', 'Voting Population', 'Total Voted %',
             'Citizen Voted %']


# In[17]:

# rename
formatted2012DF.rename(columns=dict(zip(col2012, normalCols)), inplace=True)
formatted2008DF.rename(columns=dict(zip(col2008, normalCols)), inplace=True)
formatted2004DF.rename(columns=dict(zip(col2004, normalCols)), inplace=True)
formatted2000DF.rename(columns=dict(zip(col2000, normalCols)), inplace=True)

#1996 is done already
#1992


# In[20]:

# add years
formatted2012DF['Year'] = 2012
formatted2008DF['Year'] = 2008
formatted2004DF['Year'] = 2004
formatted2000DF['Year'] = 2000
f1996['Year'] = 1996


# In[21]:

# Add them together!

combined = pd.concat([formatted2012DF, formatted2008DF, formatted2004DF, 
           formatted2000DF, f1996], ignore_index=True)


# In[24]:

combined[['Race', 'Total Population', 'Citizen Population', 'Registered Population', 'Voting Population', 'Year']].to_csv(
dirDataProc + 'elections/election-populations.csv', float_format='%.2f', index=False)

combined[['Race', 'Total Population', 'Citizen Population', 'Registered Population', 'Voting Population', 'Year']].to_csv(
dirDataProc + 'elections/election.csv', float_format='%.2f', index=False)


# In[ ]:



