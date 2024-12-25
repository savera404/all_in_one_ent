# %%
import numpy as np
import pandas as pd
import os
import gdown

# %%
current_dir = os.path.dirname(__file__)
anime_csv_path = os.path.join(current_dir, "anime.csv")
#ratings_csv_path = os.path.join(current_dir, "rating_complete.csv") since the ratings dataset is too large and Github wont allow me to upload such a large file, i am giving a google drive link which the code will read and download from there


download_url = "https://drive.google.com/uc?export=download&id=1UsrY0ewMiTcQqPiQVXkbLCjOefsABm5l"

output_file = "ratings3.csv"

# Download the file using gdown
try:
    gdown.download(download_url, output_file, quiet=False)
    print(f"File downloaded successfully: {output_file}")

    # Load the CSV file into a DataFrame
    ratings = pd.read_csv(output_file)
    print("CSV loaded successfully!")
    print(ratings.head())
except Exception as e:
    print(f"An error occurred: {e}")


# %%
ratings.rename(columns={"anime_id":"MAL_ID"},inplace=True)

# %%
anime=anime[["MAL_ID","Name"]]

# %%
anime.head()

# %%
anime_with_ratings=ratings.merge(anime,on="MAL_ID")

# %%
anime_with_ratings

# %%
rating_num=anime_with_ratings.groupby("Name").count()["rating"].reset_index() #find num of rating on each book
rating_num.rename(columns={"rating":"num_of_ratings"},inplace=True)
rating_num

# %%
rating_num["num_of_ratings"].describe()

# %%
# avg_ratings=anime_with_ratings.groupby("Name",as_index=False)["rating"].mean()
# avg_ratings.rename(columns={"rating":"avg_rating"},inplace=True)
# avg_ratings

# %%
x=anime_with_ratings.groupby("user_id").count()["rating"]>200
know_viewers=x[x].index
filtered_ratings=anime_with_ratings[anime_with_ratings["user_id"].isin(know_viewers)]
filtered_ratings

# %%
y=filtered_ratings.groupby('Name').count()["rating"]>=2000
famous_anime=y[y].index
final_ratings=filtered_ratings[filtered_ratings["Name"].isin(famous_anime)]
final_ratings

# %%
pt=final_ratings.pivot_table(index="Name",columns="user_id",values="rating")

# %%
pt.fillna(0,inplace=True)
pt.head(6)

# %%
pt.shape

# %%
from sklearn.metrics.pairwise import cosine_similarity
similarity_scores=cosine_similarity(pt)
similarity_scores.shape

# %%
similarity_scores

# %%
def recommend(anime_name):
    #fetch index
    index=np.where(pt.index==anime_name)[0][0]
    similar_items=sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True) [1:6]

    for i in similar_items:
        print(pt.index[i[0]])

# %%
recommend("Dragon Ball")


