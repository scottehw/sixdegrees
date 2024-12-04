import urllib.parse
import urllib.request
import pandas as pd
import json
import urllib
import requests

import streamlit as st

#st.set_page_config(layout="wide")
st.title("6" + u'\N{DEGREE SIGN}')

#from config import apikeystt
apikey = st.secrets["apikey"]

# Create a text element and let the reader know the data is loading.
top_text = st.text('Search for a movie and pull back all associated actors and any other movies they have starred in.')



start_movie = st.text_input("Last Watched Movie:")


if start_movie:
    url = f"https://api.themoviedb.org/3/search/movie?query={start_movie}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {apikey}"
    }

    response = requests.get(url, headers=headers)
    start_movie_data_raw = pd.DataFrame(response.json()['results'])
    start_movie_data = start_movie_data_raw[['id','title','release_date','overview']]

    #start_movie_id = st.selectbox("Pick one", ["cats", "dogs"])
    start_movie_id = start_movie_data.loc[0,'id']


    #url = f"https://api.themoviedb.org/3/movie/{start_movie_id}/credits"
    url = f"https://api.themoviedb.org/3/movie/{start_movie_id}?append_to_response=credits"

    response = requests.get(url, headers=headers)
    response_json = response.json()
    start_credits = response_json.get('credits',{})



    #start_movie_actors_data_raw = pd.DataFrame(response.json()['cast'])
    start_movie_actors_data_raw = pd.DataFrame(start_credits['cast'])

    start_movie_actors_data = start_movie_actors_data_raw[['id', 'name', 'character', 'popularity']].copy()
    start_movie_actors_data['popularity'] = pd.to_numeric(start_movie_actors_data['popularity'], errors='coerce')
    max_popularity = max(start_movie_actors_data['popularity'])
    filter_actor_popularity = st.sidebar.slider("Actor Popularity", min_value=0.0, max_value=max_popularity, value=10.0)
    start_movie_actors_data = start_movie_actors_data[start_movie_actors_data['popularity'] > filter_actor_popularity]
    #start_movie_actors_data.sort_values(by='popularity', ascending=False, inplace=True)

    st.subheader('\"' + start_movie + '\"' + ' actors')
    st.write(start_movie_actors_data)


    filter_actor = st.pills("Actor", start_movie_actors_data['name'])

    responses_list = []
    for index, row in start_movie_actors_data.iterrows():
        person_id = row['id']
        person_name = row['name']
        original_character = row['character']
        #url = f"https://api.themoviedb.org/3/person/{person_id}/combined_credits"
        url = f"https://api.themoviedb.org/3/person/{person_id}?append_to_response=combined_credits"
        response = requests.get(url, headers=headers)
        # If the response is successful, append the data to the list 
        if response.status_code == 200: 
            response_json = response.json()
            combined_credits = response_json.get('combined_credits', {})
            data_cast = pd.json_normalize(combined_credits.get('cast', []))
            if not data_cast.empty: 
                data_cast['person_id'] = person_id
                data_cast['person_name'] = person_name
                data_cast['original_character'] = original_character
                responses_list.append(data_cast)
        else: 
            print(f"Failed to fetch data for person ID {person_id}")

    if responses_list: 
        combined_actor_data_raw = pd.concat(responses_list, ignore_index=True) 
    else: 
        combined_actor_data_raw = pd.DataFrame()

    combined_actor_data = combined_actor_data_raw[combined_actor_data_raw['media_type']=="movie"]
    combined_actor_data = combined_actor_data[['person_name','original_character', 'person_id', 'id','original_title','overview','popularity','vote_count','vote_average','release_date', 'poster_path']]
    combined_actor_data.sort_values(by='vote_average', ascending=False, inplace=True)
    combined_actor_data.reset_index(drop=True, inplace=True)


    filter_movie_rating_min = st.sidebar.slider("Rating Min", min_value=0.0, max_value=10.0, value=5.5)
    filter_movie_rating_max = st.sidebar.slider("Rating Max", min_value=0.0, max_value=10.0, value=9.9)
    filter_movie_rating_count = st.sidebar.slider("Votes", min_value=0, max_value=1000, value=150)

    combined_actor_data = combined_actor_data[(combined_actor_data['vote_average'] >=filter_movie_rating_min) &
                                            (combined_actor_data['vote_average']<=filter_movie_rating_max) &
                                            (combined_actor_data['vote_count']>=filter_movie_rating_count)]
    if filter_actor:
        combined_actor_data = combined_actor_data[(combined_actor_data['person_name']==filter_actor)]

    combined_actor_data = combined_actor_data[['person_name','original_title','vote_average','release_date','overview']]

    # combined_actor_data.style.set_table_styles({
    #     'overview': [{'selector': '',
    #                   'props': [('wdith', '5000px')]}],
    # }, overwrite=False)




    st.subheader('Films starring \"'+ start_movie + '\" actors')
    st.markdown(combined_actor_data.to_html(escape=False, index=False), unsafe_allow_html=True)
    #st.dataframe(combined_actor_data)

else: 
    st.write("Please enter the name of the last watched movie.")
