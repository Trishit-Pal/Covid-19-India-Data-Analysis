#!/usr/bin/env python
# coding: utf-8

# 
# # Covid-19 India Data Analysis
# 

# In[1]:


#Importing necessary libraries
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#!pip install seaborn==0.9.0
import seaborn as sbs

import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
df_covid=pd.read_csv('covid_19_india.csv')
df_covid.head(6)  #shows first 6 rows of the dataframe


# ### Deatils about the dataset (df_covid)

# In[2]:


df_covid.info() # syntax for information about the existing dataset


# In[3]:


# description regarding number of elements in each column with cumulative details like Count,Mean and standard deviation of data etc.
df_covid.describe()


# ### Making some alterations in the dataset to suit our analysis requirements.

# In[4]:


#dropping some unrequired columns from the dataset viz. 'Sno', 'Time', 'ConfirmedIndianNational' and 'ConfirmedForeignNational'

df_covid.drop(["Sno","Time","ConfirmedIndianNational","ConfirmedForeignNational"],inplace=True,axis=1)

#altering the date format
df_covid['Date']=pd.to_datetime(df_covid['Date'],format='%Y-%m-%d')

#updated dataframe
df_covid.head(4)  #top 4 rows of the dataframe


# In[5]:


#creating a new column named 'Active Cases'
#Active Cases= Confirmed-(Deaths+ Cured cases)
df_covid['Active_Cases']=df_covid['Confirmed']-(df_covid['Deaths']+df_covid['Cured'])
df_covid.head()


# In[6]:


#creating a pivot table
csdf=pd.pivot_table(df_covid,values=["Confirmed", "Deaths", "Cured"], index="State/UnionTerritory", aggfunc=max)


# In[7]:


#Creating a new column Recovery Rate
csdf["Recovery Rate"]=csdf["Cured"]*100/csdf["Confirmed"]


# In[8]:


#Creating a new column Mortality Rate
csdf["Mortality Rate"]=csdf["Deaths"]*100/csdf["Confirmed"]


# In[9]:


#sorting alues as per confirmed cases in Descending order
csdf=csdf.sort_values(by="Confirmed", ascending=False)


# In[10]:



csdf=csdf.drop_duplicates(keep=False)
csdf.style.background_gradient(cmap="cubehelix")


# ### States based upon Active Cases (descending order)

# In[11]:


# Creating a new dataframe where data are grouped by number of Active Cases in Descending order of cases.
df_top_active_cases_states=df_covid.groupby(by='State/UnionTerritory').max()[['Active_Cases','Date']].sort_values(by=['Active_Cases'], ascending=False).reset_index()

df_top_active_cases_states.head(15)  #shows top 15 states with higest number of active cases


# ### Creating a bar-plot of Top States with most active cases with Active cases on Y-axis and States/UnionTerritories on X-axis

# In[12]:



fig_active=plt.figure(figsize=(18,7))
plt.title("Top 15 States with Most Active Cases",size=25)
ax=sbs.barplot(data=df_top_active_cases_states.iloc[:15], y="Active_Cases", x="State/UnionTerritory", linewidth=2,edgecolor='black')
plt.ylabel("Active Cases")
plt.xlabel("States / Union Territories")
plt.show()


# ###  States based upon Recovery Rate (descending order)

# In[13]:


# Creating a new dataframe where data are grouped by number of Active Cases in Descending order of cases.
df_top_recovery_rate_states=csdf.groupby(by='State/UnionTerritory').max()[['Recovery Rate']].sort_values(by=['Recovery Rate'], ascending=False).reset_index()

df_top_recovery_rate_states.head(10)  #shows top 10 states with highest recovery rate


# In[14]:


fig_rr=plt.figure(figsize=(18,8))
plt.title("Recovery Rate Plot",size=25)
ax=sbs.barplot(data=df_top_recovery_rate_states.iloc[:], y="Recovery Rate",x="State/UnionTerritory", linewidth=2,edgecolor='black')
plt.xlabel("States/ Union Territories")
plt.ylabel("Recovery Rate")
plt.show()


# ## States based upon Deaths (descending order)

# In[15]:


# Creating a new dataframe where data are grouped by number of Deaths in descending order of cases.
df_most_death_states=df_covid.groupby(by='State/UnionTerritory').max()[['Deaths','Date']].sort_values(by=['Deaths'], ascending=False).reset_index()

df_most_death_states.head(15)  #shows top 15 states with higest number of active cases


# ### Creating a bar plot of Top States with most death cases with Deaths on Y-axis and States/UnionTerritories on X-axis

# In[16]:



fig_active=plt.figure(figsize=(18,5))
plt.title("Top 15 States with Most Deaths",size=25)
ax=sbs.barplot(data=df_most_death_states.iloc[:15], y="Deaths", x="State/UnionTerritory", linewidth=2,edgecolor='black')
plt.xlabel("States/ Union Territories")
plt.ylabel("Death Cases")
plt.show()


# In[ ]:





# In[17]:


fig_trend=plt.figure(figsize=(15,6))
states_df = df_covid['State/UnionTerritory'].isin(['Maharashtra','Karnataka','Kerala','Tamil Nadu', 'Uttar Pradesh','Rajasthan'])
ax=sbs.lineplot(data=states_df, x=df_covid.Date , y=df_covid.Active_Cases )
ax.set_title("Trend of Top 6 Most Affected States", size=20)
plt.show()


# ## Reading a new csv file with the details of Statewise testing of Covid-19 Data

# In[18]:



vacc_df=pd.read_csv('covid_vaccine_statewise.csv')
vacc_df.head(4)    #top 4 elements of the dataset


# In[19]:


# description regarding number of elements in each column with cumulative details like Count,Mean and standard deviation of data etc.
vacc_df.describe()


# In[20]:


#Renaming the column on vacc_df from 'Updated On' to 'Vaccine Date'
vacc_df.rename(columns={'Updated On' : 'Vaccine Date'},inplace=True)
vacc_df.head(5)


# In[21]:


vacc_df.info()


# In[22]:


vacc_df.isnull().sum()  #shows all columns with null values and number of NULL values in each column


# In[23]:


#creating a new Dataframe named vacc_df2 after dropping columns with a large number of NULL values like 'Sputnik V(Doses Administered)','18-44 Years (Doses Administered)','45-60 Years (Doses Administered)','60+ Years (Doses Administered)'

vacc_df2=vacc_df.drop(columns=['Sputnik V (Doses Administered)','18-44 Years (Doses Administered)','45-60 Years (Doses Administered)','60+ Years (Doses Administered)'],axis=1)
vacc_df2.head()


# ### Vaccination comparison of Male and Female

# In[24]:


#creating two new dataframes for Male and Female Individuals vaccinated and plotting them on a pie-chart.
male_df=vacc_df2['Male(Individuals Vaccinated)'].sum()
female_df=vacc_df2['Female(Individuals Vaccinated)'].sum()
px.pie(names=["Female","Male"],values=[female_df,male_df],title = "Female and Male Vaccination Comparison")


# In[25]:


#renaming column 'Total Individuals Vaccinated' to 'Total'
vacc_df.rename(columns={"Total Individuals Vaccinated": "Total"}, inplace=True)

#refining the dataset by excluding the row with State='India'
vacc_df=vacc_df[vacc_df.State!='India']

#States with most vaccination
states_max_vacc=vacc_df.groupby('State')['Total'].sum().to_frame('Total')
states_max_vacc=states_max_vacc.sort_values('Total',ascending=False)[:10]
states_max_vacc.head()

#States with least Vaccination
states_min_vacc=vacc_df.groupby('State')['Total'].sum().to_frame('Total')
states_min_vacc=states_min_vacc.sort_values('Total',ascending=True)[:10]
states_min_vacc.head()


# ### Bar-Plot of Top 10 Vaccinated States

# In[26]:


fig=plt.figure(figsize=(14,7))
plt.title("Top 10 States Vaccinated", size=30)
x=sbs.barplot(data=states_max_vacc.iloc[:10], y=states_max_vacc.Total,x=states_max_vacc.index,linewidth=3, edgecolor='black')
plt.xlabel("States")
plt.ylabel("Vaccination")
plt.show()


# ### Bar-Plot of least 10 Vaccinated States

# In[27]:


fig=plt.figure(figsize=(20,8))
plt.title("Least 10 States Vaccinated", size=30)
x=sbs.barplot(data=states_min_vacc.iloc[:10], y=states_min_vacc.Total,x=states_min_vacc.index,linewidth=3, edgecolor='black')
plt.xlabel("States")
plt.ylabel("Vaccination")
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




