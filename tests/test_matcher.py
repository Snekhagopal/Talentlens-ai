from src.matcher import match_skills, normalize_skill
from src.schemas import JobRequirements, ResumeProfile


def test_normalize_aliases():
    assert normalize_skill(" K8s ") == "kubernetes"
    assert normalize_skill("ReactJS") == "react"


def test_match_skills():
    resume = ResumeProfile(skills=["Python", "Postgres", "Docker", "Excel"])
    job = JobRequirements(
        required_skills=["Python", "PostgreSQL", "Kubernetes"],
        preferred_skills=["Docker", "Kafka"],
    )
    m = match_skills(resume, job)
    assert m.matched_required == ["Python", "PostgreSQL"]
    assert m.missing_required == ["Kubernetes"]
    assert m.matched_preferred == ["Docker"]
    assert m.missing_preferred == ["Kafka"]
    assert m.extra_skills == ["Excel"]


def test_alternative_skills():
    resume = ResumeProfile(skills=["Django", "RabbitMQ"])
    job = JobRequirements(required_skills=["FastAPI/Django"], preferred_skills=["Kafka or RabbitMQ"])
    m = match_skills(resume, job)
    assert m.missing_required == [] and m.missing_preferred == []
    assert m.extra_skills == []
