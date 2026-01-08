import streamlit as st
import pandas as pd
import re
import os
import joblib
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# ==================================================
# 🎨 PREMIUM GLOBAL UI CSS
# ==================================================
def load_custom_css():
    st.markdown("""
        <style>

        /* Remove menu and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Global font + background */
        body, textarea, input {
            font-family: "Segoe UI", Roboto, sans-serif !important;
        }
        .main {
            background-color: #f5f6f4 !important;
        }

        /* Title */
        h3 {
            font-weight: 700 !important;
            color: #2b6f3e !important;
        }

        /* Textarea */
        textarea {
            border-radius: 12px !important;
            border: 1px solid #cbd5c0 !important;
            padding: 12px !important;
            font-size: 16px !important;
        }
        textarea:focus {
            border: 1px solid #2b6f3e !important;
            box-shadow: 0 0 0 1px #2b6f3e !important;
        }

        /* Buttons */
        .stButton>button {
            background: #2b6f3e !important;
            color: #fff !important;
            border-radius: 10px !important;
            padding: 10px 22px !important;
            font-size: 16px !important;
            border: none !important;
            transition: 0.25s !important;
        }
        .stButton>button:hover {
            background: #245c33 !important;
            transform: translateY(-2px);
        }

        .stDownloadButton>button {
            background: #1d5f89 !important;
            color: #fff !important;
            border-radius: 10px !important;
            padding: 10px 22px !important;
            font-size: 16px !important;
            border: none !important;
            transition: 0.25s !important;
        }
        .stDownloadButton>button:hover {
            background: #174a6a !important;
            transform: translateY(-2px);
        }

        /* File uploader */
        .uploadedFile {
            border-radius: 10px !important;
            background: #e8f0e3 !important;
        }

        /* Dataframe box */
        .stDataFrame {
            border-radius: 12px;
            box-shadow: 0 3px 8px rgba(0,0,0,0.08);
        }

        /* Chart */
        .element-container svg {
            border-radius: 12px !important;
        }

        </style>
    """, unsafe_allow_html=True)


# ==================================================
# 🔍 Improved Language Detection
# ==================================================
VI_CHARS = r"àáạảãâầấậẩẫăằắặẳẵđêềếệểễôồốộổỗơờớợởỡưừứựửữíìịỉĩúùụủũýỳỵỷỹ"

def is_vietnamese(text: str) -> bool:
    if re.search(f"[{VI_CHARS}]", text.lower()):
        return True
    english_hint = r"\b(the|this|that|is|are|was|were|good|bad)\b"
    return not bool(re.search(english_hint, text.lower()))


# ==================================================
# 🇻🇳 Vietnamese Sentiment (Improved Rule-Based)
# ==================================================
VI_POS = [
    "tốt", "tuyệt", "xuất sắc", "hài lòng",
    "ưng ý", "đẹp", "ngon", "hoàn hảo",
    "ổn", "ok", "rất thích"
]

VI_NEG = [
    "tệ", "xấu", "kém", "thất vọng", "dở",
    "lỗi", "tồi", "không tốt", "không hài lòng",
    "quá tệ", "kinh khủng", "hỏng", "rất tệ"
]

def vietnamese_sentiment(text: str):
    score = 0
    t = text.lower()
    for w in VI_POS:
        if w in t: score += 1
    for w in VI_NEG:
        if w in t: score -= 1

    if score > 0:
        return "positive", min(0.65 + score * 0.08, 0.97)
    if score < 0:
        return "negative", min(0.65 + abs(score) * 0.08, 0.97)
    return "neutral", 0.55


# ==================================================
# 🇺🇸 English Sentiment Model
# ==================================================
@st.cache_resource
def load_english_model():
    model_path = "models/en_sentiment_model.joblib"
    vec_path = "models/en_vectorizer.joblib"

    if os.path.exists(model_path) and os.path.exists(vec_path):
        return joblib.load(model_path), joblib.load(vec_path)

    texts = [
        "This product is very good", "Excellent quality and fast delivery",
        "Amazing experience, I love it", "Absolutely perfect",
        "Bad product, very disappointed", "Terrible quality",
        "It is okay, not bad", "Average quality", "Nothing special",
    ]
    labels = ["positive", "positive", "positive", "positive",
              "negative", "negative", "neutral", "neutral", "neutral"]

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=500)
    model.fit(X, labels)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)

    return model, vectorizer


# ==================================================
# 🎯 MAIN PAGE
# ==================================================
def show():
    load_custom_css()

    st.markdown(
        "<h3>Analysis – Sentiment Analysis (Vietnamese & English)</h3>",
        unsafe_allow_html=True
    )

    st.write("Analyze product reviews using machine learning + rule-based hybrid sentiment analysis.")

    model_en, vec_en = load_english_model()

    # ---------------- Input box ----------------
    st.subheader("📝 Input Product Review")
    review = st.text_area(
        "Enter a product review (Vietnamese or English):",
        height=120,
        placeholder="Ví dụ: Sản phẩm tốt / This product is excellent"
    )

    if st.button("▶️ Analyze Sentiment"):
        if not review.strip():
            st.warning("Please enter a review.")
        else:
            if is_vietnamese(review):
                sentiment, confidence = vietnamese_sentiment(review)
                lang = "Vietnamese"
            else:
                X = vec_en.transform([review])
                sentiment = model_en.predict(X)[0]
                confidence = model_en.predict_proba(X).max()
                lang = "English"

            st.success(f"Sentiment: **{sentiment.upper()}**")
            st.info(f"Confidence: **{confidence:.2f}**")
            st.caption(f"Language detected: {lang}")

    # ---------------- Batch file processing ----------------
    st.write("---")
    st.subheader("📂 Upload Reviews Dataset (CSV / TXT / DOCX)")
    st.caption("CSV: column `review` | TXT: each line | DOCX: each paragraph")

    file = st.file_uploader("Upload file", type=["csv", "txt", "docx"])

    if file:
        reviews = []

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
            if "review" not in df.columns:
                st.error("CSV must contain a column named 'review'.")
                return
            reviews = df["review"].astype(str).tolist()

        elif file.name.endswith(".txt"):
            text = file.read().decode("utf-8")
            reviews = [l.strip() for l in text.splitlines() if l.strip()]

        elif file.name.endswith(".docx"):
            doc = Document(file)
            reviews = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

        sentiments, confidences = [], []

        for r in reviews:
            if is_vietnamese(r):
                s, c = vietnamese_sentiment(r)
            else:
                X = vec_en.transform([r])
                s = model_en.predict(X)[0]
                c = model_en.predict_proba(X).max()

            sentiments.append(s)
            confidences.append(round(c, 3))

        result = pd.DataFrame({
            "review": reviews,
            "sentiment": sentiments,
            "confidence": confidences
        })

        st.success(f"Processed {len(result)} reviews.")
        st.dataframe(result, use_container_width=True)

        st.subheader("📊 Sentiment Distribution")
        st.bar_chart(result["sentiment"].value_counts())

        st.download_button(
            "⬇️ Download result (CSV)",
            result.to_csv(index=False),
            "sentiment_results.csv",
            "text/csv"
        )
