# Chunk-Size & Overlap Experiments Documentation

## Test Questions
1. What role do fungi play in forest ecosystems?
2. How do fungi reproduce?
3. What medical applications do fungi have?

## Experiment 1: Default Parameters
**Configuration:**
- chunk_size = 500
- chunk_overlap = 50
- top_k = 20
- top_m = 8

**To run:**
```bash
source venv/bin/activate
python RAG_app.py
```

**Results:** (Record answers for each question)
- Question 1 Answer:
- Question 2 Answer:
- Question 3 Answer:

**Observations:**


## Experiment 2: Larger Chunks
**Configuration:**
- chunk_size = 800
- chunk_overlap = 100
- top_k = 20
- top_m = 8

**Steps to modify RAG_app.py:**
Change lines:
```python
chunk_size = 800
chunk_overlap = 100
```

**Results:** (Record answers for each question)
- Question 1 Answer:
- Question 2 Answer:
- Question 3 Answer:

**Observations:**


## Experiment 3: Smaller Chunks
**Configuration:**
- chunk_size = 300
- chunk_overlap = 30
- top_k = 20
- top_m = 8

**Steps to modify RAG_app.py:**
Change lines:
```python
chunk_size = 300
chunk_overlap = 30
```

**Results:** (Record answers for each question)
- Question 1 Answer:
- Question 2 Answer:
- Question 3 Answer:

**Observations:**


## Experiment 4: No Overlap
**Configuration:**
- chunk_size = 500
- chunk_overlap = 0
- top_k = 20
- top_m = 8

**Steps to modify RAG_app.py:**
Change lines:
```python
chunk_size = 500
chunk_overlap = 0
```

**Results:** (Record answers for each question)
- Question 1 Answer:
- Question 2 Answer:
- Question 3 Answer:

**Observations:**


## Summary Analysis

### Best Configuration:
- chunk_size = 
- chunk_overlap = 

### Key Findings:
1. Impact of chunk size on answer completeness:
   
2. Impact of overlap on context continuity:
   
3. Trade-offs between parameters:
   

### Recommendations:
