import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ============================
#       CUSTOM CSS
# ============================
CSS = """
<style>
/* GLOBAL */
body {
    background: #f5f7fa;
    font-family: "Segoe UI", sans-serif;
}

/* Title Decoration */
.page-title {
    font-size: 32px !important;
    font-weight: 700;
    color: #2b6f3e;
    border-left: 6px solid #2b6f3e;
    padding-left: 12px;
    margin-bottom: 20px;
}

/* CARD STYLE */
.card {
    background: white;
    padding: 22px;
    border-radius: 12px;
    margin-top: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    transition: 0.2s ease;
}
.card:hover {
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #33cc77, #22884f);
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 10px;
    font-size: 17px;
    font-weight: 600;
    transition: 0.2s ease;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #2dbd6e, #1f7a45);
    transform: scale(1.03);
}

/* TEXTAREA */
textarea {
    border-radius: 10px !important;
}

/* File uploader */
.css-1p0rl0g {
    border-radius: 10px !important;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ============================
#      LOAD DEMO MODEL
# ============================
@st.cache_resource
def load_demo_model():
    texts = [
        "This product is very good",
        "Excellent quality and fast delivery",
        "Bad product, very disappointed",
        "Terrible experience",
        "It is okay, not bad",
        "Average quality"
    ]
    labels = ["positive", "positive", "negative", "negative", "neutral", "neutral"]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression()
    model.fit(X, labels)

    return model, vectorizer


# ============================
#        MAIN PAGE
# ============================
def show():
    st.markdown("<div class='page-title'>Analysis – Sentiment Analysis</div>", unsafe_allow_html=True)
    st.write("Analyze product reviews and classify sentiment using AI sentiment prediction.")

    model, vectorizer = load_demo_model()

    # ============================
    #   TEXT INPUT CARD
    # ============================
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader("📝 Input Product Review")
        review = st.text_area(
            "Enter a product review (Vietnamese or English):",
            height=120
        )

        if st.button("▶️ Analyze Sentiment"):
            X = vectorizer.transform([review])
            pred = model.predict(X)[0]
            proba = model.predict_proba(X).max()

            st.success(f"Predicted Sentiment: **{pred.upper()}**")
            st.info(f"Confidence: **{proba:.2f}**")

        st.markdown("</div>", unsafe_allow_html=True)

    # ============================
    #   CSV UPLOAD CARD
    # ============================
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📂 Upload Reviews Dataset (CSV)")
    file = st.file_uploader("CSV with column: review", type=["csv"])

    if file:
        df = pd.read_csv(file)

        X = vectorizer.transform(df["review"])
        df["sentiment"] = model.predict(X)

        st.dataframe(df.head())

        st.subheader("📊 Sentiment Distribution")
        fig, ax = plt.subplots()
        df["sentiment"].value_counts().plot(
            kind="bar", ax=ax, color=["green", "gray", "red"]
        )
        st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)
