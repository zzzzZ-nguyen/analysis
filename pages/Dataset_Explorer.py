import streamlit as st
import pandas as pd

def show():
    st.header("📊 Dataset Explorer")

    st.info("Upload dataset để xem nhanh cấu trúc dữ liệu.")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.subheader("Preview Dataset")
        st.dataframe(df)

        st.subheader("Columns Info")
        st.write(df.dtypes)

        st.subheader("Statistics")
        st.write(df.describe())
