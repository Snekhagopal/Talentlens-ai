import pytest
from pydantic import ValidationError

from src.schemas import JobRequirements, MatchScore, ResumeProfile


def test_resume_skills_deduped_case_insensitive():
    r = ResumeProfile(skills=["Python", "python", " SQL ", ""])
    assert r.skills == ["Python", "SQL"]


def test_job_defaults():
    j = JobRequirements.model_validate({})
    assert j.required_skills == [] and j.min_experience_years == 0


def test_negative_experience_rejected():
    with pytest.raises(ValidationError):
        ResumeProfile(experience_years=-1)


def test_score_bounds():
    with pytest.raises(ValidationError):
        MatchScore(overall=120, required_skills=0, preferred_skills=0, experience=0)
