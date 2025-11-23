# Deep-Dive Questions About the RAG System

## Question 1: What is embedding dimensionality and why does it matter for RAG systems?

**Answer:**
Embedding dimensionality refers to the number of dimensions in the vector representation of text. In this RAG system, we use the "all-distilroberta-v1" model which produces 768-dimensional embeddings. Each dimension captures different semantic features of the text.

**Why it matters:**
- Higher dimensions can capture more nuanced semantic relationships
- More dimensions require more storage and computation
- The dimension must match between the query embedding and document embeddings for similarity search
- 768 dimensions is a sweet spot balancing expressiveness and efficiency

**In our code:**
```python
model = SentenceTransformer(model_name)  # Creates 768-dim embeddings
dimension = embeddings.shape[1]  # Gets dimension (768)
index = faiss.IndexFlatL2(dimension)  # FAISS index matches this dimension
```

---

## Question 2: How does FAISS IndexFlatL2 search work and what are its trade-offs?

**Answer:**
FAISS IndexFlatL2 performs exhaustive nearest neighbor search using L2 (Euclidean) distance. It computes the distance between the query vector and every vector in the index.

**How it works:**
1. Query vector is encoded into the same dimensional space as documents
2. FAISS calculates L2 distance: sqrt(Σ(query[i] - doc[i])²) for each document
3. Returns the k documents with smallest distances (closest matches)

**Trade-offs:**
- **Pros:** Exact search (no approximation), simple, guaranteed to find true nearest neighbors
- **Cons:** Slow for large datasets (O(n) complexity), not scalable beyond ~100k vectors
- **Alternatives:** IndexIVFFlat (faster but approximate), IndexHNSW (graph-based, very fast)

**In our code:**
```python
index = faiss.IndexFlatL2(dimension)  # Exact search
distances, I = index.search(q_arr, k)  # Returns k nearest neighbors
```

---

## Question 3: Why is chunk overlap important and how does it prevent information loss?

**Answer:**
Chunk overlap creates redundancy at chunk boundaries, ensuring that information spanning multiple chunks isn't split awkwardly.

**The problem without overlap:**
```
Chunk 1: "...fungi form mycorrhizal associat"
Chunk 2: "ions with trees, creating vast..."
```
The concept "mycorrhizal associations" is split, making it hard to retrieve.

**With overlap (50 characters):**
```
Chunk 1: "...fungi form mycorrhizal associations with trees..."
Chunk 2: "...mycorrhizal associations with trees, creating vast..."
```
Now both chunks contain the complete concept.

**Trade-offs:**
- **Optimal overlap:** 10-20% of chunk_size (our 50/500 = 10%)
- **Too little:** Risk splitting important information
- **Too much:** Redundant storage, slower retrieval, potential duplicate results
- **Our deduplication:** `dedupe_preserve_order()` removes near-duplicates after re-ranking

**In our code:**
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,  # 10% overlap
)
```

---

## Question 4: What is the purpose of the cross-encoder re-ranker and how does it differ from bi-encoder embeddings?

**Answer:**
The system uses a two-stage retrieval approach:

**Stage 1 - Bi-Encoder (Fast Retrieval):**
- Encodes queries and documents separately into fixed-size vectors
- Uses FAISS for fast similarity search
- Retrieves top_k=20 candidates
- Fast but less accurate (can't see query-document interactions)

**Stage 2 - Cross-Encoder (Accurate Re-ranking):**
- Takes (query, document) pairs and scores them together
- Model sees both query and document simultaneously
- Can capture fine-grained relevance
- Slower but much more accurate
- Re-ranks 20 candidates down to top_m=8 best matches

**Why this architecture?**
- Bi-encoder: Fast initial filtering (search millions of documents in ms)
- Cross-encoder: Precise final selection (score only 20 candidates)
- Best of both worlds: Speed + Accuracy

**In our code:**
```python
# Stage 1: Fast retrieval with bi-encoder
candidates = retrieve_chunks(question, k=top_k)  # Get 20 candidates

# Stage 2: Accurate re-ranking with cross-encoder
relevant_chunks = rerank_chunks(question, candidates, m=top_m)  # Keep 8 best
```

**Cross-encoder scoring:**
```python
pairs = [(question, chunk) for chunk in candidate_chunks]
scores = reranker.predict(pairs)  # Scores each (Q, chunk) pair
```

---

## Question 5: How does prompt design affect RAG answer quality and what strategies prevent hallucination?

**Answer:**
The prompt is the final critical step where retrieved context meets the LLM. Poor prompt design can lead to hallucinations (making up information) even with perfect retrieval.

**Our Prompt Strategy:**

1. **System Prompt - Sets Boundaries:**
```python
system_prompt = (
    "You are a knowledgeable assistant that answers questions based on the "
    "provided context. If the answer is not in the context, say you don't know."
)
```
- Explicitly instructs to use ONLY provided context
- Tells model to admit when it doesn't know
- Prevents relying on training data

2. **User Prompt - Provides Context:**
```python
user_prompt = f"""Context:
{context}

Question: {question}

Answer:"""
```
- Clearly labels the context section
- Separates question from context
- Simple structure reduces confusion

**Anti-Hallucination Strategies:**
- ✓ "based on the provided context" - Constrains source
- ✓ "say you don't know" - Allows uncertainty
- ✓ temperature=0.0 - Deterministic, less creative
- ✓ Context first, then question - Clear information hierarchy
- ✓ Re-ranking ensures relevant chunks - Better context quality

**What NOT to do:**
- ❌ "Use your knowledge to answer..." - Encourages hallucination
- ❌ High temperature - More creative but less accurate
- ❌ Vague instructions - Model fills gaps with training data
- ❌ No context label - Model confuses context with general knowledge

**In our code:**
```python
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.0,  # Deterministic
    max_tokens=500
)
```

---

## Summary: How These Components Work Together

1. **Document Processing:** Text → Chunks (with overlap) → Embeddings (768-dim)
2. **Indexing:** Embeddings → FAISS IndexFlatL2 (exact search)
3. **Query Stage 1:** Question → Embedding → FAISS search → Top 20 candidates
4. **Query Stage 2:** Cross-encoder re-ranks 20 → Best 8 chunks
5. **Answer Generation:** 8 chunks + Question → GPT-4 (with anti-hallucination prompt) → Answer

Each component has specific trade-offs that balance accuracy, speed, and reliability.
