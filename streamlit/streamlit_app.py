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
    
    if not os.path.exists(db_path):
        if os.path.exists(chunks_file):
            with st.spinner("Initializing knowledge base for first run..."):
                chunks = load_chunks(chunks_file)
                # Ensure the vector store uses the absolute path
                import chromadb
                client = chromadb.PersistentClient(path=db_path)
                from chromadb.utils import embedding_functions
                emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
                collection = client.get_or_create_collection(name="icici_mf_facts", embedding_function=emb_fn)
                
                # Re-using the logic from vector_store but with explicit paths
                from src.static_knowledge import STATIC_DOCS
                ids = [c["chunk_id"] for c in chunks]
                documents = [c["text"] for c in chunks]
                metadatas = [c["metadata"] for c in chunks]
                for doc in STATIC_DOCS:
                    ids.append(doc["id"])
                    documents.append(doc["text"])
                    metadatas.append({"source": doc["source"], "title": doc["title"]})
                collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        else:
            st.error(f"Missing knowledge base: {chunks_file} not found.")

ensure_db_initialized()

# --- Page Configuration ---
st.set_page_config(
    page_title="Groww ICICI Prudential Fund Facts Assistant",
    page_icon="💼",
    layout="centered"
)

# --- Custom CSS for Refined Groww Aesthetic ---
st.markdown("""
    <style>
    .stApp { background-color: #0c0e12; color: #e0e0e0; }
    .block-container { max-width: 720px; width: 95%; padding-top: 3rem; margin: 0 auto; }
    [data-testid="stSidebar"] { background-color: #171c24; border-right: 1px solid #2d343f; }
    .stButton>button {
        background-color: transparent !important; color: #00D09C !important;
        border: 1px solid #2d343f !important; border-radius: 10px;
        width: 100%; text-align: left !important;
    }
    .stButton>button:hover { border-color: #00D09C !important; background-color: rgba(0, 208, 156, 0.05) !important; }
    [data-testid="stChatMessage"] { background-color: #171c24 !important; border-radius: 12px !important; border: 1px solid #2d343f !important; }
    .disclaimer { background-color: rgba(242, 147, 57, 0.05); border: 1px solid rgba(242, 147, 57, 0.3); padding: 1rem; border-radius: 10px; color: #f29339; font-size: 0.85rem; text-align: center; }
    .footer { text-align: center; padding: 2rem 0; font-size: 0.8rem; color: #636e72; }
    .logo-text { color: #00D09C; font-weight: 800; font-size: 1.8rem; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="logo-text">Groww</div>', unsafe_allow_html=True)
    st.markdown("### Fund Facts Assistant")
    st.divider()
    st.markdown("#### 🚀 Capabilities\n- Scheme Details\n- Rules & Loads\n- Taxation\n- How-To Guides")
    if st.button("Clear History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main UI ---
st.markdown("<h1>💼 ICICI Prudential Assistant</h1>", unsafe_allow_html=True)
st.markdown('<div class="disclaimer"><strong>⚠️ Important:</strong> Factual information only. Not for investment advice.</div>', unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []

example_queries = [
    "What is the expense ratio of ICICI Prudential Bluechip Fund?",
    "When does the lock-in period for ICICI Prudential ELSS end?",
    "What is the minimum SIP amount for ICICI Prudential Bluechip Fund?"
]

if not st.session_state.messages:
    st.markdown("### 👋 Hello! I'm the **Groww Fund Facts Assistant**.")

st.markdown("##### Try asking:")
for q_text in example_queries:
    if st.button(q_text, key=f"btn_{q_text}", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": q_text})
        with st.spinner("Retrieving data..."):
            response = query_rag(q_text)
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

if prompt := st.chat_input("Query fund facts..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    greetings = ["hi", "hello", "hey"]
    is_greeting = any(prompt.lower().strip().startswith(g) for g in greetings) and len(prompt.split()) <= 3

    with st.chat_message("assistant"):
        if is_greeting:
            greeting_resp = "Hi there! 👋 I'm your **Groww Fund Facts Assistant**. How can I help you today?"
            st.markdown(greeting_resp)
            st.session_state.messages.append({"role": "assistant", "content": greeting_resp})
        else:
            with st.spinner("Checking records..."):
                response = query_rag(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown('<div class="footer">Sources: ICICI Prudential AMC, AMFI, SEBI.</div>', unsafe_allow_html=True)
