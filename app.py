import streamlit as st
from pathlib import Path

# ==========================
# ⚙️ PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="Sentiment Analysis – Material UI Edition",
    page_icon="🧠",
    layout="wide"
)

# ==========================
# 🎨 LOAD CSS (ĐÚNG VỊ TRÍ)
# ==========================
def load_css():
    css_path = Path("theme.css")
    if css_path.exists():
        css = css_path.read_text()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Load CSS *SAU* khi page config đã xong
load_css()

# ==========================
# 🎨 HEADER – MATERIAL DESIGN
# ==========================
st.markdown(
    """
    <div class="header-card">
        <div class="header-icon">🧠</div>
        <div>
            <h2 class="header-title">Sentiment Analysis for Product Reviews</h2>
            <p class="header-sub">Modern UI • Streamlit • Machine Learning</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ==========================
# 📌 SIDEBAR – GRADIENT + ICONS
# ==========================
st.sidebar.markdown(
    """
    <div class="sidebar-title">
        📊 Navigation
    </div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "",
    ["🏠 Home", "📈 Sentiment Analysis", "⚙️ Training Info"]
)

# ==========================
# 🚀 ROUTING
# ==========================
if page == "🏠 Home":
    from pages.Home import show
    show()

elif page == "📈 Sentiment Analysis":
    from pages.Analysis import show
    show()

elif page == "⚙️ Training Info":
    from pages.Training_Info import show
    show()

# ==========================
# 👣 FOOTER – MATERIAL UI
# ==========================
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer-students">
        <h4>🎓 Students</h4>
        <p>Bùi Đức Nguyên – 235053154 – nguyenbd23@uef.edu.vn</p>
        <p>Huỳnh Ngọc Minh Quân – 235052863 – quanhnm@uef.edu.vn</p>
    </div>

    <div class="footer-instructor">
        <h4>👨‍🏫 Instructor</h4>
        <p><b>Bùi Tiến Đức</b></p>
        <a href="https://orcid.org/0000-0001-5174-3558" target="_blank">
            ORCID: 0000-0001-5174-3558
        </a>
    </div>

    <div class="footer-copy">
        © 2025 – Sentiment Analysis for E-Commerce
    </div>
    """,
    unsafe_allow_html=True
)
