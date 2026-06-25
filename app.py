"""A simple chat screen for the AI Tool Stack Advisor. Run: streamlit run app.py"""
import asyncio

import streamlit as st

from src.pipeline import run_query

st.set_page_config(page_title="AI Tool Stack Advisor", page_icon="🧰")

st.title("🧰 AI Tool Stack Advisor")
st.caption(
    "Ask which AI tools fit your team. Answers are drawn from a curated knowledge "
    "base plus the live web, and fact-checked before you see them."
)

question = st.text_input(
    "Your question",
    placeholder="e.g. what should my team use for meeting notes, and what does it cost?",
)

if st.button("Ask", type="primary") and question.strip():
    with st.spinner("The agents are researching and fact-checking..."):
        result = asyncio.run(run_query(question))

    st.markdown("### Recommendation")
    st.markdown(result["answer"] or "_No answer produced._")

    with st.expander("Behind the scenes - how the agents worked"):
        st.write(f"**Strategy chosen:** {result['route']}")
        st.write(f"**Fact-check verdict:** {result['verdict']}")
        m = result["metrics"]
        st.write(f"**Total time:** {m['total_ms']:.0f} ms")
        st.write(f"**Tool calls:** {m['tool_calls']}")
        st.write(f"**Tokens used:** {m['tokens']}")
