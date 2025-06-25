import streamlit as st
from PIL import Image

st.set_page_config(page_title="SENTILAB", layout="wide")

def show():
    logo = Image.open("assets/sentilab.png")

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .hover-box {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .hover-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }

    .hover-button {
        padding: 10px 30px;
        font-size: 18px;
        cursor: pointer;
        border: none;
        background-color: #2196F3;
        color: white;
        border-radius: 5px;
        font-weight: bold;
        transition: background-color 0.3s ease, transform 0.2s ease;
        text-decoration: none;
        display: inline-block;
    }

    .hover-button:hover {
        background-color: #1769aa !important;
        transform: scale(1.05);
    }

    .centered {
        text-align: center;
        margin: 30px 0;
    }

    button:focus {
        outline: none;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
    """
    <div style="text-align: center; background-color: #483D8B; padding: 10px; border-radius: 11px;">
        <div style="margin-top: 10px;">
            <h1 style="color: white; font-size: 36px;">SENTILAB</h1>
            <p style="color: white; font-size: 20px;">( SENTIMEN ANALISIS LABORATORIUM )</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <h1 style="color: #483D8B;">Selamat datang di SENTILAB.!</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align: center; font-size: 18px; line-height: 1.6; margin: 20px;">
            " Selamat datang di website kami! Web ini dirancang untuk memudahkan pengguna dalam
            melakukan tugas-tugas berkaitan dengan analisis sentimen dengan antarmuka yang sederhana dan efisien.
            Kami berfokus untuk memberikan pengalaman terbaik dengan fitur-fitur yang mumpuni
            namun mudah digunakan oleh siapapun yang membutuhkan tanpa Ngoding sama sekali. "
        </div>
        """, unsafe_allow_html=True)

    st.video("https://www.youtube.com/watch?v=xV3VIYpyZPg")

    st.markdown(
    """
    <div class="centered">
        <a href="https://drive.google.com/uc?export=download&id=1ORUuDsWnO6bRjGdz7g4SerTAszHcNPWa" target="_blank" class="hover-button" 
           style="padding: 10px 20px; background-color: #2196F3; color: white; border: none; border-radius: 5px; text-decoration: none; font-weight: bold;">
            📄 Unduh Panduan PDF
        </a>
    </div>
    """,
    unsafe_allow_html=True
)



    st.markdown(
    """
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-top: 30px;">
        <div class="hover-box" style="flex: 1; min-width: 300px; max-width: 400px; background-color: #483D8B; padding: 20px; border-radius: 10px; text-align: center;">
            <h3 style="color: white;">SCRAPING MUDAH</h3>
            <p style="color: white;">Scraping komentar untuk mendapatkan data dengan mudah dari platform seperti YouTube, X (Twitter), Play Store</p>
        </div>
        <div class="hover-box" style="flex: 1; min-width: 300px; max-width: 400px; background-color: #483D8B; padding: 20px; border-radius: 10px; text-align: center;">
            <h3 style="color: white;">PREPROCESSING MUDAH</h3>
            <p style="color: white;">Preprocessing data lebih mudah dan cepat, dilengkapi fitur otomatis dan manual untuk kemudahan dan kedetailan pengguna</p>
         </div>
        <div class="hover-box" style="flex: 1; min-width: 300px; max-width: 400px; background-color: #483D8B; padding: 20px; border-radius: 10px; text-align: center;">
            <h3 style="color: white;">MODELING MUDAH</h3>
            <p style="color: white;">Modeling cepat dengan 5 model populer: Naive Bayes, SVM, KNN, Random Forest, Adaboost</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
