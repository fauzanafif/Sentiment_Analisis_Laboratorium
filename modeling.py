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
import time

def train_model(model_name, X_train, X_test, y_train, y_test):
    models = {
        'Naive Bayes': MultinomialNB(),
        'SVM': SVC(),
        'Random Forest': RandomForestClassifier(),
        'AdaBoost': AdaBoostClassifier(),
        'KNN': KNeighborsClassifier(),
    }
    
    model = models.get(model_name)
    if model is None:
        st.write("Model tidak didukung")
        return None, None

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    return accuracy, precision, recall, f1, y_pred

def model_quality(accuracy):
    if accuracy < 0.6:
        return "Buruk"
    elif accuracy < 0.7:
        return "Cukup"
    elif accuracy < 0.8:
        return "Baik"
    else:
        return "Sangat Baik"

def show():

    st.markdown("""
        <style>
            .header {
                font-size: 36px;
                font-weight: bold;
                color: #008080;
                text-align: center;
                padding: 20px;
            }
            .subheader {
                font-size: 18px;
                color: #555;
                text-align: center;
                padding: 10px;
            }
            .button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .button:hover {
                background-color: #45a049;
            }
            .card {
                border: 1px solid #ddd;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                background-color: #f9f9f9;
            }
            .metric-table {
                width: 100%;
                margin-top: 20px;
                border-collapse: collapse;
            }
            .metric-table th, .metric-table td {
                text-align: center;
                padding: 12px;
                border: 1px solid #ddd;
            }
            .metric-table th {
                background-color: #4CAF50;
                color: white;
            }
            .container {
                display: flex;
                justify-content: space-between;
                gap: 20px;
                flex-wrap: wrap;
            }
            .card-container {
                width: 48%;
                margin-top: 10px;
            }
            .small-container {
                width: 100%;
                display: inline-block;
                box-sizing: border-box;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
<div class='header'> 
    <h1 style="color: #483D8B; font-family: 'Arial', sans-serif;">
        Analisis Sentimen dengan Berbagai Model
    </h1>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div class='subheader'>Evaluasi beberapa model machine learning untuk klasifikasi sentimen.</div>", unsafe_allow_html=True)

    model_names = [
        "Naive Bayes", 
        "SVM", 
        "Random Forest", 
        "AdaBoost", 
        "KNN"
    ]

    uploaded_file = st.file_uploader("Unggah dataset (CSV, Excel, JSON, TXT)", type=["csv", "xlsx", "json", "txt"])
    
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]

        try:
            if file_extension == 'csv':
                data = pd.read_csv(uploaded_file)
            elif file_extension == 'xlsx':
                data = pd.read_excel(uploaded_file)
            elif file_extension == 'json':
                data = pd.read_json(uploaded_file)
            elif file_extension == 'txt':
                data = pd.read_csv(uploaded_file, sep="\t") 
            else:
                st.error("Format file tidak didukung.")
                return

            st.write("Dataset berhasil diunggah:")
            st.dataframe(data.head())  

            if 'Komentar' in data.columns and 'Label' in data.columns:
                data['Komentar'] = data['Komentar'].fillna("") 

                X = data['Komentar']  
                y = data['Label']  

                if st.button("Cek Akurasi", key="cek_akurasi"):
                    with st.spinner("Memproses data..."):
                        vectorizer = TfidfVectorizer()
                        X_tfidf = vectorizer.fit_transform(X)

                        X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

                        ros = RandomOverSampler(random_state=42)
                        X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)

                    st.success("Data berhasil diproses dan diseimbangkan!")

                    progress_bar = st.progress(0)
                    total_models = len(model_names)
                    metrics = [] 
                    overall_sentiments = pd.Series(dtype='int')  

                    for i, model_name in enumerate(model_names):
                        accuracy, precision, recall, f1, y_pred = train_model(model_name, X_train_resampled, X_test, y_train_resampled, y_test)
                        
                        if accuracy is not None:
                            metrics.append({
                                'Model': model_name,
                                'Akurasi': accuracy,
                                'Precision': precision,
                                'Recall': recall,
                                'F1-Score': f1,
                                'Kualitas': model_quality(accuracy)
                            })
                            
                            overall_sentiments = pd.concat([overall_sentiments, pd.Series(y_pred)], ignore_index=True)

                        progress = (i + 1) / total_models
                        progress_bar.progress(progress)

                        time.sleep(0.5)

                    st.success("Semua model selesai dievaluasi!")

                    if not overall_sentiments.empty:
                        sentiment_counts = overall_sentiments.value_counts()

                        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

                        colors = ['red', 'green', 'yellow']  
                        labels = ['Negative', 'Positive', 'Netral']  

                        ax1.pie(sentiment_counts.values, 
                                labels=sentiment_counts.index, 
                                autopct='%1.1f%%', 
                                startangle=90, 
                                colors=colors[:len(sentiment_counts)],  
                                wedgeprops={'edgecolor': 'black'})  
                        ax1.set_title("Distribusi Prediksi Sentimen (Pie Chart)")

                        sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax2, palette=colors[:len(sentiment_counts)])
                        ax2.set_xlabel("Label Sentimen")
                        ax2.set_ylabel("Jumlah Prediksi")
                        ax2.set_title("Distribusi Prediksi Sentimen (Bar Chart)")

                        st.pyplot(fig)

                    if metrics:
                        metrics_df = pd.DataFrame(metrics)
                        st.markdown("<div class='card'><h3>Ringkasan Metrik Model</h3></div>", unsafe_allow_html=True)
                        st.dataframe(metrics_df)
                        
            else:
                st.error("Dataset harus memiliki kolom 'Komentar' dan 'Label'.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses file: {e}")
    else:
        st.warning("Silakan unggah dataset.")

if __name__ == "__main__":
    show()
