"""
Clara - Translation Assistant
A Streamlit app for translating English to Kinyarwanda
"""

import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Clara",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Blue theme with responsive design
st.markdown("""
<style>
    /* Responsive base */
    * {
        box-sizing: border-box;
    }
    
    /* Main container - full width - NO SPACING */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Make the main block container fill the page */
    .main {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Adjust Streamlit header for sidebar toggle */
    header {
        visibility: visible !important;
    }
    
    /* Remove all default padding/margin from elements */
    .element-container {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Chat header - Blue gradient - NO SPACING */
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    
    .chat-header h1 {
        margin: 0;
        font-size: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
    }
    
    @media (min-width: 768px) {
        .chat-header {
            padding: 1.5rem;
        }
        .chat-header h1 {
            font-size: 28px;
            gap: 15px;
        }
    }
    
    /* Chat container - Soft blue background - NO SIDE SPACING */
    .chat-container {
        background: linear-gradient(to bottom, #e8f4f8, #f0f9ff);
        padding: 1rem;
        border-left: none !important;
        border-right: none !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
    
    @media (min-width: 768px) {
        .chat-container {
            padding: 2rem 1rem;
        }
    }
    
    /* User message bubble - Blue */
    .user-message {
        background-color: #4285f4;
        color: white;
        padding: 10px 14px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 20px 12px 0;
        box-shadow: 0 2px 4px rgba(66, 133, 244, 0.3);
        text-align: right;
        word-wrap: break-word;
        max-width: 85%;
        margin-left: auto;
    }
    
    @media (min-width: 768px) {
        .user-message {
            max-width: 75%;
            padding: 12px 18px;
            margin: 8px 80px 12px 0;
        }
    }
    
    /* Assistant message bubble - Light blue */
    .assistant-message {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 10px 14px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0 12px 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: left;
        word-wrap: break-word;
        max-width: 85%;
        border-left: 3px solid #2196F3;
    }
    
    @media (min-width: 768px) {
        .assistant-message {
            max-width: 75%;
            padding: 12px 18px;
            margin: 8px 0 12px 80px;
        }
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 10px;
        opacity: 0.7;
        margin-top: 8px;
    }
    
    @media (min-width: 768px) {
        .timestamp {
            font-size: 11px;
        }
    }
    
    /* Chat input styling */
    [data-testid="chatInputContainer"] {
        border-radius: 0 !important;
        margin: 0 !important;
        padding: 1rem !important;
        background: linear-gradient(to top, #f8faff, #ffffff) !important;
        border-top: 2px solid #e3f2fd !important;
    }
    
    @media (min-width: 768px) {
        [data-testid="chatInputContainer"] {
            padding: 1.5rem !important;
        }
    }
    
    /* Add margin to chat container to account for chat input */
    .chat-container {
        padding-bottom: 80px !important;
    }
    
    /* Hide Streamlit default elements */
    footer {visibility: hidden;}
    
    /* Keep header visible for sidebar toggle */
    header {
        visibility: visible !important;
        height: auto !important;
    }
    
    /* Ensure sidebar toggle button is always visible */
    button[kind="header"] {
        display: block !important;
        visibility: visible !important;
    }
    
    /* Sidebar styling - Move to right side */
    [data-testid="stSidebar"] {
        order: 2;
    }
    
    [data-testid="stAppViewContainer"] > [data-testid="stAppViewBlockContainer"] {
        display: flex;
        flex-direction: row-reverse;
    }
    
    .css-1d391kg {
        padding-top: 3rem;
    }
    
    /* Mobile responsiveness for columns */
    @media (max-width: 768px) {
        /* Adjust column behavior on mobile */
        [data-testid="column"] {
            width: 100% !important;
        }
        
        /* Adjust sidebar width on mobile */
        section[data-testid="stSidebar"] {
            min-width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Better spacing on mobile */
        .chat-container {
            padding: 0.75rem 0.5rem;
        }
        
        .input-container {
            padding: 0.75rem;
        }
    }
    
    /* Responsive buttons */
    button {
        font-size: 14px;
        padding: 0.5rem;
    }
    
    @media (min-width: 768px) {
        button {
            font-size: 16px;
            padding: 0.75rem;
        }
    }
    
    /* Responsive text sizing for welcome message */
    @media (max-width: 768px) {
        .welcome-icon { font-size: 36px !important; }
        .welcome-title { font-size: 18px !important; }
        .welcome-sub { font-size: 12px !important; }
    }
    
    @media (min-width: 768px) {
        .welcome-icon { font-size: 64px !important; }
        .welcome-title { font-size: 24px !important; }
        .welcome-sub { font-size: 16px !important; }
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
BASE_URL = "https://nmt-api.umuganda.digital/api/v1/translate/"

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "source_lang" not in st.session_state:
    st.session_state.source_lang = "en"

def translate_text(src, tgt, text):
    """Translate text using the NMT API"""
    try:
        response = requests.post(
            BASE_URL,
            json={"src": src, "tgt": tgt, "text": text},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("translation", "")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 406:
            return "❌ Error: This language pair is not supported"
        return f"❌ Error: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Main UI
def main():
    # Header
    st.markdown("""
    <div class="chat-header">
        <h1>💬 Clara Translation</h1>
        <p style="margin: 8px 0 0 0; opacity: 0.95;">English ↔ Kinyarwanda</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🌐 Language")
        st.markdown("---")
        
        # Language selection buttons in sidebar
        if st.button("🇬🇧 → 🇷🇼 English to Kinyarwanda", use_container_width=True, key="en_rw", 
                     type="primary" if st.session_state.source_lang == "en" else "secondary"):
            st.session_state.source_lang = "en"
            st.rerun()
        
        if st.button("🇷🇼 → 🇬🇧 Kinyarwanda to English", use_container_width=True, key="rw_en",
                     type="primary" if st.session_state.source_lang == "rw" else "secondary"):
            st.session_state.source_lang = "rw"
            st.rerun()
        
        st.markdown("---")
        st.markdown("## 💬 Chat")
        
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        if st.session_state.chat_history:
            st.metric("Messages", len(st.session_state.chat_history))
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        **Clara** c'est juste un assistant de traduction pour traduire entre l'anglais au kinyarwanda.
        Il peut pas traduire entre le français au kinyarwanda mais il peut aider a faire des trucs simple
        surtout pour apprendre le kinyarwanda.
        
        """)
    
    # Chat messages container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message["type"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    {message['text']}
                    <div class="timestamp">You • {message.get('lang_label', 'English')}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    {message['text']}
                    <div class="timestamp">Clara • {message.get('lang_label', 'Kinyarwanda')}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 40px 20px;">
            <div class="welcome-icon" style="margin-bottom: 15px;">🌐</div>
            <div class="welcome-title" style="font-weight: 600; margin-bottom: 8px;">Bienvenue!</div>
            <div class="welcome-sub" style="opacity: 0.8;">tu peux commencer à ecrire un message en anglais et traduire au kinyarwanda</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input - uses Streamlit's built-in chat input with proper icons
    user_input = st.chat_input(f"Type a message in {'English' if st.session_state.source_lang == 'en' else 'Kinyarwanda'}...")
    
    # Handle translation
    if user_input:
        with st.spinner("Translating..."):
            # Determine source and target languages
            src = st.session_state.source_lang
            tgt = "rw" if src == "en" else "en"
            src_label = "English" if src == "en" else "Kinyarwanda"
            tgt_label = "Kinyarwanda" if tgt == "rw" else "English"
            
            # Translate
            translation = translate_text(src, tgt, user_input)
            
            # Add to chat history
            st.session_state.chat_history.append({
                "type": "user",
                "text": user_input,
                "language": src,
                "lang_label": src_label
            })
            
            st.session_state.chat_history.append({
                "type": "assistant",
                "text": translation,
                "language": tgt,
                "lang_label": tgt_label
            })
            
            st.rerun()

if __name__ == "__main__":
    main()
