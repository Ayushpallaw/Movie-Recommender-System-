import streamlit as st
import pickle
import pandas as pd
import requests

# --- Page Config and Styling ---
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 100%;
            font-size: 1.1em;
        }
        .movie-title {
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            margin-top: 5px;
        }
        img {
            margin-top: 0px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Fetch Poster Function ---
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=90cccffff616df86855a68ddbe491c59&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

# --- Recommend Function ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# --- Load Data ---
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- App Title & Input ---
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("##  Select a Movie to get Recommendations")

selected_movie_name = st.selectbox("🎞️ Choose a movie", movies['title'].values)

# --- Show Recommendations ---
if st.button('🚀 Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(recommended_movie_posters[i], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{recommended_movie_names[i]}</div>", unsafe_allow_html=True)
