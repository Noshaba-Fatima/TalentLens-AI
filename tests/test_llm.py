
from app.services.llm_service import llm

response = llm.invoke(
    "You are TalentLens AI. Introduce yourself "
    "in two sentences and explain your purpose."
)

print(response.content)
