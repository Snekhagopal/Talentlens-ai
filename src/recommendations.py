"""LLM-generated suggestions for improving fit."""
from src import prompts
from src.gemini_client import GeminiClient
from src.schemas import JobRequirements, MatchScore, Recommendations, ResumeProfile, SkillMatch


def _fmt(items: list[str]) -> str:
    return ", ".join(items) if items else "none"


def generate_recommendations(
    resume: ResumeProfile,
    job: JobRequirements,
    skills: SkillMatch,
    score: MatchScore,
    client: GeminiClient,
) -> Recommendations:
    prompt = prompts.RECOMMENDATIONS.format(
        score=score.overall,
        job_title=job.title or "target",
        matched=_fmt(skills.matched_required),
        missing_required=_fmt(skills.missing_required),
        missing_preferred=_fmt(skills.missing_preferred),
        experience=resume.experience_years,
        min_experience=job.min_experience_years,
    )
    data = client.chat_json(prompts.SYSTEM_JSON, prompt)
    return Recommendations.model_validate(data)
