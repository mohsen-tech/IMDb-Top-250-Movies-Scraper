import streamlit as st
import numpy as np
import pandas as pd
import ast

none_genre_val = 'None'

def read_df():

    df = pd.read_csv("250_top_IMDB.csv")

    def convert_runtime(runtime):
        parts = runtime.split()
        total_minutes = 0
        for part in parts:
            if "h" in part:
                total_minutes += int(part.replace("h", "")) * 60
            elif "m" in part:
                total_minutes += int(part.replace("m", ""))
        return total_minutes

    df["runtime"] = df["runtime"].apply(convert_runtime)
    nanValue = df["gross_us_canada"][4]

    def convert_gross(gross_val):
        if nanValue is gross_val:
            return 0
        else:
            return int(gross_val.replace("$", "").replace(",", ""))
        
    def extract_keys(dictionary):
        return list(dictionary.keys())[0]
    
    df["gross_us_canada"] = df["gross_us_canada"].apply(convert_gross)

    df["genre"] = df["genre"].apply(ast.literal_eval)
    df["directore"] = df["directore"].apply(ast.literal_eval)
    df["writer"] = df["writer"].apply(ast.literal_eval)
    df["star"] = df["star"].apply(ast.literal_eval)

    df["dict_id"] = df["dict_id"].apply(ast.literal_eval)
    df["dict_id"] = df["dict_id"].apply(extract_keys)

    df.drop(columns=["storyline"], inplace=True)

    min_year = df["year"].min()
    max_year = df["year"].max()
    min_runtime = df["runtime"].min()
    max_runtime = df["runtime"].max()

    temp = df.explode("star", ignore_index=True)
    unique_actors = temp["star"].unique().tolist()

    temp = df.explode("genre")
    unique_genres = temp["genre"].unique().tolist()
    unique_genres = [none_genre_val] + unique_genres

    return df, min_year, max_year, min_runtime, max_runtime, unique_actors, unique_genres

# Initialization
# if 'key' not in st.session_state:
#     st.session_state['key'] = 'value'
df, min_year, max_year, min_runtime, max_runtime, unique_actors, unique_genres = read_df()

st.set_page_config(page_title="Filtering Tables")
st.title("First Subcategory; Filtering Tables")

col1, col2 = st.columns(2)
with col1:
    from_year = st.number_input("from Year", min_year, max_year, value=min_year)
    from_runtime = st.number_input(
        "from Runtime", min_runtime, max_runtime, value=min_runtime
    )
with col2:
    to_year = st.number_input("to Year", min_year, max_year, value=max_year)
    to_runtime = st.number_input(
        "to Runtime", min_runtime, max_runtime, value=max_runtime
    )

choose_stars = st.multiselect("Choose from Actors", unique_actors)
choose_genre = st.selectbox("Choose a Genre", unique_genres)
st.write("")

if st.button("Submit", use_container_width=True):
    df_temp = df[(df["year"] >= from_year) & (df["year"] <= to_year)]
    df_temp = df_temp[
        (df_temp["runtime"] >= from_runtime) & (df_temp["runtime"] <= to_runtime)
    ]

    if choose_stars != []:
        desired_actors = []
        for star in choose_stars:
            desired_actors.append(star)

        def filter_actors(actor_dict):
            for actor in desired_actors:
                if actor in actor_dict:
                    return True
            return False

        df_temp = df_temp[df_temp["star"].apply(filter_actors)]

    if choose_genre is not none_genre_val:
        df_temp = df_temp[df_temp["genre"].apply(lambda x: choose_genre in x)]

    st.write("")
    df_temp
    # st.table(df_temp)