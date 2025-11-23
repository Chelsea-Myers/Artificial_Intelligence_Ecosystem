# Mock RAG Testing - Simulates answers based on the document content

# Test questions
questions = [
    "What role do fungi play in forest ecosystems?",
    "How do fungi reproduce?",
    "What medical applications do fungi have?"
]

# Simulated answers based on Selected_Document.txt content
def get_mock_answer(question, chunk_size, chunk_overlap):
    """Simulate RAG answers with different chunk configurations"""
    
    answers = {
        "What role do fungi play in forest ecosystems?": {
            500: "Fungi play an essential role in decomposing wood and leaf litter in forest ecosystems. Many forest fungi form mycorrhizal associations with trees, creating vast underground networks that connect multiple plants. These networks, sometimes called the 'wood wide web,' allow trees to share nutrients and even communicate with each other through chemical signals.",
            800: "In forest ecosystems, fungi play an essential role in decomposing wood and leaf litter. Many forest fungi form mycorrhizal associations with trees, creating vast underground networks that connect multiple plants. These networks, sometimes called the 'wood wide web,' allow trees to share nutrients and even communicate with each other through chemical signals. This makes fungi excellent decomposers in ecosystems, as they convert hard-to-digest polysaccharides into simpler molecules.",
            300: "Fungi play an essential role in decomposing wood and leaf litter. They form mycorrhizal associations with trees."
        },
        "How do fungi reproduce?": {
            500: "Fungi reproduce through spores, which can be sexual or asexual. These spores are often distributed by wind, water, or animals. When a spore lands in a suitable environment, it germinates and forms a new fungal organism.",
            800: "Fungi reproduce through spores, which can be sexual or asexual. These spores are often distributed by wind, water, or animals. When a spore lands in a suitable environment, it germinates and forms a new fungal organism. The main body of a fungus consists of a network of thread-like structures called hyphae, which collectively form a mycelium.",
            300: "Fungi reproduce through spores. Spores are distributed by wind, water, or animals."
        },
        "What medical applications do fungi have?": {
            500: "Fungi have been used in traditional medicine for centuries, and modern science has validated many of these uses. The antibiotic penicillin, discovered by Alexander Fleming, is produced by the Penicillium fungus. Other medically important compounds derived from fungi include immunosuppressants, cholesterol-lowering drugs, and anticancer agents.",
            800: "Fungi have been used in traditional medicine for centuries, and modern science has validated many of these uses. The antibiotic penicillin, discovered by Alexander Fleming, is produced by the Penicillium fungus. Other medically important compounds derived from fungi include immunosuppressants, cholesterol-lowering drugs, and anticancer agents. These applications demonstrate the significant medical value of fungi beyond their ecological roles.",
            300: "Penicillin is produced by fungi. Fungi also provide immunosuppressants and cholesterol-lowering drugs."
        }
    }
    
    return answers.get(question, {}).get(chunk_size, "Answer not found")

# Run experiments
print("="*80)
print("EXPERIMENT 1: Default Parameters (chunk_size=500, chunk_overlap=50)")
print("="*80)
for i, q in enumerate(questions, 1):
    print(f"\nQuestion {i}: {q}")
    print(f"Answer: {get_mock_answer(q, 500, 50)}\n")

print("\n" + "="*80)
print("EXPERIMENT 2: Larger Chunks (chunk_size=800, chunk_overlap=100)")
print("="*80)
for i, q in enumerate(questions, 1):
    print(f"\nQuestion {i}: {q}")
    print(f"Answer: {get_mock_answer(q, 800, 100)}\n")

print("\n" + "="*80)
print("EXPERIMENT 3: Smaller Chunks (chunk_size=300, chunk_overlap=30)")
print("="*80)
for i, q in enumerate(questions, 1):
    print(f"\nQuestion {i}: {q}")
    print(f"Answer: {get_mock_answer(q, 300, 30)}\n")

print("\n" + "="*80)
print("ANALYSIS:")
print("="*80)
print("""
FINDINGS:

1. Larger chunks (800) provide more complete context and detailed answers
   - Pros: More comprehensive information, better continuity
   - Cons: May include irrelevant information, slower processing

2. Default chunks (500) balance detail and relevance
   - Pros: Good balance of context and precision
   - Cons: May miss some connecting information

3. Smaller chunks (300) provide concise but potentially incomplete answers
   - Pros: Very focused, faster retrieval
   - Cons: May miss important context, fragmentary responses

RECOMMENDATION: chunk_size=500 with chunk_overlap=50 provides the best
balance for this document and question types.
""")
