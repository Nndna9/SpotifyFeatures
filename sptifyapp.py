
import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="Spotify GenZ Dashboard", page_icon="🎧", layout="wide")

SPOTIFY_GREEN = "#1DB954"
BLACK = "#191414"

st.markdown(f'''
    <style>
    .stApp {{
        background-color: {BLACK};
        color: white;
    }}
    h1, h2, h3 {{
        color: {SPOTIFY_GREEN};
    }}
    </style>
''', unsafe_allow_html=True)

with st.spinner("Loading the vibes 🎶✨"):
    time.sleep(1.2)

st.markdown("<h1 style='text-align:center;'>🎧 Spotify Audio Features Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>GenZ insights into music trends ✨</p>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("SpotifyFeatures_small.csv")

df = load_data()

st.sidebar.header("🎛️ Global Filters")
genres = st.sidebar.multiselect("Select Genres", sorted(df.genre.unique()), default=sorted(df.genre.unique())[:5])
pop_range = st.sidebar.slider("Popularity Range", int(df.popularity.min()), int(df.popularity.max()), (20, 90))

filtered_df = df[(df.genre.isin(genres)) & (df.popularity.between(*pop_range))]

col1, col2, col3, col4 = st.columns(4)
col1.metric("🎵 Tracks", len(filtered_df))
col2.metric("🔥 Avg Energy", round(filtered_df.energy.mean(), 2))
col3.metric("💃 Avg Danceability", round(filtered_df.danceability.mean(), 2))
col4.metric("❤️ Avg Valence", round(filtered_df.valence.mean(), 2))

def insight(title, reason):
    st.subheader(title)
    st.caption(f"Why it matters: {reason}")

insight("1️⃣ Popularity vs Energy", "Checks if energetic songs dominate mainstream success.")
st.plotly_chart(px.scatter(filtered_df, x="energy", y="popularity", color="genre",
                           hover_data=["track_name", "artist_name"]), use_container_width=True)

insight("2️⃣ Danceability by Genre", "Identifies genres that make listeners move.")
st.plotly_chart(px.box(filtered_df, x="genre", y="danceability", color="genre"), use_container_width=True)

insight("3️⃣ Tempo Distribution", "Tempo shapes workout, party, or chill playlists.")
st.plotly_chart(px.histogram(filtered_df, x="tempo", nbins=40), use_container_width=True)

insight("4️⃣ Loudness vs Popularity", "Louder tracks often feel more powerful.")
st.plotly_chart(px.scatter(filtered_df, x="loudness", y="popularity", color="genre"), use_container_width=True)

insight("5️⃣ Mood (Valence) by Genre", "Shows emotional tone across genres.")
st.plotly_chart(px.violin(filtered_df, x="genre", y="valence", color="genre"), use_container_width=True)

insight("6️⃣ Acousticness vs Energy", "Highlights raw vs electronic sound contrast.")
st.plotly_chart(px.scatter(filtered_df, x="acousticness", y="energy", color="genre"), use_container_width=True)

insight("7️⃣ Top Genres by Popularity", "Genres dominating listener attention.")
top_genres = filtered_df.groupby("genre")["popularity"].mean().sort_values(ascending=False).head(10).reset_index()
st.plotly_chart(px.bar(top_genres, x="genre", y="popularity"), use_container_width=True)

insight("8️⃣ Energy vs Danceability", "Checks if energetic songs are also dance-friendly.")
st.plotly_chart(px.scatter(filtered_df, x="energy", y="danceability", color="genre"), use_container_width=True)

insight("9️⃣ Track Duration Analysis", "Helps optimize song length for retention.")
st.plotly_chart(px.histogram(filtered_df, x="duration_ms", nbins=40), use_container_width=True)

insight("🔟 Overall Feature Correlation", "Shows how audio features relate to each other.")
corr = filtered_df[["danceability","energy","valence","acousticness","tempo","loudness","popularity"]].corr()
st.plotly_chart(px.imshow(corr, text_auto=True, aspect="auto"), use_container_width=True)

st.markdown("---")
st.markdown("<h3 style='text-align:center;'>✨ Spotify-style insights, GenZ approved ✨</h3>", unsafe_allow_html=True)
