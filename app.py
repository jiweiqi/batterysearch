# app.py

import streamlit as st
from search import hybrid_search
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Load environment variables and initialize OpenAI client
load_dotenv()

# Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
TOP_RESULTS_COUNT = int(os.getenv("TOP_RESULTS_COUNT", 3))
MAX_SOURCE_LENGTH = int(os.getenv("MAX_SOURCE_LENGTH", 200))

# print llm model configuration
print(f"\n\nLLM Model: {LLM_MODEL}")
print(f"Debug Mode: {DEBUG_MODE}")
print(f"Top Results Count: {TOP_RESULTS_COUNT}")
print(f"Max Source Length: {MAX_SOURCE_LENGTH}")

AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")
if AI_PROVIDER == "ollama":
    client = ChatOllama(
        model=LLM_MODEL,
        temperature=0,
    )
else:
    client = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.context = ""


def setup_sidebar():
    with st.sidebar:
        st.title("BatterySearch")
        st.caption("Disclaimer: BatterySearch can make mistakes. Consider checking important information.")
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.session_state.context = ""
            st.rerun()


def display_chat_history():
    for message in st.session_state.messages:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)


def get_search_results(bm25_query, vector_query):
    bm25_results, vector_results = hybrid_search(bm25_query, vector_query, top_k=TOP_RESULTS_COUNT)
    return bm25_results, vector_results


def update_context(bm25_results: List[Dict], vector_results: List[Dict]):
    all_results = bm25_results + vector_results
    all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
    context = "\n\n".join([f"Document: {r['file_name']}\nContent: {r['content']}" for r in all_results])
    st.session_state.context = context


def display_search_results(bm25_results: List[Dict], vector_results: List[Dict]):
    with st.expander("View Search Results"):
        st.subheader("BM25 Search Results")
        for result in bm25_results:
            st.markdown(
                f"<small>Source: {result['file_name']} (Chunk {result['chunk_number']}/{result['total_chunks']})</small> (score: {result.get('score', 'N/A'):.3f})",
                unsafe_allow_html=True,
            )
            st.markdown(f"<small>{result['content']}</small>", unsafe_allow_html=True)

        st.subheader("Vector Search Results")
        for result in vector_results:
            st.markdown(
                f"<small>Source: {result['file_name']} (Chunk {result['chunk_number']}/{result['total_chunks']})</small> (score: {result.get('score', 'N/A'):.3f})",
                unsafe_allow_html=True,
            )
            st.markdown(f"<small>{result['content']}</small>", unsafe_allow_html=True)


def get_ai_response(messages):
    llm_messages = []
    for msg in messages:
        if isinstance(msg, SystemMessage):
            role = "system"
        elif isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        else:
            continue  # Skip unsupported message types
        llm_messages.append({"role": role, "content": msg.content})

    if DEBUG_MODE:
        st.write(llm_messages)

    response = client.invoke(llm_messages)
    return response.content


def main():
    initialize_session_state()
    setup_sidebar()
    display_chat_history()

    query = st.chat_input("What would you like to know about batteries?")

    if query:
        st.session_state.messages.append(HumanMessage(content=query))
        with st.chat_message("user"):
            st.markdown(query)

        keyword_results, vector_results = get_search_results(query, query)
        update_context(keyword_results, vector_results)

        messages = [
            SystemMessage(
                content=(
                    "You are an expert assistant specializing in battery engineering related to consumer electronics products."
                    "Utilize the provided context below to answer the user's queries accurately:\n\n"
                    f"{st.session_state.context}\n\n"
                    "Guidelines:\n"
                    "1. **Citations:** Always cite your sources by referencing the source file names in square brackets. "
                    "For example, [file_name.html]. If multiple sources are used, list all relevant citations.\n"
                    "2. **Clarity and Precision:** Provide clear, concise, and precise answers.\n"
                    "3. **Handling Insufficient Information:** If the context does not contain enough information to answer the question, clearly state that the information is insufficient to provide an accurate answer.\n"
                    "4. **Derivation Explanation:** After providing the answer, include a brief explanation of how you derived the answer from the provided sources."
                    "Reference the specific sources that contributed to each part of your explanation.\n\n"
                    "Avoid deriving answers from outside the provided context. Only use information from the context provided to you.\n\n"
                    "Your goal is to assist the user effectively by leveraging the given context and adhering to the above guidelines."
                )
            ),
        ] + st.session_state.messages

        assistant_response = get_ai_response(messages)
        st.session_state.messages.append(AIMessage(content=assistant_response))
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        display_search_results(keyword_results, vector_results)


if __name__ == "__main__":
    main()
