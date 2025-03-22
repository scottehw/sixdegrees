from movie_search import apikey
import streamlit as st
import pandas as pd
import requests


start_movie = "The Machinist"
url = f"https://api.themoviedb.org/3/search/movie?query={start_movie}"
headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {apikey}"
    }
response = requests.get(url, headers=headers)
start_movie_data_raw = pd.DataFrame(response.json()['results'])
start_movie_data = start_movie_data_raw[['id','title','release_date','overview']]



size = "w154"
image = f"http://image.tmdb.org/t/p/{size}/diAYqR4xdF9Hnj7qun6DEQhRrT2.jpg"

col1, col2 = st.columns(2)
col1.header("column 1")
col1.image(image)

col2.header("Column 2")
col2.dataframe(start_movie_data)


print(apikey)