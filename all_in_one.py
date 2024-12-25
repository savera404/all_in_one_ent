import streamlit as st

st.title("All in One Recommender System")
st.header("See recommendations for movies, books, and kdramas")



ent_types=[None,"Movies","Books","Kdramas"]

if "ent_type" not in st.session_state:
    st.session_state.ent_type = None


def choose_type():

    st.header("What are you searching for?")
    rec_type = st.selectbox("Choose an option",ent_types)

    if st.button("Go!"):
        st.session_state.ent_type = rec_type
        if rec_type == "Movies":
            st.switch_page("pages/movie.py")
        elif rec_type == "Books":
            st.switch_page("pages/book.py")
        #elif rec_type == "Animes":
         #   st.switch_page("pages/anime.py")
        elif rec_type=="Kdramas":
            st.switch_page("pages/kdrama.py")
        st.rerun()

ent_type = st.session_state.ent_type


choose_type()

# to_movie_page=st.Page("movie_recommender/movie.py",
#                       default=(ent_type=="Movies"),
# )
