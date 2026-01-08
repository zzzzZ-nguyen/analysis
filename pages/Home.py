import streamlit as st

# ============================
#       CUSTOM CSS
# ============================
CSS = """
<style>
.page-title {
    font-size: 36px !important;
    font-weight: 800;
    color: #2b6f3e;
    background: linear-gradient(90deg, #2b6f3e, #3fa55b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    margin-top: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    border-left: 6px solid #ffcc00;
    transition: 0.2s;
}
.card:hover {
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    transform: translateY(-3px);
}

.card h4 {
    color: #d12c2c;
    margin-top: 0px;
    font-size: 22px;
}

ul li {
    margin-bottom: 6px;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ============================
#        CARD FUNCTION
# ============================
def card(html):
    st.markdown(f"<div class='card'>{html}</div>", unsafe_allow_html=True)

# ============================
#            PAGE
# ============================
def show():
    
    st.markdown("<h2 class='page-title'>Topic 5 – Sentiment Analysis for Product Reviews</h2>",
                unsafe_allow_html=True)

    # CARD 1
    card("""
<h4>📌 1. Problem Overview</h4>
The project develops an intelligent sentiment analysis system that automatically
classifies product reviews into <b>Positive, Neutral, or Negative</b> to support
decision-making for e-commerce businesses.
""")

    # CARD 2
    card("""
<h4>🎯 2. Objectives</h4>
<ul>
    <li>Analyze customer opinions from product reviews.</li>
    <li>Support Vietnamese and English text.</li>
    <li>Visualize sentiment distribution.</li>
    <li>Provide real-time sentiment prediction.</li>
</ul>
""")

    # CARD 3
    card("""
<h4>🛠️ 3. Technologies</h4>
<ul>
    <li>Python, Streamlit</li>
    <li>Scikit-learn, TF-IDF</li>
    <li>Logistic Regression, SVM, XGBoost (optional)</li>
</ul>
""")

    st.write("---")
