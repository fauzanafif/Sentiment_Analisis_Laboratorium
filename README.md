# 🧠 SENTILAB — Sentiment Analysis Laboratory

![SENTILAB](assets/sentilab.png)

**SENTILAB (Sentiment Analysis Laboratory)** adalah aplikasi berbasis web yang digunakan untuk melakukan analisis sentimen secara otomatis menggunakan teknologi **Machine Learning** dan **Natural Language Processing (NLP)**.

Aplikasi ini membantu pengguna melakukan proses pengumpulan data, preprocessing teks, pelatihan model, evaluasi performa, hingga prediksi sentimen dari berbagai sumber data seperti komentar media sosial.

---

## 🚀 Demo Application

🌐 Live Demo:
https://sentilab.streamlit.app/

---

## 📌 Features

### 📥 Data Collection

Mengambil data komentar dari berbagai platform:

* YouTube Comment Scraper
* Twitter / X Scraper
* Google Play Store Review Scraper

### 🧹 Text Preprocessing

Melakukan proses pengolahan teks sebelum masuk ke model:

* Cleaning text
* Case folding
* Tokenization
* Stopword removal
* Stemming Bahasa Indonesia
* Normalisasi teks

### 🤖 Machine Learning Classification

Membandingkan beberapa algoritma Machine Learning:

* Naive Bayes
* Support Vector Machine (SVM)
* K-Nearest Neighbor (KNN)
* Random Forest
* AdaBoost

### 📊 Model Evaluation

Menampilkan hasil evaluasi model:

* Accuracy
* Precision
* Recall
* F1-Score
* Confusion Matrix

### 📈 Visualization

Menyediakan visualisasi data:

* Sentiment distribution
* Word cloud
* Grafik hasil analisis

### 📂 Export Data

Pengguna dapat mengunduh hasil analisis dalam format:

* Excel (.xlsx)
* Dataset hasil preprocessing

---

## 🛠️ Tech Stack

### Programming Language

* Python

### Framework

* Streamlit

### Machine Learning

* Scikit-Learn
* Imbalanced-Learn

### NLP

* Sastrawi
* NLTK

### Data Processing

* Pandas
* NumPy

### Visualization

* Matplotlib
* Seaborn
* WordCloud

---

## 📂 Project Structure

```
Sentiment_Analisis_Laboratorium/

│
├── assets/
│   ├── logo.png
│   ├── positive.txt
│   └── negative.txt
│
├── main.py
├── home.py
├── modeling.py
├── scraping.py
├── preprocessing.py
├── Try_Model.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone repository:

```bash
git clone https://github.com/fauzanafif/Sentiment_Analisis_Laboratorium.git
```

Masuk folder project:

```bash
cd Sentiment_Analisis_Laboratorium
```

Install dependency:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

Jalankan aplikasi:

```bash
streamlit run main.py
```

Kemudian buka:

```
http://localhost:8501
```

---

## 🧪 Workflow System

```
User Input Data
        |
        v
Data Scraping
        |
        v
Text Preprocessing
        |
        v
Feature Extraction (TF-IDF)
        |
        v
Machine Learning Model
        |
        v
Sentiment Prediction
        |
        v
Visualization & Export
```

---

## 🎯 Purpose

Project ini dibuat untuk:

* Mempelajari implementasi NLP menggunakan Machine Learning
* Membantu proses analisis opini pengguna
* Membandingkan performa beberapa algoritma klasifikasi
* Menyediakan platform pembelajaran analisis sentimen berbasis web

---

## 👨‍💻 Developer

**Fauzan Afif**

Machine Learning | Web Developer | IT Solution

GitHub:
https://github.com/fauzanafif

---

## 📄 License

This project is developed for educational and research purposes.
