
"""Model name and application settings, loaded from environment / .env."""
import os

from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Scoring weights (must sum to 1.0)
REQUIRED_SKILL_WEIGHT = 0.7
PREFERRED_SKILL_WEIGHT = 0.2
EXPERIENCE_WEIGHT = 0.1

SUPPORTED_EXTENSIONS = (".pdf", ".docx", ".txt")
