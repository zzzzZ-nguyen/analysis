import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ==================================================
# 🔮 GLOBAL CUSTOM CSS – MATCH MAIN THEME
# ==================================================
CSS = """
<style>
body {
    background: linear-gradient(180deg, #eef2ff, #fafbff);
    font-family: "Inter", "Segoe UI", sans-serif;
}
.page-title {
    font-size: 34px;
    font-weight: 800;
    background: linear-gradient(45deg, #6c63ff, #9d4edd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-left: 6px;
    margin-bottom: 20px;
}
.card {
    background: #ffffffea;
    padding: 24px;
    border-radius: 18px;
    margin-top: 18px;
    box-shadow:
        4px 4px 16px rgba(0,0,0,0.07),
        -4px -4px 16px rgba(255,255,255,0.6);
    transition: 0.25s ease;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow:
        6px 6px 20px rgba(0,0,0,0.10),
        -6px -6px 20px rgba(255,255,255,0.7);
}
.stButton>button {
    background: linear-gradient(45deg, #6c63ff, #9d4edd) !important;
    color: white !important;
    padding: 0.65rem 1.3rem;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    border: none;
    transition: 0.25s ease;
}
.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(108,99,255,0.45);
}
.stDownloadButton>button {
    background: linear-gradient(45deg, #1d5f89, #3a85b9) !important;
}
textarea {
    border-radius: 12px !important;
    border: 1px solid #d6dafc !important;
}
textarea:focus {
    border: 1px solid #6c63ff !important;
    box-shadow: 0 0 0 1px #6c63ff !important;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ==================================================
# 🧠 LOAD DEMO MODEL
# ==================================================
@st.cache_resource
def load_demo_model():
    texts = [
        "This product is very good",
        "Excellent quality and fast delivery",
        "Bad product, very disappointed",
        "Terrible experience",
        "It is okay, not bad",
        "Average quality",
        "Amazing, I really love it!",
        "Poor build and awful material",
    ]

    labels = ["positive", "positive", "negative", "negative", "neutral", "neutral", "positive", "negative"]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression()
    model.fit(X, labels)

    return model, vectorizer


# ==================================================
# 🎯 MAIN PAGE
# ==================================================
def show():
    st.markdown("<div class='page-title'>🇺🇸 English Sentiment Analysis – AI Engine</div>", unsafe_allow_html=True)
    st.write("Analyze English product reviews using a machine learning sentiment classifier.")

    model, vectorizer = load_demo_model()

    # ==================================================
    # ✏️ INPUT REVIEW CARD
    # ==================================================
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📝 Input Review")

    review = st.text_area(
        "Enter an English product review:",
        height=120,
        placeholder="Example: The product quality is excellent..."
    )

    if st.button("▶️ Analyze Sentiment"):
        if not review.strip():
            st.warning("Please enter a review.")
        else:
            X = vectorizer.transform([review])
            pred = model.predict(X)[0]
            proba = model.predict_proba(X).max()

            st.success(f"**Sentiment: {pred.upper()}**")
            st.info(f"Confidence Score: **{proba:.2f}**")

    st.markdown("</div>", unsafe_allow_html=True)

    # ==================================================
    # 📂 UPLOAD CSV ANALYSIS
    # ==================================================
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📂 Batch Analysis (CSV File)")

    st.caption("CSV must contain a column named **review**")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        try:
            df = pd.read_csv(file)

            if "review" not in df.columns:
                st.error("❌ CSV file must contain a 'review' column.")
                st.markdown("</div>", unsafe_allow_html=True)
                return

            X = vectorizer.transform(df["review"].astype(str))
            df["sentiment"] = model.predict(X)

            st.success(f"Processed {len(df)} reviews.")

            st.dataframe(df, use_container_width=True)

            # ==================================================
            # 📊 BEAUTIFUL DONUT CHART
            # ==================================================
            st.subheader("📊 Sentiment Distribution")

            counts = df["sentiment"].value_counts()
            labels = counts.index
            sizes = counts.values

            fig, ax = plt.subplots(figsize=(4, 4))
            wedges, _ = ax.pie(
                sizes,
                wedgeprops=dict(width=0.4),
                startangle=160,
                autopct="%1.1f%%"
            )
            ax.set(aspect="equal")
            ax.legend(wedges, labels, title="Sentiments", loc="center left")
            st.pyplot(fig)

            # ==================================================
            # ⬇️ DOWNLOAD PROCESSED FILE
            # ==================================================
            st.download_button(
                "⬇️ Download Results (CSV)",
                df.to_csv(index=False),
                "sentiment_results_ENG.csv",
                "text/csv"
            )

        except Exception as e:
            st.error(f"⚠️ Error reading file: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
