#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity='all'


# In[2]:


url='https://www.imdb.com/list/ls046196709/?sort=list_order,asc&st_dt=&mode=detail&page=1'


# In[ ]:





# In[3]:


page=requests.get(url)


# In[4]:


page.status_code


# In[5]:


content=page.text


# In[6]:


soup=BeautifulSoup(content)


# In[7]:


soup


# In[8]:


a=soup.find('div',attrs={'class':'lister-item-content'})
a.text


# In[9]:


title=[]
year=[]
certificate=[]
time=[]
genre=[]
ratings=[]
metascore=[]
votes=[]
gross=[]
pg_no=[]


# In[10]:


for x in range(1,6):
    url='https://www.imdb.com/list/ls046196709/?sort=list_order,asc&st_dt=&mode=detail&page={}'.format(x)
    pagecontent=requests.get(url).text
    soup=BeautifulSoup(pagecontent)
    
    
    for i in soup.find_all('div',attrs={'class':'lister-item mode-detail'}):
        movie_name=i.h3.a.text
        title.append(movie_name)

        released_year=i.h3.find('span',class_='lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        year.append(released_year)

        cert_ficate=i.p.span.text
        certificate.append(cert_ficate)

        runtime= i.p.find('span',class_='runtime').text
        time.append(runtime)

        type_=i.p.find('span',class_='genre').text.replace('\n','').replace(' ','')
        genre.append(type_)

        rate=i.find('span',class_='ipl-rating-star__rating').text
        ratings.append(rate)

        meta=i.find('span',class_='metascore').text.replace(' ','') if i.find('span',class_='metascore') else 'NaN'
        metascore.append(meta)

        value=i.find_all('span',attrs={'name':'nv'})
        vote=value[0].text
        votes.append(vote)

        gross_count=value[1].text if len(value)>1 else 'NaN'
        gross.append(gross_count)
        

        
        pg_no.append(x)
    print('page number{}'.format(x))


# In[11]:


movie_df=pd.DataFrame({'Title':title,
                      'Released_Year':year,
                      'Certificate':certificate,
                      'Movie_Duration':time,
                      'Genre':genre,
                      'Ratings':ratings,
                      'Metascore':metascore,
                      'Votes':votes,
                      'Gross':gross,
                      'Page_No.':pg_no})


# In[12]:


movie_df


# In[13]:


movie_df.to_csv(r'C:\Data\movie_data.csv')


# In[14]:


data=pd.read_csv(r'C:\Data\movie_data.csv')


# In[15]:


for x,y in data["Certificate"].value_counts().items():
    print(x,y)


# In[16]:


for x,y in data["Certificate"].value_counts().items():
    print(x,y)


# In[17]:


l=[]
for x,y in data["Certificate"].value_counts().items():
    if y<=5 and x!='PG'and x!='G':
        l.append(x)
(l)
    


# In[18]:


z=data['Certificate'].replace(l,np.nan)
data['Certificate']=z
data['Certificate']


# In[19]:


data['Gross'].fillna('NR',inplace=True)
y=data['Gross'].apply(lambda x:x.replace("$",""))
data['Gross']=y


# In[20]:


r=data['Gross'].apply(lambda x:x.replace("M",""))
data['Gross']=r


# In[21]:


data


# In[22]:


data['Votes'] = data['Votes'].astype(str)
a=data['Votes'].str.replace(',', '', regex=False).astype(int)


# In[23]:


data['Votes']=a


# In[24]:


data['Votes']


# In[25]:


data


# In[26]:


data[['Time','Duration']]=data['Movie_Duration'].str.split(' ',expand=True)
data.drop(['Movie_Duration','Duration','Unnamed: 0'],axis=1,inplace=True)
data


# In[27]:


data.columns


# In[ ]:





# In[28]:


final_df=data[['Title','Released_Year','Time','Certificate','Genre','Ratings','Metascore','Votes','Gross','Page_No.']]


# In[29]:


final_df


# In[30]:


final_df.to_csv(r'C:\Data\top_movie.csv')

 
final_df.to_excel(r'C:\Data\top_movies.xlsx')
 


# ## 1. Checking Duplicate Rows

# In[31]:


# Checking Duplicate Values

final_df.duplicated().value_counts()


# In[32]:


final_df.info()


# In[33]:


final_df = final_df.replace('NR', np.nan)


# In[34]:


final_df['Gross'].value_counts()


# ## 2. Handling Missing Values

# In[35]:


final_df.isna() # checking for null values


# In[36]:


final_df.isna().sum() # Calculating number of null Values


# In[37]:


np.sum(final_df.isna().sum())


# In[38]:


final_df.Released_Year.head(177)


# In[39]:


# removing unwanted value from column

final_df['Released_Year']=final_df['Released_Year'].str.replace('I','')


# In[40]:


final_df.Released_Year.head(177)


# In[41]:


final_df


# ## Get the Missing values for each column

# In[42]:


final_df.isna().sum()


# In[43]:


np.round((final_df.isna().sum()/len(final_df))*100,2).astype(str)+'%'


# In[44]:


np.sum(final_df.isna().sum())

final_df.shape

np.round(np.sum(final_df.isna().sum()/len(final_df))*100,2).astype(str)+'%'


# ## Replace Missing Values with mean or median

# In[45]:


final_df.info()


# In[46]:


final_df.select_dtypes(include=np.number) # to select numeric columns
final_df.select_dtypes(include=np.object) # to select object columns


# In[47]:


final_df_numeric=final_df.select_dtypes(include=np.number)


# In[48]:


final_df_numeric.isna().sum()


# In[49]:


final_df_numeric.mean()
final_df_numeric.median()


# In[50]:


final_df_numeric[final_df_numeric.Metascore.isna()].index


# In[51]:


final_df_numeric.Metascore.fillna(final_df_numeric.Metascore.mean())[[14,  54,  62,  73,  75,  88, 111, 114, 116, 141, 147, 156, 161,
            162, 163, 164, 165, 166, 186, 189, 190, 204, 219, 236, 238, 246,
            250, 251, 257, 259, 261, 265, 266, 267, 268, 271, 277, 280, 350,
            376, 378, 380, 381, 382, 384, 388, 391, 444, 463, 471, 472, 474,
            486]]

final_df_numeric.Metascore.fillna(final_df_numeric.Metascore.median())[[14,  54,  62,  73,  75,  88, 111, 114, 116, 141, 147, 156, 161,
            162, 163, 164, 165, 166, 186, 189, 190, 204, 219, 236, 238, 246,
            250, 251, 257, 259, 261, 265, 266, 267, 268, 271, 277, 280, 350,
            376, 378, 380, 381, 382, 384, 388, 391, 444, 463, 471, 472, 474,
            486]]


# In[52]:


final_df[final_df_numeric.columns].fillna(final_df.mean())


# In[53]:


final_df.Metascore.fillna(final_df.Metascore.mean(),inplace=True)


# In[54]:


## Replacing the Null VAlues With Mode

final_df['Certificate'].mode()


# In[55]:


final_df.Certificate.fillna(final_df.Certificate.mode()[0],inplace=True)


# In[56]:


final_df.isna().sum()


# In[57]:


## REplacing the null Values with Mode

final_df['Gross'].mode()


# In[58]:


final_df.Gross.fillna(final_df.Gross.mode()[0],inplace=True)


# In[59]:


final_df.isna().sum()


# In[60]:


final_df


# In[61]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

# choose a style option
plt.style.use('bmh')


# In[62]:


final_df.Certificate.unique()


# In[63]:


sns.barplot(data=final_df,x=final_df.Certificate,y=final_df.Votes)


# In[64]:


type(final_df.Gross)


# In[65]:


final_df.Gross=final_df.Gross.astype(float)


# In[66]:


final_df.info()


# In[67]:


plt.figure(figsize=(20,10),dpi=200)
sns.lineplot(data=final_df,x=final_df.Released_Year,y=np.arange(0,487),size=200,);


# In[68]:


final_df.Gross.sort_values


# In[69]:


final_df[20:45]


# In[70]:


plt.bar(data=final_df,x=final_df.Title,y=final_df.Gross)


plt.xticks()


# In[71]:


final_df.info()


# In[72]:


final_df.Released_Year=final_df.Released_Year.astype(int)


# In[75]:


final_df.Time=final_df.Time.astype(int)


# In[76]:


final_df.info()


# In[80]:


final_df[final_df['Time']==final_df['Time'].max()]


# In[81]:


final_df[final_df['Time']==final_df['Time'].min()]


# In[85]:


final_df[final_df['Ratings']==final_df['Ratings'].max()]


# In[86]:


final_df[final_df['Ratings']==final_df['Ratings'].min()]


# In[87]:


final_df.describe()


# In[88]:


pd.options.display.float_format = '{:.2f}'.format


# In[89]:


final_df.describe()


# In[93]:


plt.figure(figsize=(10,15), dpi = 50)

plt.pie(final_df.Certificate.value_counts(),labels=final_df.Certificate.value_counts().index,autopct='%.2f%%' )
plt.title('Most Watched Movies as per Certificate');


# In[96]:


plt.figure(figsize=(10,5))
sns.countplot(data=final_df,x='Ratings')
plt.title('Movie Rating Count Plot');


# In[105]:


plt.xticks(rotation=270)

sns.barplot(data=final_df,x=final_df.Genre[0:20],y='Votes',ci= None)
plt.title('Genre V/S Votes');


# In[ ]:




