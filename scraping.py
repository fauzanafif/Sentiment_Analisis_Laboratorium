import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from io import BytesIO
from google_play_scraper import reviews
import tweepy

def download_file(df, file_format):
    buffer = BytesIO()
    if file_format == "CSV":
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
                "Tanggal": review['at'],
                "User": review['userName'],
                "Komentar": review['content'],  # diseragamkan jadi Komentar
                "Skor": review['score']
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
                "Tanggal": tweet.created_at,
                "User": tweet.user.screen_name,
                "Komentar": tweet.full_text,  # diseragamkan jadi Komentar
                "Likes": tweet.favorite_count,
                "Retweet": tweet.retweet_count
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
                replies.append({
                    "Tanggal": published,
                    "User": user,
                    "Komentar": comment,  # diseragamkan jadi Komentar
                    "Likes": likeCount
                })

                if item['snippet']['totalReplyCount'] > 0:
                    for reply in item['replies']['comments']:
                        published = reply['snippet']['publishedAt']
                        user = reply['snippet']['authorDisplayName']
                        repl = reply['snippet']['textDisplay']
                        likeCount = reply['snippet']['likeCount']
                        replies.append({
                            "Tanggal": published,
                            "User": user,
                            "Komentar": repl,  # diseragamkan jadi Komentar
                            "Likes": likeCount
                        })

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

def show():
    if "scraped_data" not in st.session_state:
        st.session_state.scraped_data = None
        st.session_state.scraped_columns = []

    st.title("📊 Scraping Data Berbasis Web")
    st.markdown("Selamat datang di aplikasi scraping data! Pilih platform yang ingin Anda scraping.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Scraping YouTube"):
            st.session_state['platform'] = 'youtube'
    with col2:
        if st.button("Scraping Twitter"):
            st.session_state['platform'] = 'twitter'
    with col3:
        if st.button("Scraping PlayStore"):
            st.session_state['platform'] = 'playstore'

    platform = st.session_state.get('platform', 'youtube')

    if platform == 'youtube':
        st.subheader("🎥 Scraping Komentar YouTube")
        api_key = st.text_input("🔑 API Key YouTube:")
        video_id = st.text_input("🔗 Video ID YouTube:")
        if st.button("Scrape Komentar"):
            if api_key and video_id:
                comments = video_comments(api_key, video_id)
                if comments:
                    df = pd.DataFrame(comments)
                    st.session_state.scraped_data = df
                    st.session_state.scraped_columns = df.columns
                else:
                    st.session_state.scraped_data = None
                    st.warning("Tidak ada komentar ditemukan atau Video ID salah.")
            else:
                st.warning("Silakan masukkan API Key dan Video ID.")

    elif platform == 'twitter':
        st.subheader("🐦 Scraping Twitter")
        api_key = st.text_input("API Key Twitter:")
        api_secret = st.text_input("API Secret Twitter:")
        access_token = st.text_input("Access Token Twitter:")
        access_token_secret = st.text_input("Access Token Secret Twitter:")
        query = st.text_input("Masukkan Query Pencarian Twitter:")
        if st.button("Scrape Twitter"):
            if all([api_key, api_secret, access_token, access_token_secret, query]):
                tweets = scrape_twitter(api_key, api_secret, access_token, access_token_secret, query)
                if tweets:
                    df = pd.DataFrame(tweets)
                    st.session_state.scraped_data = df
                    st.session_state.scraped_columns = df.columns
                else:
                    st.session_state.scraped_data = None
                    st.warning("Tidak ada data ditemukan atau terjadi kesalahan.")
            else:
                st.warning("Silakan lengkapi semua data.")

    elif platform == 'playstore':
        st.subheader("📱 Scraping PlayStore")
        app_id = st.text_input("Masukkan ID Aplikasi PlayStore:")
        if st.button("Scrape PlayStore"):
            if app_id:
                reviews_data = scrape_playstore(app_id)
                if reviews_data:
                    df = pd.DataFrame(reviews_data)
                    st.session_state.scraped_data = df
                    st.session_state.scraped_columns = df.columns
                else:
                    st.session_state.scraped_data = None
                    st.warning("Tidak ada data ditemukan atau terjadi kesalahan.")
            else:
                st.warning("Silakan masukkan ID aplikasi.")

    # Menampilkan data yang telah di-scrape
    if st.session_state.scraped_data is not None:
        st.markdown("### 📋 Data yang telah di-scrape:")
        st.dataframe(st.session_state.scraped_data)

        # Unduh data
        st.markdown("### 💾 Simpan Data")
        file_format = st.radio("Pilih format file:", ["CSV", "JSON"])
        buffer, mime_type = download_file(st.session_state.scraped_data, file_format)
        if buffer:
            st.download_button(
                label=f"⬇️ Download {file_format}",
                data=buffer,
                file_name=f"data_mentah.{file_format.lower()}",
                mime=mime_type
            )

if __name__ == "__main__":
    show()
