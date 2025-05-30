# 🎉 Special Days Assistant Agent

This project is a smart, multi-functional AI agent built using **Google's Agent Development Kit (ADK)** and **Gemini 2.0 Flash**. It helps users discover and celebrate special days with meaningful information, ideas, and greeting content.

## ✨ Features

Ask natural language queries like:
- **“What is special today?”**
- **“What are the special days in May?”**
- **“What is special on 26-May-2025?”**
And receive:
- ✅ A brief summary of the special day's significance  
- ✅ 4–6 celebration or event suggestions  
- ✅ A warm 3–4 line wishing message  
- ✅ A social-media/email-friendly text card message

## 🛠️ Tech Stack

- **Google Generative AI SDK** (`gemini-2.0-flash`)
- **Google Agent Development Kit (ADK)**: `LlmAgent`, `SequentialAgent`
- **Python** (modular and tool-based design)
- **dotenv** for secure API key handlin
1. Install dependencies

pip install -r requirements.txt
2. Set up your .env file
Create a .env file in the root directory:
env
GOOGLE_API_KEY=your_google_genai_api_key
▶️ Run the Agent
Run the sample test queries from agent.py:
python agent.py
🧠 How It Works
The assistant is a sequential agent pipeline with the following flow:

SpecialDayLookupAgent → Finds special days based on query

SummaryAgent → Summarizes the meaning of the first special day

EventIdeasAgent → Suggests celebration ideas

MessageAgent → Generates a warm wishing message

EmailTextCardAgent → Creates a shareable text card

Each agent uses tool-calling via function handlers, leveraging Gemini's LLM for structured outputs.
