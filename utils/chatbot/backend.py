import os
import uuid
import sqlite3
from typing import TypedDict, Annotated
from datetime import datetime
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage as LCSystemMessage,
)

# from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI


# ========================
# Utility functions
# ========================
def generate_thread_id():
    return uuid.uuid4()


def update_chat_name_from_first_message(session_state, thread_id, user_message):
    # Update chat name if it currently is the default or empty
    current_name = session_state.get("chat_thread_names", {}).get(thread_id, "")
    if current_name.startswith("Chat "):  # Means default name assigned
        snippet = user_message.replace("\n", " ")[:30].strip()
        if snippet:
            session_state["chat_thread_names"][thread_id] = snippet


# ========================
# Load environment variables
# ========================
load_dotenv()


# ---- Chat state definition ----
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ---- Initialize LLM ----
# llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7, max_retries=2)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")


# ---- Chat node ----
def chat_node(state: ChatState):
    system_prompt = (
        "You are a caring, concise mental wellness companion. "
        "Respond empathetically in 2–5 short sentences. "
        "Offer practical, safe, non-clinical tips. "
        "Do not reveal chain-of-thought or internal reasoning. "
        "If you detect crisis (self-harm/violence), advise contacting local emergency services or hotlines."
    )
    history: list[BaseMessage] = state["messages"]

    # Prepend system prompt if not already present
    if not history or not isinstance(history[0], LCSystemMessage):
        formatted = [LCSystemMessage(content=system_prompt)] + history
    else:
        formatted = history

    # Convert BaseMessage objects to dict format for Groq LLM
    messages_for_groq = []
    for msg in formatted:
        if isinstance(msg, LCSystemMessage):
            role = "system"
        elif isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        else:
            role = "user"
        messages_for_groq.append({"role": role, "content": msg.content})

    reply = llm.invoke(messages_for_groq)

    reply_text = reply.content if hasattr(reply, "content") else str(reply)
    return {"messages": history + [AIMessage(content=reply_text)]}


# ---- Build LangGraph ----
conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
chatbot = graph.compile(checkpointer=checkpointer)


# ---- Thread utilities ----
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)


def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])
