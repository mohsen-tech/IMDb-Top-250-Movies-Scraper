import streamlit as st

# For enhanced visual aesthetics and improved implementation, 
# the 'pages' directory has been added to the dashboard, 
# and the code related to its sections has been placed separately in a .zip file.

st.set_page_config(page_title="Dashboard")
"""
# Dashboard Instructions

## Subcategory 1: Table Filtering

In this subcategory, you need to collect information from the user and display tables on the page based on their interests and preferences. Use `st.dataframe` or `st.table` to create these tables.

**Implementation of all the following items is mandatory:**

1. A table of movies produced within the user's specified time range. For example, a table of movies produced between 1997 and 2021, where the user can input their desired years.
2. A table of movies with a duration that falls within the user's specified range. For example, a table of movies that are between 80 and 120 minutes long, where the user can input their desired durations.
3. A table of movies in which the user's preferred actor or actors have appeared. For example, a table of movies in which either Leonardo DiCaprio or Matthew McConaughey has acted. It is not necessary for both actors to appear in the same movie; just display movies in which either actor has played a role. The user can select any number of actors.
4. A table of movies with a specific genre. The user can only select one genre (they cannot view movies belonging to different genres in a single table). For example, a table of movies with the Crime genre, which the user has selected.

## Subcategory 2: Static Charts

These charts are more analytical and do not require specific user inputs for display.

**Implementation of all the following items is mandatory:**

1. A bar chart of the top 10 highest-grossing films.
2. A bar chart of the top 5 most frequently appearing actors (number of appearances in the top 250 films).
3. A pie chart displaying the number of different genres.
4. A pie chart displaying the age ratings of the films.
5. A chart showing the number of occurrences of each age rating within each genre. For example, how many times different age ratings have been seen in the Crime genre (you can refer to `st.barchart` for guidance).

## Subcategory 3: Interactive Charts

In this subcategory, we aim to create charts that align with user preferences.

**Implementation of the following item is mandatory:**

1. Display a bar chart of the highest-grossing films in the user's selected genre. To do this, take the user's input for their desired genre (only one genre can be selected), and show them the top-grossing films in that genre in the form of a bar chart.

## Subcategory 4: Advanced Additions and Applications

Solving this subcategory is optional. In this fourth subcategory, we intend to extract more advanced insights from the data we have collected. Overcoming the challenges in this section may not be possible with your current knowledge, so additional reading and research may be required!

1. Create word clouds based on movie storylines for different genres. You can have different word clouds for different genres.
2. Develop a recommendation system based on the information from each movie. When the user provides the name of a movie, the system should suggest similar movies.
3. Create a graph of actor collaborations, where each node in the graph represents an actor, and the edges in the graph represent collaborations between two actors. The number of collaborations between two actors determines the weight of the edge. If two actors have not collaborated, there will be no edge between them.
4. Add any other charts or filters that you believe would help the user find their desired content in Subcategory 1.

*Note: The implementation details and code for each of these tasks would require programming and data analysis skills.*
"""