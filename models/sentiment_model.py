import re
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ==========================
#  VN detection
# ==========================
VI_CHARS = r"àáạảãâầấậẩẫăằắặẳẵđêềếệểễôồốộổỗơờớợởỡưừứựửữíìịỉĩúùụủũýỳỵỷỹ"

def is_vietnamese(text: str) -> bool:
    if re.search(f"[{VI_CHARS}]", text.lower()):
        return True
    english_hint = r"\b(the|this|that|is|are|good|bad)\b"
    return not bool(re.search(english_hint, text.lower()))


# ==========================
#  VN Sentiment
# ==========================
VI_POS = ["tốt", "tuyệt", "xuất sắc", "hài lòng", "ưng ý", "đẹp", "ngon", "hoàn hảo", "ok", "rất thích"]
VI_NEG = ["tệ", "xấu", "kém", "thất vọng", "dở", "lỗi", "tồi", "không tốt", "quá tệ", "kinh khủng", "hỏng"]

def vietnamese_sentiment(text: str):
    score = 0
    t = text.lower()
    for w in VI_POS:
        if w in t: score += 1
    for w in VI_NEG:
        if w in t: score -= 1

    if score > 0:
        return "positive", min(0.65 + score * 0.08, 0.97)
    if score < 0:
        return "negative", min(0.65 + abs(score) * 0.08, 0.97)
    return "neutral", 0.55


# ==========================
#  EN Sentiment Model
# ==========================
def load_english_model():
    model_path = "models/en_sentiment_model.joblib"
    vec_path = "models/en_vectorizer.joblib"

    if os.path.exists(model_path) and os.path.exists(vec_path):
        return joblib.load(model_path), joblib.load(vec_path)

    texts = [
        "This product is very good", "Excellent quality and fast delivery",
        "Amazing experience", "Bad product", "Very disappointed",
        "Terrible quality", "It is okay", "Average quality", "Nothing special"
    ]
    labels = ["positive","positive","positive","negative","negative","negative","neutral","neutral","neutral"]

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=500)
    model.fit(X, labels)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)

    return model, vectorizer
