import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import RandomOverSampler

st.set_page_config(page_title="Dashboard Analisis Sentimen", layout="wide")

def train_model(model_name, X_train, X_test, y_train, y_test):
    models = {
        'Naive Bayes': MultinomialNB(),
        'SVM': SVC(probability=True),
        'Random Forest': RandomForestClassifier(),
        'AdaBoost': AdaBoostClassifier(),
        'KNN': KNeighborsClassifier(),
    }

    model = models.get(model_name)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    return accuracy, precision, recall, f1, y_pred

def display_header():
    st.markdown("""
        <div style="text-align: center; padding: 15px; background-color: #4CAF50; border-radius: 10px;">
            <h1 style="color: white;">Dashboard Analisis Sentimen</h1>
            <p style="color: white;">Evaluasi berbagai model machine learning untuk analisis sentimen</p>
        </div>
    """, unsafe_allow_html=True)

def show():
    display_header()

    with st.sidebar:
        st.title("Navigasi")
        st.markdown("Pilih model dan parameter:")
        selected_model = st.selectbox("Pilih Model", ["Naive Bayes", "SVM", "Random Forest", "AdaBoost", "KNN"])
        test_size = st.slider("Ukuran Data Uji (%)", 10, 50, 20)

    uploaded_file = st.file_uploader("Unggah dataset (CSV, Excel, JSON)", type=["csv", "xlsx", "json"])

    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1]

        if file_extension == "csv":
            data = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            data = pd.read_excel(uploaded_file)
        elif file_extension == "json":
            data = pd.read_json(uploaded_file)
        else:
            st.error("Format file tidak didukung.")
            return

        if 'Komentar' in data.columns and 'Label' in data.columns:
            st.success("Dataset berhasil diunggah!")

            with st.expander("Pratinjau Dataset"):
                st.write(data.head())

            X = data['Komentar'].fillna("")
            y = data['Label']
            vectorizer = TfidfVectorizer()
            X_tfidf = vectorizer.fit_transform(X)

            X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=test_size / 100, random_state=42)
            ros = RandomOverSampler(random_state=42)
            X_train, y_train = ros.fit_resample(X_train, y_train)

            if st.button("Latih Model"):
                with st.spinner("Melatih model..."):
                    accuracy, precision, recall, f1, y_pred = train_model(selected_model, X_train, X_test, y_train, y_test)

                st.success("Model selesai dilatih!")
                st.markdown(f"### Hasil Evaluasi Model: {selected_model}")
                metrics = {
                    "Akurasi": accuracy,
                    "Precision": precision,
                    "Recall": recall,
                    "F1-Score": f1
                }


                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Akurasi", f"{accuracy:.2%}")
                col2.metric("Precision", f"{precision:.2%}")
                col3.metric("Recall", f"{recall:.2%}")
                col4.metric("F1-Score", f"{f1:.2%}")

                sentiment_counts = pd.Series(y_pred).value_counts()
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax, palette="viridis")
                ax.set_title("Distribusi Prediksi Sentimen")
                ax.set_xlabel("Label")
                ax.set_ylabel("Jumlah")
                st.pyplot(fig)

        else:
            st.error("Dataset harus memiliki kolom 'Komentar' dan 'Label'.")

if __name__ == "__main__":
    show()
