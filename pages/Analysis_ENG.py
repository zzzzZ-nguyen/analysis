from utils_ui import ai_typing, loading_skeleton, gauge_chart, colored_tag, save_history

def show():
    st.markdown("<div class='page-title'>🇺🇸 English Sentiment Analysis – AI Enhanced</div>", unsafe_allow_html=True)
    st.write("Analyze English product reviews with animations, gauge meter, and history tracking.")

    model, vectorizer = load_demo_model()

    # Dark mode toggle
    dark = st.toggle("🌙 Dark Mode")
    if dark:
        st.markdown("<style>body{background:#1a1a1a;color:white;}</style>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📝 Input Review")

    review = st.text_area("Enter your review:", height=120)

    if st.button("▶️ Analyze Sentiment"):
        if not review.strip():
            st.warning("Please enter your review.")
        else:
            loading_skeleton(5)
            time.sleep(1.2)

            X = vectorizer.transform([review])
            pred = model.predict(X)[0]
            proba = float(model.predict_proba(X).max())

            save_history(review, pred, proba)

            st.success("Analysis Complete!")
            ai_typing(f"Sentiment detected: **{pred.upper()}**")
            st.markdown(colored_tag(pred), unsafe_allow_html=True)

            st.info(f"Confidence Score: **{proba:.2f}**")
            gauge_chart(proba)

    st.markdown("</div>", unsafe_allow_html=True)

    # ============================
    # 📜 HISTORY LOG
    # ============================
    if "history" in st.session_state and st.session_state.history:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📜 Analysis History")

        df = pd.DataFrame(st.session_state.history)

        df_style = df.style.apply(
            lambda x: ["color:#51cf66" if v=="positive"
                       else "color:#ff6b6b" if v=="negative"
                       else "color:#ffd93d" for v in x],
            subset=["sentiment"]
        )

        st.dataframe(df_style, use_container_width=True)

        st.download_button(
            "⬇️ Download History",
            df.to_csv(index=False),
            "history_sentiment.csv",
            "text/csv"
        )

        st.markdown("</div>", unsafe_allow_html=True)
