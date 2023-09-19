import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import html
import re
import random
import json


def find_one(html_str, pattern_str):
    """
    find one attr value in element
    like title, year, rating, duration, gross

    Parameters
    ----------
    html_str : str
    pattern_str : str

    Returns
    -------
    str or np.nan
    """
    match = re.search(pattern_str, html_str)
    if match:
        return html.unescape(match.group(1))
    else:
        return np.nan


def find_many(html_str, pattern_str):
    """
    find many attr value in element
    like genres, urls, names, duration

    Parameters
    ----------
    html_str : str
    pattern_str : str

    Returns
    -------
    list
    """
    match = re.findall(pattern_str, html_str)
    if match:
        return html.unescape(match)
    else:
        []


def create_specific_dict(name_list, url_list, pattern_str):
    """
    Specifically, it concatenates two lists and creates a dictionary

    Parameters
    ----------
    name_list : list
    url_list : list
    pattern_str : str

    Returns
    -------
    dict
    """
    result_dict = {}
    for url, name in zip(url_list, name_list):
        match = re.search(pattern_str, url)
        if match:
            url = match.group(1)
        else:
            url = np.nan
        result_dict[name] = url
    return result_dict


def find_url_id_title(html_str, pattern_str):
    url_pattern = r"/title/tt(\d+)"

    matches = re.search(pattern_str, html_str)
    if matches:
        url = matches.group(1)
        title = matches.group(2)

    title = html.unescape(title)
    url = url.split("/")
    url = "/".join(url[:-1])

    match = re.search(url_pattern, url)
    if match:
        id = match.group(1)
    else:
        id = np.nan

    return url, id, title


def find_story_line(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        story_line = response.json()
        story_line = story_line["data"]["title"]["summaries"]["edges"][0]["node"][
            "plotText"
        ]["plaidHtml"]
        story_line = html.unescape(story_line)
        return story_line
    print("Failed to fetch the website.", response.status_code)
    return -1


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
]

story_line_url0 = "https://caching.graphql.imdb.com/?operationName=TMD_Storyline&variables=%7B%22isAutoTranslationEnabled%22%3Afalse%2C%22locale%22%3A%22en-US%22%2C%22titleId%22%3A%22"
story_line_url2 = "%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22sha256Hash%22%3A%22ad739d75c0062966ebf299e3aedc010e17888355fde6d0eee417f30368f38c14%22%2C%22version%22%3A1%7D%7D"

url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
main_url = "https://www.imdb.com"
headers = {
    "User-Agent": random.choice(user_agents),
    "Accept-Language": "en-US,en;q=0.5",
}
story_line_headers = {
    "Content-Type": "application/json",
}

title_link_pattern = r'<a class="ipc-title-link-wrapper" href="(/title/tt\d+/\?ref_=chttp_t_\d+)" tabindex="\d+"><h3 class="ipc-title__text">(\d+\.\s+.+)</h3></a>'
title_pattern = r'<span class="sc-afe43def-1 fDTGTb">(.*?)</span>'
year_pattern = r'href="/title/tt\d+/releaseinfo\?ref_=tt_ov_rdat" role="button" tabindex="0">(\d+)</a>'
rating_pattern = r'href="/title/tt\d+/parentalguide/certificates\?ref_=tt_ov_pg" role="button" tabindex="0">(.*?)</a>'
# duration_pattern = r'role="presentation">(\d+h \d+m)</li>'
# duration_pattern = r'role="presentation">(\d+h(?: \d+m)?)</li>'
duration_pattern = r'role="presentation">(\d+h(?: \d+m)?|(\d+m))</li>'
genres_pattern = r'<span class="ipc-chip__text">(.*?)</span>'
dr_url_pattern = r'href="(/name/nm\d+/\?ref_=tt_ov_dr)"'
wr_url_pattern = r'href="(/name/nm\d+/\?ref_=tt_ov_wr)"'
st_url_pattern = r'href="(/name/nm\d+/\?ref_=tt_ov_st)"'
name_pattern = r"<a.*?>(.*?)</a>"
gross_label_pattern = r'class="ipc-metadata-list-item__label">(.*?)</span>'
gross_value_pattern = r'class="ipc-metadata-list-item__list-content-item">(.*?)</span>'
id_in_url_pattern = r"/name/nm(\d+)/\?ref_=tt_ov"

response = requests.get(url, headers=headers)
if response.status_code == 200:
    html_content = response.content
else:
    print("Failed to fetch the website.")

df = pd.DataFrame(
    columns=[
        "dict_id",
        "title",
        "year",
        "parental_guide",
        "runtime",
        "genre",
        "directore",
        "writer",
        "star",
        "storyline",
        "gross_us_canada",
    ]
)


soup = BeautifulSoup(html_content, "html.parser")
title_link_elements = soup.find(
    "ul",
    attrs={
        "class": "ipc-metadata-list ipc-metadata-list--dividers-between sc-3f13560f-0 sTTRj compact-list-view ipc-metadata-list--base"
    },
).find_all("a", attrs={"class": "ipc-title-link-wrapper"})
# title_link_elements

cnt = 0
for element in title_link_elements:
    cnt = cnt + 1
    # if cnt > 21:
    #     break

    movie_url, movie_id, movie_name = find_url_id_title(
        str(element), title_link_pattern
    )
    temp_dict = {}
    temp_dict[movie_id] = movie_name
    url = main_url + movie_url

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content
    else:
        print("Failed to fetch the website.")
        print(cnt)
        break
    soup = BeautifulSoup(html_content, "html.parser")

    # class="ipc-overflowText ipc-overflowText--pageSection ipc-overflowText--base" --> Storyline
    tyrd_element = soup.find(
        "div", attrs={"class": "sc-dffc6c81-0 iwmAVw"}
    )  # element for title, year, rating, duration
    genres_element = soup.find("div", attrs={"class": "ipc-chip-list__scroller"})
    name_url_elements = soup.find_all(
        "div", attrs={"class": "ipc-metadata-list-item__content-container"}
    )
    gross_element = soup.find(
        "li",
        attrs={
            "class": "ipc-metadata-list__item sc-6d4f3f8c-2 byhjlB",
            "data-testid": "title-boxoffice-grossdomestic",
        },
    )

    movie_title = find_one(str(tyrd_element), title_pattern)
    release_year = find_one(str(tyrd_element), year_pattern)
    movie_rating = find_one(str(tyrd_element), rating_pattern)
    movie_duration = find_one(str(tyrd_element), duration_pattern)
    genres = find_many(str(genres_element), genres_pattern)

    dr_url = find_many(str(name_url_elements[0]), dr_url_pattern)
    dr_name = find_many(str(name_url_elements[0]), name_pattern)
    dr_dict = create_specific_dict(dr_name, dr_url, id_in_url_pattern)

    wr_url = find_many(str(name_url_elements[1]), wr_url_pattern)
    wr_name = find_many(str(name_url_elements[1]), name_pattern)
    wr_dict = create_specific_dict(wr_name, wr_url, id_in_url_pattern)

    st_url = find_many(str(name_url_elements[2]), st_url_pattern)
    st_name = find_many(str(name_url_elements[2]), name_pattern)
    st_dict = create_specific_dict(st_name, st_url, id_in_url_pattern)

    # gross_label = find_one(str(gross_element), gross_label_pattern)
    gross_value = find_one(str(gross_element), gross_value_pattern)

    parts = movie_url.split("/")
    if len(parts) > 2:
        story_line_url1 = parts[2]
    else:
        print("can't find")
        print(cnt)
        break
    storyline = find_story_line(
        story_line_url0 + story_line_url1 + story_line_url2, story_line_headers
    )

    new_row = {
        "dict_id": temp_dict,
        "title": movie_title,
        "year": release_year,
        "parental_guide": movie_rating,
        "runtime": movie_duration,
        "genre": genres,
        "directore": dr_dict,
        "writer": wr_dict,
        "star": st_dict,
        "storyline": storyline,
        "gross_us_canada": gross_value,
    }
    df.loc[len(df)] = new_row

df.to_csv("250_top_IMDB.csv", index=False)