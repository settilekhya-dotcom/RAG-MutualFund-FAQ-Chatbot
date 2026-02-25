import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "chroma_db"
COLLECTION_NAME = "icici_mf_facts"
MODEL_NAME = "llama-3.3-70b-versatile"

# Opinion-detecting keywords to trigger the refusal guard
ADVICE_KEYWORDS = [
    "should i", "should i buy", "should i sell", "is it good", "is it worth",
    "recommend", "advise", "best fund", "better fund", "good investment",
    "will it", "will the", "will this", "predict", "forecast", "portfolio advice",
    "good returns", "give returns", "double my", "grow my money",
    "is this a good", "worth investing", "should i invest"
]

REFUSAL_MESSAGE = """I'm a facts-only assistant and cannot provide investment advice, recommendations, or opinions. For personalized guidance, please consult a qualified financial advisor.

Learn more about mutual fund basics at: https://groww.in/learn/mutual-funds"""

SYSTEM_PROMPT = """You are a factual FAQ assistant for ICICI Prudential Mutual Fund.
Your ONLY job is to answer factual questions about MF schemes using the context provided.
Rules you MUST follow:
1. Answer ONLY from the provided context. Do NOT use any outside knowledge.
2. Every answer MUST end with a source citation on a separate line at the very bottom, separated from the main text by TWO newlines.
3. Use the format:
   Source:
   <url>
4. If an answer involves steps or a process, you MUST format it as a numbered or bulleted markdown list. Put each step on a new line.
5. If the answer is NOT in the context, respond EXACTLY with the text in Rule 6.
6. Refusal text: "I'm a facts-only assistant and cannot provide investment advice, recommendations, or opinions. For personalized guidance, please consult a qualified financial advisor.\n\nLearn more about mutual fund basics at: https://groww.in/learn/mutual-funds"
7. NEVER provide investment advice, opinions, predictions, or recommendations.
8. Be factual, concise, and direct."""

def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )

def is_advice_query(query: str) -> bool:
    query_lower = query.lower()
    return any(kw in query_lower for kw in ADVICE_KEYWORDS)

def retrieve_context(collection, query: str, n_results: int = 3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append({"text": doc, "source": meta.get("source", ""), "title": meta.get("title", "")})
    return chunks

def build_prompt(query: str, context_chunks: list) -> str:
    context_str = ""
    for i, chunk in enumerate(context_chunks):
        context_str += f"\n[Source {i+1}: {chunk['source']}]\n{chunk['text']}\n"
    
    return f"""Context:
{context_str}

User Question: {query}

Instructions: Answer the question ONLY using the context above.
Your response MUST end with the source citation formatted exactly like this:

Source:
<url>"""

def query_rag(query: str) -> str:
    # Check for advice-seeking queries first
    if is_advice_query(query):
        return REFUSAL_MESSAGE
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return "Error: GROQ_API_KEY not set in environment. Please add it to your .env file."
    
    # Retrieve relevant context
    collection = get_collection()
    context_chunks = retrieve_context(collection, query)
    
    if not context_chunks:
        return REFUSAL_MESSAGE
    
    # Build prompt and call Groq
    prompt = build_prompt(query, context_chunks)
    client = Groq(api_key=groq_api_key)
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=512
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    # Quick test
    test_queries = [
        "What is the expense ratio of ICICI Prudential Bluechip Fund?",
        "What is the lock-in period for ICICI Prudential ELSS Tax Saver Fund?",
        "Should I buy ICICI Prudential Flexicap Fund?"
    ]
    for q in test_queries:
        print(f"\nQ: {q}")
        print(f"A: {query_rag(q)}")
        print("-" * 60)
