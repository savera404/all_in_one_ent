import streamlit as st
import numpy as np
from book_recommender.book_recommender import similarity_scores,final_ratings,pt

st.title("Book Recommender")
st.header("See amazing suggestions and recommendations based on your favourite book")

def book_poster(ISBN):
    return 'http://images.amazon.com/images/P/{}.01.MZZZZZZZ.jpg'.format(ISBN)

def recommend(book_name):
    # Fetch the index of the selected book
    index = np.where(pt.index == book_name)[0][0]
    
    # Get similarity scores for the selected book and sort them in descending order
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    # Prepare lists to store recommendations
    recommended_books = []
    recommended_books_posters = []

    for item in similar_items:
        # Get the book title and ISBN (assuming you have ISBN data in your pt or another DataFrame)
        book_title = pt.index[item[0]]
        
        # Fetch ISBN and get the image URL for the book cover
        # Assuming `final_ratings` has a column "ISBN" with ISBN codes for each "Book-Title"
        isbn = final_ratings.loc[final_ratings["Book-Title"] == book_title, "ISBN"].values[0]
        image_url = book_poster(isbn)

        # Append to the lists
        recommended_books.append(book_title)
        recommended_books_posters.append(image_url)
    
    return recommended_books, recommended_books_posters

unique_books = final_ratings[['Book-Title', 'ISBN']].drop_duplicates(subset='Book-Title')

book_name = st.selectbox(
    "Choose a book", unique_books['Book-Title'].values)

st.write("You selected:", book_name)
#get poster of selected book
isbn=isbn = final_ratings.loc[final_ratings["Book-Title"] == book_name, "ISBN"].values[0]
selected_book_poster=book_poster(isbn)
st.image(selected_book_poster,width=200)

if st.button("Recommend"):
    names,posters = recommend(book_name)
    st.write("Recommended Books:")
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




