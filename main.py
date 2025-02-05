import streamlit as st
import about
import scraping as scraping
import modeling
import preprocesing


st.sidebar.image("sentilab.png", use_container_width=True)
st.sidebar.title("Navigation")


pages = ['About', 'Scraping Komentar', 'Preprocessing', 'Modeling']
selected_page = st.sidebar.selectbox("Menu", pages)

if selected_page == 'About':
    about.show()  

elif selected_page == 'Scraping Komentar':
    scraping.show()  

elif selected_page == 'Preprocessing':
    preprocesing.show()  

elif selected_page == 'Modeling':
    modeling.show()
