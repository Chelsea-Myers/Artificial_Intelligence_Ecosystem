# 3.1 Suppress Noisy Logs
import logging
from transformers import logging as hf_logging
import warnings

# Set log levels to ERROR for specific loggers
logging.getLogger("langchain.text_splitter").setLevel(logging.ERROR)
hf_logging.set_verbosity_error()

# Filter Python warnings
warnings.filterwarnings("ignore")

# 3.2 ChatGPT API Credentials
from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

# Read the OpenAI API key and set it
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

# 3.3 Parameters
chunk_size = 500
chunk_overlap = 50
model_name = "sentence-transformers/all-distilroberta-v1"
top_k = 20

# Re-ranking parameters
cross_encoder_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
top_m = 8

# 3.4 Read the Pre-scraped Document
with open("Selected_Document.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 3.5 Split into Appropriately-Sized Chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
)
chunks = text_splitter.split_text(text)

# 3.6 Embed & Build FAISS Index
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Load the embedding model
model = SentenceTransformer(model_name)

# Encode chunks with progress bar
embeddings = model.encode(chunks, show_progress_bar=True)

# Convert to NumPy float32 array
embeddings = np.array(embeddings, dtype=np.float32)

# Initialize FAISS IndexFlatL2 with correct dimension
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add embeddings to the index
index.add(embeddings)

# 3.7 Retrieval Function
def retrieve_chunks(question, k=top_k):
    """
    Retrieve the top k most relevant chunks for a given question.
    
    Args:
        question (str): The user's question
        k (int): Number of chunks to retrieve (default: top_k)
    
    Returns:
        list: List of the top k relevant text chunks
    """
    # Encode the question
    q_vec = model.encode([question], show_progress_bar=False)
    
    # Convert to NumPy float32 array
    q_arr = np.array(q_vec, dtype=np.float32)
    
    # Search FAISS index for top k nearest neighbors
    distances, I = index.search(q_arr, k)
    
    # Return corresponding text chunks
    retrieved_chunks = [chunks[i] for i in I[0]]
    return retrieved_chunks

# 3.8 Implement a Cross-Encoder Re-Ranker
from sentence_transformers import CrossEncoder

# Initialize the cross-encoder model
reranker = CrossEncoder(cross_encoder_name)

def dedupe_preserve_order(items):
    """
    Remove duplicates while preserving first occurrence order.
    Normalizes whitespace to avoid near-duplicate slices.
    
    Args:
        items (list): List of text chunks
    
    Returns:
        list: Deduplicated list
    """
    seen = set()
    result = []
    for item in items:
        # Normalize whitespace
        normalized = " ".join(item.split())
        if normalized not in seen:
            seen.add(normalized)
            result.append(item)
    return result

def rerank_chunks(question, candidate_chunks, m=top_m):
    """
    Re-rank candidate chunks using a cross-encoder and return top m.
    
    Args:
        question (str): The user's question
        candidate_chunks (list[str]): List of candidate text chunks
        m (int): Number of top chunks to return (default: top_m)
    
    Returns:
        list[str]: Top m re-ranked chunks after deduplication
    """
    # Create (question, chunk) pairs
    pairs = [(question, chunk) for chunk in candidate_chunks]
    
    # Score pairs with cross-encoder (higher = more relevant)
    scores = reranker.predict(pairs)
    
    # Sort by score descending and select top m
    scored_chunks = list(zip(candidate_chunks, scores))
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    
    # Select top m chunks
    top_chunks = [chunk for chunk, score in scored_chunks[:m]]
    
    # Light deduplication
    top_chunks = dedupe_preserve_order(top_chunks)
    
    return top_chunks

# 3.9 Q&A with ChatGPT
def answer_question(question):
    """
    Answer a question using RAG: retrieve chunks, re-rank, and query ChatGPT.
    
    Args:
        question (str): The user's question
    
    Returns:
        str: The assistant's answer
    """
    # Step 1: Retrieve candidate chunks (top_k = 20)
    candidates = retrieve_chunks(question, k=top_k)
    
    # Step 2: Re-rank and get top_m chunks
    relevant_chunks = rerank_chunks(question, candidates, m=top_m)
    
    # Step 3: Join chunks into a single context string
    context = "\n\n".join(relevant_chunks)
    
    # Step 4: Define system prompt
    system_prompt = (
        "You are a knowledgeable assistant that answers questions based on the provided context. "
        "If the answer is not in the context, say you don't know."
    )
    
    # Step 5: Build user prompt
    user_prompt = f"""Context:
{context}

Question: {question}

Answer:"""
    
    # Step 6: Call OpenAI Chat Completions API
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0,
        max_tokens=500
    )
    
    # Step 7: Return the assistant's reply
    answer = response.choices[0].message.content.strip()
    return answer

# 3.10 Interactive Loop
if __name__ == "__main__":
    print("RAG Q&A System Ready!")
    print("Enter 'exit' or 'quit' to end.")
    print()
    
    while True:
        question = input("Your question: ")
        if question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        print("Answer:", answer_question(question))
        print()
