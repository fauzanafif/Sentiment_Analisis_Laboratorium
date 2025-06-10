
import streamlit as st
st.cache_data.clear()
import home
import scraping as scraping
import modeling
import preprocesing


st.sidebar.image("sentilab.png")
st.sidebar.title("Navigation")


pages = ['Home', 'Scraping Komentar', 'Preprocessing', 'Modeling']
selected_page = st.sidebar.selectbox("Menu", pages)

if selected_page == 'Home':
    home.show()  

elif selected_page == 'Scraping Komentar':
    scraping.show()  

elif selected_page == 'Preprocessing':
    preprocesing.show()  

elif selected_page == 'Modeling':
    modeling.show()
