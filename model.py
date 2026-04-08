import pandas as pd 
import numpy as np 
import ast

movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

movies = movies.merge(credits, on='title')
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords','cast', 'crew']]
movies.dropna(inplace=True)

def convert(text):
    L =[]
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

def convert_cast(text):
    L =[]
    counter = 0
    for i in ast.literal_eval(text):
        if counter !=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L 
movies['cast'] = movies['cast'].apply(convert_cast)

def fetch_director(text):
    L=[]
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L
movies['crew'] = movies['crew'].apply(fetch_director)

def collapse(L):
    return [i.replace(" ", "") for i in L]
movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)

movies['tags'] = (
    movies['genres']*6 + 
    movies['keywords']*3 + 
    movies['cast']*2 + 
    movies['crew']*2
)

new_df = movies[['movie_id', 'title', 'tags', 'genres']].copy()
new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

#Vectorization
from sklearn.feature_extraction.text import TfidfVectorizer

cv= TfidfVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

#Similarity Matrix
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

import pickle 
pickle.dump(new_df, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))