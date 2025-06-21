
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
import numpy as np
import io



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
        st.error(f"Terjadi kesalahan saat memproses file: {e}")
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
        return None, None, None, None

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    return accuracy, precision, recall, f1

def model_quality(accuracy):
    if accuracy < 0.6:
        return "Buruk"
    elif accuracy < 0.7:
        return "Cukup"
    elif accuracy < 0.8:
        return "Baik"
    else:
        return "Sangat Baik"

def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return buf

def show():
    st.title("📊 Dashboard Analisis Sentimen")

    uploaded_file = st.file_uploader("Unggah dataset (CSV, Excel, JSON, TXT)", type=["csv", "xlsx", "json", "txt"])

    if uploaded_file is not None:
        data = load_data(uploaded_file)

        if data is None or 'Komentar' not in data.columns or 'Label' not in data.columns:
            st.error("Dataset harus memiliki kolom 'Komentar' dan 'Label'!")
            return

        data['Komentar'] = data['Komentar'].fillna("")
        X = data['Komentar']
        y = data['Label']

        if 'run_analysis' not in st.session_state:
            st.session_state.run_analysis = False

        if st.button("Jalankan Analisis"):
            st.session_state.run_analysis = True

        if st.session_state.run_analysis:
            with st.spinner("Memproses data..."):
                vectorizer = TfidfVectorizer()
                X_tfidf = vectorizer.fit_transform(X)

                try:
                    X_train, X_test, y_train, y_test = train_test_split(
                        X_tfidf, y, test_size=0.2, random_state=42, stratify=y
                    )
                except ValueError as e:
                    st.error(f"Terjadi kesalahan saat membagi data: {e}")
                    return

                if len(np.unique(y_train)) < 2:
                    st.error("Data pelatihan harus memiliki setidaknya dua kelas. Silakan periksa dataset Anda.")
                    return

                ros = RandomOverSampler(random_state=42)
                try:
                    X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)
                except ValueError as e:
                    st.error(f"Terjadi kesalahan saat melakukan resampling: {e}")
                    return

            model_names = ['Naive Bayes', 'SVM', 'Random Forest', 'AdaBoost', 'KNN']
            metrics = []

            for model_name in model_names:
                with st.spinner(f"Melatih model {model_name}..."):
                    accuracy, precision, recall, f1 = train_model(model_name, X_train_resampled, X_test, y_train_resampled, y_test)
                    if accuracy is not None:
                        metrics.append({
                            'Model': model_name,
                            'Akurasi': accuracy,
                            'Precision': precision,
                            'Recall': recall,
                            'F1-Score': f1,
                            'Kualitas': model_quality(accuracy)
                        })

            st.success("✅ Semua model selesai dievaluasi!")
            metrics_df = pd.DataFrame(metrics)

            col1, col2 = st.columns([3, 3])

            with col1:
                st.subheader("📊 Perbandingan Performa Model")
                st.dataframe(metrics_df, use_container_width=True)

                # Buat Excel dalam buffer
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    metrics_df.to_excel(writer, index=False, sheet_name='Performa Model')

                # Tombol unduh Excel
                st.download_button(
                label="📥 Unduh Tabel Performa Model (Excel)",
                data=excel_buffer.getvalue(),
                file_name="performa_model.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
    )
            with col2:
                st.subheader("☁️ WordCloud Keseluruhan")
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(data['Komentar']))
                fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
                ax_wc.imshow(wordcloud, interpolation='bilinear')
                ax_wc.axis("off")
                st.pyplot(fig_wc, use_container_width=True)

                st.download_button(
                    "📥 Unduh WordCloud",
                    data=fig_to_bytes(fig_wc),
                    file_name="wordcloud_utama.png",
                    mime="image/png",
                    use_container_width=True
                )

            st.markdown("---")
            col3, col4 = st.columns([3, 3])

            with col3:
                st.subheader("📊 Grafik Perbandingan Akurasi Model")
                fig_bar, ax = plt.subplots(figsize=(10, 5))
                sns.barplot(x='Model', y='Akurasi', data=metrics_df, ax=ax, palette='coolwarm', hue='Model', legend=False)
                ax.set_ylim(0, 1)
                st.pyplot(fig_bar, use_container_width=True)

                st.download_button(
                    "📥 Unduh Grafik Model",
                    data=fig_to_bytes(fig_bar),
                    file_name="perbandingan_model.png",
                    mime="image/png",
                    use_container_width=True
                )

            with col4:
                st.subheader("📊 Distribusi Sentimen")
                sentiment_counts = data['Label'].value_counts()
                fig_pie, ax_pie = plt.subplots(figsize=(6, 3))
                ax_pie.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'black'})
                ax_pie.axis('equal')
                st.pyplot(fig_pie, use_container_width=True)

                st.download_button(
                    "📥 Unduh Distribusi Sentimen",
                    data=fig_to_bytes(fig_pie),
                    file_name="distribusi_sentimen.png",
                    mime="image/png",
                    use_container_width=True
                )

            st.markdown("---")
            st.subheader("📌 WordCloud Berdasarkan Sentimen")
            col_pos, col_neg, col_neu = st.columns(3)

            positive_text = ' '.join(data[data['Label'].str.lower() == 'positif']['Komentar'].dropna())
            negative_text = ' '.join(data[data['Label'].str.lower() == 'negatif']['Komentar'].dropna())
            neutral_text = ' '.join(data[data['Label'].str.lower() == 'netral']['Komentar'].dropna())

            with col_pos:
                st.markdown("✅ **Positif**")
                wordcloud_pos = WordCloud(width=400, height=300, background_color='white', colormap='Greens').generate(positive_text)
                fig_pos, ax_pos = plt.subplots()
                ax_pos.imshow(wordcloud_pos, interpolation='bilinear')
                ax_pos.axis("off")
                st.pyplot(fig_pos, use_container_width=True)
                st.download_button("📥 Unduh WordCloud Positif", data=fig_to_bytes(fig_pos), file_name="wordcloud_positif.png", mime="image/png", use_container_width=True)

            with col_neg:
                st.markdown("🚫 **Negatif**")
                wordcloud_neg = WordCloud(width=400, height=300, background_color='white', colormap='Reds').generate(negative_text)
                fig_neg, ax_neg = plt.subplots()
                ax_neg.imshow(wordcloud_neg, interpolation='bilinear')
                ax_neg.axis("off")
                st.pyplot(fig_neg, use_container_width=True)
                st.download_button("📥 Unduh WordCloud Negatif", data=fig_to_bytes(fig_neg), file_name="wordcloud_negatif.png", mime="image/png", use_container_width=True)

            with col_neu:
                st.markdown("💬 **Netral**")
                wordcloud_neu = WordCloud(width=400, height=300, background_color='white', colormap='Blues').generate(neutral_text)
                fig_neu, ax_neu = plt.subplots()
                ax_neu.imshow(wordcloud_neu, interpolation='bilinear')
                ax_neu.axis("off")
                st.pyplot(fig_neu, use_container_width=True)
                st.download_button("📥 Unduh WordCloud Netral", data=fig_to_bytes(fig_neu), file_name="wordcloud_netral.png", mime="image/png", use_container_width=True)

if __name__ == "__main__":
    show()
