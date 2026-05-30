import streamlit as st
import re
import string
import random
import math
import pandas as pd

# --------------------------
# CONFIG
# --------------------------
COMMON_PASSWORDS = [
    'password','123456','qwerty','abc123','letmein','admin','welcome',
    'monkey','password1','12345678','123456789','baseball','football',
    'jennifer','iloveyou','superman','sunshine'
]

if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------
# PASSWORD GENERATOR (FIXED)
# --------------------------
def generate_password(length=14):
    if length < 4:
        length = 4

    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    all_chars = string.ascii_letters + string.digits + string.punctuation

    while len(password) < length:
        password.append(random.choice(all_chars))

    random.shuffle(password)
    return ''.join(password)

# --------------------------
# ENTROPY
# --------------------------
def entropy(password):
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(c in string.punctuation for c in password): pool += 32

    if pool == 0:
        return 0

    return round(len(password) * math.log2(pool), 2)

# --------------------------
# ATTACK TIME
# --------------------------
def attack_time(ent):
    guesses = 2 ** ent
    seconds = guesses / 1e9

    if seconds < 1:
        return "Instant crack"
    elif seconds < 3600:
        return "Minutes"
    elif seconds < 86400:
        return "Hours"
    elif seconds < 31536000:
        return "Days/Months"
    else:
        return "Years+ (Safe)"

# --------------------------
# STRENGTH LABEL
# --------------------------
def strength(score):
    if score < 3:
        return "🔴 Very Weak"
    elif score < 5:
        return "🟠 Weak"
    elif score < 7:
        return "🟡 Moderate"
    elif score < 9:
        return "🟢 Strong"
    return "🔵 Very Strong"

# --------------------------
# NEW: SEQUENTIAL CHECK (FIXED)
# --------------------------
def has_sequential(password):
    password = password.lower()

    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789"
    ]

    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in password:
                return True

    return False

# --------------------------
# ANALYSIS (IMPROVED SCORING)
# --------------------------
def analyze(password):
    score = 0
    feedback = []

    # Length
    if len(password) >= 12:
        score += 3
    elif len(password) >= 8:
        score += 2
    else:
        feedback.append("❌ Use at least 8-12 characters")

    # Character variety
    types = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password)
    ])
    score += types

    if types < 3:
        feedback.append("⚠️ Add uppercase, numbers & symbols")

    # Common password
    if password.lower() in COMMON_PASSWORDS:
        score -= 3
        feedback.append("❌ Very common password")

    # Repeating pattern
    if re.search(r"(.)\1\1", password):
        score -= 1
        feedback.append("⚠️ Repeating characters detected")

    # NEW: Sequential check
    if has_sequential(password):
        score -= 2
        feedback.append("⚠️ Sequential pattern detected (abc / 123)")

    score = max(0, min(10, score))
    return score, feedback

# --------------------------
# UI
# --------------------------
st.set_page_config(page_title="Password Analyzer", layout="wide")
st.title("🔐 Next-Level Password Security Analyzer )")

col1, col2 = st.columns(2)

# LEFT
with col1:
    length = st.slider("Password Length", 6, 24, 14)

    if st.button("Generate Strong Password"):
        password = generate_password(length)
        st.code(password)

    password = st.text_input("Enter Password", type="password")

# RIGHT
with col2:
    if password:
        score, fb = analyze(password)
        ent = entropy(password)

        st.subheader("Security Score")
        st.progress(score / 10)

        st.write("Status:", strength(score))

        st.metric("Entropy (bits)", ent)
        st.write("Attack Time:", attack_time(ent))

        st.subheader("Suggestions")

        if fb:
            for f in fb:
                st.warning(f)
        else:
            st.success("Perfect strong password!")

        # HISTORY (cleaned)
        st.session_state.history.append(password)
        st.subheader("Recent Passwords")
        st.write(list(dict.fromkeys(st.session_state.history[-5:])))

# --------------------------
# CHART (YOUR FEATURE KEPT)
# --------------------------
st.subheader("📊 Security Analysis Chart")

if password:
    data = pd.DataFrame({
        "Metric": ["Length", "Complexity", "Entropy"],
        "Value": [
            len(password),
            sum([
                any(c.islower() for c in password),
                any(c.isupper() for c in password),
                any(c.isdigit() for c in password),
                any(c in string.punctuation for c in password)
            ]),
            entropy(password)
        ]
    })

    st.bar_chart(data.set_index("Metric"))