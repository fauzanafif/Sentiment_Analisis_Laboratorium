import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import RandomOverSampler

@st.cache_data
def load_data(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1]
    try:
        if file_extension == 'csv':
            return pd.read_csv(uploaded_file)
        elif file_extension == 'xlsx':
            return pd.read_excel(uploaded_file)
        elif file_extension == 'json':
            return pd.read_json(uploaded_file)
        elif file_extension == 'txt':
            return pd.read_csv(uploaded_file, sep="\t")
        else:
            return None
    except Exception as e:
        st.error(f"Error processing the file: {e}")
        return None

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
    st.title("📊 Dashboard Analisis Sentimen")
    
    uploaded_file = st.file_uploader("Unggah dataset (CSV, Excel, JSON, TXT)", type=["csv", "xlsx", "json", "txt"])
    
    if uploaded_file is not None:
        if 'data' not in st.session_state:
            st.session_state.data = load_data(uploaded_file)

        data = st.session_state.data
        if data is not None and 'Komentar' in data.columns and 'Label' in data.columns:
            data['Komentar'] = data['Komentar'].fillna("") 
            X = data['Komentar']  
            y = data['Label']  

            if 'run_analysis' not in st.session_state:
                st.session_state.run_analysis = False

            if st.button("Jalankan Analisis", key="cek_akurasi"):
                st.session_state.run_analysis = True

            if st.session_state.run_analysis:
                with st.spinner("Memproses data..."):
                    vectorizer = TfidfVectorizer()
                    X_tfidf = vectorizer.fit_transform(X)
                    X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)
                    ros = RandomOverSampler(random_state=42)
                    X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)
                
                model_names = ['Naive Bayes', 'SVM', 'Random Forest', 'AdaBoost', 'KNN']
                metrics = []
                
                for model_name in model_names:
                    with st.spinner(f"Melatih model {model_name}..."):
                        accuracy, precision, recall, f1, _ = train_model(model_name, X_train_resampled, X_test, y_train_resampled, y_test)
                        if accuracy is not None:
                            metrics.append({
                                'Model': model_name,
                                'Akurasi': accuracy,
                                'Precision': precision,
                                'Recall': recall,
                                'F1-Score': f1,
                                'Kualitas': model_quality(accuracy)
                            })
                
                st.success("Semua model selesai dievaluasi!")
                metrics_df = pd.DataFrame(metrics)
                
                col1, col2 = st.columns([2, 2])
                
                with col1:
                    st.subheader("📊 Perbandingan Performa Model")
                    st.dataframe(metrics_df)
                
                with col2:
                    st.subheader("📊 Visualisasi WordCloud")
                    wordcloud = WordCloud(width=400, height=170, background_color='white').generate(' '.join(data['Komentar']))
                    fig_wc, ax_wc = plt.subplots(figsize=(5, 2.5))
                    ax_wc.imshow(wordcloud, interpolation='bilinear')
                    ax_wc.axis("off")
                    st.pyplot(fig_wc)
                
                col3, col4 = st.columns([2, 2])
                
                with col3:
                    st.subheader("📊 Visualisasi Perbandingan Model")
                    fig, ax = plt.subplots(figsize=(5, 3))
                    sns.barplot(x='Model', y='Akurasi', data=metrics_df, ax=ax, palette='coolwarm')
                    ax.set_ylim(0, 1)
                    ax.tick_params(axis='x', labelsize=8)
                    st.pyplot(fig)
                
                with col4:
                    st.subheader("📊 Distribusi Sentimen")
                    color_mapping = {
                        'Positif': 'green',
                        'Negatif': 'red',
                        'Netral': 'gray'
                    }
                    
                    sentiment_counts = data['Label'].str.strip().str.capitalize().value_counts()
                    colors = [color_mapping.get(label, 'blue') for label in sentiment_counts.index]
                    
                    fig_pie, ax_pie = plt.subplots(figsize=(5, 3))
                    wedges, texts, autotexts = ax_pie.pie(
                        sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=colors,
                        startangle=140, wedgeprops={'edgecolor': 'black'}
                    )
                    
                    for text in texts + autotexts:
                        text.set_fontsize(8)
                    
                    st.pyplot(fig_pie)

if __name__ == "__main__":
    show()
