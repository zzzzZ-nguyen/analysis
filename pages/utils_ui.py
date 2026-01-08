import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
#  AI TYPING EFFECT
# ==========================================
def ai_typing(text, speed=0.015):
    placeholder = st.empty()
    displayed = ""
    for ch in text:
        displayed += ch
        placeholder.markdown(f"**{displayed}**")
        time.sleep(speed)


# ==========================================
#  LOADING SKELETON
# ==========================================
def loading_skeleton(duration=2.0):
    with st.spinner("🔍 AI is analyzing…"):
        # Fake skeleton loading
        skeleton = st.empty()
        for i in range(12):
            skeleton.markdown(
                f"""
                <div style="
                    background: linear-gradient(90deg, #ddd, #f6f6f6, #ddd);
                    height: 18px;
                    width: {40 + i*5}%;
                    border-radius: 8px;
                    margin-bottom: 6px;
                    animation: pulse 1.2s infinite;
                ">
                </div>
                """,
                unsafe_allow_html=True,
            )
            time.sleep(duration / 12)
        skeleton.empty()


# ==========================================
#  GAUGE CHART (Đồng hồ cảm xúc)
# ==========================================
def gauge_chart(score):
    """
    score: -1 (negative) → 1 (positive)
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=(score + 1) * 50,  # chuyển -1..1 → 0..100
            title={"text": "Sentiment Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "black"},
                "steps": [
                    {"range": [0, 33], "color": "#ff4e4e"},    # red
                    {"range": [33, 66], "color": "#cccccc"},  # gray
                    {"range": [66, 100], "color": "#4caf50"}, # green
                ],
            },
        )
    )
    st.plotly_chart(fig, use_container_width=True)


# ==========================================
#  colored sentiment tag
# ==========================================
def colored_tag(sentiment):
    css = {
        "positive": "background:#4caf50;color:white;padding:6px 12px;border-radius:8px;",
        "negative": "background:#ff4e4e;color:white;padding:6px 12px;border-radius:8px;",
        "neutral": "background:#999;color:white;padding:6px 12px;border-radius:8px;",
    }
    return f"<span style='{css.get(sentiment,'')}'> {sentiment.upper()} </span>"


# ==========================================
#  SAVE HISTORY TO CSV
# ==========================================
def save_history(text, sentiment, confidence):
    history_file = "sentiment_history.csv"

    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "review": text,
        "sentiment": sentiment,
        "confidence": confidence,
    }

    # Append hoặc tạo mới
    try:
        df = pd.read_csv(history_file)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    except:
        df = pd.DataFrame([new_entry])

    df.to_csv(history_file, index=False)
