import streamlit as st
from PIL import Image

st.set_page_config(page_title="SENTILAB", layout="wide")

def show():

    logo = Image.open("assets/sentilab.png")
    st.markdown(
    """
    <div style="text-align: center; background-color: #483D8B; padding: 10px; border-radius: 11px;">
        <div style="margin-top: 10px;">
            <h1 style="color: white; font-size: 36px;">SENTILAB</h1>
            <p style="color: white; font-size: 20px;">( SENTIMEN ANALISIS LABORATORIUM )</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <h1 style="color: #483D8B; font-family: 'Arial', sans-serif;">Selamat datang di SENTILAB.!</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div style="text-align: center; font-size: 18px; line-height: 1.6; margin: 20px;">
            " Selamat datang di website kami! Web  ini dirancang untuk memudahkan pengguna dalam
            melakukan tugas-tugas berkaitan dengan analisis sentimen dengan antarmuka yang sederhana dan efisien.
            Kami berfokus untuk memberikan pengalaman terbaik dengan fitur-fitur yang mumpuni
            namun mudah digunakan oleh siapapun "
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div style="text-align: center; margin: 20px 0;">
            <iframe src="https://www.youtube.com/embed/X9g_89SA9Bo" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen style="border: 5px solid #483D8B; border-radius: 10px; width: 100%; max-width: 660px; height: auto; aspect-ratio: 16/9;"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align: center; margin: 20px 0;">
            <button style="padding: 10px 30px; font-size: 18px; cursor: pointer; border: none; background-color: #2196F3; color: white; border-radius: 5px; font-weight: bold;" 
                    onclick="window.alert('Tutorial akan segera tersedia. Pantau terus update kami!')">
                Panduan PDF
            </button>
        </div>
        """,
        unsafe_allow_html=True
    )

    # st.markdown(
    #     """
    #     <div style="margin: 20px; font-size: 18px;">
    #         <h2 style="color: #483D8B;">Beri Masukan</h2>
    #         Kami sangat menghargai feedback dari pengguna untuk terus meningkatkan kualitas aplikasi.
    #         Jika Anda memiliki saran atau masukan, jangan ragu untuk memberitahu kami.
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )

    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <a href="https://www.example.com" target="_blank" style="font-size: 18px; color: white; background-color: #483D8B; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Keunggulan SENTILAB</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-top: 30px;">
            <div style="flex: 1; min-width: 300px; max-width: 400px; background-color: #483D8B; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <h3>EASY SCRAPING</h3>
                <p>Scraping komentar dengan mudah dengan berbagai platform seperti youtube, X (Tweeter), Playstore</p>
                <a href="Scraping\scraping.py" style="color: white; text-decoration: underline;">Baca Selengkapnya</a>
            </div>
            <div style="flex: 1; min-width: 300px; max-width: 400px; background-color: #483D8B; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <h3>EASY PREPROCESING</h3>
                <p>Preprocesing data lebih mudah dan cepat</p>
                <a href="preprocesing.py" style="color: white; text-decoration: underline;">Baca Selengkapnya</a>
            </div>
            <div style="flex: 1; min-width: 300px; max-width: 400px; background-color: #483D8B; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <h3>EASY MODELING</h3>
                <p>Modeling dengan cepat menggunakan 5 model terpopuler yaitu Naive Bayes, SVM (Support Vector Mechine), KNN, Rndiom Forest, Adaboost</p>
                <a href="modeling.py" style="color: white; text-decoration: underline;">Baca Selengkapnya</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

