import streamlit as st
import anthropic
import datetime
import webbrowser

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Aria — AI Virtual Assistant",
    page_icon="🤖",
    layout="centered"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e0e0ff !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #0d0d2b 0%, #0a0a0f 60%) !important;
}

h1, h2, h3 { font-family: 'Orbitron', monospace !important; }
p, div, span, label { font-family: 'Exo 2', sans-serif !important; }

/* Header */
.aria-header {
    text-align: center;
    padding: 2rem 0 1rem 0;
}
.aria-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff, #7b2fff, #ff006e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 4px;
    margin: 0;
}
.aria-subtitle {
    font-family: 'Exo 2', sans-serif;
    color: #6677aa;
    font-size: 0.9rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}
.aria-avatar {
    font-size: 4rem;
    display: block;
    margin-bottom: 0.5rem;
    animation: pulse 3s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); filter: drop-shadow(0 0 10px #00d4ff88); }
    50% { transform: scale(1.05); filter: drop-shadow(0 0 25px #7b2fff88); }
}

/* Chat messages */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem 0;
}
.msg-user {
    display: flex;
    justify-content: flex-end;
}
.msg-aria {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 0.7rem;
}
.bubble-user {
    background: linear-gradient(135deg, #7b2fff, #00d4ff);
    color: white;
    padding: 0.8rem 1.2rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-family: 'Exo 2', sans-serif;
    font-size: 0.95rem;
    box-shadow: 0 4px 20px #7b2fff44;
}
.bubble-aria {
    background: linear-gradient(135deg, #0d1133, #131728);
    border: 1px solid #2a2d5a;
    color: #c8d0ff;
    padding: 0.8rem 1.2rem;
    border-radius: 18px 18px 18px 4px;
    max-width: 75%;
    font-family: 'Exo 2', sans-serif;
    font-size: 0.95rem;
    box-shadow: 0 4px 20px #00000066;
}
.aria-icon {
    font-size: 1.5rem;
    margin-top: 0.2rem;
    flex-shrink: 0;
}

/* Input area */
[data-testid="stTextInput"] input {
    background: #0d1133 !important;
    border: 1px solid #2a2d5a !important;
    border-radius: 12px !important;
    color: #e0e0ff !important;
    font-family: 'Exo 2', sans-serif !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 15px #00d4ff33 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7b2fff, #00d4ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px #7b2fff55 !important;
}

/* Quick action chips */
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.5rem 0 1rem 0;
    justify-content: center;
}
.chip {
    background: #0d1133;
    border: 1px solid #2a2d5a;
    color: #8899cc;
    padding: 0.35rem 0.9rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-family: 'Exo 2', sans-serif;
    cursor: pointer;
    transition: all 0.2s;
}
.chip:hover {
    border-color: #00d4ff;
    color: #00d4ff;
}

/* Status bar */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #445588;
    font-size: 0.75rem;
    font-family: 'Exo 2', sans-serif;
    margin-bottom: 1rem;
    justify-content: center;
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #00ff88;
    box-shadow: 0 0 8px #00ff88;
    animation: blink 2s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Divider */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2d5a, #00d4ff44, #2a2d5a, transparent);
    margin: 1rem 0;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Config ─────────────────────────────────────────────────────────────────────
API_KEY = st.secrets["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"]
ASSISTANT_NAME = "Aria"

SYSTEM_PROMPT = f"""You are {ASSISTANT_NAME}, a sleek and intelligent AI virtual assistant.
Be helpful, friendly, and concise (2-4 sentences unless detail is needed).
Today is {datetime.date.today().strftime('%A, %B %d, %Y')}.
When asked to open a website, respond naturally and mention the site name."""

QUICK_ACTIONS = [
    "🕐 What time is it?",
    "📅 What's today's date?",
    "🌍 Tell me a fun fact",
    "💡 Give me a productivity tip",
    "🔢 Explain AI in simple terms",
]

WEBSITES = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "wikipedia": "https://wikipedia.org",
    "reddit": "https://reddit.com",
}

# ── Session State ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="aria-header">
    <span class="aria-avatar">🤖</span>
    <p class="aria-title">ARIA</p>
    <p class="aria-subtitle">AI Virtual Assistant</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="status-bar">
    <div class="status-dot"></div>
    <span>ONLINE · Powered by Claude AI · Ready to assist</span>
</div>
<div class="glow-divider"></div>
""", unsafe_allow_html=True)

# ── Quick Action Chips ─────────────────────────────────────────────────────────
st.markdown('<div class="chip-row">' +
    ''.join([f'<span class="chip">{a}</span>' for a in QUICK_ACTIONS]) +
    '</div>', unsafe_allow_html=True)

# ── AI Response Function ───────────────────────────────────────────────────────
def get_response(user_input: str) -> str:
    low = user_input.lower()

    # Local quick replies
    if any(w in low for w in ["hello", "hi", "hey"]):
        return f"Hey there! 👋 I'm {ASSISTANT_NAME}, your AI assistant. What can I help you with today?"
    if "time" in low and "date" not in low:
        return f"🕐 The current time is **{datetime.datetime.now().strftime('%I:%M %p')}**."
    if "date" in low or "today" in low:
        return f"📅 Today is **{datetime.date.today().strftime('%A, %B %d, %Y')}**."

    # Website opener
    for site, url in WEBSITES.items():
        if site in low and ("open" in low or "go to" in low or "visit" in low):
            return f"🌐 Opening **{site.capitalize()}** for you! → [Click here]({url})"

    # Claude AI
    try:
        client = anthropic.Anthropic(api_key=API_KEY)
        history = [{"role": m["role"], "content": m["content"]}
                   for m in st.session_state.messages[-10:]]
        history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=history,
        )
        return response.content[0].text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ── Chat Display ───────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="msg-aria" style="display:flex; align-items:flex-start; gap:0.7rem; margin:1rem 0;">
        <span class="aria-icon">🤖</span>
        <div class="bubble-aria">Hello! I'm <strong>Aria</strong>, your AI assistant. Ask me anything — I can answer questions, tell you the time & date, open websites, and much more! ✨</div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-user">
            <div class="bubble-user">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-aria" style="display:flex; align-items:flex-start; gap:0.7rem; margin:0.5rem 0;">
            <span class="aria-icon">🤖</span>
            <div class="bubble-aria">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "message",
        placeholder="Ask Aria anything...",
        label_visibility="collapsed",
        key=f"input_{st.session_state.input_key}"
    )
with col2:
    send = st.button("SEND ➤")

# ── Handle Send ────────────────────────────────────────────────────────────────
if (send or user_input) and user_input.strip():
    text = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": text})

    with st.spinner("Aria is thinking..."):
        reply = get_response(text)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.input_key += 1
    st.rerun()

# ── Clear Button ───────────────────────────────────────────────────────────────
if st.session_state.messages:
    st.markdown("<br>", unsafe_allow_html=True)
    col_c1, col_c2, col_c3 = st.columns([2, 1, 2])
    with col_c2:
        if st.button("🗑️ CLEAR"):
            st.session_state.messages = []
            st.rerun()
