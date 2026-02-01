import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from live_connection import fetch_live_tweets, get_tweets_df
import base64
# PAGE CONFIG

st.set_page_config(layout="wide", page_title="Social Media  Dashboard")

def style_plotly(fig, dark_mode):
    text_color = "white" if dark_mode else "black"
    grid_color = "rgba(255,255,255,0.2)" if dark_mode else "rgba(0,0,0,0.15)"

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_color),
        legend=dict(font=dict(color=text_color)),
       
    )

    fig.update_xaxes(
        tickfont=dict(color="white" if dark_mode else "black"),
        title_font=dict(color="white" if dark_mode else "black"),
        showgrid=True,
        gridcolor="rgba(255,255,255,0.2)" if dark_mode else "rgba(0,0,0,0.15)",
    )

    fig.update_yaxes(
        tickfont=dict(color="white" if dark_mode else "black"),
        title_font=dict(color="white" if dark_mode else "black"),
        showgrid=True,
        gridcolor="rgba(255,255,255,0.2)" if dark_mode else "rgba(0,0,0,0.15)",
    )

    return fig

# DARK MODE TOGGLE

dark_mode = st.sidebar.checkbox("Dark Mode", value=True)

def set_bg_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            transition: background 0.5s ease;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
# APPLY BACKGROUND BASED ON MODE
if dark_mode:
    set_bg_image("assets/dark_bg.png")
    text_color = "white"
    st.markdown("""
    <style>
    .block-container {
    background: rgba(0, 0, 0, 0.55);
    padding: 2rem;
    border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    set_bg_image("assets/light_bg.png")
    text_color = "#111111"
    
# text color fix 
st.markdown(
    f"""
    <style>
    h1, h2, h3, h4, p, span, div {{
        color: {text_color} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# refresh button css 

def style_buttons(dark_mode):
    if dark_mode:
        bg = "#1f2937"        # dark gray
        text = "white"
        border = "#374151"
    else:
        bg = "#ffffff"        # white
        text = "#111827"      # dark text
        border = "#111827"

    st.markdown(
        f"""
        <style>
        div.stButton > button {{
            background-color: {bg};
            color: {text};
            border: 2px solid {border};
            border-radius: 10px;
            padding: 0.5rem 1.2rem;
            font-weight: 600;
        }}
        div.stButton > button:hover {{
            background-color: #2563eb;
            color: white;
            border-color: #2563eb;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

style_buttons(dark_mode)

# Refresh dashboard every 30 seconds (30000 ms)

st_autorefresh(interval=30000, key="data_refresh")

# FETCH LIVE TWEETS 

@st.cache_data(ttl=60)  # cache for 60 seconds
def get_all_tweets():
    fetch_live_tweets()       # fetch new tweets from API
    return get_tweets_df()    # return as DataFrame

df_tweets = get_all_tweets() 

# 🚨 NEGATIVITY SPIKE ALERT

if not df_tweets.empty:
    now = pd.Timestamp.now()
    last_5 = df_tweets[
        (df_tweets['time'] >= now - pd.Timedelta(minutes=5)) &
        (df_tweets['sentiment'] == 'Negative')
    ]

    prev_5 = df_tweets[
        (df_tweets['time'] >= now - pd.Timedelta(minutes=10)) &
        (df_tweets['time'] < now - pd.Timedelta(minutes=5)) &
        (df_tweets['sentiment'] == 'Negative')
    ]

    if len(prev_5) > 0 and len(last_5) > len(prev_5) * 1.5:
        st.error("🚨 ALERT: Sudden spike in negative sentiment!")

# Manual refresh button
if st.button("🔄 Refresh Tweets Now"):
    fetch_live_tweets()        # fetch new tweets from API
    df_tweets = get_tweets_df()  # update DataFrame
    st.rerun()    # refresh the dashboard immediately

# HEADER

st.markdown(
    f"<h1 style='text-align: center; color: {'white' if dark_mode else 'black'}'>Real-Time Social Media Sentiment Analytics </h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<h3 style='text-align: center; color: {'white' if dark_mode else 'black'}'>Total Followers: 23,004</h3>",
    unsafe_allow_html=True
)

# LIVE PLATFORM OVERVIEW

# Twitter metrics from live tweets
df_today = df_tweets[df_tweets['time'].dt.date == pd.Timestamp('today').date()] if not df_tweets.empty else pd.DataFrame()
twitter_tweets = len(df_today)
twitter_retweets = twitter_tweets * 2  
twitter_likes = twitter_tweets * 5     

# Session state for delta so "today" updates dynamically
if "last_twitter" not in st.session_state:
    st.session_state.last_twitter = 0
twitter_delta = twitter_tweets - st.session_state.last_twitter
st.session_state.last_twitter = twitter_tweets

# Simulate / replace with API data if available
facebook_followers = 1987
facebook_delta = 12
instagram_followers = 11000 
instagram_delta = 1099
youtube_followers = 8239
youtube_delta = 144

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Facebook", value=f"{facebook_followers:,}", delta=f"{facebook_delta} today")
with col2:
    st.metric("Twitter", value=f"{twitter_tweets}", delta=f"{twitter_delta} today")
with col3:
    st.metric("Instagram", value=f"{instagram_followers:,}", delta=f"{instagram_delta} today")
with col4:
    st.metric("YouTube", value=f"{youtube_followers:,}", delta=f"{youtube_delta} today")

# OVERVIEW - TODAY

today = pd.Timestamp(datetime.now().date())
df_today = df_tweets[df_tweets['time'].dt.date == today.date()]

today_counts = df_today['sentiment'].value_counts()
positive_today = today_counts.get('Positive', 0)
negative_today = today_counts.get('Negative', 0)
neutral_today = today_counts.get('Neutral', 0)

total_today = len(df_today)
likes_today = total_today * 5       
retweets_today = total_today * 2    
profile_views_today = 52000        

st.markdown("### Platform Overview - Today")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Facebook Page Views", value="87", delta="3%")
    st.metric(label="Facebook Likes", value="52", delta="2%")
with col2:
    st.metric(label="Twitter Retweets", value="117", delta="303%")
    st.metric(label="Twitter Likes", value="507", delta="553%")
with col3:
    st.metric(label="Instagram Likes", value="5,462", delta="2,257%")
    st.metric(label="Instagram Profile Views", value="52k", delta="1,375%")
with col4:
    st.metric(label="YouTube Likes", value="107", delta="-19%")
    st.metric(label="YouTube Total Views", value="1,407", delta="-12%")

# SENTIMENT METRICS

st.markdown("### Sentiment Overview")
if not df_tweets.empty:
    sentiment_counts = df_tweets['sentiment'].value_counts()
    positive_count = sentiment_counts.get('Positive', 0)
    negative_count = sentiment_counts.get('Negative', 0)
    neutral_count = sentiment_counts.get('Neutral', 0)
else:
    positive_count = negative_count = neutral_count = 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Positive Tweets", positive_count)
with col2:
    st.metric("Negative Tweets", negative_count)
with col3:
    st.metric("Neutral Tweets", neutral_count)

# PIE CHART - SENTIMENT DISTRIBUTION

if not df_tweets.empty:
    df_pie = df_tweets['sentiment'].value_counts().reset_index()
    df_pie.columns = ['sentiment', 'count']
    st.markdown("### Tweet Sentiment Distribution")
    fig_pie = px.pie(
        df_pie,
        names='sentiment',
        values='count',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white" if dark_mode else "black",
        showlegend =False,
    )
    fig_pie.update_traces(
        textfont=dict(color="white" if dark_mode else "black")
    )

    st.plotly_chart(fig_pie, use_container_width=True)

# LINE CHART - TWEETS OVER TIME

if not df_tweets.empty:
    df_tweets['time'] = pd.to_datetime(df_tweets['time'])
    tweets_by_time = df_tweets.groupby(df_tweets['time'].dt.floor('min')).size().reset_index(name='count')
    st.markdown("### Tweets Over Time")
    fig_line = px.line(
        tweets_by_time,
        x='time',
        y='count',
        markers=True
    )
    fig_line = style_plotly(fig_line, dark_mode)
    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white" if dark_mode else "black",

    )
    fig_line.update_traces(
        textfont=dict(color="white" if dark_mode else "black")
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
# follower comparison 

followers_data = {
    "Facebook": 1987,
    "Twitter": 1044,
    "Instagram": 11000,
    "YouTube": 8239
}

df_followers = pd.DataFrame(
    list(followers_data.items()),
    columns=["platform", "followers"]
)
st.markdown("### Followers Comparison by Platform")

fig = px.bar(
    df_followers,
    x="platform",
    y="followers"
)
fig = style_plotly(fig, dark_mode)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white" if dark_mode else "black",

)
st.plotly_chart(fig, use_container_width=True)

