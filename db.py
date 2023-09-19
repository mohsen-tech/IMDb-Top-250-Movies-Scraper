import numpy as np
import pandas as pd
import mysql.connector
import ast


def convert_runtime(runtime):
    parts = runtime.split()
    total_minutes = 0
    for part in parts:
        if "h" in part:
            total_minutes += int(part.replace("h", "")) * 60
        elif "m" in part:
            total_minutes += int(part.replace("m", ""))
    return total_minutes


def connect_database(my_db, my_cursor, host, user, password, database_name):
    my_db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name,
    )
    my_cursor = my_db.cursor()
    return my_db, my_cursor


def disconnect_database(my_db, my_cursor):
    my_cursor.close()
    my_db.close()
    return my_db, my_cursor


def create_df_main(df, df_main):
    for index, row in df.iterrows():
        dcit_id = eval(row["dict_id"])
        for i in dcit_id:
            id = i

        directore = eval(row["directore"])
        for i in directore:
            new_row = {
                "movie_id": id,
                "movie_title": row["title"],
                "person_id": directore[i],
                "person_name": i,
                "role": "directore",
            }
            df_main.loc[len(df_main)] = new_row

        writer = eval(row["writer"])
        for i in writer:
            new_row = {
                "movie_id": id,
                "movie_title": row["title"],
                "person_id": writer[i],
                "person_name": i,
                "role": "writer",
            }
            df_main.loc[len(df_main)] = new_row

        star = eval(row["star"])
        for i in star:
            new_row = {
                "movie_id": id,
                "movie_title": row["title"],
                "person_id": star[i],
                "person_name": i,
                "role": "star",
            }
            df_main.loc[len(df_main)] = new_row
    return df_main


df = pd.read_csv("250_top_IMDB.csv")

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


df["gross_us_canada"] = df["gross_us_canada"].apply(convert_gross)
df["parental_guide"] = df["parental_guide"].apply(convert_parental_guide)

df_main = pd.DataFrame(
    columns=[
        "movie_id",
        "movie_title",
        "person_id",
        "person_name",
        "role",
    ]
)
df_main = create_df_main(df, df_main)

# Enter the following values to connect to the database
host = ""
user = ""
password = ""
database = ""

my_db = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
)
my_cursor = my_db.cursor()
my_cursor.execute("CREATE DATABASE " + database)
my_db.commit()
my_db, my_cursor = disconnect_database(my_db, my_cursor)

create_movie_table_query = """
CREATE TABLE IF NOT EXISTS movie (
    id VARCHAR(8) PRIMARY KEY,
    title VARCHAR(128),
    year INT,
    runtime INT,
    parental_guide VARCHAR(8),
    gross_us_canada INT
)
"""
create_person_table_query = """
CREATE TABLE IF NOT EXISTS person (
    id VARCHAR(8) PRIMARY KEY,
    name VARCHAR(32)
)
"""
create_cast_table_query = """
CREATE TABLE IF NOT EXISTS cast (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id VARCHAR(8),
    person_id VARCHAR(8),
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (person_id) REFERENCES person(id)
)
"""
create_crew_table_query = """
CREATE TABLE IF NOT EXISTS crew (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id VARCHAR(8),
    person_id VARCHAR(8),
    role VARCHAR(8),
    FOREIGN KEY (movie_id) REFERENCES movie(id),
    FOREIGN KEY (person_id) REFERENCES person(id)
)
"""
create_genre_table_query = """
CREATE TABLE IF NOT EXISTS genre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id VARCHAR(8),
    genre VARCHAR(16),
    FOREIGN KEY (movie_id) REFERENCES movie(id)
)
"""
create_storyline_table_query = """
CREATE TABLE IF NOT EXISTS storyline (
    movie_id VARCHAR(8),
    content TEXT,
    FOREIGN KEY (movie_id) REFERENCES movie(id)
)
"""
# cursor.execute("SELECT * FROM test.movie")


# section 1 (movie table)
def create_movie_table(my_db, my_cursor, df):
    for index, row in df.iterrows():
        dcit_id = eval(row["dict_id"])
        for i in dcit_id:
            id = i

        movie_data = {
            "id": id,
            "title": row["title"],
            "year": row["year"],
            "runtime": row["runtime"],
            "parental_guide": row["parental_guide"],
            "gross_us_canada": row["gross_us_canada"],
        }
        add_movie_query = """
        INSERT INTO movie (id, title, year, runtime, parental_guide, gross_us_canada)
        VALUES (%(id)s, %(title)s, %(year)s, %(runtime)s, %(parental_guide)s, %(gross_us_canada)s)
        """
        my_cursor.execute(add_movie_query, movie_data)


my_db, my_cursor = connect_database(my_db, my_cursor, host, user, password, database)
my_cursor.execute(create_movie_table_query)
create_movie_table(my_db, my_cursor, df)
my_db.commit()
my_db, my_cursor = disconnect_database(my_db, my_cursor)


# section 2 (storyline table)
def create_storyline_table(my_db, my_cursor, df):
    for index, row in df.iterrows():
        dcit_id = eval(row["dict_id"])
        for i in dcit_id:
            id = i

        storyline_data = {
            "movie_id": id,
            "content": row["storyline"],
        }
        add_storyline_query = """
        INSERT INTO storyline (movie_id, content)
        VALUES (%(movie_id)s, %(content)s)
        """
        my_cursor.execute(add_storyline_query, storyline_data)


my_db, my_cursor = connect_database(my_db, my_cursor, host, user, password, database)
my_cursor.execute(create_storyline_table_query)
create_storyline_table(my_db, my_cursor, df)
my_db.commit()
my_db, my_cursor = disconnect_database(my_db, my_cursor)


# section 3 (person table)
def create_df_person(df, df_person):
    for index, row in df.iterrows():
        directore = eval(row["directore"])
        for i in directore:
            new_row = {
                "id": directore[i],
                "name": i,
            }
            df_person.loc[len(df_person)] = new_row

        writer = eval(row["writer"])
        for i in writer:
            new_row = {
                "id": writer[i],
                "name": i,
            }
            df_person.loc[len(df_person)] = new_row

        star = eval(row["star"])
        for i in star:
            new_row = {
                "id": star[i],
                "name": i,
            }
            df_person.loc[len(df_person)] = new_row
    return df_person


def create_person_table(my_db, my_cursor, df_person):
    for index, row in df_person.iterrows():
        person_data = {
            "id": row["id"],
            "name": row["name"],
        }
        add_person_query = """
        INSERT INTO person (id, name)
        VALUES (%(id)s, %(name)s)
        """
        my_cursor.execute(add_person_query, person_data)


df_person = pd.DataFrame(
    columns=[
        "id",
        "name",
    ]
)
df_person = create_df_person(df, df_person)
df_person.drop_duplicates(inplace=True)

my_db, my_cursor = connect_database(my_db, my_cursor, host, user, password, database)
my_cursor.execute(create_person_table_query)
create_person_table(my_db, my_cursor, df_person)
my_db.commit()
my_db, my_cursor = disconnect_database(my_db, my_cursor)


# section 4 (cast table)
def create_cast_table(my_db, my_cursor, df_cast):
    for index, row in df_cast.iterrows():
        cast_data = {
            "movie_id": row["movie_id"],
            "person_id": row["person_id"],
        }
        add_cast_query = """
        INSERT INTO cast (movie_id, person_id)
        VALUES (%(movie_id)s, %(person_id)s)
        """
        my_cursor.execute(add_cast_query, cast_data)


df_join = pd.merge(df_main, df_person, left_on="person_id", right_on="id")
df_join = df_join.drop(columns=["id", "name"])
df_cast = df_join[df_join[["person_id", "movie_id"]].duplicated() == False]
# df_cast = df_cast[df_cast["role"] == "star"]

my_db, my_cursor = connect_database(my_db, my_cursor, host, user, password, database)
my_cursor.execute(create_cast_table_query)
create_cast_table(my_db, my_cursor, df_cast)
my_db.commit()
my_db, my_cursor = disconnect_database(my_db, my_cursor)


# section 5 (crew table)
def create_crew_table(my_db, my_cursor, df_crew):
    for index, row in df_crew.iterrows():
        crew_data = {
            "movie_id": row["movie_id"],
            "person_id": row["person_id"],
            "role": row["role"],
        }
        add_crew_query = """
        INSERT INTO crew (movie_id, person_id, role)
        VALUES (%(movie_id)s, %(person_id)s, %(role)s)
        """
        my_cursor.execute(add_crew_query, crew_data)


df_crew = df_join[df_join["role"] != "star"]
df_crew.loc[df_crew["role"] == "directore", "role"] = "director"

my_db, my_cursor = connect_database(my_db, my_cursor, host, user, password, database)
my_cursor.execute(create_crew_table_query)
create_crew_table(my_db, my_cursor, df_crew)
my_db.commit()
my_db, my_cursor = disconnect_database(my_db, my_cursor)


# section 6 (genre table)
def create_genre_table(my_db, my_cursor, df_genre):
    for index, row in df_genre.iterrows():
        dcit_id = eval(row["dict_id"])
        for i in dcit_id:
            id = i
        genre_list = ast.literal_eval(row["genre"])
        for genre in genre_list:
            genre_data = {
                "movie_id": id,
                "genre": genre,
            }
            add_genre_query = """
            INSERT INTO genre (movie_id, genre)
            VALUES (%(movie_id)s, %(genre)s)
            """
            my_cursor.execute(add_genre_query, genre_data)


my_db, my_cursor = connect_database(my_db, my_cursor, host, user, password, database)
my_cursor.execute(create_genre_table_query)
create_genre_table(my_db, my_cursor, df)
my_db.commit()
my_db, my_cursor = disconnect_database(my_db, my_cursor)