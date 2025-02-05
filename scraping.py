import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from io import BytesIO
from google_play_scraper import reviews
import tweepy
from TikTokApi import TikTokApi
import sys

def download_file(df, file_format):
    buffer = BytesIO()
    if file_format == "Excel":
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
        buffer.seek(0)
        return buffer, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif file_format == "CSV":
        buffer.write(df.to_csv(index=False).encode("utf-8"))
        buffer.seek(0)
        return buffer, "text/csv"
    elif file_format == "JSON":
        buffer.write(df.to_json(orient="records").encode("utf-8"))
        buffer.seek(0)
        return buffer, "application/json"
    return None, None

def scrape_playstore(app_id, count=2000):
    try:
        result, _ = reviews(app_id, lang='id', count=count)
        reviews_data = []
        for review in result:
            reviews_data.append({
                "Date": review['at'],
                "User": review['userName'],
                "Content": review['content'],
                "Score": review['score']
            })
        return reviews_data
    except Exception as e:
        st.error(f"Error scraping PlayStore: {str(e)}")
        return []

def scrape_twitter(api_key, api_secret, access_token, access_token_secret, query, count=10):
    try:
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
        api = tweepy.API(auth)
        tweets = api.search_tweets(q=query, count=count, tweet_mode='extended')
        results = []
        for tweet in tweets:
            results.append({
                "Date": tweet.created_at,
                "User": tweet.user.screen_name,
                "Tweet": tweet.full_text,
                "Likes": tweet.favorite_count,
                "Retweets": tweet.retweet_count
            })
        return results
    except Exception as e:
        st.error(f"Error scraping Twitter: {str(e)}")
        return []

def video_comments(api_key, video_id):
    replies = []
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.commentThreads().list(part='snippet,replies', videoId=video_id).execute()

        while video_response:
            for item in video_response['items']:
                published = item['snippet']['topLevelComment']['snippet']['publishedAt']
                user = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                likeCount = item['snippet']['topLevelComment']['snippet']['likeCount']
                replies.append([published, user, comment, likeCount])

                if item['snippet']['totalReplyCount'] > 0:
                    for reply in item['replies']['comments']:
                        published = reply['snippet']['publishedAt']
                        user = reply['snippet']['authorDisplayName']
                        repl = reply['snippet']['textDisplay']
                        likeCount = reply['snippet']['likeCount']
                        replies.append([published, user, repl, likeCount])

            if 'nextPageToken' in video_response:
                video_response = youtube.commentThreads().list(
                    part='snippet,replies',
                    pageToken=video_response['nextPageToken'],
                    videoId=video_id
                ).execute()
            else:
                break
    except HttpError as e:
        st.error(f"API Error: {str(e)}")
        return []
    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")
        return []

    return replies

def extract_tiktok_video_id(video_url):
    import re
    match = re.search(r'video/(\d+)', video_url)
    if match:
        return match.group(1)
    else:
        st.error("URL TikTok tidak valid.")
        return None

def scrape_tiktok_comments(video_url):
    try:
        api = TikTokApi()
        video_id = extract_tiktok_video_id(video_url)
        if video_id is None:
            return []
        
        comments = api.video(id=video_id).comments()
        results = []
        for comment in comments:
            results.append({
                "Date": comment.create_time,
                "User": comment.author.username,
                "Comment": comment.text,
                "Likes": comment.digg_count
            })
        return results
    except Exception as e:
        st.error(f"Error scraping TikTok: {str(e)}")
        return []

def show():
    if "scraped_data" not in st.session_state:
        st.session_state.scraped_data = None
        st.session_state.scraped_columns = []

    st.markdown(
        """
        <style>
            .stButton>button {
                background-color: #483D8B;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
            }
            .stTextInput>div>input {
                border: 2px solid #483D8B;
                border-radius: 5px;
            }
        </style>
        """, unsafe_allow_html=True
    )

    st.title("📊 Scraping Data Berbasis Web")
    st.markdown("Selamat datang di aplikasi scraping data! Pilih platform yang ingin Anda scraping.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Scraping YouTube"):
            st.session_state['platform'] = 'youtube'
    with col2:
        if st.button("Scraping Twitter"):
            st.session_state['platform'] = 'twitter'
    with col3:
        if st.button("Scraping PlayStore"):
            st.session_state['platform'] = 'playstore'
    with col4:
        if st.button("Scraping TikTok"):
            st.session_state['platform'] = 'tiktok'

    platform = st.session_state.get('platform', 'youtube')

    if platform == 'youtube':
        st.subheader("🎥 Scraping Komentar YouTube")
        api_key = st.text_input("🔑 API Key YouTube:")
        video_id = st.text_input("🔗 Video ID YouTube:")
        if st.button("Scrape Komentar"):
            if api_key and video_id:
                comments = video_comments(api_key, video_id)
                if comments:
                    st.session_state.scraped_data = pd.DataFrame(comments, columns=['PublishedAt', 'User', 'Comment', 'Likes'])
                    st.session_state.scraped_columns = ['PublishedAt', 'User', 'Comment', 'Likes']
                else:
                    st.session_state.scraped_data = None
                    st.warning("Tidak ada komentar ditemukan atau Video ID salah.")
            else:
                st.warning("Silakan masukkan API Key dan Video ID.")


    elif platform == 'twitter':
        st.subheader("Scraping Twitter")
        api_key = st.text_input("API Key Twitter:")
        api_secret = st.text_input("API Secret Twitter:")
        access_token = st.text_input("Access Token Twitter:")
        access_token_secret = st.text_input("Access Token Secret Twitter:")
        query = st.text_input("Masukkan Query Pencarian Twitter:")
        if st.button("Scrape Twitter"):
            if all([api_key, api_secret, access_token, access_token_secret, query]):
                tweets = scrape_twitter(api_key, api_secret, access_token, access_token_secret, query)
                if tweets:
                    st.session_state.scraped_data = pd.DataFrame(tweets)
                    st.session_state.scraped_columns = tweets[0].keys()
                else:
                    st.session_state.scraped_data = None
                    st.warning("Tidak ada data ditemukan atau terjadi kesalahan.")
            else:
                st.warning("Silakan lengkapi semua data.")

    elif platform == 'playstore':
        st.subheader("Scraping PlayStore")
        app_id = st.text_input("Masukkan ID Aplikasi PlayStore:")
        if st.button("Scrape PlayStore"):
            if app_id:
                reviews_data = scrape_playstore(app_id)
                if reviews_data:
                    st.session_state.scraped_data = pd.DataFrame(reviews_data)
                    st.session_state.scraped_columns = reviews_data[0].keys()
                else:
                    st.session_state.scraped_data = None
                    st.warning("Tidak ada data ditemukan atau terjadi kesalahan.")
            else:
                st.warning("Silakan masukkan ID aplikasi.")

    elif platform == 'tiktok':
        st.subheader("Scraping TikTok")
        video_url = st.text_input("Masukkan URL Video TikTok:")
        if st.button("Scrape Komentar TikTok"):
            if video_url:
                tiktok_comments = scrape_tiktok_comments(video_url)
                if tiktok_comments:
                    st.session_state.scraped_data = pd.DataFrame(tiktok_comments)
                    st.session_state.scraped_columns = tiktok_comments[0].keys()
                else:
                    st.session_state.scraped_data = None
                    st.warning("Tidak ada data ditemukan atau terjadi kesalahan.")
            else:
                st.warning("Silakan masukkan URL Video TikTok.")

    # Menampilkan data yang telah di-scrape
    if st.session_state.scraped_data is not None:
        st.markdown("### Data yang telah di-scrape:")
        st.write(st.session_state.scraped_data)

        # Unduh data
        st.markdown("### Simpan Data")
        file_format = st.radio("Pilih format file:", ["Excel", "CSV", "JSON"])
        buffer, mime_type = download_file(st.session_state.scraped_data, file_format)
        if buffer:
            st.download_button(
                label=f"Download {file_format}",
                data=buffer,
                file_name=f"scraped_data.{file_format.lower()}",
                mime=mime_type
            )

if __name__ == "__main__":
    show()
