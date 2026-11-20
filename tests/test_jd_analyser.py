
from app.agents.jd_analyser import analyze_job_description


sample_jd = """
We are looking for a Python Backend Developer
with 2-4 years of experience.

Responsibilities:
- Develop REST APIs using FastAPI.
- Design and optimize PostgreSQL queries.
- Build scalable backend services.
- Implement asynchronous programming.

Required skills:
- Python
- FastAPI
- PostgreSQL
- REST APIs
- Async programming

Preferred skills:
- Docker
- AWS
- Redis

A bachelor's degree in Computer Science
or a related field is preferred.
"""


initial_state = {
    "jd_text": sample_jd
}


result = analyze_job_description(initial_state)

job = result["job_description"]

print("\nJOB ANALYSIS RESULT")
print("=" * 50)

print(job.model_dump_json(indent=4))

print("\nJob title:", job.job_title)
print("Required skills:")

for skill in job.required_skills:
    print(
        skill.name,
        "|",
        skill.category.value,
        "|",
        skill.proficiency.value
    )
