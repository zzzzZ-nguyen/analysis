import streamlit as st
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from pathlib import Path
import time
import matplotlib.pyplot as plt

def show():
    st.markdown("## ⚙️ Model Training – PRO Dashboard")

    data_dir = Path("data")
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)

    # =============================
    # Load dataset
    # =============================
    st.subheader("📂 Load Training Dataset")

    files = list(data_dir.glob("*.*"))

    if not files:
        st.error("❌ No dataset in /data. Please upload files.")
        return

    file_selected = st.selectbox(
        "Choose dataset file:",
        files,
        format_func=lambda x: x.name
    )

    ext = file_selected.suffix.lower()

    try:
        if ext == ".csv":
            df = pd.read_csv(file_selected)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file_selected)
        elif ext == ".txt":
            df = pd.read_csv(file_selected, sep="\n", header=None, names=["text"])
        else:
            st.error("❌ Unsupported file format.")
            return
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return

    st.success("📄 Dataset loaded successfully!")
    st.dataframe(df.head(), use_container_width=True)

    # =============================
    # Column selection
    # =============================
    st.subheader("🧩 Select Columns")

    text_col = st.selectbox("Text column:", df.columns)
    label_col = st.selectbox("Label column:", df.columns)

    # =============================
    # Select model type
    # =============================
    st.subheader("🤖 Choose Machine Learning Model")

    algo = st.radio(
        "Algorithm:",
        [
            "Logistic Regression",
            "Support Vector Machine (SVM)",
            "Naive Bayes"
        ]
    )

    # =============================
    # Train button
    # =============================
    if st.button("🚀 Train Model"):
        if text_col == label_col:
            st.error("Text column and label column must be different!")
            return

        X = df[text_col].astype(str)
        y = df[label_col]

        with st.status("🔍 Training model, please wait...", expanded=True) as status:
            st.write("➡️ Splitting dataset...")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            time.sleep(0.5)

            st.write("➡️ Vectorizing (TF-IDF)...")
            vectorizer = TfidfVectorizer()
            X_train_vec = vectorizer.fit_transform(X_train)
            X_test_vec = vectorizer.transform(X_test)
            time.sleep(0.5)

            st.write("➡️ Training algorithm...")
            if algo == "Logistic Regression":
                model = LogisticRegression(max_iter=200)
            elif algo == "Support Vector Machine (SVM)":
                model = SVC(probability=True)
            else:
                model = MultinomialNB()

            model.fit(X_train_vec, y_train)
            time.sleep(0.5)

            st.write("➡️ Evaluating...")
            y_pred = model.predict(X_test_vec)
            accuracy = accuracy_score(y_test, y_pred)

            status.update(label="✅ Training Completed!", state="complete")

        st.success(f"🎉 Training Success — Accuracy: **{accuracy:.4f}**")

        # =============================
        # Plot accuracy
        # =============================
        st.subheader("📊 Accuracy Visualization")

        fig, ax = plt.subplots()
        ax.bar(["Accuracy"], [accuracy])
        ax.set_ylim(0, 1)
        st.pyplot(fig)

        # =============================
        # Save model + vectorizer
        # =============================
        st.subheader("💾 Save Model")

        model_name = st.text_input("Model name:", "sentiment_model")

        if st.button("💾 Save to /models"):
            model_path = model_dir / f"{model_name}.pkl"
            vec_path = model_dir / f"{model_name}_vectorizer.pkl"

            joblib.dump(model, model_path)
            joblib.dump(vectorizer, vec_path)

            st.success(f"✅ Model saved: {model_path.name}")
            st.success(f"📦 Vectorizer saved: {vec_path.name}")
