import streamlit as st
import pandas as pd
import time

from utils_ui import (
    ai_typing,
    loading_skeleton,
    gauge_chart,
    colored_tag,
    save_history,
    load_custom_css
)

from models import load_english_model, is_vietnamese, vietnamese_sentiment


def show():
    # Load custom CSS
    load_custom_css()

    st.markdown("<h3>Analysis – Sentiment Analysis (VN + ENG) – Enhanced</h3>", unsafe_allow_html=True)

    # Load English model
    model_en, vec_en = load_english_model()

    # Dark mode toggle
    dark = st.toggle("🌙 Dark Mode")
    if dark:
        st.markdown("""
            <style>
                body { background: #1f1f1f !important; color: white !important; }
                .stMarkdown, .stTextInput, textarea { color: white !important; }
            </style>
        """, unsafe_allow_html=True)

    # TEXT REVIEW INPUT
    st.subheader("📝 Input Review")
    review = st.text_area("Enter review:")

    if st.button("▶️ Analyze Sentiment"):
        if not review.strip():
            st.warning("Please enter your review.")
        else:
            # Beautiful loading animation
            loading_skeleton(4)
            time.sleep(1)

            # Auto detect language
            if is_vietnamese(review):
                sentiment, confidence = vietnamese_sentiment(review)
                lang = "Vietnamese"
            else:
                X = vec_en.transform([review])
                sentiment = model_en.predict(X)[0]
                confidence = float(model_en.predict_proba(X).max())
                lang = "English"

            # Save history
            save_history(review, sentiment, confidence)

            # Animated typing AI response
            ai_typing(f"Detected language: **{lang}**")

            # Colored sentiment badge
            st.markdown(colored_tag(sentiment), unsafe_allow_html=True)

            # Gauge meter
            gauge_chart(confidence)

    # HISTORY SECTION
    if "history" in st.session_state:
        st.subheader("📜 History")
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)

        st.download_button(
            "⬇️ Download History CSV",
            df.to_csv(index=False),
            "history.csv"
        )
