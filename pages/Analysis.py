# ================================================================
# 🌟 ANALYSIS PAGE – SENTIMENT ANALYZER PRO
# Modern UI • Dual Language • Batch Processing
# ================================================================

import streamlit as st
import pandas as pd
import re
import os
import joblib
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# ================================================================
# 🎨 LOAD CUSTOM CSS – PREMIUM UI
# ================================================================
def load_custom_css():
    st.markdown("""
        <style>

        /* Hide Streamlit default menu/footer */
        #MainMenu, footer {visibility: hidden;}

        body {font-family: "Segoe UI", Roboto, sans-serif;}

        /* Smooth fade */
        .fade-in {
            animation: fadein 0.8s ease-in-out;
        }
        @keyframes fadein {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Section Title */
        .section-title {
            font-size: 24px;
            font-weight: 800;
            color: #1f4c2f;
            padding-bottom: 6px;
        }

        /* Result Card */
        .result-card {
            border-radius: 14px;
            padding: 18px 22px;
            margin-top: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }

        .positive {
            border-left: 8px solid #2ecc71;
            background: #eafaf1;
        }
        .negative {
            border-left: 8px solid #e74c3c;
            background: #fdecea;
        }
        .neutral {
            border-left: 8px solid #7f8c8d;
            background: #f2f4f5;
        }

        .result-label {
            font-size: 20px;
            font-weight: 700;
        }
        .result-confidence {
            font-size: 16px;
            opacity: 0.8;
        }

        /* Upload Box */
        .upload-card {
            border-radius: 12px;
            padding: 15px;
            background: #f5f7f6;
        }

        </style>
    """, unsafe_allow_html=True)


# ================================================================
# 🔍 Improved Vietnamese Language Detection
# ================================================================
VI_CHARS = r"àáạảãâầấậẩẫăằắặẳẵđêềếệểễôồốộổỗơờớợởỡưừứựửữíìịỉĩúùụủũýỳỵỷỹ"

def is_vietnamese(text: str) -> bool:
    if re.search(f"[{VI_CHARS}]", text.lower()):
        return True

    # English pattern detection
    english_hint = r"\b(the|this|that|is|are|was|were|good|bad|quality|product)\b"
    if re.search(english_hint, text.lower()):
        return False

    return True


# ================================================================
# 🇻🇳 Vietnamese Sentiment (Improved Lexicon-Based)
# ================================================================
VI_POS = ["tốt", "tuyệt", "xuất sắc", "hài lòng", "ưng ý", "đẹp", "ngon", "hoàn hảo"]
VI_NEG = ["tệ", "xấu", "kém", "thất vọng", "dở", "lỗi", "tồi", "quá tệ", "kinh khủng"]


def vietnamese_sentiment(text: str):
    score = 0
    t = text.lower()

    for w in VI_POS:
        if w in t: score += 1
    for w in VI_NEG:
        if w in t: score -= 1

    if score > 0:
        return "positive", min(0.70 + score * 0.07, 0.98)
    if score < 0:
        return "negative", min(0.70 + abs(score) * 0.07, 0.98)
    return "neutral", 0.55


# ================================================================
# 🇺🇸 English ML Model
# ================================================================
@st.cache_resource
def load_english_model():
    model_path = "models/en_sentiment_model.joblib"
    vec_path = "models/en_vectorizer.joblib"

    if os.path.exists(model_path) and os.path.exists(vec_path):
        return joblib.load(model_path), joblib.load(vec_path)

    # Fallback tiny dataset
    texts = [
        "This product is very good", "Excellent quality", "Amazing experience",
        "Bad product", "Terrible quality", "Very poor", "It is okay"
    ]
    labels = ["positive", "positive", "positive", "negative", "negative", "negative", "neutral"]

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=500)
    model.fit(X, labels)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)

    return model, vectorizer


# ================================================================
# 🎯 MAIN PAGE VIEW
# ================================================================
def show():
    load_custom_css()

    st.markdown("<div class='section-title fade-in'>📈 Sentiment Analysis</div>", unsafe_allow_html=True)
    st.write("Analyze customer reviews in **Vietnamese or English** using AI + rule-based hybrid model.")

    model_en, vec_en = load_english_model()

    # ============================================================
    # 📝 SINGLE TEXT ANALYSIS
    # ============================================================
    st.subheader("📝 Analyze a Single Review")
    review = st.text_area(
        "",
        height=110,
        placeholder="Nhập đánh giá sản phẩm... | Example: This product is excellent"
    )

    if st.button("▶️ Analyze", use_container_width=True):
        if not review.strip():
            st.warning("⚠️ Please enter some text.")
        else:
            with st.spinner("🔍 Analyzing..."):
                if is_vietnamese(review):
                    sentiment, confidence = vietnamese_sentiment(review)
                else:
                    X = vec_en.transform([review])
                    sentiment = model_en.predict(X)[0]
                    confidence = model_en.predict_proba(X).max()

            # UI result card
            st.markdown(
                f"""
                <div class="result-card fade-in {sentiment}">
                    <div class="result-label">Sentiment: {sentiment.upper()}</div>
                    <div class="result-confidence">Confidence: {confidence:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ============================================================
    # 📂 BATCH ANALYSIS
    # ============================================================
    st.markdown("<br><div class='section-title'>📂 Batch File Processing</div>", unsafe_allow_html=True)
    st.caption("Upload TXT / CSV / DOCX file for batch sentiment analysis")

    file = st.file_uploader("Upload your dataset:", type=["txt", "csv", "docx"])

    if file:
        container = st.container()
        with container:
            st.markdown("<div class='upload-card fade-in'>", unsafe_allow_html=True)

            reviews = []

            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
                if "review" not in df.columns:
                    st.error("CSV must include a column named 'review'")
                    return
                reviews = df["review"].astype(str).tolist()

            elif file.name.endswith(".txt"):
                reviews = file.read().decode("utf-8").splitlines()

            elif file.name.endswith(".docx"):
                doc = Document(file)
                reviews = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

            sentiments = []
            confidences = []

            with st.spinner("Processing reviews..."):
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

            st.success("🎉 File processed successfully!")
            st.dataframe(result, use_container_width=True)

            st.subheader("📊 Sentiment Distribution")
            st.bar_chart(result["sentiment"].value_counts())

            st.download_button(
                "⬇️ Download CSV",
                result.to_csv(index=False),
                "sentiment_results.csv",
                "text/csv",
                use_container_width=True
            )

            st.markdown("</div>", unsafe_allow_html=True)
