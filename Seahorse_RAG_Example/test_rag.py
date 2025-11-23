"""
Test script for RAG_app.py with different chunk size configurations
"""

# Test questions about fungi
test_questions = [
    "What role do fungi play in forest ecosystems?",
    "How do fungi reproduce?",
    "What medical applications do fungi have?"
]

print("=" * 80)
print("RAG SYSTEM TEST - DEFAULT PARAMETERS")
print("chunk_size=500, chunk_overlap=50, top_k=20, top_m=8")
print("=" * 80)
print()

# Import the answer_question function from RAG_app
import sys
sys.path.insert(0, '.')

try:
    from RAG_app import answer_question
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*80}")
        print(f"QUESTION {i}: {question}")
        print('='*80)
        try:
            answer = answer_question(question)
            print(f"\nANSWER:\n{answer}")
        except Exception as e:
            print(f"\nERROR: {e}")
        print()
        
except ImportError as e:
    print(f"Error importing RAG_app: {e}")
    print("\nMake sure RAG_app.py is in the current directory and all dependencies are installed.")
