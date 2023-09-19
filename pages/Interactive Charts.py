import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import ast


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

    temp = df.explode("genre")
    unique_genres = temp["genre"].unique().tolist()
    unique_genres = unique_genres

    return df, unique_genres

df, unique_genres = read_df()

st.set_page_config(page_title="Interactive Charts")
st.title("Third Subcategory; Interactive Charts")

choose_genre = st.selectbox("Choose a Genre", unique_genres)
st.write("")

if st.button("Submit", use_container_width=True):

    temp = df.explode("genre")
    genre_df = temp[temp["genre"] == choose_genre]
    sorted_genre_df = genre_df.sort_values(by="gross_us_canada", ascending=False)
    top_movies = sorted_genre_df.head(10)
    # top_movies
    fig = px.bar(
        top_movies,
        x="title",
        y="gross_us_canada",
        title="Bar Chart of 10 Best Selling Movies in a Genre",
    )
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)