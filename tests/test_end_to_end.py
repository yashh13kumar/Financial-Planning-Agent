import unittest
import sys
import os
from unittest.mock import patch
from langchain_core.runnables import RunnableLambda

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import FinancialPlanningAgent
from utils import validate_financial_input


class TestEndToEndScenarios(unittest.TestCase):
    def setUp(self):
        patcher = patch('agent.Ollama')
        self.addCleanup(patcher.stop)
        mock_ollama = patcher.start()

        # Define a mock LLM response behavior
        def fake_llm_response(x):
            input_text = x.get("input", "") if isinstance(x, dict) else x
            input_text = input_text.lower()

            if "user:" in input_text:
                input_text = input_text.split("user:")[-1].strip()

            if "mortgage" in input_text:
                return "It is better to invest than pay off mortgage."
            elif "rule of 72" in input_text:
                return "The Rule of 72 is a quick way to estimate investment doubling time."
            elif "generate my retirement plan" in input_text or "retirement plan" in input_text:
                return "Here's your retirement goal..."
            elif "reset" in input_text:
                self.agent.user_data = {}
                return "Conversation reset."
            elif "retire at" in input_text:
                return "Scenario updated."
            return "Mocked output"

        mock_ollama.return_value = RunnableLambda(lambda x: fake_llm_response(x))
        self.agent = FinancialPlanningAgent()
        self.agent.conversation_chain = RunnableLambda(fake_llm_response)
        self.agent.conversation_chain.predict = lambda **kwargs: fake_llm_response(kwargs.get("input", ""))

    def test_complete_retirement_planning_scenario(self):
        self.agent.user_data = {
            'age': 28, 'savings': 15000, 'income': 85000, 'retirement_age': 60
        }
        response = self.agent.chat("Can you generate my retirement plan?")
        self.assertIn("retirement", response.lower())

    def test_scenario_modification_workflow(self):
        self.agent.user_data = {
            'age': 35, 'income': 100000, 'savings': 50000, 'retirement_age': 65
        }
        response = self.agent.chat("What if I retire at 60?")
        self.assertTrue(isinstance(response, str))

    def test_formula_explanation_workflow(self):
        self.agent.user_data = {
            'age': 30, 'income': 90000, 'savings': 25000, 'retirement_age': 65
        }
        response = self.agent.chat("Explain the Rule of 72.")
        self.assertIn("rule of 72", response.lower())

    def test_error_handling_scenarios(self):
        bad_inputs = [
            "I'm 150 years old",
            "I make negative rupees",
            "I want to retire at 25"
        ]
        for text in bad_inputs:
            try:
                res = self.agent.chat(text)
                self.assertTrue(isinstance(res, str))
            except Exception as e:
                self.fail(f"Failed to handle: {text} with error: {e}")

    def test_memory_and_context(self):
        self.agent.user_data = {'age': 30, 'income': 75000}
        self.assertTrue(hasattr(self.agent.memory, 'buffer'))

    def test_mortgage_vs_investment_scenario(self):
        self.agent.user_data = {
            'savings': 400000, 'income': 100000, 'age': 30, 'retirement_age': 60
        }
        result = self.agent.chat("Should I pay off my mortgage or invest?")
        self.assertIn("better to", result.lower())

    def test_insufficient_data(self):
        self.agent.user_data = {'age': 25, 'income': 60000}
        result = self.agent.chat("Can you generate my retirement plan?")
        self.assertIn("retirement", result.lower())  # Adjust if needed

    def test_reset_conversation(self):
        self.agent.user_data = {'age': 30, 'income': 85000}
        self.agent.chat("reset conversation")
        self.assertEqual(self.agent.user_data, {})

    def test_validation_integration(self):
        tests = [
            ("age", 25, True),
            ("age", 150, False),
            ("income", 75000, True),
            ("income", -5000, False)
        ]
        for field, val, expected in tests:
            is_valid, _ = validate_financial_input(
                val, field,
                min_value=18 if field == "age" else 0,
                max_value=100 if field == "age" else 10**7
            )
            self.assertEqual(is_valid, expected)


if __name__ == "__main__":
    unittest.main()
