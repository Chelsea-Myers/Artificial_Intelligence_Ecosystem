# Symptom-to-Diagnosis Chatbot (Rule-Based AI System)# Sample submission for the Building a Rule-Based AI System in Python project.



------



## Part 1: Initial Project Ideas## Part 1: Initial Project Ideas



### 1. Project Idea 1: Symptom-to-Diagnosis Chatbot### 1. Project Idea 1: Recipe Recommender

- **Description:** A chatbot that analyzes user-described symptoms and provides basic health condition assessments with advice. The user describes their symptoms, and the system matches them to potential conditions using keyword-based rules.- **Description:** A system that recommends recipes based on ingredients the user has on hand. The user enters ingredients, and the system matches them to recipes using predefined rules.  

- **Rule-Based Approach:**  - **Rule-Based Approach:**  

  - The system checks for specific keyword combinations in the symptom description.  - The system checks for exact matches and partial matches with the ingredients required for recipes in a dataset.  

  - Different symptom patterns trigger different condition assessments and advice.  - Missing ingredients are suggested for partial matches.

  - **IMPORTANT:** This is NOT medical advice or a real diagnostic tool.

### 2. Project Idea 2: Simple Chatbot

### 2. Project Idea 2: Simple Conversational Chatbot- **Description:** A chatbot that responds to user inputs with predefined answers. The chatbot simulates a conversation by identifying keywords and phrases in user inputs.  

- **Description:** A chatbot that responds to user inputs with predefined answers. The chatbot simulates a conversation by identifying keywords and phrases in user inputs.  - **Rule-Based Approach:**  

- **Rule-Based Approach:**    - Responses are based on keywords such as "hello," "help," or "bye."  

  - Responses are based on keywords such as "hello," "help," or "bye."    - For example, if the user says "hello," the system responds with "Hi there! How can I assist you?"

  - For example, if the user says "hello," the system responds with "Hi there! How can I assist you?"

### 3. Project Idea 3: Travel Packing List Generator

### 3. Project Idea 3: Travel Packing List Generator- **Description:** A system that generates a packing list based on the user’s destination, climate, and trip duration.  

- **Description:** A system that generates a packing list based on the user's destination, climate, and trip duration.  - **Rule-Based Approach:**  

- **Rule-Based Approach:**    - The system uses rules to recommend items.  

  - The system uses rules to recommend items.    - For example, if the destination is "beach" and the climate is "hot," the system suggests sunscreen, swimsuits, and sunglasses.

  - For example, if the destination is "beach" and the climate is "hot," the system suggests sunscreen, swimsuits, and sunglasses.

### **Chosen Idea:** Recipe Recommender  

### **Chosen Idea:** Symptom-to-Diagnosis Chatbot  **Justification:** I chose this project because it is practical and applicable to real-life scenarios. It allows me to work with datasets, apply conditional logic, and create a system that provides meaningful recommendations based on user input.

**Justification:** I chose this project because it demonstrates how rule-based AI systems can process natural language input and apply conditional logic to provide relevant feedback. It's educational and shows the limitations of rule-based systems compared to machine learning approaches. The system emphasizes that it's not a medical professional and encourages users to seek real medical advice.

---

---

## Part 2: Rules/Logic for the Chosen System

## Part 2: Rules/Logic for the Chosen System

The **Recipe Recommender** system will follow these rules:

The **Symptom-to-Diagnosis Chatbot** system will follow these rules:

1. **Exact Match Rule:**  

1. **Emergency Symptoms Rule:**     - **IF** all ingredients in a recipe are found in the user’s ingredient list → **Recommend the recipe.**

   - **IF** symptoms include "chest pain" OR "difficulty breathing" OR "shortness of breath" → **Urgent warning to seek immediate medical help.**

2. **Partial Match Rule:**  

2. **Flu-like Illness Rule:**     - **IF** 75% or more of the ingredients in a recipe match the user’s ingredient list →  

   - **IF** symptoms include "fever" AND "cough" AND ("body aches" OR "chills" OR "sore muscles") → **Suggest flu-like illness with rest and hydration advice.**     - **Recommend the recipe.**  

     - **Suggest the missing ingredients.**

3. **Common Cold Rule:**  

   - **IF** symptoms include ("runny nose" OR "stuffy nose" OR "congestion") AND ("sore throat" OR "cough") AND NO high fever → **Suggest common cold with rest and OTC remedies.**3. **Common Ingredients Rule:**  

   - Ingredients like salt, pepper, and water are considered optional and will not be counted as missing.

4. **Allergy Rule:**  

   - **IF** symptoms include "sneezing" AND ("itchy eyes" OR "watery eyes") AND NO fever → **Suggest allergy-like symptoms with avoidance and antihistamine advice.**4. **No Match Rule:**  

   - **IF** no recipes match → **Suggest adding more ingredients** for better recommendations.

5. **Migraine Rule:**  

   - **IF** symptoms include "headache" AND ("light sensitivity" OR "sound sensitivity" OR "nausea") → **Suggest migraine-type headache with rest in dark/quiet room.**5. **Low Ingredient Rule:**  

   - **IF** fewer than three ingredients are provided → **Notify the user** and suggest adding more ingredients.

6. **General Fatigue Rule:**  

   - **IF** symptoms include "tired" OR "fatigue" OR "exhausted" → **Suggest general mild illness with rest and hydration.**---



7. **Unknown Condition Rule:**  ## Part 3: Rules/Logic for the Chosen System

   - **IF** no clear symptom pattern matches → **Acknowledge limitation and recommend professional consultation.**

Sample input and output: 

---

Enter your ingredients (comma-separated): chicken, rice, soy sauce

## Part 3: Sample Input and OutputYou are close to making Chicken Fried Rice! Missing: garlic.



Sample interactions with the chatbot:Enter your ingredients (comma-separated): garlic, soy sauce

No recipes match. Try adding more ingredients.

```

Describe your symptoms: I have a runny nose, sore throat, and coughEnter your ingredients (comma-separated): pasta, tomatoes, garlic, olive oil

You can make Spaghetti Pomodoro!

Possible condition: Common cold

Advice: Your symptoms sound like a common cold. Rest, stay hydrated, and consider ---

over-the-counter cold remedies if appropriate. If things get worse, check in with 

a healthcare provider.## Part 4: Reflection

```

### Project Overview:

```This project involved designing a practical, rule-based system to recommend recipes based on user inputs. The system uses logical conditions (e.g., exact and partial matches) to evaluate user-provided ingredients against recipes in the dataset.

Describe your symptoms: chest pain and shortness of breath

### Challenges:

Possible condition: Possible serious condition- **Handling Partial Matches:**  

Advice: Your symptoms could be serious. Please contact a healthcare professional   Deciding on a threshold (75%) that balances flexibility with accuracy was challenging.

or emergency services immediately. This chatbot is not a medical professional.- **Common Ingredients:**  

```  Ensuring common ingredients like salt and water don’t skew the results. I resolved this by excluding them from the missing ingredient list.



```

Describe your symptoms: sneezing and itchy watery eyes



Possible condition: Allergy-like symptoms

Advice: Your symptoms sound similar to allergies. Try to avoid possible triggers 

(like pollen or pets) and talk to a doctor or pharmacist about allergy medications 

if needed.

```



---



## Part 4: Reflection



### Project Overview:

This project demonstrates a rule-based AI system that processes natural language symptom descriptions and applies conditional logic to provide basic health condition assessments. The system uses IF-ELIF-ELSE statements and keyword matching to identify patterns in user input.

### Key Features:
- **Safety-first approach:** Prioritizes emergency symptoms and directs users to seek immediate help.
- **Multiple symptom patterns:** Covers common conditions like colds, flu, allergies, and migraines.
- **Clear disclaimers:** Emphasizes that this is NOT medical advice and NOT a diagnostic tool.

### Challenges:
- **Keyword matching limitations:**  
  The system relies on exact keyword matches, which means variations in phrasing might not be recognized. For example, "stuffy nose" is recognized but "blocked nose" might not be.
- **No context understanding:**  
  Unlike machine learning systems, this rule-based approach cannot understand context, severity levels, or complex symptom interactions.
- **Ethical considerations:**  
  Ensuring users understand this is a demonstration tool, not a medical diagnostic system, is critical.

### Learning Outcomes:
- Gained hands-on experience with rule-based AI systems and conditional logic.
- Understood the importance of clear user communication and ethical considerations in health-related applications.
- Recognized the limitations of rule-based systems compared to machine learning approaches.

---

## How to Run

1. Make sure you have Python 3.x installed
2. Run the program:
   ```
   python symptom_chatbot.py
   ```
3. Describe your symptoms when prompted
4. Type 'quit' or 'exit' to end the program

**Remember:** This is a demonstration of rule-based AI systems. It is NOT medical advice and NOT a real diagnostic tool. Always consult healthcare professionals for medical concerns.
