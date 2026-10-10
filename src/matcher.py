"""Compare resume skills against job skills, tolerant of common spelling variants."""
import re

from src.schemas import JobRequirements, ResumeProfile, SkillMatch

ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "postgres": "postgresql",
    "k8s": "kubernetes",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nodejs": "node.js",
    "node": "node.js",
    "reactjs": "react",
    "react.js": "react",
    "aws cloud": "aws",
    "amazon web services": "aws",
    "gcp": "google cloud",
    "sklearn": "scikit-learn",
}


def normalize_skill(skill: str) -> str:
    s = re.sub(r"\s+", " ", skill.strip().lower())
    return ALIASES.get(s, s)


def skill_alternatives(skill: str) -> set[str]:
    """Split "FastAPI/Django" or "Kafka or RabbitMQ" into normalized alternatives."""
    parts = re.split(r"\s*/\s*|\s+or\s+", skill.strip(), flags=re.IGNORECASE)
    return {normalize_skill(p) for p in parts if p.strip()} | {normalize_skill(skill)}


def match_skills(resume: ResumeProfile, job: JobRequirements) -> SkillMatch:
    resume_norm = {normalize_skill(s) for s in resume.skills}

    def split(skills: list[str]) -> tuple[list[str], list[str]]:
        matched = [s for s in skills if skill_alternatives(s) & resume_norm]
        missing = [s for s in skills if not skill_alternatives(s) & resume_norm]
        return matched, missing

    matched_req, missing_req = split(job.required_skills)
    matched_pref, missing_pref = split(job.preferred_skills)

    job_norm = set().union(*(skill_alternatives(s) for s in job.required_skills + job.preferred_skills))
    extra = [s for s in resume.skills if normalize_skill(s) not in job_norm]

    return SkillMatch(
        matched_required=matched_req,
        missing_required=missing_req,
        matched_preferred=matched_pref,
        missing_preferred=missing_pref,
        extra_skills=extra,
    )
