from langchain_core.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama
from utils import format_currency
from formulas import FinancialFormulas
import re

class FinancialPlanningAgent:
    def __init__(self):
        self.llm = Ollama(model="llama3:8b-instruct-q4_0")
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.formulas = FinancialFormulas()
        self.user_data = {}

        self.conversation_chain = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self._build_prompt(),
            verbose=False
        )

    def _build_prompt(self):
        template = """You are a financial planning assistant.
Use only the user's provided data to answer. Never assume or invent missing data.
Always use real financial reasoning or formulas. Be concise, polite, and realistic.

{chat_history}
User: {input}
AI:"""
        return PromptTemplate(input_variables=["chat_history", "input"], template=template)

    def chat(self, user_input: str) -> str:
        self.user_data.update(self._extract_financial_data(user_input))

        if "reset" in user_input.lower():
            self.reset_conversation()
            return "🔄 Conversation reset. Please start by sharing your financial details again."

        if not self._has_sufficient_data():
            missing = [f for f in ["age", "income", "savings", "retirement_age"] if f not in self.user_data]
            return f"⚠️ Missing context: please provide your {', '.join(missing)}."

        # Inject known user profile into LLM prompt
        context = f"""You are a helpful financial advisor AI. Here's the user's profile:
- Age: {self.user_data['age']}
- Annual Income: ₹{format_currency(self.user_data['income'])}
- Current Savings: ₹{format_currency(self.user_data['savings'])}
- Target Retirement Age: {self.user_data['retirement_age']}
- Risk Tolerance: {self.user_data.get('risk_tolerance', 'Not specified')}

Answer the following query using only this data. If a formula applies, use it. Be concise:
User: {user_input}
AI:"""

        try:
            response = self.llm.invoke(context)
            return response if isinstance(response, str) else response.get("output", "").strip()
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"

    def _extract_financial_data(self, text):
        data = {}
        try:
            def parse_amount(val):
                val = val.lower().replace("₹", "").replace(",", "").strip()
                multiplier = 1
                if 'l' in val: multiplier = 100000; val = val.replace('l', '')
                elif 'k' in val: multiplier = 1000; val = val.replace('k', '')
                return int(float(val.strip()) * multiplier)

            # Extract age
            if match := re.search(r'(\d{2})\s*(?:years?\s*old|yo|age)', text.lower()):
                data["age"] = int(match.group(1))

            # Income
            if match := re.search(r'(?:income|salary|earn|make)[^\d₹]*₹?\s*([\d,.kKlL]+)', text):
                data["income"] = parse_amount(match.group(1))

            # Savings
            if match := re.search(r'(?:savings|saved|have)[^\d₹]*₹?\s*([\d,.kKlL]+)', text):
                data["savings"] = parse_amount(match.group(1))

            # Retirement age
            if match := re.search(r'retire(?:ment)?[^0-9]{0,10}(\d{2})', text.lower()):
                data["retirement_age"] = int(match.group(1))

            # Risk tolerance
            for risk in ["conservative", "moderate", "aggressive"]:
                if risk in text.lower():
                    data["risk_tolerance"] = risk
        except Exception:
            pass
        return data

    def _has_sufficient_data(self):
        return all(self.user_data.get(k) is not None for k in ["age", "income", "savings", "retirement_age"])

    def get_user_data(self):
        return self.user_data.copy()

    def update_user_data(self, new_data: dict):
        if not isinstance(new_data, dict):
            raise ValueError("Expected a dictionary.")

        # Normalize keys
        if "current_income" in new_data:
            new_data["income"] = new_data.pop("current_income")
        if "current_savings" in new_data:
            new_data["savings"] = new_data.pop("current_savings")
        if "monthly_expenses" in new_data:
            new_data["expenses"] = new_data.pop("monthly_expenses")

        self.user_data.update(new_data)

    def reset_conversation(self):
        self.user_data = {}
        if hasattr(self.memory, "clear"):
            self.memory.clear()
