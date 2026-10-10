"""Serialize a MatchReport for download."""
import csv
import io

from src.schemas import MatchReport


def to_json(report: MatchReport) -> str:
    return report.model_dump_json(indent=2)


def to_csv(report: MatchReport) -> str:
    """One row per job skill, plus summary rows for the scores."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["section", "item", "value"])

    s = report.score
    for name, value in [
        ("overall", s.overall),
        ("required_skills", s.required_skills),
        ("preferred_skills", s.preferred_skills),
        ("experience", s.experience),
    ]:
        writer.writerow(["score", name, value])

    sk = report.skills
    for skill in sk.matched_required:
        writer.writerow(["required_skill", skill, "matched"])
    for skill in sk.missing_required:
        writer.writerow(["required_skill", skill, "missing"])
    for skill in sk.matched_preferred:
        writer.writerow(["preferred_skill", skill, "matched"])
    for skill in sk.missing_preferred:
        writer.writerow(["preferred_skill", skill, "missing"])

    if report.recommendations:
        for tip in report.recommendations.suggestions:
            writer.writerow(["recommendation", tip, ""])

    return buf.getvalue()
