import streamlit as st
import pandas as pd
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

abbreviation_dict = {
    # Negasi
    "tdk": "tidak", "gak": "tidak", "ga": "tidak","gk":"tidak","engga":"tidak", "jgn": "jangan", 
    "blm": "belum", "bkn": "bukan", "br":"baru","aja":"saja","bcra":"bicara", "gede":"besar"
    ,"ws":"sudah","sja":"saja","sja":"saja","jwb":"jawab","y":"iya",'nda':"tidak"
    # Kata ganti
    ,"sy": "saya", "aku": "aku", "gw": "gue", "lu": "lo", "sdah":"sudah","koq":" ","wes":"sudah"
    ,"mrk": "mereka", "kmu": "kamu", "kalian": "kalian", "jd":"jadi","gj":"tidak jelas"
    ,"kami": "kami", "kita": "kita", "doi": "dia","sm":"sama","ni":"ini","lu":"kamu","sdh":"sudah"
    # Preposisi & konjungsi
    ,"dr": "dari", "ke": "ke", "di": "di", "pd": "pada", 
    "utk": "untuk", "dg": "dengan", "krn": "karena", 
    "klo": "kalau", "kl": "kalau", "kalo": "kalau", 
    "jika": "jika", "kpd": "kepada", "yg": "yang", 
    "stlh": "setelah", "sblm": "sebelum","quot":" ",
    # Kata umum
    "jg": "juga", "sdh": "sudah", "udh": "sudah", 
    "udah": "sudah", "dpt": "dapat", "bgt": "banget", 
    "skrg": "sekarang", "skrng": "sekarang", 
    "trs": "terus", "trus": "terus", "dlm": "dalam", 
    "org": "orang", "tgl": "tanggal", "tggl": "tanggal", 
    "hr": "hari", "bln": "bulan", "thn": "tahun", 
    "th": "tahun", "sm": "sama", "spt": "seperti", 
    "kyk": "kayak", "kek": "kayak", "aja": "saja", 
    "aj": "saja", "doang": "saja",
    # Pertanyaan
    "ap": "apa", "knp": "kenapa", "kpn": "kapan", 
    "gmn": "gimana", "dmna": "dimana", "dmn": "dimana",
    # Istilah gaul
    "mantul": "mantap betul", "santuy": "santai", 
    "gercep": "gerak cepat", "pcr": "pacar", 
    "bucin": "budak cinta", "gaje": "gak jelas", 
    "mager": "malas gerak", "tbtb": "tiba-tiba", 
    "typo": "salah ketik", "kepo": "ingin tahu",
    "gabut": "gak ada kerjaan", "baper": "bawa perasaan",
    # Ekspresi
    "wkwk": " ", "haha": " ", "lol": "", 
     "duh": "aduh",
    # Tambahan kata kerja
    "ngmg": "ngomong", "bcr": "bicara", "mkn": "makan",
    "mls": "malas", "tdr": "tidur",
    # Istilah online
    "cmiiw": "correct me if I'm wrong", 
    "btw": "by the way", "otw": "on the way",
    "dll": "dan lain-lain", "dsb": "dan sebagainya",
    "afk": "away from keyboard", "asap": "as soon as possible"
}



def replace_abbreviations(text):
    words = text.lower().split()
    replaced = [abbreviation_dict.get(word, word) for word in words]
    return ' '.join(replaced)

def clean_text(text, custom_stopwords, apply_stemming, custom_stems, auto_stopwords, auto_stemming):
    try:
        if not isinstance(text, str):
            return ''
        
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

        emoji_pattern = re.compile("[" 
            u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF" u"\U0001F1E0-\U0001F1FF"
            u"\U00002700-\U000027BF" u"\U0001F900-\U0001F9FF"
            u"\U00002600-\U000026FF" u"\U0000200D"
            u"\U00002300-\U000023FF" u"\U0001FA70-\U0001FAFF"
        "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)

        text = replace_abbreviations(text)
        words = text.lower().split()

        default_stopwords = [
        'nya', 'ya', 'halo','lah','yaa','dih','apaan', 'coba', 'quot', 'sih', 'nih', 'dong', 'kayak', 'banget',
        'liat', 'aja', 'gitu', 'ampun', 'makasih', 'terima', 'kasih', 'bang', 'deh', 'di',
        'dong', 'loh', 'lah', 'nyaa', 'yaa', 'uh', 'wkwk', 'wkwkwk', 'hehe', 'huhu',
        'hehehe', 'hadeh', 'waduh', 'aduh', 'hmm', 'hmmm', 'eh', 'yaudah', 'nggak',
        'ngga', 'ga', 'gak', 'kok', 'padahal', 'doang', 'biar', 'malah', 'jangan',
        'boleh', 'udah', 'sudah', 'baru', 'tuh', 'kan', 'itu', 'ini', 'gini', 'gituan',
        'nanti', 'besok', 'hari', 'mbak', 'mas', 'bro', 'sis', 'woy', 'oi', 'sob',
        'agan', 'gan', 'min', 'admin', 'anda', 'saya', 'aku', 'gue', 'elo', 'loe',
        'lu', 'gua', 'kamu', 'dia', 'kalian', 'mereka', 'kita', 'kami', 'pun', 'toh',
        'lagi', 'terus', 'terusnya', 'terlalu', 'sama', 'yang', 'seperti', 'daripada',
        'atau', 'dan', 'tapi', 'kalau', 'jadi', 'dari', 'buat', 'untuk', 'agar',
        'karena', 'sebab', 'oleh', 'dengan', 'tanpa', 'tentang', 'meskipun', 'namun',
        'bahkan', 'misalnya', 'contohnya', 'dll', 'dst', 'dsb', 'etc', 'ok', 'oke',
        'okay', 'sip', 'mantap', 'nice', 'thanks', 'thank', 'thankyou', 'btw', 'imo',
        'idk', 'cmiiw', 'wfm', 'yoi', 'yuk', 'ayo', 'nah', 'ngapain', 'siapa',
        'dimana', 'kapan', 'kenapa', 'bagaimana', 'hahaha', 'hahahaha', 'lmao', 'lol',
        'wtf', 'astaga', 'astagfirullah', 'inshaallah', 'insyaallah', 'alhamdulillah',
        'masyaallah', 'subhanallah',
        # Kata netral
        'orang', 'presiden', 'prabowo', 'manusia', 'pacar', 'anak', 'laki', 'wanita',
        'hidup', 'tanggung', 'hukum', 'korban', 'bayar', 'tv', 'jeep', 'pinggir',
        # Sosial media umum
        'komen', 'video', 'judul', 'konten', 'caption', 'story', 'stream', 'live',
        'nonton', 'like', 'subscribe', 'share', 'streamer'
    ]

        stop_words = set(default_stopwords + custom_stopwords)
        words = [w for w in words if w not in stop_words]

        if auto_stemming or apply_stemming:
            if apply_stemming:
                words = [custom_stems.get(w, stemmer.stem(w)) for w in words]
            else:
                words = [stemmer.stem(w) for w in words]

        return " ".join(words)

    except Exception as e:
        st.warning(f"⚠️ Gagal membersihkan teks: {e}")
        return ""

def apply_label(text, positive_words, negative_words, threshold=0.1, prefer_dominant=True):
    try:
        words = text.split()
        total = len(words) if len(words) > 0 else 1
        pos = sum(1 for w in words if w in positive_words)
        neg = sum(1 for w in words if w in negative_words)
        pos_score = pos / total
        neg_score = neg / total

        if pos_score - neg_score > threshold:
            return "Positif"
        elif neg_score - pos_score > threshold:
            return "Negatif"
        else:
            if prefer_dominant:
                if pos > neg:
                    return "Positif"
                elif neg > pos:
                    return "Negatif"
            return "Netral"
    except Exception as e:
        st.warning(f"⚠️ Gagal menentukan label: {e}")
        return "Netral"

def load_words_from_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        st.warning(f"📁 File tidak ditemukan: {path}")
        return []
    except Exception as e:
        st.warning(f"⚠️ Gagal memuat file {path}: {e}")
        return []

def show():
    st.title("✨ Preprocessing Data untuk Analisis Sentimen")

    uploaded_file = st.file_uploader("📂 Unggah Dataset (CSV)", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"❌ Gagal membaca file CSV: {e}")
            return

        if 'df' not in st.session_state:
            st.session_state.df = df

        st.subheader("📊 Dataset Asli")
        st.dataframe(st.session_state.df, use_container_width=True, height=500)

        st.sidebar.header("⚙️ Pengaturan Preprocessing")

        try:
            if st.sidebar.checkbox("Hapus Kolom"):
                cols = st.sidebar.multiselect("Pilih kolom", st.session_state.df.columns.tolist())
                st.session_state.df.drop(columns=cols, inplace=True)

            if st.sidebar.checkbox("Rename Kolom"):
                for col in st.session_state.df.columns:
                    new_col = st.sidebar.text_input(f"Rename '{col}'", value=col)
                    if new_col != col:
                        st.session_state.df.rename(columns={col: new_col}, inplace=True)
        except Exception as e:
            st.warning(f"⚠️ Gagal memodifikasi kolom: {e}")

        manual_stop = st.sidebar.checkbox("Stopword Manual")
        auto_stop = st.sidebar.checkbox("Stopword Otomatis")
        custom_stop = []
        if manual_stop:
            stop_input = st.sidebar.text_area("Stopwords (pisahkan dengan koma)", "")
            custom_stop = [w.strip().lower() for w in stop_input.split(",") if w.strip()]

        manual_stem = st.sidebar.checkbox("Stemming Manual")
        auto_stem = st.sidebar.checkbox("Stemming Otomatis")
        custom_stem = {}
        if manual_stem:
            stem_input = st.sidebar.text_area("Custom Stem (kata:stem)", "")
            if stem_input:
                try:
                    custom_stem = {i.split(":")[0].strip(): i.split(":")[1].strip() for i in stem_input.split(",") if ":" in i}
                except Exception as e:
                    st.warning(f"⚠️ Format stem manual salah: {e}")

        st.sidebar.header("📌 Label Sentimen")
        use_auto_dict = st.sidebar.checkbox("Gunakan Kamus Otomatis")
        pos_words = []
        neg_words = []

        if use_auto_dict:
            pos_words = load_words_from_file("assets/positive.txt")
            neg_words = load_words_from_file("assets/negative.txt")

        manual_label = st.sidebar.checkbox("Label Manual")
        if manual_label:
            pos_input = st.sidebar.text_area("Kata-kata Positif (Manual)", "")
            neg_input = st.sidebar.text_area("Kata-kata Negatif (Manual)", "")
            pos_words += [w.strip().lower() for w in pos_input.split(",") if w.strip()]
            neg_words += [w.strip().lower() for w in neg_input.split(",") if w.strip()]

        if st.sidebar.button("🔧 Jalankan Preprocessing"):
            try:
                text_col = None
                for col in st.session_state.df.columns:
                    if st.session_state.df[col].dtype == 'object':
                        text_col = col
                        break

                if text_col:
                    st.session_state.df[text_col] = st.session_state.df[text_col].apply(
                        lambda x: clean_text(x, custom_stop, manual_stem, custom_stem, auto_stop, auto_stem)
                    )

                    if use_auto_dict or manual_label:
                        st.session_state.df["Label"] = st.session_state.df[text_col].apply(
                            lambda x: apply_label(x, pos_words, neg_words)
                        )
                        st.info("Labeling sentimen selesai.")

                    st.session_state.df = st.session_state.df[st.session_state.df[text_col].str.strip() != ""]
                    st.session_state.df.dropna(inplace=True)

                    st.subheader("✅ Dataset Setelah Preprocessing & Labeling")
                    st.dataframe(st.session_state.df, use_container_width=True, height=500)

                    st.download_button(
                        label="💾 Unduh Dataset",
                        data=st.session_state.df.to_csv(index=False),
                        file_name="processed_data.csv",
                        mime="text/csv"
                    )
                else:
                    st.error("❌ Tidak ditemukan kolom teks dalam dataset.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat preprocessing: {e}")

if __name__ == "__main__":
    show()
