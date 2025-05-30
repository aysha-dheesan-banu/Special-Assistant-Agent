import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.adk.agents import LlmAgent, SequentialAgent

# ——————————————————————————————————————————————
# 0) Load .env from this folder
# ——————————————————————————————————————————————
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# ——————————————————————————————————————————————
# 1) Configure the Google Gen AI SDK
# ——————————————————————————————————————————————
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("Missing GOOGLE_API_KEY in .env")
genai.configure(api_key=api_key)

# ——————————————————————————————————————————————
# 2) Tool functions for Special Days Agent
# ——————————————————————————————————————————————
def generate_day_summary(day_name: str) -> str:
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    resp = model.generate_content(
        f"Give a short overview of the significance and origin of '{day_name}'."
    )
    return resp.text

def create_event_ideas(day_summary: str) -> str:
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    resp = model.generate_content(
        "Based on the following description, suggest 4–6 meaningful celebration or event ideas:\n\n"
        f"{day_summary}"
    )
    return resp.text

def create_wishing_message(day_summary: str) -> str:
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    resp = model.generate_content(
        "Write a warm 3–4 line wishing message suitable for social media or a greeting card for this special day:\n\n"
        f"{day_summary}"
    )
    return resp.text

def generate_email_text_card(summary: str) -> str:
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    prompt = (
        "Using the following summary of a special day, generate a short, heartfelt wishing message "
        "formatted like a text card suitable for sending by email or posting on social media.\n\n"
        "Add emojis if appropriate. Keep it visually spaced and warm.\n\n"
        f"Day Summary:\n{summary}"
    )
    response = model.generate_content(prompt)
    return response.text

def find_special_days(query: str) -> str:
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    prompt = (
        "You are a calendar assistant. Respond clearly to queries like:\n"
        "- 'What is special today?'\n"
        "- 'What is special on 26-May-2025?'\n"
        "- 'What are the special days in May?'\n"
        "- 'What are the special days in 2025?'\n\n"
        f"Query: {query}\n\n"
        "Answer with the special days mentioned, separated by commas or bullet points."
    )
    resp = model.generate_content(prompt)
    return resp.text

# ——————————————————————————————————————————————
# 3) Define LLM Agents
# ——————————————————————————————————————————————
special_day_agent = LlmAgent(
    name="SpecialDayLookupAgent",
    model="gemini-2.0-flash",
    description="Answers queries about special days by date, month, or year.",
    instruction=(
        "Call find_special_days(query), where query is the user's original question, "
        "and return only the special days related to that time."
    ),
    tools=[find_special_days],
    output_key="special_days"
)

summary_agent = LlmAgent(
    name="SummaryAgent",
    model="gemini-2.0-flash",
    description="Summarizes the meaning of a special day.",
    instruction=(
        "Extract the first special day name from the input (which may be a list or paragraph) and "
        "call generate_day_summary(day_name) with that name, then return only the summary."
    ),
    tools=[generate_day_summary],
    output_key="summary"
)

events_agent = LlmAgent(
    name="EventIdeasAgent",
    model="gemini-2.0-flash",
    description="Suggests celebration ideas based on the summary.",
    instruction="Call create_event_ideas(summary) and return only the ideas.",
    tools=[create_event_ideas],
    output_key="ideas"
)

message_agent = LlmAgent(
    name="MessageAgent",
    model="gemini-2.0-flash",
    description="Creates a short wishing message based on the summary.",
    instruction="Call create_wishing_message(summary) and return only the message.",
    tools=[create_wishing_message],
    output_key="message"
)

email_card_agent = LlmAgent(
    name="EmailTextCardAgent",
    model="gemini-2.0-flash",
    description="Creates an email or social media friendly text card for a special day.",
    instruction="Call generate_email_text_card(summary) and return only the text card output.",
    tools=[generate_email_text_card],
    output_key="email_card"
)

# ——————————————————————————————————————————————
# 4) Orchestration agent
# ——————————————————————————————————————————————
root_agent = SequentialAgent(
    name="SpecialDaysAssistant",
    sub_agents=[
        special_day_agent,
        summary_agent,
        events_agent,
        message_agent,
        email_card_agent
    ],
    description="Answers special day queries → gives overview → celebration ideas → wishing message → text card"
)

# ✨ Fix for ADK — expose the agent as expected
agent = root_agent

# ——————————————————————————————————————————————
# 5) Example usage (for testing)
# ——————————————————————————————————————————————
if __name__ == "__main__":
    test_queries = [
        "What is special today?",
        "What are the special days in May?",
        "What is special on 26-May-2025?",
        "What are the special days in 2025?",
        "Tell me the special days in January",
        "Are there any special days in November?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        result = root_agent.run({"query": query})
        print("Special Days:\n", result.get("special_days", "No special days found."))
        print("Summary:\n", result.get("summary", "No summary available."))
        print("Event Ideas:\n", result.get("ideas", "No event ideas available."))
        print("Wishing Message:\n", result.get("message", "No wishing message available."))
        print("Email/Text Card Message:\n", result.get("email_card", "No card message available."))
        print("="*60) 







