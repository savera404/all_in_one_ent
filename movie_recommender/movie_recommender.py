#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
import pandas as pd
import os

# In[6]:


# movies=pd.read_csv("tmdb_5000_movies.csv")
# creds=pd.read_csv("tmdb_5000_credits.csv")


# Get the directory of the current file (movie_recommender.py)
current_dir = os.path.dirname(__file__)
movies_csv_path = os.path.join(current_dir, "tmdb_5000_movies.csv")
credits_csv_path = os.path.join(current_dir, "tmdb_5000_credits.csv")

# Load the CSV files using the full paths
movies = pd.read_csv(movies_csv_path)
creds = pd.read_csv(credits_csv_path)

# In[7]:


movies.head()


# In[8]:


creds.head()


# In[9]:


movies=movies.merge(creds,on="title")


# In[10]:


movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# In[11]:


movies.columns


# In[12]:


movies.head()


# In[13]:


movies.isnull().sum()


# In[14]:


movies.dropna(inplace=True)


# movies.duplicated().sum()

# In[15]:


movies.iloc[0].genres


# In[16]:


import ast


# In[17]:


def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L


# In[18]:


movies['genres']=movies['genres'].apply(convert)


# In[19]:


movies.head()


# In[20]:


movies['keywords']=movies['keywords'].apply(convert)


# In[21]:


movies['cast'][0]


# In[22]:


def convert3(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L


# In[23]:


movies['cast']=movies['cast'].apply(convert3)


# In[24]:


movies.head()


# In[25]:


movies['crew'][0]


# In[26]:


def fetch_director(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
            break
    return L


# movies['crew'].apply(fetch_director)

# In[27]:


movies['crew']=movies['crew'].apply(fetch_director)


# In[28]:


movies['overview']=movies['overview'].apply(lambda x:x.split())


# In[29]:


movies.head()


# In[30]:


movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])


# In[31]:


movies.head()


# In[32]:


movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']


# movies.head()

# 

# In[33]:


movies.head()


# In[34]:


newdf=movies[["movie_id","title","tags"]]
newdf


# In[35]:


newdf['tags'][0]


# In[36]:


newdf['tags']=newdf['tags'].apply(lambda x:" ".join(x) )


# In[37]:


newdf['tags'][0]


# In[38]:


newdf['tags']=newdf['tags'].apply(lambda x:x.lower() )


# In[39]:


newdf.head()


# In[40]:


from sklearn.feature_extraction.text import CountVectorizer
cv= CountVectorizer(max_features=5000, stop_words="english")
cv.fit_transform(newdf['tags']).toarray()


# In[41]:


vectors=cv.fit_transform(newdf['tags']).toarray()


# In[42]:


vectors[0]


# In[43]:


list(cv.get_feature_names_out())


# In[44]:


import nltk


# In[45]:


from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()


# In[46]:


def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


# In[47]:


newdf.tags[0]


# In[48]:


newdf['tags']=newdf['tags'].apply(stem)


# In[49]:


from sklearn.metrics.pairwise import cosine_similarity 
cosine_similarity(vectors).shape


# In[50]:


similarity=cosine_similarity(vectors)


# In[51]:


def recommend(movie):
    movie_index=newdf[newdf['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movies_list:
        print (newdf.iloc[i[0]].title)


# In[ ]:


recommend("Batman Begins")


# In[53]:


recommend("Avatar")


# In[54]:


recommend("John Carter")

