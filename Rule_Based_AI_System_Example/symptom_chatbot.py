"""
Symptom-to-Diagnosis Chatbot (Rule-Based)

This program is a simple example of a rule-based AI system.
It does NOT use machine learning. Instead, it uses IF-ELIF-ELSE
rules to give basic, non-professional feedback based on
keywords found in the user's description of symptoms.

IMPORTANT: This is NOT medical advice or a real diagnostic tool.
"""

def diagnose(symptoms_text):
    """
    Take the user's symptom description (already converted to lowercase)
    and apply rule-based logic to return a (condition, advice) pair.
    """

    text = symptoms_text  # shorter name for convenience

    # --- Rule 1: General safety / emergency-type symptoms ---
    if ("chest pain" in text or
        "difficulty breathing" in text or
        "shortness of breath" in text):
        condition = "Possible serious condition"
        advice = (
            "Your symptoms could be serious. "
            "Please contact a healthcare professional or emergency services immediately. "
            "This chatbot is not a medical professional."
        )
        return condition, advice

    # --- Rule 2: Flu-like illness ---
    if ("fever" in text and "cough" in text and
        ("body aches" in text or "chills" in text or "sore muscles" in text)):
        condition = "Flu-like illness"
        advice = (
            "Your symptoms sound like a flu-like illness. "
            "Consider resting, drinking plenty of fluids, and monitoring your temperature. "
            "Talk to a doctor if your symptoms are severe or do not improve."
        )
        return condition, advice

    # --- Rule 3: Common cold ---
    if (("runny nose" in text or "stuffy nose" in text or "congestion" in text)
        and ("sore throat" in text or "scratchy throat" in text or "cough" in text)
        and ("high fever" not in text and "102" not in text)):
        condition = "Common cold"
        advice = (
            "Your symptoms sound like a common cold. "
            "Rest, stay hydrated, and consider over-the-counter cold remedies if appropriate. "
            "If things get worse, check in with a healthcare provider."
        )
        return condition, advice

    # --- Rule 4: Allergies ---
    if ("sneezing" in text and
        ("itchy eyes" in text or "watery eyes" in text or "itchy nose" in text) and
        ("fever" not in text and "temperature" not in text)):
        condition = "Allergy-like symptoms"
        advice = (
            "Your symptoms sound similar to allergies. "
            "Try to avoid possible triggers (like pollen or pets) and talk to a doctor "
            "or pharmacist about allergy medications if needed."
        )
        return condition, advice

    # --- Rule 5: Headache / migraine-like ---
    if ("headache" in text and
        ("light sensitivity" in text or "sensitive to light" in text or
         "sound sensitivity" in text or "nausea" in text)):
        condition = "Migraine-like headache"
        advice = (
            "Your symptoms sound like a migraine-type headache. "
            "Rest in a dark, quiet room and stay hydrated. "
            "If this is severe, new, or different from your usual headaches, "
            "contact a healthcare professional."
        )
        return condition, advice

    # --- Rule 6: General mild illness / fatigue ---
    if ("tired" in text or "fatigue" in text or "exhausted" in text or "not feeling well" in text):
        condition = "General mild illness / fatigue"
        advice = (
            "You may be experiencing general fatigue or a mild illness. "
            "Try resting, drinking water, and taking care of yourself. "
            "If you are worried or things do not improve, see a doctor."
        )
        return condition, advice

    # --- Rule 7: No clear match ---
    condition = "Unknown / unclear"
    advice = (
        "I am not sure what your symptoms might indicate based on what you typed. "
        "This simple rule-based chatbot is very limited. "
        "Please contact a healthcare professional for real medical advice."
    )
    return condition, advice


def main():
    """
    Main loop of the program.
    Gets user input, calls diagnose(), and prints the result.
    """

    print("Welcome to the Symptom Helper (Rule-Based Chatbot)")
    print("--------------------------------------------------")
    print("This is NOT medical advice and NOT a real diagnosis tool.")
    print("It just demonstrates how rule-based AI systems work.\n")

    while True:
        user_input = input("Describe your symptoms (or type 'quit' to exit): ").strip()

        # Allow the user to exit the program
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye! Take care of your health.")
            break

        # Convert to lowercase for easier keyword matching
        symptoms_lower = user_input.lower()

        # Apply the rule-based diagnosis
        condition, advice = diagnose(symptoms_lower)

        # Show the result
        print("\nPossible condition:", condition)
        print("Advice:", advice)
        print("\n----------------------------------------\n")


# Run the program only if this file is executed directly
if __name__ == "__main__":
    main()
