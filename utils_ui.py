import streamlit as st
import time
import numpy as np
import plotly.graph_objects as go


# ============================
# 🔥 AI typing animation
# ============================
def ai_typing(text, delay=0.015):
    output = ""
    container = st.empty()
    for char in text:
        output += char
        container.markdown(f"<p style='font-size:17px;'>{output}</p>", unsafe_allow_html=True)
        time.sleep(delay)


# ============================
# ⌚ Loading Skeleton
# ============================
def loading_skeleton(lines=3):
    for _ in range(lines):
        st.markdown("""
            <div style="
                height:18px;
                background:linear-gradient(90deg,#e6e6e6,#f4f4f4,#e6e6e6);
                background-size:300% 100%;
                border-radius:6px;
                margin:8px 0;
                animation:skeleton 1.4s infinite;
            "></div>

            <style>
            @keyframes skeleton {
                0% {background-position:0 0;}
                100% {background-position:-300% 0;}
            }
            </style>
        """, unsafe_allow_html=True)


# ============================
# 📉 Gauge Chart
# ============================
def gauge_chart(confidence):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#6c63ff"},
            "steps": [
                {"range": [0, 33], "color": "#ff6b6b"},
                {"range": [33, 66], "color": "#ffd93d"},
                {"range": [66, 100], "color": "#51cf66"}
            ],
        },
    ))
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)


# ============================
# 📌 Colored Sentiment Tag
# ============================
def colored_tag(sentiment):
    color = {
        "positive": "#51cf66",
        "negative": "#ff6b6b",
        "neutral": "#ffd93d"
    }.get(sentiment, "#888")
    
    return f"""
        <span style="
            background:{color};
            padding:6px 12px;
            color:white;
            border-radius:8px;
            font-weight:600;">
            {sentiment.upper()}
        </span>
    """


# ============================
# 📌 Save history
# ============================
def save_history(text, sentiment, confidence):
    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append({
        "review": text,
        "sentiment": sentiment,
        "confidence": round(confidence, 3)
    })
