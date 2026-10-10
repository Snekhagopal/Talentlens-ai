"""Pydantic models shared across the app."""
from pydantic import BaseModel, Field, field_validator


def _clean_skills(skills: list[str]) -> list[str]:
    seen, out = set(), []
    for s in skills:
        s = str(s).strip()
        if s and s.lower() not in seen:
            seen.add(s.lower())
            out.append(s)
    return out


class ResumeProfile(BaseModel):
    name: str | None = None
    skills: list[str] = Field(default_factory=list)
    experience_years: float = Field(default=0, ge=0)
    education: list[str] = Field(default_factory=list)
    summary: str = ""

    @field_validator("skills")
    @classmethod
    def dedupe_skills(cls, v: list[str]) -> list[str]:
        return _clean_skills(v)


class JobRequirements(BaseModel):
    title: str = ""
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    min_experience_years: float = Field(default=0, ge=0)
    responsibilities: list[str] = Field(default_factory=list)

    @field_validator("required_skills", "preferred_skills")
    @classmethod
    def dedupe_skills(cls, v: list[str]) -> list[str]:
        return _clean_skills(v)


class SkillMatch(BaseModel):
    matched_required: list[str] = Field(default_factory=list)
    missing_required: list[str] = Field(default_factory=list)
    matched_preferred: list[str] = Field(default_factory=list)
    missing_preferred: list[str] = Field(default_factory=list)
    extra_skills: list[str] = Field(default_factory=list)


class MatchScore(BaseModel):
    overall: float = Field(ge=0, le=100)
    required_skills: float = Field(ge=0, le=100)
    preferred_skills: float = Field(ge=0, le=100)
    experience: float = Field(ge=0, le=100)


class Recommendations(BaseModel):
    summary: str = ""
    suggestions: list[str] = Field(default_factory=list)


class MatchReport(BaseModel):
    resume: ResumeProfile
    job: JobRequirements
    skills: SkillMatch
    score: MatchScore
    recommendations: Recommendations | None = None
