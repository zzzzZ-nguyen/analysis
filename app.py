# ======================================================
# 🌟 SENTIMENT ANALYSIS DASHBOARD (PRO VERSION)
# Streamlit + Modern UI + Professional Layout
# ======================================================

import streamlit as st
from pathlib import Path

# ======================================================
# 🎨 PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Sentiment Analysis Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# 🎨 LOAD CUSTOM CSS + ANIMATION
# ======================================================
def load_css():
    css_path = Path("theme.css")
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text()}</style>",
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ theme.css NOT FOUND — UI có thể hiển thị sai !")

load_css()

# ======================================================
# ✨ GLOBAL CUSTOM JS – SMOOTH FADE ANIMATION
# ======================================================
st.markdown(
    """
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            document.body.style.opacity = 0;
            setTimeout(function(){ document.body.style.transition = "opacity 0.8s"; document.body.style.opacity = 1;}, 50);
        });
    </script>
    """,
    unsafe_allow_html=True,
)

# ======================================================
# 🌟 HEADER – PREMIUM DESIGN
# ======================================================
st.markdown(
    """
    <div class="header-card pro-shadow">
        <div class="header-icon">🧠</div>
        <div class="header-text">
            <h1 class="header-title">Sentiment Analysis Dashboard</h1>
            <p class="header-sub">AI • NLP • Machine Learning • Streamlit UI</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)


# ======================================================
# 🎨 SIDEBAR – PRO GRADIENT + ICON NAVIGATOR
# ======================================================
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-title">📌 Navigation</div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "",
        [
            "🏠 Home",
            "📈 Sentiment Analysis",
            "📊 Dataset Explorer",
            "⚙️ Training Info",
        ],
        label_visibility="collapsed"
    )

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="sidebar-footer">
            <b>📘 Dashboard v2.0</b><br>
            Improved UI • Faster • Cleaner
        </div>
        """,
        unsafe_allow_html=True
    )


# ======================================================
# 🚀 ROUTING – LOAD PAGES
# ======================================================
if page == "🏠 Home":
    from pages.Home import show
    show()

elif page == "📈 Sentiment Analysis":
    from pages.Analysis import show
    show()

elif page == "📊 Dataset Explorer":
    from pages.Dataset_Explorer import show  # optional page
    show()

elif page == "⚙️ Training Info":
    from pages.Training_Info import show
    show()


# ======================================================
# 🦶 PREMIUM FOOTER – RESPONSIVE 2-COLUMN
# ======================================================
st.markdown("<br><div class='divider'></div>", unsafe_allow_html=True)

footer_html = """
<div class="footer-card pro-shadow">
<div class="footer-grid">
<div class="footer-section">
            <h4>🎓 Students</h4>
            <p>• <b>Bùi Đức Nguyên</b> – 235053154 – nguyenbd23@uef.edu.vn</p>
            <p>• <b>Huỳnh Ngọc Minh Quân</b> – 235052863 – quanhnm@uef.edu.vn</p>
        </div>
<div class="footer-section">
            <h4>👨‍🏫 Instructor</h4>
            <p><b>Bùi Tiến Đức</b></p>
            <a href="https://orcid.org/0000-0001-5174-3558" target="_blank">
                ORCID: 0000-0001-5174-3558
            </a>
        </div>
    </div>

    <div class="footer-copy">
        © 2025 — Sentiment Analysis for E-Commerce. All rights reserved.
    </div>

</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
