from src.matcher import match_skills
from src.schemas import JobRequirements, ResumeProfile
from src.scoring import calculate_score, experience_score


def test_experience_score():
    assert experience_score(2, 4) == 50
    assert experience_score(10, 4) == 100
    assert experience_score(0, 0) == 100


def test_perfect_match():
    resume = ResumeProfile(skills=["Python", "SQL"], experience_years=5)
    job = JobRequirements(required_skills=["Python"], preferred_skills=["SQL"], min_experience_years=3)
    score = calculate_score(resume, job, match_skills(resume, job))
    assert score.overall == 100


def test_partial_match():
    resume = ResumeProfile(skills=["Python"], experience_years=1)
    job = JobRequirements(required_skills=["Python", "Go"], preferred_skills=["SQL"], min_experience_years=2)
    score = calculate_score(resume, job, match_skills(resume, job))
    # 50*0.7 + 0*0.2 + 50*0.1
    assert score.overall == 40.0
