import streamlit as st
from kdrama_recommender.kdrama_rec import data, new_data, similarity

st.title("Kdrama Recommender")
st.header("See amazing suggestions and recommendations based on your favourite kdrama")

def drama_poster(drama_name):
    result=data.loc[data['Name'].str.contains(drama_name)]

    return result['Image-URL'].iloc[0]


def recommend(drama):
    kdrama_index=new_data[new_data['Name']==drama].index[0]
    distances=similarity[kdrama_index]
    kdrama_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_dramas=[]
    recommended_dramas_posters=[]
    for i in kdrama_list:
        drama_name= new_data.iloc[i[0]].Name
        recommended_dramas.append(new_data.iloc[i[0]].Name)
        recommended_dramas_posters.append(drama_poster(drama_name))
    return recommended_dramas, recommended_dramas_posters



drama_name = st.selectbox(
    "Choose a kdrama", new_data['Name'].values)

st.write("You selected:", drama_name)

# Get the poster of the selected drama
selected_drama_index = new_data[new_data['Name'] == drama_name].index[0]
selected_drama_name = new_data.iloc[selected_drama_index].Name
selected_drama_poster = drama_poster(selected_drama_name)
st.image(selected_drama_poster,width=200)

if st.button("Recommend"):
    names,posters = recommend(drama_name)
    st.write("Recommended Drama:")
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



