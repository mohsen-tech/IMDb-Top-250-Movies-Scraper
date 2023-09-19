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

    def convert_parental_guide(parental_guide_val):
        if (
            parental_guide_val in ["null", "blank", "Not Rated"]
            or nanValue is parental_guide_val
        ):
            return "Unrated"
        return parental_guide_val

    def extract_keys(dictionary):
        return list(dictionary.keys())[0]

    df["gross_us_canada"] = df["gross_us_canada"].apply(convert_gross)
    df["parental_guide"] = df["parental_guide"].apply(convert_parental_guide)

    df["genre"] = df["genre"].apply(ast.literal_eval)
    df["directore"] = df["directore"].apply(ast.literal_eval)
    df["writer"] = df["writer"].apply(ast.literal_eval)
    df["star"] = df["star"].apply(ast.literal_eval)

    df["dict_id"] = df["dict_id"].apply(ast.literal_eval)
    df["dict_id"] = df["dict_id"].apply(extract_keys)

    df.drop(columns=["storyline"], inplace=True)

    return df


def top_stars(df, top_n=10):
    df_star = pd.DataFrame(
        columns=[
            "person_id",
            "person_name",
        ]
    )

    def create_df_main(df, df_star):
        for index, row in df.iterrows():
            star = row["star"]
            for i in star:
                new_row = {
                    "person_id": star[i],
                    "person_name": i,
                }
                df_star.loc[len(df_star)] = new_row
        return df_star

    df_star = create_df_main(df, df_star)
    temp = df_star.value_counts()
    temp = temp.head(top_n)
    return pd.DataFrame(temp).reset_index()


df = read_df()
top_n = 10

st.set_page_config(page_title="Static Charts")
st.title("Second Subcategory; Static Charts")

top_10_movies = df.nlargest(top_n, "gross_us_canada")
fig = px.bar(
    top_10_movies,
    x="title",
    y="gross_us_canada",
    title="Bar Chart of 10 Best Selling Movies",
)
tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    st.plotly_chart(fig, theme="streamlit")
with tab2:
    st.plotly_chart(fig, theme=None)


top_10_stars = top_stars(df)
fig = px.bar(
    top_10_stars,
    x="person_name",
    y="count",
    title="Bar Chart of the 10 Most Prolific Actors",
)
tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    st.plotly_chart(fig, theme="streamlit")
with tab2:
    st.plotly_chart(fig, theme=None)


temp = df.explode("genre")
temp = temp["genre"].value_counts()
temp = pd.DataFrame(temp).reset_index()
fig = px.pie(
    temp, values="count", names="genre", title="Pie Chart of the number of each Genre"
)
tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    st.plotly_chart(fig, theme="streamlit")
with tab2:
    st.plotly_chart(fig, theme=None)


temp = df["parental_guide"].value_counts()
temp = pd.DataFrame(temp).reset_index()
fig = px.pie(
    temp,
    values="count",
    names="parental_guide",
    title="Pie Chart of the number of `parental_guide` Rating in Movies",
)
tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    st.plotly_chart(fig, theme="streamlit")
with tab2:
    st.plotly_chart(fig, theme=None)


df_exploded = df.explode("genre")
genre_age_counts = (
    df_exploded.groupby(["genre", "parental_guide"]).size().unstack(fill_value=0)
)
genre_age_counts
st.bar_chart(genre_age_counts)