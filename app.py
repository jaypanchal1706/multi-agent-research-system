import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from pipeline import run_research_pipeline

load_dotenv()

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🔎 Multi-Agent Research System")
st.caption(
    "Enter a topic in which you want to do research, Agents can make a report for you."
)

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        **Pipeline**
        1. Search Agent — finds relevant web sources.
        2. Reader Agent — reads a selected source.
        3. Writer — drafts a research report.
        4. Critic — evaluates the report.
        """
    )
    st.divider()

if not os.getenv("GROQ_API_KEY"):
    st.warning("GROQ_API_KEY was not found. Check your project's .env file.")
if not os.getenv("TAVILY_API_KEY"):
    st.warning("TAVILY_API_KEY was not found. Check your project's .env file.")

st.subheader("What would you like to research?")
with st.form("research_form"):
    topic = st.text_area(
        "Research topic",
        placeholder=(
            "Example: Why are technology stocks rising despite negative "
            "US economic news today?"
        ),
        height=100,
    )
    submitted = st.form_submit_button(
        "Run research Pipeline",
        type="primary",
        use_container_width=True,
    )

if submitted:
    topic = topic.strip()

    if not topic:
        st.error("Enter a research topic before starting.")
    else:
        st.session_state["last_topic"] = topic
        st.session_state.pop("research_state", None)

        try:
            with st.status(
                "Running your multi-agent research pipeline...",
                expanded=True,
            ) as status:
                st.write(
                    "The Search Agent, Reader Agent, Writer, and Critic are "
                    "running. Results will appear here when the pipeline finishes."
                )

                result = run_research_pipeline(topic)

                st.session_state["research_state"] = result
                status.update(
                    label="Research pipeline completed.",
                    state="complete",
                    expanded=False,
                )
        except Exception as exc:
            st.error("The research pipeline failed.")
            st.exception(exc)
            st.info(
                "Check that your API keys are set in .env and that your Groq "
                "model has available rate-limit capacity. Fix the error and "
                "run the research again."
            )

result = st.session_state.get("research_state")

if result:
    st.divider()
    st.header("Research results")
    st.caption(f"Topic: {st.session_state.get('last_topic', '')}")

    report_tab, critic_tab, search_tab, reader_tab = st.tabs(
        ["📄 Final report", "🧪 Critic review", "🔍 Search results", "📚 Reader output"]
    )

    with report_tab:
        report = result.get("report", "No report was returned.")
        st.markdown(report)
        st.download_button(
            "Download report as Markdown",
            data=str(report),
            file_name="research_report.md",
            mime="text/markdown",
            use_container_width=False,
        )

    with critic_tab:
        st.markdown(result.get("feedback", "No critic feedback was returned."))

    with search_tab:
        st.text_area(
            "Search Agent response",
            value=str(result.get("search_result", "")),
            height=350,
            disabled=True,
        )

    with reader_tab:
        st.text_area(
            "Reader Agent response",
            value=str(result.get("scraped_content", "")),
            height=350,
            disabled=True,
        )

st.divider()
st.caption("Research outputs may contain incomplete or outdated information. Verify important claims against the cited sources.")
