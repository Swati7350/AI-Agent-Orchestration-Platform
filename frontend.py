# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq

from agent_store import (
    save_agent,
    load_agents,
    route_agent,
    run_agent,
    save_all_agents,
    load_chat_history,
    save_chat_history
)
from whatsapp_service import (
    send_whatsapp_message
)
# ===================================
# PAGE CONFIG
# ===================================
st.set_page_config(
    page_title="LangGraph Agent UI",
    layout="wide"
)

# ===================================
# SESSION STATE
# ===================================
if "agents" not in st.session_state:
    st.session_state.agents = load_agents()

if "show_agents" not in st.session_state:
    st.session_state.show_agents = False

if "show_manage_agents" not in st.session_state:
    st.session_state.show_manage_agents = False

# restore chat on reload
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

if "active_agent" not in st.session_state:
    st.session_state.active_agent = None

if "show_whatsapp" not in st.session_state:
    st.session_state.show_whatsapp = False

# ===================================
# SIDEBAR → VIEW AGENTS
# ===================================
with st.sidebar:

    if st.button("📂 View All Agents"):
        st.session_state.show_agents = (
            not st.session_state.show_agents
        )

    if st.session_state.show_agents:

        agents = st.session_state.agents

        if not agents:
            st.info("No agents found.")

        else:
            for name, config in agents.items():

                with st.expander(f"🤖 {name}"):

                    st.write(
                        f"**Model:** "
                        f"{config['model_name']}"
                    )

                    st.write(
                        f"**Provider:** "
                        f"{config['model_provider']}"
                    )

                    st.write(
                        f"**Search:** "
                        f"{config['allow_search']}"
                    )

                    st.write("**Prompt:**")

                    st.text_area(
                        "Prompt",
                        value=config["system_prompt"],
                        height=120,
                        disabled=True,
                        key=f"prompt_{name}"
                    )


# ===================================
# SIDEBAR → MANAGE AGENTS
# ===================================
with st.sidebar:

    if st.button("⚙️ Manage Agents"):
        st.session_state.show_manage_agents = (
            not st.session_state.show_manage_agents
        )

    if st.session_state.show_manage_agents:

        action = st.selectbox(
            "Action",
            ["Edit Agent", "Delete Agent"]
        )

        agents = st.session_state.agents

        # ---------------- EDIT ----------------
        if action == "Edit Agent":

            agent_name = st.selectbox(
                "Select Agent",
                list(agents.keys())
            )

            model = st.text_input(
                "Model Name",
                agents[agent_name]["model_name"]
            )

            provider = st.text_input(
                "Provider",
                agents[agent_name]["model_provider"]
            )

            prompt = st.text_area(
                "System Prompt",
                agents[agent_name]["system_prompt"]
            )

            if st.button("💾 Update"):

                agents[agent_name][
                    "model_name"
                ] = model

                agents[agent_name][
                    "model_provider"
                ] = provider

                agents[agent_name][
                    "system_prompt"
                ] = prompt

                st.session_state.agents = (
                    agents
                )

                save_agent({
                    "name": agent_name,
                    **agents[agent_name]
                })

                st.success(
                    f"Agent '{agent_name}' updated!"
                )

        # ---------------- DELETE ----------------
        elif action == "Delete Agent":

            agent_name = st.selectbox(
                "Select Agent to Delete",
                list(agents.keys())
            )

            if st.button("🗑️ Delete"):

                del agents[agent_name]

                st.session_state.agents = (
                    agents
                )

                save_all_agents(agents)

                st.success(
                    f"Agent '{agent_name}' deleted!"
                )


# ===================================
# MAIN LAYOUT
# ===================================
left_col, right_col = st.columns([7, 3])


# ===================================
# LEFT → CREATE AGENT
# ===================================
with left_col:

    st.title("AI Chatbot Agents")
    st.write(
        "Create and Interact with AI Agents!"
    )

    agent_name = st.text_input(
        "Agent Name"
    )

    system_prompt = st.text_area(
        "Define your AI System Prompt:",
        height=100
    )

    MODEL_NAMES_GROQ = [
        "llama-3.3-70b-versatile",
        "mixtral-8x7b-32768"
    ]

    MODEL_NAMES_OPENAI = [
        "gpt-4o-mini"
    ]

    provider = st.radio(
        "Select Provider:",
        ("Groq", "OpenAI")
    )

    if provider == "Groq":

        selected_model = st.selectbox(
            "Select Groq Model:",
            MODEL_NAMES_GROQ
        )

    else:

        selected_model = st.selectbox(
            "Select OpenAI Model:",
            MODEL_NAMES_OPENAI
        )

    allow_web_search = st.checkbox(
        "Allow Web Search"
    )

    user_query = st.text_area(
        "Ask a Test query with AI:",
        height=150,
        placeholder="Ask Anything!"
    )

    spacer, button_col = st.columns([3, 2])

    with button_col:

        if st.button(
            "💾 Save Agent",
            use_container_width=True
        ):

            if agent_name.strip():

                agent_data = {
                    "name": agent_name,
                    "model_name":
                        selected_model,
                    "model_provider":
                        provider,
                    "system_prompt":
                        system_prompt,
                    "allow_search":
                        allow_web_search
                }

                save_agent(agent_data)

                # refresh session
                st.session_state.agents = (
                    load_agents()
                )

                st.success(
                    "Agent saved!"
                )

            else:
                st.error(
                    "Enter agent name"
                )

    # ---------------- TEST AGENT ----------------
    if st.button("Ask Agent!"):

        if user_query.strip():

            import requests

            payload = {
                "model_name":
                    selected_model,
                "model_provider":
                    provider,
                "system_prompt":
                    system_prompt,
                "messages":
                    [user_query],
                "allow_search":
                    allow_web_search
            }

            API_URL = (
                "http://127.0.0.1:9999/chat"
            )

            response = requests.post(
                API_URL,
                json=payload
            )

            if response.status_code == 200:

                response_data = (
                    response.json()
                )

                if "error" in response_data:

                    st.error(
                        response_data["error"]
                    )

                else:

                    st.subheader(
                        "**Agent Response**"
                    )

                    st.markdown(
                        response_data[
                            "response"
                        ]
                    )


# ===================================
# RIGHT → CHAT
# ===================================
with right_col:

    st.subheader(
        "💬 Chat With Agent"
    )

    # render old messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_message = st.chat_input(
        "Message agent..."
    )

    if user_message:

        llm = ChatGroq(
            model="llama-3.3-70b-versatile"
        )

        agents = st.session_state.agents

        if st.session_state.active_agent is None:

            agent_name = route_agent(
                user_message,
                llm,
                agents
            )

            st.session_state.active_agent = (
                agent_name
            )

        agent = agents[
            st.session_state.active_agent
        ]

        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })

        save_chat_history(
            st.session_state.messages
        )

        # FIXED
        response = run_agent(
            agent,
            user_message,
            llm,
            st.session_state.messages[:-1]
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        # trigger whatsapp UI
        if "whatsapp" in response.lower():
            st.session_state.show_whatsapp = True

        save_chat_history(
            st.session_state.messages
        )

        st.rerun()

    # ===================================
    # WHATSAPP SHARE UI
    # ===================================
    # ===================================
# WHATSAPP SHARE
# ===================================
st.divider()

st.markdown("### 📲 Share Discussion")
st.info(
    "Send your finalized details to WhatsApp.\n\n"
    "✔ Enter 10-digit mobile number (India)\n\n"
    "✔ Or include country code (+91XXXXXXXXXX)\n\n"
    "✔ Click send to receive your discussion instantly"
)
phone = st.text_input(
    "WhatsApp Number",
    placeholder="9876543210"
)

if st.button("🟢 Send via WhatsApp"):

    if not phone.strip():
        st.warning(
            "Enter phone number"
        )

    elif len(st.session_state.messages) < 2:
        st.warning(
            "No itinerary found."
        )

    else:

        # latest assistant response
        itinerary = None

        for msg in reversed(
            st.session_state.messages
        ):
            if msg["role"] == "assistant":
                itinerary = msg["content"]
                break

        send_whatsapp_message(
            phone,
            itinerary
        )

        st.success(
            "Travel plan sent on WhatsApp!"
        )