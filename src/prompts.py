"""Prompt templates sent to the LLM."""

SYSTEM_JSON = (
    "You are a precise recruiting assistant. "
    "Always respond with a single valid JSON object and nothing else."
)

RESUME_EXTRACTION = """Extract structured information from the resume below.
Return JSON with exactly these keys:
- "name": string or null
- "skills": list of short skill names (technologies, tools, languages, methods)
- "experience_years": number, total years of professional experience
- "education": list of strings (degree, institution)
- "summary": one-sentence professional summary

Resume:
\"\"\"
{resume_text}
\"\"\""""

JOB_EXTRACTION = """Extract structured requirements from the job description below.
Return JSON with exactly these keys:
- "title": job title
- "required_skills": list of short skill names that are mandatory
- "preferred_skills": list of short skill names that are nice-to-have
- "min_experience_years": number (0 if not stated)
- "responsibilities": list of short strings

Job description:
\"\"\"
{job_text}
\"\"\""""

RECOMMENDATIONS = """A candidate scored {score}/100 against the "{job_title}" role.
Matched required skills: {matched}
Missing required skills: {missing_required}
Missing preferred skills: {missing_preferred}
Candidate experience: {experience} years (role asks for {min_experience}).

Return JSON with keys:
- "summary": 2-3 sentences assessing fit
- "suggestions": list of 3-6 concrete, actionable ways to improve the resume or close skill gaps"""
