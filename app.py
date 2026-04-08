import streamlit as st 
import pickle 
import pandas as pd 
import requests 

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

API_KEY = "http://www.omdbapi.com/?i=tt3896198&apikey=33e0b32e"

def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey=33e0b32e"

    try:
        data = requests.get(url).json()
        if data.get('Response') == 'True' and data.get('Poster') != "N/A":
            return data['Poster']
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except: 
        return "https://via.placeholder.com/300x450?text=No+Image"
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    selected_genre = movies.iloc[index].genres

    movies_list = []

    for i in range(len(movies)):
        genre_score = len(set(selected_genre) & set(movies.iloc[i].genres))
        similarity_score = similarity[index][i]

        if genre_score >= 2:
            final_score = similarity_score + (genre_score * 1.5)
            movies_list.append((i, final_score))

    if len(movies_list) < 5:
        for i in range(len(movies)):
            genre_score = len(set(selected_genre) & set(movies.iloc[i].genres))
            similarity_score = similarity[index][i]

            if genre_score >= 1:
                final_score = similarity_score + (genre_score * 1.2)
                movies_list.append((i, final_score))

    movies_list = sorted(movies_list, reverse=True, key=lambda x: x[1])

    seen = set()
    unique_movies = []
    for i in movies_list:
        if i[0] not in seen:
            unique_movies.append(i)
            seen.add(i[0])

    top_movies = unique_movies[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in top_movies:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters
    
st.title("🎬 Movie Recommender System")
selected_movie= st.selectbox(
    "Select your movie",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    
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

