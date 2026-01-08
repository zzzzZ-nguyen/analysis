from utils_ui import ai_typing, loading_skeleton, gauge_chart, colored_tag, save_history

def show():
    load_custom_css()

    st.markdown("<h3>Analysis – Sentiment Analysis (VN + ENG) – Enhanced</h3>", unsafe_allow_html=True)

    model_en, vec_en = load_english_model()

    dark = st.toggle("🌙 Dark Mode")
    if dark:
        st.markdown("<style>body{background:#1f1f1f;color:white;}</style>", unsafe_allow_html=True)

    st.subheader("📝 Input Review")
    review = st.text_area("Enter review:")

    if st.button("▶️ Analyze Sentiment"):
        if not review.strip():
            st.warning("Please enter your review.")
        else:
            loading_skeleton(4)
            time.sleep(1)

            if is_vietnamese(review):
                sentiment, confidence = vietnamese_sentiment(review)
                lang = "Vietnamese"
            else:
                X = vec_en.transform([review])
                sentiment = model_en.predict(X)[0]
                confidence = float(model_en.predict_proba(X).max())
                lang = "English"

            save_history(review, sentiment, confidence)

            ai_typing(f"Detected language: **{lang}**")
            st.markdown(colored_tag(sentiment), unsafe_allow_html=True)
            gauge_chart(confidence)

    # Show history same as ENG version
    if "history" in st.session_state:
        st.subheader("📜 History")
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)

        st.download_button("⬇️ Download History CSV", df.to_csv(index=False), "history.csv")
