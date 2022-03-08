#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


match_data=pd.read_csv('/Users/babloo/Downloads/match_data.csv')
ball_data=pd.read_csv('/Users/babloo/Downloads/ball_data.csv')


# In[4]:


match_data.head()


# In[5]:


ball_data.head()


# In[6]:


#sum of null values
match_data.isnull().sum()


# In[7]:


#sum of null values
ball_data.isnull().sum()


# In[8]:


match_data.shape


# In[9]:


ball_data.shape


# In[10]:


#priniting column names
match_data.columns


# In[11]:


print('Matches played so far:',match_data.shape[0])
print('\nCities played at:\n',match_data['city'].unique())
print('\nTeams particated in the IPL:\n',match_data['team1'].unique())


# In[12]:


#Creating a new attribute season
match_data['season']=pd.DatetimeIndex(match_data['date']).year
match_data.head()


# In[13]:


#Matches played per season
match_per_season=match_data.groupby(['season'])['id'].count().reset_index().rename(columns={'id':'matches'})
match_per_season


# In[14]:


sns.countplot(match_data['season'])
plt.xticks(rotation=90,fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel('season',fontsize=10)
plt.ylabel('matches',fontsize=10)
plt.title('Total number of matches played per season',fontsize=10,fontweight='bold')


# In[15]:


#joining both the dataframes using leftjoin on id
season_data = match_data[['id','season']].merge(ball_data,left_on = 'id',right_on = 'id',how = 'left').drop('id',axis=1)
season_data.head()


# In[16]:


#Total runs scored in each season
season=season_data.groupby(['season'])['total_runs'].sum().reset_index()
p=season.set_index('season')
ax=plt.axes()
ax.set(facecolor='black')
sns.lineplot(data=p,palette='ch:s=-.2,r=.6')
plt.title('Total runs in each season',fontsize=12,fontweight='bold')
plt.show()


# In[17]:


#Runs scored per match in each season
runs_per_match=pd.concat([match_per_season,season.iloc[:,1]],axis=1)
runs_per_match['Runs per Season']=runs_per_match['total_runs']/runs_per_match['matches']
runs_per_match.set_index('season',inplace=True)
runs_per_match


# In[18]:


toss=match_data['toss_winner'].value_counts()
ax=plt.axes()
ax.set(facecolor="black")
sns.set(rc={'figure.figsize':(15,10)},style='darkgrid')
ax.set_title('No.of Tosses Won by each Team',fontsize=15,fontweight="bold")
sns.barplot(y=toss.index,x=toss,orient='h',palette='ch:s=-.2,r=.6',saturation=1)
plt.xlabel('Tosses won')
plt.ylabel('teams')
plt.show()


# In[19]:


ax=plt.axes()
ax.set(facecolor="black")
sns.countplot(x='season',hue='toss_decision',data=match_data,palette='ch:s=-.2,r=.6',saturation=1)
plt.xticks(rotation=90,fontsize=10)
plt.yticks(fontsize=15)
plt.xlabel('\n Season',fontsize=15)
plt.ylabel('count',fontsize=15)
plt.ylabel('count',fontsize=15)
plt.title('Toss decision across seasons',fontsize=12,fontweight="bold")
plt.show()


# In[22]:


#Match results by batting first or chasing
match_data['result'].value_counts()


# In[26]:


#Best stadium to win by chasing
match_data.venue[match_data.result!='runs'].mode()


# In[24]:


#Best stadium to bat first
match_data.venue[match_data.result!='wickets'].mode()


# In[30]:


#Best stadium for any IPL team when they win the toss
match_data.venue[match_data.toss_winner=='Chennai Super Kings'][match_data.winner=='Chennai Super Kings'].mode()


# In[32]:


#Best chasing team
match_data.winner[match_data.result!='runs'].mode()


# In[33]:


#team with maximum wins batting first
match_data.winner[match_data.result!='wickets'].mode()


# In[46]:


#Does wining toss mean winning the match?
toss=match_data['toss_winner'] == match_data['winner']
plt.figure(figsize=(5,10))
sns.countplot(toss)
plt.show()


# In[45]:


#Does choosing batting first or second help in winning matches?
plt.figure(figsize=(5,10))
sns.countplot(match_data.toss_decision[match_data.toss_winner==match_data.winner])
plt.show()


# In[49]:


#Rohit's performance
player=(ball_data['batsman']=='RG Sharma')
df_rohit=ball_data[player]
df_rohit.head()


# In[55]:


df_rohit['dismissal_kind'].value_counts().plot.pie(autopct='%1.1f%%',shadow=True,rotatelabels=True)
plt.title("Dismissal Kind",fontweight="bold",fontsize=15)
plt.show()


# In[56]:


def count(df_rohit,runs):
    return len(df_rohit[df_rohit['batsman_runs']==runs])*runs


# In[59]:


print("Runs scored from 1's : ",count(df_rohit,1))
print("Runs scored from 2's : ",count(df_rohit,2))
print("Runs scored from 4's : ",count(df_rohit,4))
print("Runs scored from 6's : ",count(df_rohit,6))


# In[60]:


#Match with highest Loss Margin
match_data[match_data['result_margin']==match_data['result_margin'].max()]


# In[64]:


#Top 10 players with maximum runs
runs = ball_data.groupby(['batsman'])['batsman_runs'].sum().reset_index()
runs.columns=['Batsman','runs']
y=runs.sort_values(by='runs',ascending=False).head(10).reset_index().drop('index',axis=1)
y


# In[72]:


ax=plt.axes()
ax.set(facecolor="black")
sns.barplot(x=y['Batsman'],y=y['runs'],palette='ch:s=-.2,r=.6',saturation=1)
plt.xticks(rotation=90,fontsize=13)
plt.yticks(fontsize=13)
plt.xlabel('\n Player',fontsize=15,fontweight="bold")
plt.ylabel('Total Runs',fontsize=15,fontweight="bold")
plt.title("Top 10 run scores in IPL",fontsize=20,fontweight="bold")


# In[78]:


ax=plt.axes()
ax.set(facecolor="grey")
match_data.player_of_match.value_counts()[:10].plot(kind='bar')
plt.xlabel('Player',fontsize=13,fontweight="bold")
plt.ylabel('MOM Awards Count',fontsize=13,fontweight="bold")
plt.title("Players with Maximum Awards in IPL",fontsize=15,fontweight="bold")


# 
