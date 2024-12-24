# %%
import numpy as np
import pandas as pd
import os

# %%

current_dir = os.path.dirname(__file__)
drama_csv_path = os.path.join(current_dir, "top100_kdrama.csv")
images_csv_path = os.path.join(current_dir, "drama_list.csv")

# Load the CSV files using the full paths
dramas = pd.read_csv(drama_csv_path)
images = pd.read_csv(images_csv_path)

data=dramas.merge(images, on='Name')
data.head()

# %%
data=data[['Name','Synopsis','Cast','Genre','Tags','Image-URL']]

# %%
data

# %%
data['Synopsis']=data['Synopsis'].apply(lambda x:x.split())
data['Tags']=data['Tags'].apply(lambda x:x.split(','))
data['Cast']=data['Cast'].apply(lambda x:x.split(','))
data['Genre']=data['Genre'].apply(lambda x:x.split(','))
data

# %%
data.dtypes

# %%
data['Cast']=data['Cast'].apply(lambda x:[i.replace(" ","")for i in x])
data['Tags']=data['Tags'].apply(lambda x:[i.replace(" ","") for i in x])
data

# %%
data['tags_comb']=data['Synopsis']+data['Cast']+data['Genre']+data['Tags']
data

# %%
data["tags_comb"][3]

# %%
new_data=data[['Name','tags_comb','Image-URL']]
new_data

# %%
new_data['tags_comb']=new_data['tags_comb'].apply(lambda x:" ".join(x))
new_data['tags_comb'][9]

# %%
new_data['tags_comb']=new_data['tags_comb'].apply(lambda x:x.lower())
new_data

# %%
from sklearn.feature_extraction.text import CountVectorizer
cv= CountVectorizer(max_features=5000, stop_words="english")
cv.fit_transform(new_data['tags_comb']).toarray()

# %%
vectors=cv.fit_transform(new_data['tags_comb']).toarray()

# %%
list(cv.get_feature_names_out())

# %%
import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

# %%
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

# %%
new_data['tags_comb']=new_data['tags_comb'].apply(stem)

# %%
from sklearn.metrics.pairwise import cosine_similarity 
similarity=cosine_similarity(vectors)
similarity.shape


# %%
similarity

# %%
def recommend(kdrama):
    kdrama_index=new_data[new_data['Name']==kdrama].index[0]
    distances=similarity[kdrama_index]
    kdrama_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in kdrama_list:
        print (new_data.iloc[i[0]].Name)

# %%
recommend("The Penthouse")

# %%
merged_df = pd.merge(dramas, images, on="Name", how="outer", indicator=True)
# Rows that were only in df1
lost_in_df2 = merged_df[merged_df["_merge"] == "left_only"]

# Rows that were only in df2
lost_in_df1 = merged_df[merged_df["_merge"] == "right_only"]

print("Rows lost from file2:", lost_in_df2)
#print("Rows lost from file1:", lost_in_df1)



