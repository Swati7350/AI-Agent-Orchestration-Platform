# 🤖 AI Agent Orchestration Platform

A full-stack AI system to create, configure, and orchestrate multiple AI agents that collaborate autonomously to complete tasks, with real tool execution and external messaging integration.

---

## 🚀 Overview

This platform allows users to:

* Create and manage AI agents (personality, tools, memory, limits)
* Build multi-agent workflows with collaboration
* Run agents using a real execution runtime (not a mock UI)
* Connect at least one agent to external channels (WhatsApp / Telegram / Slack)
* Monitor live agent activity, messages, and execution logs

---

## 🧠 Key Features

* 👤 Agent CRUD (name, role, prompt, model, tools)
* 🔗 Multi-agent workflow orchestration
* 🧠 Memory + message history persistence
* ⚙️ Configurable behavior (rules, schedules, guardrails)
* 💬 External messaging integration (WhatsApp/Telegram/Slack)
* 📊 Real-time logs + monitoring dashboard
* 🔄 Async agent-to-agent communication

---

## 🏗️ Architecture

* **Frontend:** Streamlit / Web UI for agent + workflow management
* **Backend:** Python-based AI runtime (Langchain / custom runtime)
* **Persistence:** Agents Memory, workflows, and message history
* **Messaging Layer:** WhatsApp
* **LLM Provider:** Groq / OpenAI (configurable)

---

## ⚙️ Setup

```bash
conda create -n agent_env python=3.10 -y
conda activate agent_env
pip install -r requirements.txt
pip install pipfile
```

Create `.env` file:

```
GROQ_API_KEY=your_key
OPENAI_API_KEY=your_key
TAVILY_API_KEY=your_key
TWILIO_SID=your_key
TWILIO_AUTH_TOKEN=your_token
```

Run:

```bash
streamlit run frontend.py
```

---

## 📦 Requirements

* Fully working multi-agent runtime (not UI mock)
* At least 2 collaborating agents
* One external messaging-connected agent
* Persistent message history visible in UI
* Real-time execution logs

---

## 📊 Evaluation Focus

* End-to-end working system (40%)
* Architecture + code quality (30%)
* UI/UX + configurability (20%)
* Documentation (10%)

---

## 🧩 Notes

* LangChain allows breaking the system into:
    Tools (WhatsApp sender, search, etc.)
    Prompts (agent behavior definitions)
    Memory (conversation history)
    Chains / Agents (decision logic)
* System must run locally with a single setup command
* Async agent communication is required

---

## ✨ Author

Built for AI Engineer Hiring Challenge · Yuno AI Team
