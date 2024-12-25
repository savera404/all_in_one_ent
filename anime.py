import streamlit as st
import numpy as np
import requests
from anime_recommender.anime_rec_col import similarity_scores,pt, final_ratings

st.title("Anime Recommender")
st.header("See amazing suggestions and recommendations based on your favourite anime")

def anime_poster(anime_id):
    headers = {
    "X-MAL-CLIENT-ID": "c82989ac9884bdf891e559dd6d060a51"
}
    url='https://api.myanimelist.net/v2/anime/{}?fields=main_picture'.format(anime_id)

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    # Access the medium-size image URL
        medium_image_url = data.get("main_picture", {}).get("medium")
    return medium_image_url

def recommend(anime_name):
    #fetch index
    index=np.where(pt.index==anime_name)[0][0]
    similar_items=sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True) [1:6]

    recommended_anime = []
    recommended_anime_posters = []

    for item in similar_items:
        anime_title = pt.index[item[0]]
        
       
        anime_id = final_ratings.loc[final_ratings["Name"] == anime_title, "MAL_ID"].values[0]
        image_url = anime_poster(anime_id)

        # Append to the lists
        recommended_anime.append(anime_title)
        recommended_anime_posters.append(image_url)
    
    return recommended_anime,recommended_anime_posters

unique_animes = final_ratings[['Name', 'MAL_ID']].drop_duplicates(subset='Name')

anime_name = st.selectbox(
    "Choose an anime", unique_animes['Name'].values)

st.write("You selected:", anime_name)
#get poster of selected book
anime_id = final_ratings.loc[final_ratings["Name"] == anime_name, "MAL_ID"].values[0]
selected_anime_poster=anime_poster(anime_id)
st.image(selected_anime_poster,width=200)

if st.button("Recommend"):
    names,posters = recommend(anime_name)
    st.write("Recommended Animes:")
    col1, col2, col3, col4,col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])





