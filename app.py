import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests  # We need requests for hitting the API


movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies_list = movies['title'].values
st.title('Movie Recommender System')
option = st.selectbox(
    'Select a movie',
    movies_list)


# to find the posters, we need to create a function that will take movie_id as input and hit API to get poster path
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}'
                            '?api_key=dd3377717a60ec31d36404ee5581fae3&language=en-US'.format(movie_id))
    data = response.json()
    #print(data['poster_path'])
    return 'https://image.tmdb.org/t/p/original/'+data['poster_path']



def recommend_movies(movie):
    index_of_movie = movies[movies.title == movie].index[0]
    recommended_movies = np.argsort(similarity[index_of_movie])[-6:-1][::-1]
    # print(recommended_movies)
    ans = []
    posters = []
    for i in recommended_movies:
        ans.append(movies.iloc[i]['title'])
        posters.append(fetch_poster(int(movies.iloc[i]['id'])))
        #print(movies.iloc[i]['id'])
        #posters.append(fetch_poster(movies.iloc[i]['id']))
    return ans, posters

if st.button('Recommend'):
    ans,posters = recommend_movies(option)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(ans[0])
        st.image(posters[0])
    with col2:
        st.text(ans[1])
        st.image(posters[1])
    with col3:
        st.text(ans[2])
        st.image(posters[2])
    with col4:
        st.text(ans[3])
        st.image(posters[3])
    with col5:
        st.text(ans[4])
        st.image(posters[4])

