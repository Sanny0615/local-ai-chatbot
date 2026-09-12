import streamlit as st
import ollama


# =========================================================
# UI STYLING
# =========================================================

st.markdown("""
<style>

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(139, 92, 246, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(236, 72, 153, 0.14),
                transparent 28%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(127, 29, 29, 0.12),
                transparent 35%
            ),
            #08070d;

        color: #f5f3ff;
    }


    .main .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }


    h1 {
        text-align: center;

        font-size: 2.6rem !important;
        font-weight: 800 !important;

        letter-spacing: 1px;

        background: linear-gradient(
            90deg,
            #a78bfa,
            #ec4899,
            #f43f5e
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        text-shadow:
            0 0 25px rgba(168, 85, 247, 0.25);
    }


    .subtitle {
        text-align: center;

        color: #a1a1aa;

        margin-top: -15px;
        margin-bottom: 30px;
    }


    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #0d0a16,
            #09070d
        );

        border-right: 1px solid rgba(168, 85, 247, 0.25);
    }


    section[data-testid="stSidebar"] h2 {
        color: #c4b5fd;
    }


    [data-testid="stChatMessage"] {
        border-radius: 16px;

        padding: 12px 16px;
        margin: 10px 0;

        border: 1px solid rgba(168, 85, 247, 0.15);

        background: rgba(20, 16, 30, 0.75);

        box-shadow:
            0 0 18px rgba(124, 58, 237, 0.08);
    }


    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: linear-gradient(
            135deg,
            rgba(76, 29, 149, 0.35),
            rgba(20, 16, 30, 0.85)
        );

        border-left: 3px solid #a855f7;
    }


    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: linear-gradient(
            135deg,
            rgba(157, 23, 77, 0.22),
            rgba(20, 16, 30, 0.85)
        );

        border-left: 3px solid #ec4899;
    }


    [data-testid="stChatInput"] {
        border: 1px solid rgba(168, 85, 247, 0.45);

        border-radius: 14px;

        box-shadow:
            0 0 15px rgba(139, 92, 246, 0.12),
            inset 0 0 10px rgba(236, 72, 153, 0.03);
    }


    .stButton > button {
        width: 100%;

        border-radius: 10px;

        border: 1px solid rgba(236, 72, 153, 0.45);

        background: linear-gradient(
            90deg,
            rgba(124, 58, 237, 0.25),
            rgba(190, 24, 93, 0.25)
        );

        color: #f5f3ff;

        font-weight: 600;

        transition: 0.2s ease;
    }


    .stButton > button:hover {
        border-color: #ec4899;

        box-shadow:
            0 0 18px rgba(236, 72, 153, 0.25);

        transform: translateY(-1px);
    }


    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #c084fc;
    }


    .status {
        text-align: center;

        color: #71717a;

        font-size: 0.8rem;

        margin-top: 25px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.title("⚔️ Shadow AI")

st.markdown(
    '<div class="subtitle">'
    'Your local AI companion • Powered by Llama 3.2'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Settings")

    temperature = st.slider(
        "🌡️ Temperature",
        0.0,
        1.0,
        0.7
    )

    st.caption(
        "Lower = more predictable\n\n"
        "Higher = more varied"
    )

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# CHAT HISTORY STORAGE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# DISPLAY OLD MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# =========================================================
# USER INPUT
# =========================================================

question = st.chat_input(
    "Ask Shadow AI something..."
)


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # Display user message
    st.chat_message("user").write(question)


    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })


    # =====================================================
    # OLLAMA STREAMING REQUEST
    # =====================================================

    response = ollama.chat(

        model="llama3.2:3b",

        messages=[
            {
                "role": "system",

                "content": """
                You are a helpful beginner-friendly AI tutor.

                Keep answers concise and simple.

                Give one simple example when useful.

                Do not give unnecessary information.

                If the user asks for more detail,
                then explain more.
                """
            },

            *st.session_state.messages
        ],

        options={
            "temperature": temperature
        },

        stream=True
    )


    # =====================================================
    # DISPLAY STREAMING RESPONSE
    # =====================================================

    with st.chat_message("assistant"):

        answer = st.write_stream(
            chunk["message"]["content"]
            for chunk in response
        )


    # =====================================================
    # STORE COMPLETE AI ANSWER
    # =====================================================

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="status">'
    '⚡ Local AI • Ollama • Llama 3.2 3B'
    '</div>',
    unsafe_allow_html=True
)