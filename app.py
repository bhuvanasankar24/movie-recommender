import streamlit as st
import pandas as pd
import numpy as np
import ast
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page config
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# 🔥 LOAD DATA FROM GOOGLE DRIVE
@st.cache_data
def load_data():
    movies = pd.read_csv("https://drive.google.com/uc?export=download&id=1AjlkKIZ23NoRSRuUKFputCHlHlvGwLX5")
    credits = pd.read_csv("https://drive.google.com/uc?export=download&id=1gsNpyFDH2bKD9iF_f5i4D-ErRUtBtqn-")

    movies = movies.merge(credits, on='title')
    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    movies.dropna(inplace=True)

    # Convert JSON-like strings to list
    def convert(text):
        return [i['name'] for i in ast.literal_eval(text)]

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)

    def convert_cast(text):
        return [i['name'] for i in ast.literal_eval(text)[:3]]

    movies['cast'] = movies['cast'].apply(convert_cast)

    def fetch_director(text):
        return [i['name'] for i in ast.literal_eval(text) if i['job'] == 'Director']

    movies['crew'] = movies['crew'].apply(fetch_director)

    def collapse(L):
        return [i.replace(" ", "") for i in L]

    for col in ['cast','crew','genres','keywords']:
        movies[col] = movies[col].apply(collapse)

    # 🎯 STRONG TAGS (genre-focused)
    movies['tags'] = (
        movies['genres']*6 + 
        movies['keywords']*3 + 
        movies['cast']*2 + 
        movies['crew']*2
    )

    new_df = movies[['movie_id','title','tags','genres']]

    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())

    # Vectorization
    tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
    vectors = tfidf.fit_transform(new_df['tags']).toarray()

    similarity = cosine_similarity(vectors)

    return new_df, similarity

movies, similarity = load_data()

# 🎯 POSTER FETCH (OMDb)
def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey=33e0b32e"
    try:
        data = requests.get(url).json()
        if data.get('Response') == 'True' and data.get('Poster') != "N/A":
            return data['Poster']
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except:
        return "https://via.placeholder.com/300x450?text=Error"

# 🎯 RECOMMEND FUNCTION (FINAL HYBRID LOGIC)
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    selected_genre = movies.iloc[index].genres

    movies_list = []

    # STEP 1: STRICT FILTER
    for i in range(len(movies)):
        genre_score = len(set(selected_genre) & set(movies.iloc[i].genres))
        similarity_score = similarity[index][i]

        if genre_score >= 2:
            final_score = similarity_score + (genre_score * 1.5)
            movies_list.append((i, final_score))

    # STEP 2: RELAX IF NEEDED
    if len(movies_list) < 5:
        for i in range(len(movies)):
            genre_score = len(set(selected_genre) & set(movies.iloc[i].genres))
            similarity_score = similarity[index][i]

            if genre_score >= 1:
                final_score = similarity_score + (genre_score * 1.2)
                movies_list.append((i, final_score))

    # SORT + REMOVE DUPLICATES
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

# 🎨 UI
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Search or select a movie",
    movies['title'].values
)

if st.button('Show Recommended'):
    names, posters = recommend(selected_movie)

    cols = st.columns(len(names))

    for i in range(len(names)):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
