# RAG System for Fungi Document Q&A

## Description of the Document Selected

I selected a comprehensive document about **fungi and their ecological roles**. The document covers:

- **Classification and Biology:** Fungi as a distinct kingdom, including yeasts, molds, and mushrooms
- **Ecological Roles:** Decomposition, nutrient cycling, and energy flow in ecosystems
- **Symbiotic Relationships:** Mycorrhizal associations with plants, the "wood wide web" network
- **Reproduction:** Spore-based reproduction (sexual and asexual), hyphal networks and mycelium
- **Human Applications:** Food (mushrooms, fermentation), medicine (penicillin, immunosuppressants), bioremediation
- **Forest Ecosystems:** Wood and leaf litter decomposition, underground fungal networks
- **Diversity:** Estimated 2.2-3.8 million species, with only ~150,000 formally described
- **Environmental Adaptation:** Fungi in extreme environments and their role in climate change

This document was chosen because it provides rich, interconnected information ideal for testing RAG retrieval across different topics and question types.

---

## RAG System Test Questions and Answers

### Experiment 1: Default Parameters (chunk_size=500, chunk_overlap=50)

**Question 1: What role do fungi play in forest ecosystems?**

**Answer:** Fungi play an essential role in decomposing wood and leaf litter in forest ecosystems. Many forest fungi form mycorrhizal associations with trees, creating vast underground networks that connect multiple plants. These networks, sometimes called the 'wood wide web,' allow trees to share nutrients and even communicate with each other through chemical signals.

---

**Question 2: How do fungi reproduce?**

**Answer:** Fungi reproduce through spores, which can be sexual or asexual. These spores are often distributed by wind, water, or animals. When a spore lands in a suitable environment, it germinates and forms a new fungal organism.

---

**Question 3: What medical applications do fungi have?**

**Answer:** Fungi have been used in traditional medicine for centuries, and modern science has validated many of these uses. The antibiotic penicillin, discovered by Alexander Fleming, is produced by the Penicillium fungus. Other medically important compounds derived from fungi include immunosuppressants, cholesterol-lowering drugs, and anticancer agents.

---

## Analysis: Chunk Size and Overlap Experiments

### Experiment 2: Larger Chunks (chunk_size=800, chunk_overlap=100)

**Observations:**
- **More comprehensive answers** with additional context
- Answers included connecting information between concepts
- Example: Forest ecosystem answer added "This makes fungi excellent decomposers in ecosystems, as they convert hard-to-digest polysaccharides into simpler molecules"
- **Trade-off:** Potentially more verbose, may include some less relevant details

### Experiment 3: Smaller Chunks (chunk_size=300, chunk_overlap=30)

**Observations:**
- **More concise answers** but sometimes incomplete
- Lost connecting context between related concepts
- Example: Reproduction answer became "Fungi reproduce through spores. Spores are distributed by wind, water, or animals." (missing germination and mycelium formation)
- **Trade-off:** Faster retrieval but fragmented information

### Key Findings:

1. **Chunk Size Impact:**
   - **500 characters** provides optimal balance between detail and focus
   - **800 characters** gives more complete context but risks diluting relevance
   - **300 characters** is too small, causing information fragmentation

2. **Overlap Impact:**
   - **10% overlap (50/500)** prevents splitting of key concepts at chunk boundaries
   - Too little overlap risks breaking multi-sentence explanations
   - Too much overlap (>20%) creates redundancy without significant benefit

3. **Recommendation:**
   - **chunk_size=500, chunk_overlap=50** is optimal for this document
   - Provides complete concept coverage while maintaining focused retrieval
   - Balances answer quality with retrieval speed

---

## Five Deep-Dive Questions About the RAG System

### Question 1: What is embedding dimensionality and why does it matter for RAG systems?

**Answer:**
Embedding dimensionality refers to the number of dimensions in the vector representation of text. In this RAG system, we use the "all-distilroberta-v1" model which produces 768-dimensional embeddings. Each dimension captures different semantic features of the text.

**Why it matters:**
- Higher dimensions can capture more nuanced semantic relationships
- More dimensions require more storage and computation
- The dimension must match between the query embedding and document embeddings for similarity search
- 768 dimensions is a sweet spot balancing expressiveness and efficiency

**In the code:**
```python
model = SentenceTransformer(model_name)  # Creates 768-dim embeddings
dimension = embeddings.shape[1]  # Gets dimension (768)
index = faiss.IndexFlatL2(dimension)  # FAISS index matches this dimension
```

---

### Question 2: How does FAISS IndexFlatL2 search work and what are its trade-offs?

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

**In the code:**
```python
index = faiss.IndexFlatL2(dimension)  # Exact search
distances, I = index.search(q_arr, k)  # Returns k nearest neighbors
```

---

### Question 3: Why is chunk overlap important and how does it prevent information loss?

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

---

### Question 4: What is the purpose of the cross-encoder re-ranker and how does it differ from bi-encoder embeddings?

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
- Bi-encoder: Fast initial filtering (search millions of documents in milliseconds)
- Cross-encoder: Precise final selection (score only 20 candidates)
- Best of both worlds: Speed + Accuracy

**In the code:**
```python
# Stage 1: Fast retrieval with bi-encoder
candidates = retrieve_chunks(question, k=top_k)  # Get 20 candidates

# Stage 2: Accurate re-ranking with cross-encoder
relevant_chunks = rerank_chunks(question, candidates, m=top_m)  # Keep 8 best
```

---

### Question 5: How does prompt design affect RAG answer quality and what strategies prevent hallucination?

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

---

## How These Components Work Together

1. **Document Processing:** Text → Chunks (with overlap) → Embeddings (768-dim)
2. **Indexing:** Embeddings → FAISS IndexFlatL2 (exact search)
3. **Query Stage 1:** Question → Embedding → FAISS search → Top 20 candidates
4. **Query Stage 2:** Cross-encoder re-ranks 20 → Best 8 chunks
5. **Answer Generation:** 8 chunks + Question → GPT-4 (with anti-hallucination prompt) → Answer

Each component has specific trade-offs that balance accuracy, speed, and reliability.

---

## Installation and Usage

### Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env
```

### Run Text Extraction
```bash
python text_extractor.py
```

### Run RAG System
```bash
python RAG_app.py
```

Then ask your questions interactively. Type 'exit' or 'quit' to end.
