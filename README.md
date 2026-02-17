Customer Service Evaluation System

This project implements a hybrid Quality Assurance (QA) evaluation system for customer service transcripts, combining deterministic rule-based checks with Large Language Model (LLM) scoring.

------------------------------------------------------------
Project Structure
------------------------------------------------------------
project1/
├── src/
│   ├── core/
│   │   ├── rules.py        # Deterministic rule engine (PII, data integrity)
│   │   ├── evaluator.py    # Hybrid evaluation logic
│   │   └── llm_client.py   # OpenAI API interaction
│   └── utils/
│       └── text_tools.py   # Text formatting utilities
├── tests/
│   └── test_rules.py       # Unit tests for rule engine
├── .github/
│   └── workflows/
│       └── test.yml        # CI pipeline configuration
├── Dockerfile              # Container configuration
├── main.py                 # Entry point script
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

------------------------------------------------------------
Prerequisites
------------------------------------------------------------
- Python 3.10+
- OpenAI API Key
- Docker (optional)

------------------------------------------------------------
Installation and Usage
------------------------------------------------------------

Method 1: Run with Docker (Recommended)

1) Build the image:
   docker build -t kontakt-task .

2) Run the container (replace your-api-key-here with your actual key):
   docker run -e OPENAI_API_KEY="your-api-key-here" -v ${PWD}:/app kontakt-task

   Note:
   - ${PWD} works in Git Bash / Linux / macOS
   - On Windows PowerShell, use:
     docker run -e OPENAI_API_KEY="your-api-key-here" -v ${PWD}:/app kontakt-task

------------------------------------------------------------

Method 2: Run Locally

1) Install dependencies:
   pip install -r requirements.txt

2) Set the environment variable:

   Linux / macOS:
   export OPENAI_API_KEY="your-api-key-here"

   Windows (PowerShell):
   $env:OPENAI_API_KEY="your-api-key-here"

3) Run the evaluation:
   python main.py

4) Run unit tests:
   python -m unittest discover -s tests

------------------------------------------------------------
Technical Decisions
------------------------------------------------------------

LLM Selection: gpt-4o-mini

gpt-4o-mini was selected for:
- Cost-efficiency: Lower cost per token compared to larger GPT-4-class models, suitable for batch processing.
- Multilingual support: Strong performance for Azerbaijani / Russian / English code-switching.
- Latency: Faster inference to keep the pipeline responsive.

------------------------------------------------------------
Hybrid Approach
------------------------------------------------------------

To ensure robustness and optimize API usage, the system uses a two-layer architecture:

Layer 1: Rule-Based Engine (src/core/rules.py)
- Handles objective checks such as:
  - PII detection (e.g., credit card-like patterns)
  - Empty transcript detection
  - Audio duration validation
  - Data integrity checks
- Runs first to filter invalid transcripts without incurring LLM costs.

Layer 2: LLM Engine (src/core/evaluator.py)
- Handles subjective criteria requiring semantic understanding:
  - Politeness and tone
  - Solution delivery quality
  - Customer needs analysis

------------------------------------------------------------
Challenges and Solutions
------------------------------------------------------------

1) Hallucinations
- Challenge: The model occasionally fabricated discounts or offers not present in the transcript.
- Solution: Enforced a strict requirement to output an evidence_snippet. If it cannot quote supporting text, it must return null evidence.

2) Mixed Language Processing
- Challenge: Transcripts frequently switch between Russian and Azerbaijani.
- Solution: A multilingual system prompt instructs the model to interpret context across languages to keep scoring consistent.

------------------------------------------------------------
Future Improvements
------------------------------------------------------------
- Advanced PII redaction: Add NER-based detection (spaCy / Hugging Face models) for names, addresses, and more sensitive entities beyond regex patterns.
- Direct audio processing: Integrate Whisper to transcribe raw audio files directly, removing dependency on pre-existing text transcripts.
- Visualization dashboard: Build a Streamlit or React-based UI to visualize agent performance metrics and trends over time.


