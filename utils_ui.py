import streamlit as st
import time
import math

# ============================================================
# 1️⃣ LOAD CUSTOM CSS
# ============================================================
def load_custom_css():
    css = """
    <style>

    /* Smooth Fade In */
    .fade-in {
        animation: fadeIn 0.6s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* AI Typing Animation */
    .ai-typing {
        font-size: 18px;
        color: #4a4a4a;
        border-left: 3px solid #4a90e2;
        padding-left: 10px;
        margin-bottom: 12px;
        animation: fadeIn 0.4s ease-in-out;
    }

    /* Gauge Chart */
    .gauge-wrap {
        text-align: center;
        margin-top: 15px;
    }

    /* Colored Tags */
    .tag {
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 18px;
        display: inline-block;
        margin-top: 10px;
    }
    .pos { background: #2ecc71; color: white; }
    .neu { background: #95a5a6; color: white; }
    .neg { background: #e74c3c; color: white; }

    /* Skeleton Loader */
    .skeleton {
        background: linear-gradient(-90deg, #e0e0e0 0%, #f5f5f5 50%, #e0e0e0 100%);
        background-size: 400% 400%;
        animation: pulse 1.3s ease infinite;
        height: 18px;
        margin-bottom: 10px;
        border-radius: 6px;
    }
    @keyframes pulse {
        0% { background-position: 0% 0%; }
        100% { background-position: -135% 0%; }
    }

    </style>
    """

    st.markdown(css, unsafe_allow_html=True)


# ============================================================
# 2️⃣ SKELETON LOADING (Facebook effect)
# ============================================================
def loading_skeleton(lines=3):
    with st.container():
        for _ in range(lines):
            st.markdown("<div class='skeleton'></div>", unsafe_allow_html=True)
            time.sleep(0.12)


# ============================================================
# 3️⃣ AI TYPING EFFECT — type chữ từng ký tự
# ============================================================
def ai_typing(text):
    container = st.empty()
    displayed = ""

    for char in text:
        displayed += char
        container.markdown(f"<div class='ai-typing'>{displayed}</div>", unsafe_allow_html=True)
        time.sleep(0.01)


# ============================================================
# 4️⃣ GAUGE CHART — cảm xúc dạng đồng hồ
# ============================================================
def gauge_chart(value):
    percentage = value * 100

    st.markdown("<h4 style='text-align:center;'>Confidence</h4>", unsafe_allow_html=True)

    fig_html = f"""
    <div class="gauge-wrap fade-in">
        <svg width="240" height="160">
            <path d="M20 140 A100 100 0 0 1 220 140" fill="none" stroke="#ddd" stroke-width="20"/>
            <path d="M20 140 A100 100 0 0 1 220 140"
                  fill="none"
                  stroke="#4CAF50"
                  stroke-width="20"
                  stroke-dasharray="{percentage*3.14:.1f} 1000"/>
            <circle cx="{120 + 90 * math.cos((percentage/100*3.14)-3.14)}"
                    cy="{140 + 90 * math.sin((percentage/100*3.14)-3.14)}"
                    r="8"
                    fill="#4CAF50"/>
        </svg>
        <div style="font-size:24px;font-weight:700;">{percentage:.1f}%</div>
    </div>
    """

    st.markdown(fig_html, unsafe_allow_html=True)


# ============================================================
# 5️⃣ COLORED SENTIMENT TAG
# ============================================================
def colored_tag(sentiment):
    sentiment = sentiment.lower()

    if sentiment == "positive":
        return "<div class='tag pos'>😊 POSITIVE</div>"
    elif sentiment == "negative":
        return "<div class='tag neg'>😡 NEGATIVE</div>"
    else:
        return "<div class='tag neu'>😐 NEUTRAL</div>"


# ============================================================
# 6️⃣ SAVE HISTORY INTO SESSION STATE
# ============================================================
def save_history(text, sentiment, confidence):

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append({
        "review": text,
        "sentiment": sentiment,
        "confidence": round(confidence, 3)
    })
