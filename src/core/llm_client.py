import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

try:
    from openai import OpenAI
except Exception as e:
    OpenAI = None  # type: ignore
    _OPENAI_IMPORT_ERROR = e


class LLMClient:
    def __init__(self, model: str | None = None):
        if OpenAI is None:
            raise ImportError("openai package not installed") from _OPENAI_IMPORT_ERROR

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing in .env")

        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"

    def evaluate_call(self, transcript_text: str, criteria_text: str) -> dict:
        # UPDATED PROMPT: Added language instruction
        system_prompt = f"""
You are a Quality Assurance Specialist for a Customer Service center in Azerbaijan.
Evaluate the following call transcript based strictly on these criteria:

{criteria_text}

Output Requirements:
1. Return purely JSON (no markdown).
2. Keys MUST be in English (e.g., "score", "reasoning", "probability").
3. **The content of the "reasoning" field MUST be in Azerbaijani.**
4. Keys MUST be exactly: KR2.1, KR2.2, KR2.3, KR2.4, KR2.5
5. Each KR must have:
   - "score": integer 0-3
   - "reasoning": short but specific explanation in Azerbaijani
   - "evidence_snippet": quote from the transcript
   - "probability": "HIGH" or "LOW" (confidence in your score)
6. If you cannot find evidence, set "evidence_snippet": "N/A" and "probability": "LOW".
7. If PII is shared and NOT stopped by the operator, KR2.5 must be 0.
"""
        user_prompt = f"Transcript:\n{transcript_text}"

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.0,
                max_tokens=1200
            )
            return json.loads(resp.choices[0].message.content)
        except Exception as e:
            logger.exception("LLM error: %s", e)
            return {}