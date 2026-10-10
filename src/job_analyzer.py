"""Turn raw resume / job text into structured, validated models via the LLM."""
from src import prompts
from src.gemini_client import GeminiClient
from src.schemas import JobRequirements, ResumeProfile


def analyze_job(job_text: str, client: GeminiClient) -> JobRequirements:
    data = client.chat_json(prompts.SYSTEM_JSON, prompts.JOB_EXTRACTION.format(job_text=job_text))
    return JobRequirements.model_validate(data)


def analyze_resume(resume_text: str, client: GeminiClient) -> ResumeProfile:
    data = client.chat_json(prompts.SYSTEM_JSON, prompts.RESUME_EXTRACTION.format(resume_text=resume_text))
    return ResumeProfile.model_validate(data)
