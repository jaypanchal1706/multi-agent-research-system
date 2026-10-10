Multi-Agent Research System
A simple AI research app that uses multiple agents to search the web, read sources, write a report, and review it.
Tech Stack
- Python
- LangChain
- Groq
- Tavily
- Streamlit
Setup
1. Install dependencies:
   uv sync
2. Create a .env file and add your API keys:
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
3. Start the app:
   uv run streamlit run app.py
Workflow
1. Search the web for relevant sources.
2. Scrape a selected source.
3. Generate a research report.
4. Review the report with a critic chain.
