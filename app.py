
import pickle
import pandas as pd
import streamlit as st

# Function to fetch movie details based on IMDb ID
def get_movie_details(imdb_id):
    imdb_link = f"https://www.imdb.com/title/{imdb_id}/"
    return imdb_link

# Function to fetch movie poster URL
def get_movie_poster(poster_path):
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"

# Function to recommend movies
def recommend(movie, val):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:val + 1]
    recommended_movies = [(movies.iloc[i[0]].title, movies.iloc[i[0]].imdb_id, movies.iloc[i[0]].poster_path) for i in movies_list]
    return recommended_movies

# Load data and UI setup
movies_dict = pickle.load(open('movie_dict20k.pkl', 'rb'))
similarity = pickle.load(open('similarity_20k.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Main UI
st.markdown("<h1 style='color: #000000; background-color: #34AABD; padding: 10px; text-align: center; margin-bottom: 0; font-size: 35px;'>🎬 Movie Recommender</h1>", unsafe_allow_html=True)
selected_movie = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)
num_movies_str = st.text_input("Select the number of related movies", "5")
num_movies = int(num_movies_str)

# Show recommendations on button click
if st.button('Show Recommendation'):
    recommended_movies = recommend(selected_movie, num_movies)
    
    # Display recommended movies with posters and IMDb links in grid layout
    col_count = 5
    num_rows = -(-len(recommended_movies) // col_count)  # Ceiling division to determine the number of rows needed
    for i in range(num_rows):
        col = st.columns(col_count)  # Create columns for each movie
        for j in range(col_count):
            index = i * col_count + j
            if index < len(recommended_movies):
                with col[j]:
                    rec_movie = recommended_movies[index]
                    poster_url = get_movie_poster(rec_movie[2])
                    imdb_link = get_movie_details(rec_movie[1])
                    st.image(poster_url, width=150)
                    st.markdown(f"[{rec_movie[0]}]({imdb_link})", unsafe_allow_html=True)  # Render HTML in markdown

# Footer with different background color
# st.markdown("<h3 style='color: white; background-color: #34AABD; padding: 10px; text-align: center; margin-top: 0; font-size: 14px;'>Explore 20,000 top-rated films from 2000 to 2024. Dive in and enjoy!</h3>", unsafe_allow_html=True)

st.markdown("<h3 style='color: black; background-color: #34AABD; padding: 10px; text-align: center; margin-top: 0; font-size: 14px;'> Dive into <span style='color: #EA051D;'>20,000</span>  Top-Rated Films ( <span style='color: #EA051D;'>2000-2024</span> ) and Explore IMDb Links!</h3>", unsafe_allow_html=True)


import base64  # Add this import for base64 encoding
# Path to your local image file
background_image_path = "D:\HD_Wallpapers\hd_a91644acb03146e6377c5c3af80935a3.jpg"
# Add background image to the app
st.markdown(
    f"""
    <style>
        .reportview-container {{
            background: url(data:image/jpeg;base64,{base64.b64encode(open(background_image_path, "rb").read()).decode()})
        }}
    </style>
    """,
    unsafe_allow_html=True
)