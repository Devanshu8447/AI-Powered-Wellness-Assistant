# import streamlit as st
# from datetime import datetime
# from langchain_core.messages import (
#     HumanMessage,
#     AIMessage,
#     SystemMessage as LCSystemMessage,
# )

# from utils.chatbot.backend import (
#     chatbot,
#     generate_thread_id,
#     retrieve_all_threads,
#     load_conversation,
#     update_chat_name_from_first_message,
# )


# # ========================
# # Frontend utilities
# # ========================
# def add_thread(thread_id):
#     if thread_id not in st.session_state["chat_threads"]:
#         st.session_state["chat_threads"].append(thread_id)


# def reset_chat():
#     thread_id = generate_thread_id()
#     st.session_state["thread_id"] = thread_id
#     add_thread(thread_id)
#     st.session_state["message_history"] = []

#     if "chat_histories" not in st.session_state:
#         st.session_state["chat_histories"] = {}
#     st.session_state["chat_histories"][thread_id] = []

#     if "chat_thread_names" not in st.session_state:
#         st.session_state["chat_thread_names"] = {}
#     count = len(st.session_state["chat_threads"])
#     now_str = datetime.now().strftime("%b %d, %Y %H:%M")
#     st.session_state["chat_thread_names"][thread_id] = f"Chat {count + 1} - {now_str}"


# # =================
# # FRONTEND (Streamlit)
# # =================
# def run_emotion_chat():
#     st.subheader("🗣️ Emotion-Based Chatbot")

#     # ---- SESSION SETUP ----
#     if "message_history" not in st.session_state:
#         st.session_state["message_history"] = []
#     if "thread_id" not in st.session_state:
#         st.session_state["thread_id"] = generate_thread_id()
#     if "chat_threads" not in st.session_state:
#         st.session_state["chat_threads"] = retrieve_all_threads()
#     if "chat_thread_names" not in st.session_state:
#         st.session_state["chat_thread_names"] = {}

#     add_thread(st.session_state["thread_id"])

#     if st.session_state["thread_id"] not in st.session_state["chat_thread_names"]:
#         count = len(st.session_state["chat_threads"])
#         now_str = datetime.now().strftime("%b %d, %Y %H:%M")
#         st.session_state["chat_thread_names"][
#             st.session_state["thread_id"]
#         ] = f"Chat {count} - {now_str}"

#     CONFIG = {
#         "configurable": {"thread_id": st.session_state["thread_id"]},
#         "metadata": {"thread_id": st.session_state["thread_id"]},
#         "run_name": "chat_run",
#     }

#     # ---- SIDEBAR UI ----
#     st.sidebar.title("LangGraph Chatbot")
#     if st.sidebar.button("New Chat"):
#         reset_chat()

#     st.sidebar.header("My Conversations")
#     for thread_id in st.session_state["chat_threads"][::-1]:
#         name = st.session_state["chat_thread_names"].get(thread_id, str(thread_id))
#         if st.sidebar.button(name, key=f"thread-btn-{thread_id}"):
#             st.session_state["thread_id"] = thread_id
#             CONFIG = {"configurable": {"thread_id": thread_id}}
#             messages = load_conversation(thread_id)

#             temp_messages = []
#             for message in messages:
#                 if isinstance(message, HumanMessage):
#                     role = "user"
#                 elif isinstance(message, AIMessage):
#                     role = "assistant"
#                 elif isinstance(message, LCSystemMessage):
#                     continue
#                 else:
#                     role = "assistant"
#                 temp_messages.append({"role": role, "content": message.content})

#             st.session_state["message_history"] = temp_messages

#     # ---- MAIN CHAT HISTORY ----
#     for m in st.session_state["message_history"]:
#         with st.chat_message(m["role"]):
#             st.markdown(m["content"])

#     # ---- User input and response ----
#     user_input = st.chat_input("Tell me how you're feeling today...")

#     if user_input:
#         thread_id = st.session_state["thread_id"]
#         update_chat_name_from_first_message(st.session_state, thread_id, user_input)

#         st.session_state["message_history"].append(
#             {"role": "user", "content": user_input}
#         )
#         with st.chat_message("user"):
#             st.markdown(user_input)

#         result_state = chatbot.invoke(
#             {"messages": [HumanMessage(content=user_input)]}, config=CONFIG
#         )

#         ai_text = ""
#         msgs = result_state.get("messages", [])
#         if msgs and isinstance(msgs[-1], AIMessage):
#             ai_text = msgs[-1].content
#         else:
#             for msg in reversed(msgs):
#                 if isinstance(msg, AIMessage):
#                     ai_text = msg.content
#                     break

#         with st.chat_message("assistant"):
#             st.markdown(ai_text)

#         st.session_state["message_history"].append(
#             {"role": "assistant", "content": ai_text}
#         )


# if __name__ == "__main__":
#     run_emotion_chat()


import streamlit as st
from datetime import datetime
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage as LCSystemMessage,
)

from utils.chatbot.backend import (
    chatbot,
    generate_thread_id,
    retrieve_all_threads,
    load_conversation,
    update_chat_name_from_first_message,
)

# Import the new breathing exercise tool
from utils.chatbot.tools.breathing_exercises import (
    breathing_exercise_tool,
)  # Adjust path if needed
from utils.chatbot.tools.spotify_recommender import spotify_music_tool
from utils.chatbot.tools.daily_checkin import daily_checkin_tool


# ========================
# Frontend utilities
# ========================
def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []

    if "chat_histories" not in st.session_state:
        st.session_state["chat_histories"] = {}
    st.session_state["chat_histories"][thread_id] = []

    if "chat_thread_names" not in st.session_state:
        st.session_state["chat_thread_names"] = {}
    count = len(st.session_state["chat_threads"])
    now_str = datetime.now().strftime("%b %d, %Y %H:%M")
    st.session_state["chat_thread_names"][thread_id] = f"Chat {count + 1} - {now_str}"


# =================
# FRONTEND (Streamlit)
# =================
def run_emotion_chat():
    st.subheader("🗣️ Emotion-Based Chatbot")

    # ---- SESSION SETUP ----
    if "message_history" not in st.session_state:
        st.session_state["message_history"] = []
    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = generate_thread_id()
    if "chat_threads" not in st.session_state:
        st.session_state["chat_threads"] = retrieve_all_threads()
    if "chat_thread_names" not in st.session_state:
        st.session_state["chat_thread_names"] = {}

    # Initialize spotify_token_info
    if "spotify_token_info" not in st.session_state:
        st.session_state["spotify_token_info"] = None

    add_thread(st.session_state["thread_id"])

    if st.session_state["thread_id"] not in st.session_state["chat_thread_names"]:
        count = len(st.session_state["chat_threads"])
        now_str = datetime.now().strftime("%b %d, %Y %H:%M")
        st.session_state["chat_thread_names"][
            st.session_state["thread_id"]
        ] = f"Chat {count} - {now_str}"

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_run",
    }

    # ---- SIDEBAR UI ----
    st.sidebar.title("LangGraph Chatbot")
    if st.sidebar.button("New Chat"):
        reset_chat()

    # Add the breathing exercise tool to the sidebar
    st.sidebar.markdown("---")  # Separator
    # st.sidebar.markdown("## 🧘 Wellness Tools")
    # with st.sidebar:
    #     # breathing_exercise_tool()
    #     # spotify_music_tool()
        
    #     st.sidebar.markdown("---")  # Separator

    st.sidebar.header("My Conversations")
    for thread_id in st.session_state["chat_threads"][::-1]:
        name = st.session_state["chat_thread_names"].get(thread_id, str(thread_id))
        if st.sidebar.button(name, key=f"thread-btn-{thread_id}"):
            st.session_state["thread_id"] = thread_id
            CONFIG = {"configurable": {"thread_id": thread_id}}
            messages = load_conversation(thread_id)

            temp_messages = []
            for message in messages:
                if isinstance(message, HumanMessage):
                    role = "user"
                elif isinstance(message, AIMessage):
                    role = "assistant"
                elif isinstance(message, LCSystemMessage):
                    continue
                else:
                    role = "assistant"
                temp_messages.append({"role": role, "content": message.content})

            st.session_state["message_history"] = temp_messages

    # ---- MAIN CHAT HISTORY ----
    for m in st.session_state["message_history"]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # ---- User input and response ----
    user_input = st.chat_input("Tell me how you're feeling today...")

    if user_input:
        thread_id = st.session_state["thread_id"]
        update_chat_name_from_first_message(st.session_state, thread_id, user_input)

        st.session_state["message_history"].append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(user_input)

        result_state = chatbot.invoke(
            {"messages": [HumanMessage(content=user_input)]}, config=CONFIG
        )

        ai_text = ""
        msgs = result_state.get("messages", [])
        if msgs and isinstance(msgs[-1], AIMessage):
            ai_text = msgs[-1].content
        else:
            for msg in reversed(msgs):
                if isinstance(msg, AIMessage):
                    ai_text = msg.content
                    break

        with st.chat_message("assistant"):
            st.markdown(ai_text)

        st.session_state["message_history"].append(
            {"role": "assistant", "content": ai_text}
        )


if __name__ == "__main__":
    run_emotion_chat()
