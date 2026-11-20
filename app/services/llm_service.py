
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.settings import settings


# ---------------------------------
# Groq LLM
# Used by JD Analyzer and Assessment Planner
# ---------------------------------

groq_llm = ChatGroq(
    model=settings.GROQ_MODEL,
    api_key=settings.GROQ_API_KEY,
    temperature=settings.TEMPERATURE,
    max_tokens=settings.MAX_TOKENS,
    timeout=60,
    max_retries=2
)


# ---------------------------------
# Gemini LLM
# Used by Question Generator and Quality Reviewer
# ---------------------------------

gemini_llm = ChatGoogleGenerativeAI(
    model=settings.GEMINI_MODEL,
    api_key=settings.GOOGLE_API_KEY,
    temperature=settings.TEMPERATURE,
    max_output_tokens=settings.MAX_TOKENS,
    max_retries=2
)


# Backward compatibility for any existing imports.
# We will explicitly assign providers in each agent.
llm = groq_llm
