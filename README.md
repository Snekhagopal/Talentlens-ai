# Resume Job Matcher

Compare a resume against a job description using a local LLM (via [Ollama](https://ollama.com)),
get a match score, see missing skills, and download the report as JSON or CSV.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Install Ollama, then pull the model set in .env
ollama pull llama3.1:8b
```

## Run

```bash
streamlit run app.py
```

## Test

```bash
pytest
```

## Project layout

| Path | Purpose |
|------|---------|
| `app.py` | Streamlit dashboard UI |
| `src/config.py` | Model name and settings |
| `src/resume_parser.py` | PDF / DOCX / TXT text extraction |
| `src/ollama_client.py` | Python-to-Ollama connection |
| `src/schemas.py` | Pydantic data validation |
| `src/prompts.py` | AI prompts |
| `src/job_analyzer.py` | Job description and resume analysis |
| `src/matcher.py` | Skill comparison |
| `src/scoring.py` | Match score calculation |
| `src/recommendations.py` | AI recommendations |
| `src/report_generator.py` | JSON and CSV downloads |
| `sample_data/` | Sample resume and job description |
