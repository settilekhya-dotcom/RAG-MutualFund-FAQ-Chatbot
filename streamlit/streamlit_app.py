import streamlit as st
import os
import sys

# Add parent directory to path so src modules are discoverable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_engine import query_rag
from src.vector_store import initialize_vector_store, load_chunks

# --- Database Auto-Initialization (for Streamlit Cloud) ---
@st.cache_resource
def ensure_db_initialized():
    # Use paths relative to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "chroma_db")
    chunks_file = os.path.join(base_dir, "data", "processed_chunks.json")
    
    import chromadb
    from chromadb.utils import embedding_functions
    
    try:
        client = chromadb.PersistentClient(path=db_path)
        emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        # Check if re-indexing is needed
        try:
            collection = client.get_collection(name="icici_mf_facts", embedding_function=emb_fn)
            if collection.count() > 0:
                return  # Already initialized
        except Exception:
            pass # Collection doesn't exist
            
        if os.path.exists(chunks_file):
            with st.spinner("Indexing knowledge base... please wait."):
                chunks = load_chunks(chunks_file)
                collection = client.get_or_create_collection(name="icici_mf_facts", embedding_function=emb_fn)
                
                from src.static_knowledge import STATIC_DOCS
                ids = [c["chunk_id"] for c in chunks]
                documents = [c["text"] for c in chunks]
                metadatas = [c["metadata"] for c in chunks]
                for doc in STATIC_DOCS:
                    ids.append(doc["id"])
                    documents.append(doc["text"])
                    metadatas.append({"source": doc["source"], "title": doc["title"]})
                
                collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
                st.toast(f"✅ Indexed {collection.count()} items successfully!", icon="✅")
        else:
            st.error(f"Critical Error: Data file not found at {chunks_file}")
    except Exception as e:
        st.error(f"Initialization Failed: {str(e)}")

ensure_db_initialized()

# --- Page Configuration ---
st.set_page_config(
    page_title="Groww ICICI Prudential Fund Facts Assistant",
    page_icon="💼",
    layout="centered"
)

# --- Custom CSS for Refined Groww Aesthetic & Responsiveness ---
st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp {
        background-color: #0c0e12;
        color: #e0e0e0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    }
    
    /* Center the main content area with responsiveness */
    .block-container {
        max-width: 720px;
        width: 95%;
        padding-top: 3rem;
        margin: 0 auto;
    }
    
    /* Custom Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #171c24;
        border-right: 1px solid #2d343f;
    }

    /* Primary Accent Color (Groww Green) */
    .stButton>button {
        background-color: transparent !important;
        color: #00D09C !important;
        border: 1px solid #2d343f !important;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.2s ease;
        text-align: left !important;
        padding: 0.8rem 1.2rem !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        border-color: #00D09C !important;
        background-color: rgba(0, 208, 156, 0.05) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    /* Chat Message Bubbles */
    [data-testid="stChatMessage"] {
        background-color: #171c24 !important;
        border-radius: 12px !important;
        border: 1px solid #2d343f !important;
        margin-bottom: 1.2rem !important;
        padding: 1rem !important;
    }
    
    /* User Message Specific Styling */
    [data-testid="stChatMessageContent"] p {
        line-height: 1.6;
        font-size: 1rem;
    }

    /* Disclaimer Section */
    .disclaimer {
        background-color: rgba(242, 147, 57, 0.05);
        border: 1px solid rgba(242, 147, 57, 0.3);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2.5rem;
        color: #f29339;
        font-size: 0.85rem;
        text-align: center;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        padding: 2rem 0;
        font-size: 0.8rem;
        color: #636e72;
    }
    
    /* Header Styling */
    h1 {
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1.5rem;
        text-align: center;
        font-size: clamp(1.5rem, 5vw, 2.2rem);
    }
    
    .logo-text {
        color: #00D09C;
        font-weight: 800;
        font-size: 1.8rem;
        letter-spacing: -0.5px;
    }
    
    /* Chat Input Styling */
    .stChatInputContainer {
        border-radius: 12px !important;
        background-color: #171c24 !important;
        border: 1px solid #2d343f !important;
    }

    /* Mobile/Tablet Adjustments */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1.5rem;
        }
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Content ---
with st.sidebar:
    st.markdown('<div class="logo-text">Groww</div>', unsafe_allow_html=True)
    st.markdown("### Fund Facts Assistant")
    st.divider()
    
    # System Health Diagnostics
    with st.expander("🛠️ System Health", expanded=False):
        try:
            from src.rag_engine import get_collection
            coll = get_collection()
            count = coll.count()
            st.success(f"Database: {count} items")
            if st.button("Rebuild Knowledge Base"):
                # Force delete and re-index
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                db_path = os.path.join(base_dir, "data", "chroma_db")
                if os.path.exists(db_path):
                    import shutil
                    shutil.rmtree(db_path)
                st.cache_resource.clear()
                st.rerun()
        except Exception as e:
            st.error(f"DB Error: {str(e)}")
            if st.button("Attempt Repair"):
                st.cache_resource.clear()
                st.rerun()

    st.divider()
    st.markdown("#### 🚀 Capabilities")
    st.markdown("""
    - **Scheme Details**: NAV, Inception, Managers
    - **Rules**: Min SIP, Exit loads, Unit pricing
    - **Taxation**: ELSS 3-year lock-in rules
    - **How-To**: Downloading statements & reports
    """)
    
    st.divider()
    st.markdown("#### 🛡️ Factual Only")
    st.caption("I cannot provide advice, buy/sell calls, or predictions. I only provide data from official documents.")
    
    if st.button("Clear History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main UI ---
st.markdown("<h1>💼 ICICI Prudential Assistant</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    <strong>⚠️ Important:</strong> Factual information only. Not for investment advice. 
    Please consult a qualified financial advisor before investing.
</div>
""", unsafe_allow_html=True)

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Standardized Example Questions (Vertical) ---
example_queries = [
    "What is the expense ratio of ICICI Prudential Bluechip Fund?",
    "When does the lock-in period for ICICI Prudential ELSS end?",
    "What is the minimum SIP amount for ICICI Prudential Bluechip Fund?"
]

if not st.session_state.messages:
    st.markdown("### 👋 Hello! I'm the **Groww Fund Facts Assistant**.")
    st.markdown("I can help you with factual details about ICICI Prudential Mutual Fund schemes, such as NAV, expense ratios, lock-in periods, and more.")

st.markdown("##### Try asking:")
for q_text in example_queries:
    if st.button(q_text, key=f"btn_{q_text}", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": q_text})
        with st.spinner("Retrieving data..."):
            response = query_rag(q_text)
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Query fund facts (e.g., exit load, SIP min)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Handle Greetings
    greetings = ["hi", "hello", "hey", "hola", "namaste", "good morning", "good afternoon", "good evening"]
    is_greeting = any(prompt.lower().strip().startswith(g) for g in greetings) and len(prompt.split()) <= 3

    with st.chat_message("assistant"):
        if is_greeting:
            q_list = "\n".join([f"- {q}" for q in example_queries])
            greeting_resp = f"Hi there! 👋 I'm your **Groww Fund Facts Assistant**. Would you like to ask me something? Here are some things you can ask:\n\n{q_list}"
            st.markdown(greeting_resp)
            st.session_state.messages.append({"role": "assistant", "content": greeting_resp})
        else:
            with st.spinner("Checking records..."):
                response = query_rag(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# --- Footer ---
st.markdown("""
    <div class="footer">
        Sources: ICICI Prudential AMC, AMFI, SEBI official documents.
    </div>
""", unsafe_allow_html=True)
