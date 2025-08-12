import streamlit as st
import ollama
from dotenv import load_dotenv
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import queue

# Load environment variables once at module level
load_dotenv()

# Configure the app
st.set_page_config(
    page_title="CR IT Infopark",
    page_icon="💻",
    layout="wide"
)

# Global model warm-up flag
MODEL_WARMED_UP = False
MODEL_LOCK = threading.Lock()

# Cache company knowledge loading
@st.cache_data
def load_company_knowledge():
    """Load company knowledge with caching to avoid repeated file reads"""
    try:
        with open("company_knowledge.md", "r", encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Company knowledge file not found. Please ensure company_knowledge.md exists."

# Pre-compile keywords for faster lookup
COMPANY_KEYWORDS = frozenset([
    "cr", "it", "infopark", "crit", "company", "career", "job", "success", 
    "client", "about", "services", "history", "values", "positions", 
    "benefits", "culture", "case", "studies", "achievements", "industries",
    "apply", "application", "hiring", "work", "employment", "vacancy"
])

# Cache the system prompt
@st.cache_data
def get_system_prompt():
    """Cache system prompt to avoid regenerating it every time"""
    company_knowledge = load_company_knowledge()
    return f"""You are an AI assistant for CR IT Infopark. Provide concise, helpful information about:
1. Company services, history, values
2. Job careers, positions, benefits, culture
3. Success stories, case studies, achievements
4. Clients and industries served

For non-CR IT Infopark queries, respond: "I can only answer questions about CR IT Infopark."

Company Knowledge:
{company_knowledge}

Keep responses concise and under 200 words for faster delivery."""

# Optimized keyword checking
def is_company_related_query(prompt):
    """Ultra-fast keyword checking using set operations"""
    if len(prompt) > 500:  # Skip very long prompts
        return False
    
    prompt_words = set(word.lower() for word in prompt.split() if len(word) > 2)
    return bool(COMPANY_KEYWORDS.intersection(prompt_words))

# Model warm-up function
def warm_up_model():
    """Warm up the model in background"""
    global MODEL_WARMED_UP
    try:
        with MODEL_LOCK:
            if not MODEL_WARMED_UP:
                # Quick warm-up call
                ollama.chat(
                    model='llama3',
                    messages=[{'role': 'user', 'content': 'hi'}],
                    options={'num_predict': 10}  # Limit tokens for faster warm-up
                )
                MODEL_WARMED_UP = True
    except Exception as e:
        st.error(f"Model warm-up failed: {e}")

# Optimized response generation
def generate_response_fast(prompt):
    """Generate response with performance optimizations"""
    start_time = time.time()
    
    # Quick keyword check first
    if not is_company_related_query(prompt):
        return "I can only answer questions about CR IT Infopark."
    
    try:
        # Ensure model is warmed up
        if not MODEL_WARMED_UP:
            warm_up_model()
        
        # Generate response with performance settings
        response = ollama.chat(
            model='llama3',
            messages=[
                {
                    'role': 'system',
                    'content': get_system_prompt()
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            options={
                'temperature': 0.7,
                'num_predict': 150,  # Limit response length for speed
                'top_k': 20,  # Reduce sampling space
                'top_p': 0.9,
                'num_ctx': 2048,  # Smaller context window
            }
        )
        
        elapsed = time.time() - start_time
        result = response['message']['content']
        
        # Add timing info in debug mode
        if os.getenv('DEBUG'):
            result += f"\n\n_Response time: {elapsed:.2f}s_"
            
        return result
        
    except Exception as e:
        return f"Error: {str(e)}. Please ensure Ollama is running with llama3 model."

# Initialize session state efficiently
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False

# Quick action prompts - shorter for faster processing
QUICK_ACTIONS = {
    "About Company": "Tell me about CR IT Infopark in brief",
    "Job Careers": "What jobs are available at CR IT Infopark?",
    "Success Stories": "Share CR IT Infopark success stories",
    "Clients": "Who are CR IT Infopark's clients?",
    "Apply": "How to apply at CR IT Infopark?"
}

# Background model warm-up on first load
if 'warmed_up' not in st.session_state:
    st.session_state.warmed_up = False
    # Start warm-up in background thread
    if not MODEL_WARMED_UP:
        threading.Thread(target=warm_up_model, daemon=True).start()
    st.session_state.warmed_up = True

# UI Components
st.title("💻 REXA")
st.caption("Fast AI assistant for CR IT Infopark queries")

# Performance indicator
col1, col2 = st.columns([3, 1])
with col2:
    if MODEL_WARMED_UP:
        st.success("🟢 Ready")
    else:
        st.warning("🟡 Loading...")

# Quick action buttons
st.subheader("Quick Actions")
button_cols = st.columns(5)

for i, (label, prompt) in enumerate(QUICK_ACTIONS.items()):
    with button_cols[i]:
        if st.button(f"{['🏢', '💼', '📈', '🤝', '🔄'][i]} {label}", 
                    use_container_width=True,
                    disabled=st.session_state.processing):
            st.session_state.processing = True
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate response
            with st.spinner("Processing..."):
                response = generate_response_fast(prompt)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.processing = False
            st.rerun()

# Display chat history
st.subheader("Chat History")
for message in st.session_state.messages[-10:]:  # Show only last 10 messages for performance
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about CR IT Infopark...", disabled=st.session_state.processing):
    # Immediate user message display
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response with timing
    st.session_state.processing = True
    start_time = time.time()
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response_fast(prompt)
        
        elapsed = time.time() - start_time
        st.markdown(response)
        
        # Show timing if under debug
        if elapsed > 3.0:
            st.warning(f"Response time: {elapsed:.2f}s (target: <3s)")
        elif os.getenv('DEBUG'):
            st.info(f"Response time: {elapsed:.2f}s")
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.processing = False

# Performance tips in sidebar
with st.sidebar:
    st.header("Performance Tips")
    st.info("""
    **For faster responses:**
    - Keep questions concise
    - Use quick action buttons
    - Ensure stable internet connection
    - Make sure Ollama service is running locally
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    # Performance metrics
    if st.session_state.messages:
        st.metric("Total Messages", len(st.session_state.messages))
        st.metric("Model Status", "Ready" if MODEL_WARMED_UP else "Loading")

# Custom CSS for performance
st.markdown("""
<style>
    .stChatMessage {
        animation: none !important;
        transition: none !important;
    }
    .stButton > button {
        transition: all 0.1s ease !important;
    }
    .stSpinner > div {
        border-width: 2px !important;
    }
</style>
""", unsafe_allow_html=True)