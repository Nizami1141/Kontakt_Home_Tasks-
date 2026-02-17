import unittest
from src.core.rules import RuleEngine

class TestRuleEngine(unittest.TestCase):

    def test_detects_credit_card_numbers(self):
        message = "Here is my card number 4111 1234 5678 9010 for the payment."
        leaks = RuleEngine.check_pii_leak(message)
        self.assertIn("Potential Credit Card Number detected", leaks)

    def test_ignores_safe_messages(self):
        message = "Hello, I am looking to buy a new washing machine."
        leaks = RuleEngine.check_pii_leak(message)
        self.assertEqual(leaks, [])

    def test_fails_on_empty_data(self):
        report = RuleEngine.check_data_integrity([])
        self.assertFalse(report["valid"])
        self.assertEqual(report["reason"], "Empty transcript")

    def test_fails_on_audio_too_short(self):
        quick_segment = [{"start": 0.0, "end": 0.05, "text": "Hi"}]
        report = RuleEngine.check_data_integrity(quick_segment)
        self.assertFalse(report["valid"])
        self.assertIn("Audio too short", report["reason"])

if __name__ == '__main__':
    unittest.main()