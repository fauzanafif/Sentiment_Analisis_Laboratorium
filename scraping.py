import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from io import BytesIO
from google_play_scraper import reviews
import tweepy

def add_custom_css():
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #483D8B !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 16px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
        }

        div.stButton > button:hover {
            background-color: #5A4DB8 !important;
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(72, 61, 139, 0.4);
        }

        .stDownloadButton > button {
            background-color: #483D8B !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 16px !important;
            font-size: 15px !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
        }

        .stDownloadButton > button:hover {
            background-color: #5A4DB8 !important;
            transform: scale(1.03);
            box-shadow: 0 4px 12px rgba(72, 61, 139, 0.4);
        }
        </style>
    """, unsafe_allow_html=True)

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
                "Komentar": review['content'],
                "Skor": review['score']
            })
        return reviews_data
    except Exception as e:
        st.error(f"Error scraping PlayStore: {str(e)}")
        return []

def scrape_twitter_v2(bearer_token, query, count=10):
    try:
        client = tweepy.Client(bearer_token=bearer_token)
        response = client.search_recent_tweets(query=query, max_results=count, tweet_fields=['created_at', 'lang', 'public_metrics'])
        results = []
        if response.data:
            for tweet in response.data:
                results.append({
                    "Tanggal": tweet.created_at,
                    "User": "-",
                    "Komentar": tweet.text,
                    "Likes": tweet.public_metrics.get('like_count', 0),
                    "Retweet": tweet.public_metrics.get('retweet_count', 0)
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
                    "Komentar": comment,
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
                            "Komentar": repl,
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
    add_custom_css()

    if "scraped_data" not in st.session_state:
        st.session_state.scraped_data = None
        st.session_state.scraped_columns = []

    st.title("📊 Scraping Data Berbasis Web")
    st.markdown("Selamat datang di aplikasi scraping data! Pilih platform yang ingin Anda scraping.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎥 Scraping YouTube"):
            st.session_state['platform'] = 'youtube'
    with col2:
        if st.button("🐦 Scraping Twitter"):
            st.session_state['platform'] = 'twitter'
    with col3:
        if st.button("📱 Scraping PlayStore"):
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
                    kolom_urutan = ["Komentar"] + [col for col in df.columns if col != "Komentar"]
                    df = df[kolom_urutan]
                    st.session_state.scraped_data = df
                    st.session_state.scraped_columns = df.columns
                else:
                    st.session_state.scraped_data = None
                    st.warning("Tidak ada komentar ditemukan atau Video ID salah.")
            else:
                st.warning("Silakan masukkan API Key dan Video ID.")

    elif platform == 'twitter':
        st.subheader("🐦 Scraping Twitter")
        bearer_token = st.text_input("Bearer Token Twitter:")
        query = st.text_input("Masukkan Query Pencarian Twitter:")
        count = st.number_input("Jumlah Tweet", min_value=10, max_value=100, value=10, step=10)
        if st.button("Scrape Twitter"):
            if bearer_token and query:
                tweets = scrape_twitter_v2(bearer_token, query, count)
                if tweets:
                    df = pd.DataFrame(tweets)
                    kolom_urutan = ["Komentar"] + [col for col in df.columns if col != "Komentar"]
                    df = df[kolom_urutan]
                    st.session_state.scraped_data = df
                    st.session_state.scraped_columns = df.columns
                else:
                    st.session_state.scraped_data = None
                    st.warning("Tidak ada data ditemukan atau terjadi kesalahan.")
            else:
                st.warning("Silakan lengkapi Bearer Token dan Query.")

    elif platform == 'playstore':
        st.subheader("📱 Scraping PlayStore")
        app_id = st.text_input("Masukkan ID Aplikasi PlayStore:")
        if st.button("Scrape PlayStore"):
            if app_id:
                reviews_data = scrape_playstore(app_id)
                if reviews_data:
                    df = pd.DataFrame(reviews_data)
                    kolom_urutan = ["Komentar"] + [col for col in df.columns if col != "Komentar"]
                    df = df[kolom_urutan]
                    st.session_state.scraped_data = df
                    st.session_state.scraped_columns = df.columns
                else:
                    st.session_state.scraped_data = None
                    st.warning("Tidak ada data ditemukan atau terjadi kesalahan.")
            else:
                st.warning("Silakan masukkan ID aplikasi.")

    if st.session_state.scraped_data is not None:
        st.markdown("### 📋 Data yang telah di-scrape:")
        st.dataframe(st.session_state.scraped_data)

        st.markdown("### 📂 Simpan Data")
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
