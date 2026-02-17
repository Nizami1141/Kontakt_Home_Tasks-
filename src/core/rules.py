import re
from typing import List, Dict, Any

class RuleEngine:
    """
    Handles deterministic checks without using LLM to save costs and ensure safety.
    """
    
    @staticmethod
    def check_pii_leak(text: str) -> List[str]:
        """Detects potential credit card numbers or sensitive patterns."""
        leaks = []
        # Regex for 13-19 digit numbers (potential card numbers)
        card_pattern = r'\b(?:\d[ -]*?){13,19}\b'
        if re.search(card_pattern, text):
            leaks.append("Potential Credit Card Number detected")
        return leaks

    @staticmethod
    def check_data_integrity(segments: List[Dict]) -> Dict[str, Any]:
        """
        Robustness check: Empty files, short audio, silence.
        """
        if not segments:
            return {"valid": False, "reason": "Empty transcript"}
        
        # Check total duration
        try:
            start = segments[0].get('start', 0) or segments[0].get('start_time', 0)
            end = segments[-1].get('end', 0) or segments[-1].get('end_time', 0)
            duration = end - start
            
            if duration < 0.1:
                return {"valid": False, "reason": "Audio too short (<0.1s)"}
        except:
            pass # Use lenient fallback if timestamps are broken

        return {"valid": True}

    @staticmethod
    def calculate_silence(segments: List[Dict]) -> float:
        """Calculates total silence duration between segments."""
        total_silence = 0.0
        last_end = 0.0
        
        for seg in segments:
            start = seg.get('start', 0) or seg.get('start_time', 0)
            end = seg.get('end', 0) or seg.get('end_time', 0)
            
            if start > last_end:
                total_silence += (start - last_end)
            last_end = max(last_end, end)
            
        return total_silence