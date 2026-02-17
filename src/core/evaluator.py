# src/core/evaluator.py
import os
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

import yaml

from .llm_client import LLMClient
from .rules import RuleEngine
from ..utils.text_tools import format_transcript

logger = logging.getLogger(__name__)

def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

@dataclass
class EvaluatorConfig:
    criteria_path: Optional[str] = None
    use_llm: bool = True

class Evaluator:
    def __init__(self, config: Optional[EvaluatorConfig] = None):
        self.config = config or EvaluatorConfig()

        # auto criteria path if not provided
        if not self.config.criteria_path:
            p = os.path.join("src", "prompts", "criteria_definitions.yaml")
            self.config.criteria_path = p if os.path.exists(p) else None

        self.criteria_text = ""
        if self.config.criteria_path and os.path.exists(self.config.criteria_path):
            with open(self.config.criteria_path, "r", encoding="utf-8") as f:
                self.criteria_text = yaml.safe_load(f)
            self.criteria_text = str(self.criteria_text)

        self.llm = LLMClient() if self.config.use_llm else None

    def evaluate_json(self, call_input: Dict[str, Any]) -> Dict[str, Any]:
        call_id = call_input.get("call_id", "UNKNOWN_CALL")
        segments = call_input.get("segments", [])

        integrity = RuleEngine.check_data_integrity(segments)
        if not integrity.get("valid", True):
            return {call_id: {"SYSTEM": {"score": 0, "reasoning": integrity.get("reason", "Invalid"), "probability": "HIGH"}}}

        transcript_text = format_transcript(segments)
        if not transcript_text.strip():
            return {call_id: {"SYSTEM": {"score": 0, "reasoning": "Transcript empty after cleaning", "probability": "HIGH"}}}

        results: Dict[str, Any] = {}

        # rule-based
        try:
            results["METRIC_SILENCE_SEC"] = {
                "score": round(RuleEngine.calculate_silence(segments), 3),
                "reasoning": "Total silence between segments (seconds)",
                "probability": "HIGH",
            }
        except Exception as e:
            logger.warning("Silence metric failed: %s", e)

        # LLM-based criteria scoring
        if self.llm and self.criteria_text:
            llm_out = self.llm.evaluate_call(transcript_text=transcript_text, criteria_text=self.criteria_text)
            # expected: {"KR2.1": {"score":..,"reasoning":..,"evidence_snippet":..}, ...}
            results.update(llm_out)

        return {call_id: results}
