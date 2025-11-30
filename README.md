# LogicMapper-Agent
# 🧠 LogicMapper-Agent  
### *An autonomous AI agent—built with Google ADK—that reverse-engineers legacy code into plain-English business logic and interactive dependency maps.*  

> **Modernizing the Enterprise, One Function at a Time.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-%23FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Agents-%234285F4?logo=google)](https://developers.google.com/agent)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📖 Overview

Enterprise legacy systems often hide critical business logic in decades-old, poorly documented code—posing massive risk and cost to modernization.

**LogicMapper-Agent** is an **autonomous multi-agent system** that safely and accurately *reverse-engineers* legacy applications (Java, COBOL, VB6, etc.) by:
- ✅ Extracting **human-readable business rules** (e.g., *“If tenure ≥ 5 years → apply 10% loyalty discount”*)
- ✅ Generating **interactive dependency maps** (function → data → rule)
- ✅ Proposing **modern, cloud-native refactoring plans**
- ✅ Enforcing **zero-hallucination** via rigorous QA loops & real-time documentation lookup

Built on **Google ADK** and powered by **Gemini 2.5 Pro/Flash**, LogicMapper runs as a self-coordinating pipeline—*not a chatbot*.

---

## ⚙️ How It Works

1. **📥 Ingestion**  
   Submit a legacy file, ZIP archive, or GitHub repo URL.

2. **🧠 Orchestration**  
   The *Manager Agent* assesses complexity and dispatches specialized sub-agents.

3. **🔍 Discovery & Search**  
   The *Scanner Agent* parses code—using **Google Search via Serper API** to resolve obscure libraries (no guessing).

4. **🧩 Logic Extraction**  
   Business rules are distilled and stored in a **vectorized memory bank** for traceability.

5. **🏗️ Synthesis**  
   The *Architect Agent* drafts a modernization blueprint (e.g., *“Decompose monolith → 3 microservices with event-driven APIs”*).

6. **✅ Quality Assurance**  
   The *QA Agent* validates logic fidelity and rejects hallucinated or vague proposals—triggering revision loops until output is auditable.

---

## 🏗️ Architecture

```mermaid
graph TD
    User[User Input] -->|Repo / File / ZIP| Orchestrator[Orchestrator Agent]
    Orchestrator -->|Dispatch| Scanner[Scanner Agent]
    Scanner -->|Raw Logic & Dependencies| Memory[Vector Memory Bank]
    Memory -->|Compressed Context| Analyst[Logic Analyst Agent]
    Analyst -->|Draft Spec| Architect[Architect Agent]
    Architect -->|Candidate Plan| QA[QA Agent]
    QA -- "Needs Revision" --> Analyst
    QA -- "Approved" --> Final[Final Report + Interactive Map]
