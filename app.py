# ==========================
# 🌟 BEAUTIFUL FOOTER (NEW DESIGN)
# ==========================
st.write("---")

footer_html = """
<style>
.footer-container {
    max-width: 900px;
    margin: 25px auto;
    font-family: 'Segoe UI', sans-serif;
}

/* Card style */
.footer-card {
    background: white;
    border-radius: 12px;
    padding: 20px 25px;
    border: 1px solid #e5e5e5;
    box-shadow: 0 3px 15px rgba(0,0,0,0.06);
    margin-bottom: 15px;
}

/* Yellow student box */
.student-box {
    background: #fff7c2;
    border: 1px solid #f0d878;
}

/* Title styling */
.footer-title {
    font-size: 17px;
    font-weight: bold;
    color: #2b6f3e;
    margin-bottom: 10px;
}

/* List inside boxes */
.footer-list {
    margin: 0;
    padding-left: 18px;
    line-height: 1.7;
    font-size: 15px;
}

/* Instructor section */
.instructor-row {
    display: flex;
    align-items: center;
    gap: 12px;
}

/* Copyright */
.footer-copy {
    text-align: center;
    margin-top: 12px;
    font-size: 13px;
    color: #777;
}
</style>

<div class="footer-container">

    <!-- STUDENTS -->
    <div class="footer-card student-box">
        <div class="footer-title">👨‍🎓 Students</div>
        <ul class="footer-list">
            <li>Bùi Đức Nguyên – 235053154 – nguyenbd23@uef.edu.vn</li>
            <li>Huỳnh Ngọc Minh Quân – 235052863 – quanhnm@uef.edu.vn</li>
        </ul>
    </div>

    <!-- INSTRUCTOR -->
    <div class="footer-card">
        <div class="footer-title">👨‍🏫 Instructor</div>
        <div class="instructor-row">
            <img src="https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg"
                 width="28">
            <div>
                <b>TS. Bùi Tiến Đức</b><br>
                <a href="https://orcid.org/0000-0001-5174-3558"
                   target="_blank"
                   style="color:#1a73e8; text-decoration:none;">
                   ORCID: 0000-0001-5174-3558
                </a>
            </div>
        </div>
    </div>

    <div class="footer-copy">
        © 2025 – Topic 5: Sentiment Analysis for E-Commerce<br>
        Developed with ❤️ using Python & Streamlit
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
