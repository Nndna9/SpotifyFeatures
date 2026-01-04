
import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="Spotify GenZ Dashboard", page_icon="🎧", layout="wide")

SPOTIFY_GREEN = "#1DB954"
BLACK = "#191414"
WHITE = "#FFFFFF"

st.markdown(f'''
    <style>
    .stApp {{
        background-color: {BLACK};
        color: {WHITE};
    }}
    h1, h2, h3 {{
        color: {SPOTIFY_GREEN};
    }}
    </style>
''', unsafe_allow_html=True)

with st.spinner("Loading the vibes 🎶✨"):
    time.sleep(1.5)

st.markdown("<h1 style='text-align:center;'>🎧 Spotify Audio Features Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>GenZ insights into music trends ✨</p>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("SpotifyFeatures.csv")

df = load_data()

st.sidebar.header("🎛️ Global Filters")
genres = st.sidebar.multiselect("Select Genres", sorted(df["genre"].unique()), default=sorted(df["genre"].unique())[:5])
pop_range = st.sidebar.slider("Popularity Range", int(df["popularity"].min()), int(df["popularity"].max()), (20, 90))

filtered_df = df[(df["genre"].isin(genres)) & (df["popularity"].between(pop_range[0], pop_range[1]))]

col1, col2, col3, col4 = st.columns(4)
col1.metric("🎵 Tracks", len(filtered_df))
col2.metric("🔥 Avg Energy", round(filtered_df["energy"].mean(), 2))
col3.metric("💃 Avg Danceability", round(filtered_df["danceability"].mean(), 2))
col4.metric("❤️ Avg Valence", round(filtered_df["valence"].mean(), 2))

def section(title, caption):
    st.subheader(title)
    st.caption(caption)

section("1️⃣ Popularity vs Energy", "Shows whether high-energy songs dominate mainstream success.")
st.plotly_chart(px.scatter(filtered_df, x="energy", y="popularity", color="genre"), use_container_width=True)

section("2️⃣ Danceability by Genre", "Reveals which genres make people move the most.")
st.plotly_chart(px.box(filtered_df, x="genre", y="danceability", color="genre"), use_container_width=True)

section("3️⃣ Tempo Distribution", "Tempo defines workout, party, or chill vibes.")
st.plotly_chart(px.histogram(filtered_df, x="tempo", nbins=40), use_container_width=True)

section("4️⃣ Loudness vs Popularity", "Louder tracks often feel more powerful.")
st.plotly_chart(px.scatter(filtered_df, x="loudness", y="popularity", color="genre"), use_container_width=True)

section("5️⃣ Mood (Valence) by Genre", "Emotional tone across music styles.")
st.plotly_chart(px.violin(filtered_df, x="genre", y="valence", color="genre"), use_container_width=True)

section("6️⃣ Explicit Content Trend", "Explicit tracks vs popularity.")
st.plotly_chart(px.bar(filtered_df.groupby("explicit")["popularity"].mean().reset_index(),
                       x="explicit", y="popularity"), use_container_width=True)

section("7️⃣ Acousticness vs Energy", "Raw vs electronic sound contrast.")
st.plotly_chart(px.scatter(filtered_df, x="acousticness", y="energy", color="genre"), use_container_width=True)

section("8️⃣ Top Genres by Popularity", "Genres dominating listener attention.")
top_genres = filtered_df.groupby("genre")["popularity"].mean().sort_values(ascending=False).head(10).reset_index()
st.plotly_chart(px.bar(top_genres, x="genre", y="popularity"), use_container_width=True)

section("9️⃣ Energy vs Danceability", "Are energetic songs dance-friendly?")
st.plotly_chart(px.scatter(filtered_df, x="energy", y="danceability", color="genre"), use_container_width=True)

section("🔟 Track Duration Analysis", "Optimize song length for retention.")
st.plotly_chart(px.histogram(filtered_df, x="duration_ms", nbins=40), use_container_width=True)

st.markdown("---")
st.markdown("<h3 style='text-align:center;'>✨ Made with Spotify Energy ✨</h3>", unsafe_allow_html=True)
