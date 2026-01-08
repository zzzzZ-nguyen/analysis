import streamlit as st
from pathlib import Path

# ======================================================
# 🔧 PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Sentiment Analysis for Product Reviews",
    page_icon="🧠",
    layout="wide"
)

# ======================================================
# 🎨 LOAD CUSTOM CSS
# ======================================================
def load_css():
    css_path = Path("theme.css")
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text()}</style>",
            unsafe_allow_html=True
        )
    else:
        st.error("⚠️ theme.css NOT FOUND — UI sẽ không hiển thị đúng!")

load_css()

# ======================================================
# 🎨 HEADER – MATERIAL DESIGN STYLE
# ======================================================
st.markdown(
    """
    <div class="header-card">
        <div class="header-icon">🧠</div>
        <div class="header-text">
            <h1 class="header-title">Sentiment Analysis for Product Reviews</h1>
            <p class="header-sub">Modern UI • Streamlit • Machine Learning</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ======================================================
# 📌 SIDEBAR – MATERIAL GRADIENT
# ======================================================
st.sidebar.markdown(
    """
    <div class="sidebar-title">📊 Navigation</div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "",
    ["🏠 Home", "📈 Sentiment Analysis", "⚙️ Training Info"]
)

# ======================================================
# 🚀 ROUTING – CALL TO PAGES
# ======================================================
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
# 👣 FIXED FOOTER
# ==========================

# 🚀 RESET markdown state để tránh bị dính code-block
st.markdown("<div></div>", unsafe_allow_html=True)
st.write("")  # thêm 1 dòng trắng cho chắc chắn

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

footer_html = """
<div class="footer-card">

    <div class="footer-section">
        <h4>🎓 Students</h4>
        <p>Bùi Đức Nguyên – 235053154 – nguyenbd23@uef.edu.vn</p>
        <p>Huỳnh Ngọc Minh Quân – 235052863 – quanhnm@uef.edu.vn</p>
    </div>

    <div class="footer-section">
        <h4>👨‍🏫 Instructor</h4>
        <p><b>Bùi Tiến Đức</b></p>
        <a href="https://orcid.org/0000-0001-5174-3558" target="_blank">
            ORCID: 0000-0001-5174-3558
        </a>
    </div>

    <div class="footer-copy">
        © 2025 – Sentiment Analysis for E-Commerce
    </div>

</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
