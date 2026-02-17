# Customer Service Evaluation System

This project implements a hybrid Quality Assurance (QA) evaluation system for customer service transcripts, utilizing both rule-based logic and Large Language Models (LLM).

## Project Structure

```text
project1/
├── src/
│   ├── core/
│   │   ├── rules.py       # Deterministic rule engine (PII, data integrity)
│   │   ├── evaluator.py   # Hybrid evaluation logic
│   │   └── llm_client.py  # OpenAI API interaction
│   └── utils/
│       └── text_tools.py  # Text formatting utilities
├── tests/
│   └── test_rules.py      # Unit tests for rule engine
├── .github/
│   └── workflows/
│       └── test.yml       # CI/CD pipeline configuration
├── Dockerfile             # Container configuration
├── main.py                # Entry point script
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation


Installation and Usage
Prerequisites
Python 3.10+

Docker (optional)

OpenAI API Key

Method 1: Running with Docker (Recommended)
Build the Docker image:

Bash
docker build -t kontakt-task .
Run the container:
Replace your-api-key-here with your actual OpenAI API key.

Bash
docker run -e OPENAI_API_KEY="your-api-key-here" -v ${PWD}:/app kontakt-task
Method 2: Running Locally
Install dependencies:

Bash
pip install -r requirements.txt
Set environment variables:
Linux/Mac:

Bash
export OPENAI_API_KEY="your-api-key-here"
Windows (PowerShell):

PowerShell
$env:OPENAI_API_KEY="your-api-key-here"
Run the evaluation:

Bash
python main.py
Run unit tests:

Bash
python -m unittest discover tests
Technical Decisions
LLM Selection: GPT-4o-mini
GPT-4o-mini was selected for this task due to three primary factors:

Cost-Efficiency: It offers a significantly lower cost per token compared to GPT-4, making it suitable for high-volume batch processing.

Multilingual Support: The model demonstrates strong performance in code-switching scenarios (Azerbaijani/Russian/English), which is essential for the provided dataset.

Latency: The model provides faster inference times, ensuring the pipeline remains responsive.

Hybrid Approach (Rule-Based vs. LLM)
To ensure robustness and resource optimization, the system employs a two-layer architecture:

Layer 1: Rule-Based Engine (src/core/rules.py): Handles objective checks such as PII detection (credit card patterns), empty transcripts, and audio duration validation. This layer runs first to filter out invalid data without incurring API costs.

Layer 2: LLM Engine (src/core/evaluator.py): Handles subjective criteria such as "Politeness," "Solution delivery," and "Customer needs analysis." These require semantic understanding that rule-based systems cannot provide.

Challenges and Solutions
1. Hallucinations
Challenge: The model occasionally fabricated discounts or offers that were not present in the text.
Solution: I implemented a strict prompt constraint requiring the model to extract an evidence_snippet. If the model cannot quote the exact text from the transcript to support its score, it is instructed to return a null evidence value.

2. Mixed Language Processing
Challenge: Transcripts frequently switch between Russian and Azerbaijani.
Solution: The system uses a multilingual system prompt that explicitly instructs the model to interpret context regardless of the language used, ensuring consistent scoring across language boundaries.

Future Improvements
If more time were available, the following features would be implemented:

Advanced PII Redaction: Integration of Named Entity Recognition (NER) models (e.g., Spacy or Hugging Face BERT) to detect names and addresses, supplementing the current regex-based credit card detection.

Direct Audio Processing: Integration of OpenAI Whisper to transcribe raw audio files within the pipeline, removing the dependency on pre-existing text transcripts.

Visualization Dashboard: Development of a Streamlit or React-based frontend to visualize agent performance metrics and trends over time.


### **Step 3: Save and Push**
After creating the file, run these commands to upload it to GitHub:

```powershell
git add README.md
git commit -m "Add project documentation"
git push
