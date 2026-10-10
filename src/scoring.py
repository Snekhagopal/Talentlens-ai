"""Weighted match score from skill overlap and experience."""
from src.config import EXPERIENCE_WEIGHT, PREFERRED_SKILL_WEIGHT, REQUIRED_SKILL_WEIGHT
from src.schemas import JobRequirements, MatchScore, ResumeProfile, SkillMatch


def _ratio(matched: int, total: int) -> float:
    # No requirements in a category means nothing is missing.
    return 100.0 if total == 0 else 100.0 * matched / total


def experience_score(candidate_years: float, required_years: float) -> float:
    if required_years <= 0:
        return 100.0
    return min(100.0, 100.0 * candidate_years / required_years)


def calculate_score(resume: ResumeProfile, job: JobRequirements, skills: SkillMatch) -> MatchScore:
    req = _ratio(len(skills.matched_required), len(job.required_skills))
    pref = _ratio(len(skills.matched_preferred), len(job.preferred_skills))
    exp = experience_score(resume.experience_years, job.min_experience_years)
    overall = req * REQUIRED_SKILL_WEIGHT + pref * PREFERRED_SKILL_WEIGHT + exp * EXPERIENCE_WEIGHT
    return MatchScore(
        overall=round(overall, 1),
        required_skills=round(req, 1),
        preferred_skills=round(pref, 1),
        experience=round(exp, 1),
    )
