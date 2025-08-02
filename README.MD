# 🧠 Financial Planning Agent – Valura.ai Task

An AI-powered financial planning assistant built with **LangChain**, **Ollama**, and **Streamlit**. This interactive agent collects a user’s financial profile, performs retirement-related calculations using proven formulas, and answers natural-language questions like:

- “When can I retire?”
- “How much should I save monthly?”
- “Is it better to invest or pay off my mortgage?”
- “What if inflation is 6%?”

---

## 🚀 Features

### ✅ 1. Persona Builder
- Asks friendly questions to collect:
  - Age, income, savings, retirement goals, expenses, etc.
- Stores user data in memory for dynamic follow-ups.

### ✅ 2. Formula Engine
Implements core financial formulas as pure Python functions (fully unit tested):
- **Future Value**: `FV = PV × (1 + r)^n`
- **Present Value**: `PV = FV / (1 + r)^n`
- **FV of Annuity**: `FV = PMT × [(1 + r)^n – 1] / r`
- **PV of Annuity**: `PV = PMT × [1 – (1 + r)^–n] / r`
- **NPER (Time to Goal)**: Excel-style logic
- **Rule of 72**: Years ≈ `72 / rate%`

### ✅ 3. Natural Language Q&A
- Users can ask follow-up queries like:
  - “How long will ₹40L last with ₹30K monthly?”
  - “What’s my retirement age if I save ₹1L/year at 8%?”
  - “Explain Rule of 72”

### ✅ 4. Explain-Your-Work
- Agent explains:
  - The exact formula used
  - Input variables
  - Step-by-step logic

### ✅ 5. Visual UI (Streamlit)
- Chat interface + summary cards
- Dynamic retirement projections
- Scenario simulations (e.g., early retirement, inflation)

---

## 📸 Preview

<img src="/Users/yashkumar/Desktop/2Cents/Screenshot 2025-08-03 at 4.07.00 AM.png" width="700"/>

---

## 🧪 Tests

- 9 unit tests (`test_formulas.py`)
- 9 end-to-end scenario tests (`test_end_to_end.py`)
- Covers:
  - Financial formula accuracy
  - Data validation
  - Scenario Q&A
  - Mortgage vs invest decisions
  - Fallback logic

Run tests using:
```bash
python3 -m unittest discover tests
⚙️ Setup Instructions
🖥 Requirements
Python 3.9+

Ollama with llama3 model installed

Streamlit

LangChain (v0.2+)

Optional: virtualenv

📦 Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
▶️ Run App
bash
Copy
Edit
streamlit run main.py
🧠 Architecture
agent.py – LangChain-based agent using llama3:8b-instruct via Ollama

ui.py – Full Streamlit UI: questionnaire, chat, charts, summaries

formulas.py – Core financial logic (FV, PV, annuity, NPER, Rule of 72)

tests/ – Unit tests and end-to-end interaction tests

main.py – Launches the app

🎯 Project Goals
Replicate results of calculators like CalcXML

Deliver accurate, formula-based advice

Maintain friendly UX via chat-like flow

Support dynamic follow-ups using context-aware logic



Questionnaire flow

Chat Q&A

Formula explanations

Scenario modifications

📝 License
This project was built as part of the AI Engineer Technical Task for Valura.ai.
Free to use and extend under MIT License or as directed by the company.

🙋‍♂️ Author
Yash Kumar
Email: yash7291kumar@gmail.com
GitHub: https://github.com/yashh13kumar
LinkedIn: https://www.linkedin.com/in/yash-13-kumar/