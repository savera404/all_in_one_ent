import streamlit as st
import requests
from movie_recommender.movie_recommender import newdf, similarity

st.title("Movie Recommender")
st.header("See amazing suggestions and recommendations based on your favourite movie")

def movie_poster(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=fa44323acd27eec7bcf2e3f877237955'.format(movie_id))
    data=response.json()
    return 'http://image.tmdb.org/t/p/w500/' + data['poster_path']

def recommend(movie):
    movie_index=newdf[newdf['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movie_posters=[]
    for i in movies_list:
        movie_id= newdf.iloc[i[0]].movie_id
        recommended_movies.append(newdf.iloc[i[0]].title)
        recommended_movie_posters.append(movie_poster(movie_id))
    return recommended_movies, recommended_movie_posters



movie_name = st.selectbox(
    "Choose a movie", newdf['title'].values)

st.write("You selected:", movie_name)

# Get the poster of the selected movie
selected_movie_index = newdf[newdf['title'] == movie_name].index[0]
selected_movie_id = newdf.iloc[selected_movie_index].movie_id
selected_movie_poster = movie_poster(selected_movie_id)
st.image(selected_movie_poster,width=200)

if st.button("Recommend"):
    names,posters = recommend(movie_name)
    st.write("Recommended Movies:")
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


