import nltk
nltk.download('punkt')
nltk.download('stopwords')
import streamlit as st
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

abbreviation_dict = {
    "tdk": "tidak",
    "sy": "saya",
    "dr": "dari",
    "krn": "karena",
    "klo": "kalau",
    "blm": "belum",
    "jg": "juga",
    "utk": "untuk",
}

def replace_abbreviations(text):
    words = text.split()
    replaced_words = [abbreviation_dict[word] if word in abbreviation_dict else word for word in words]
    return " ".join(replaced_words)

def clean_text(text, custom_stopwords, apply_stemming, custom_stems, auto_stopwords, auto_stemming):
    if not isinstance(text, str):
        return ''
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = replace_abbreviations(text)
    words = word_tokenize(text.lower())

    stop_words = set()
    if auto_stopwords:
        stop_words = set(stopwords.words('indonesian'))
    stop_words |= set(custom_stopwords)

    words = [word for word in words if word not in stop_words]

    if auto_stemming:
        words = [stemmer.stem(word) for word in words]
    elif apply_stemming:
        words = [custom_stems.get(word, stemmer.stem(word)) for word in words]

    return " ".join(words)

def clean_column(df, text_column, custom_stopwords, apply_stemming, custom_stems, auto_stopwords, auto_stemming):
    if text_column in df.columns:
        df[text_column] = df[text_column].apply(
            lambda x: clean_text(x, custom_stopwords, apply_stemming, custom_stems, auto_stopwords, auto_stemming) if isinstance(x, str) else ''
        )
    return df

def show():
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

    st.title("✨ Preprocessing Data untuk Analisis Sentimen")
    st.write("Unggah dataset Anda, pilih opsi preprocessing, dan sesuaikan fitur yang diinginkan.")

    uploaded_file = st.file_uploader("📂 Unggah Dataset (CSV)", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if 'df' not in st.session_state:
            st.session_state.df = df

        st.subheader("📊 DATASETS ASLI")
        st.write(st.session_state.df.head())

        st.sidebar.header("⚙️ Modifikasi Dataset")

        columns_to_remove = []
        if st.sidebar.checkbox("Hapus Kolom"):
            columns_to_remove = st.sidebar.multiselect("Pilih kolom untuk dihapus", st.session_state.df.columns.tolist())

        rename_columns = {}
        if st.sidebar.checkbox("Rename Kolom"):
            for col in st.session_state.df.columns:
                new_name = st.sidebar.text_input(f"Nama baru untuk kolom '{col}'", value=col)
                if new_name != col:
                    rename_columns[col] = new_name

        remove_stopwords = st.sidebar.checkbox("Stopword Removal Manual")
        auto_stopwords = st.sidebar.checkbox("Stopword Removal Otomatis")
        custom_stopwords = []

        if remove_stopwords:
            st.sidebar.write("Masukkan stopwords kustom yang ingin dihapus:")
            custom_stopwords_input = st.sidebar.text_area(
                "Stopwords kustom (pisahkan dengan koma)",
                placeholder="contoh: kata1, kata2, kata3"
            )
            custom_stopwords = [word.strip().lower() for word in custom_stopwords_input.split(",") if word.strip()]

        apply_stemming = st.sidebar.checkbox("Stemming Manual")
        auto_stemming = st.sidebar.checkbox("Stemming Otomatis")
        custom_stems = {}

        if apply_stemming:
            st.sidebar.write("Masukkan kata-kata yang ingin di-stem secara kustom:")
            custom_stems_input = st.sidebar.text_area(
                "Kata-kata kustom untuk stemming (pisahkan dengan koma, format: kata_asli:kata_stem)",
                placeholder="contoh: berjalan:berjal, makan:makan"
            )
            if custom_stems_input:
                custom_stems = {item.split(":")[0].strip(): item.split(":")[1].strip() for item in custom_stems_input.split(",") if ":" in item}

        if st.sidebar.button("Jalankan Preprocessing"):

            if columns_to_remove:
                st.session_state.df = st.session_state.df.drop(columns=columns_to_remove)
                st.sidebar.success(f"Kolom '{', '.join(columns_to_remove)}' berhasil dihapus.")
            if rename_columns:
                st.session_state.df.rename(columns=rename_columns, inplace=True)
                st.sidebar.success(f"Kolom berhasil diubah menjadi {rename_columns}.")

            text_column = None
            for col in st.session_state.df.columns:
                if st.session_state.df[col].dtype == 'object': 
                    text_column = col
                    break

            if text_column:
                st.session_state.df[text_column] = st.session_state.df[text_column].apply(
                    lambda x: clean_text(x, custom_stopwords, apply_stemming, custom_stems, auto_stopwords, auto_stemming)
                )

                st.subheader("📊 Dataset Setelah Preprocessing")
                st.write(st.session_state.df.head())

                st.download_button(
                    label="💾 Unduh Dataset yang Telah Diproses",
                    data=st.session_state.df.to_csv(index=False),
                    file_name="processed_data.csv",
                    mime="text/csv"
                )
            else:
                st.error("Tidak ada kolom teks yang ditemukan dalam dataset.")
        else:
            st.info("Klik tombol 'Jalankan Preprocessing' untuk memulai.")
    else:
        st.info("Silakan unggah file CSV terlebih dahulu.")

if __name__ == "__main__":
    show()
