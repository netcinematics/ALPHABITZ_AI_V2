
# from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

MODEL_NAME = "gemini-2.5-flash"
# MODEL_NAME = "gemini-1.5-pro"


RESEARCH_AGENT = Agent(
    name="CONCISE_ASSISTANT",
    model=Gemini(
        model=MODEL_NAME,
        retry_options=retry_config
    ),
    description="A concise agent that answers questions with brief answers.",
    instruction="""You are a concise assistant. Answer briefly, with a single short sentence to explain.
    Use Google Search tool for current answers. Do not be sycophantic.
    """,
    tools=[google_search],
)

print("✅ RESEARCH_AGENT defined.")