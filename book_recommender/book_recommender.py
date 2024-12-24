# %%
import numpy as np
import pandas as pd
import os
import zipfile

# %%
# books=pd.read_csv("Books.csv")
# ratings=pd.read_csv("Ratings.csv")
# users=pd.read_csv("Users.csv")
# Get the directory of the current file (movie_recommender.py)
current_dir = os.path.dirname(__file__)
books_zip_path = os.path.join(current_dir, "Books.zip")
ratings_csv_path = os.path.join(current_dir, "Ratings.csv")
users_csv_path = os.path.join(current_dir, "Users.csv")


ratings=pd.read_csv(ratings_csv_path)
users=pd.read_csv(users_csv_path)
# Extract and load the .zip file
with zipfile.ZipFile(books_zip_path, 'r') as z:
    with z.open('Books.csv') as f:  # Adjust if the file name inside the .zip differs
        books = pd.read_csv(f)

# %%
books.isnull().sum()

# %%
users.isnull().sum()

# %%
ratings.isnull().sum()

# %%
ratings.duplicated().sum()

# %%
#popularity based

# %%
ratings_and_titles=ratings.merge(books,on="ISBN") #merge books and ratings

# %%
rating_num=ratings_and_titles.groupby("Book-Title").count()["Book-Rating"].reset_index() #finding total number of ratings on each book
rating_num.rename(columns={"Book-Rating":"num_of_ratings"},inplace=True)
rating_num 

# %%
# finding avg rating of each book i.e the total of ratings on that book/ num of ratings
avg_ratings = ratings_and_titles.groupby("Book-Title", as_index=False)["Book-Rating"].mean()
avg_ratings.rename(columns={"Book-Rating": "avg_rating"}, inplace=True)
avg_ratings


# %%
popular=rating_num.merge(avg_ratings,on="Book-Title")
popular # merge both

# %%
popular=popular[popular["num_of_ratings"]>=250].sort_values("avg_rating", ascending=False).head(50)
popular #the top 50 books: we considered only those books with num of ratings >250 then we sorted these books by avg_rating to show the highest rated books

# %%
#but we need author name, image, etc so we merge with books, since we have same book titles with different ISBNS we drop duplicates
popular=popular.merge(books,on="Book-Title").drop_duplicates("Book-Title")[["Book-Title","Book-Author","Image-URL-M","num_of_ratings","avg_rating"]]
popular

# %%
#collaborative filtering

# %%
# for this model to work best we need to consider only those users who have voted more than 200 times (i.e knowledgable users) and
# books with greater than 50 number of ratings

# %%
x=ratings_and_titles.groupby("User-ID").count()["Book-Rating"]>200
know_users=x[x].index
filtered_ratings= ratings_and_titles[ratings_and_titles["User-ID"].isin(know_users)]
filtered_ratings

# %%
y=filtered_ratings.groupby("Book-Title").count()["Book-Rating"]>=50
famous_books=y[y].index


# %%
final_ratings=filtered_ratings[filtered_ratings["Book-Title"].isin(famous_books)]


# %%
final_ratings

# %%
pt=final_ratings.pivot_table(index="Book-Title",columns="User-ID", values="Book-Rating")

# %%
pt.isnull()

# %%
pt.fillna(0,inplace=True)
pt

# %%
#since each book has 810 values we can say that each book is 810 dimension vector so we will find vector (eucledean distance)
#of each vector with each vector. The movies/vectors with shortest distance will be recommended. 

# %%
from sklearn.metrics.pairwise import cosine_similarity
similarity_scores=cosine_similarity(pt)
similarity_scores.shape

# %%
similarity_scores

# %%
def recommend(book_name):
    #fetch index
    index=np.where(pt.index==book_name)[0][0]
    similar_items=sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True) [1:6]

    for i in similar_items:
        print(pt.index[i[0]])



# %%
recommend("River's End")

# %%
popular["Image-URL-M"][0]

# %%


# %%



