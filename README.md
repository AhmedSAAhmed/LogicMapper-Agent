# LogicMapper-Agent
An autonomous AI agent built with Google ADK that reverse-engineers legacy code into plain-English business logic and interactive dependency maps.

Modernizing the Enterprise, One Function at a Time.

📖 Overview

LogicMapper is an advanced autonomous multi-agent system designed to solve the critical "Legacy Modernization" problem in enterprise environments.

Legacy systems trap critical business logic in opaque, undocumented silos. LogicMapper automates the discovery, analysis, and refactoring of these systems by "mapping" obscure legacy code into clear, modern architecture specifications using Agentic AI.

⚙️ How the App Works

LogicMapper operates not as a chatbot, but as an autonomous pipeline. Here is the lifecycle of a request:

Ingestion: The user provides a target (a single legacy file, a GitHub repository URL, or a zip upload).

Orchestration (The Brain): The Manager Agent analyzes the request complexity and assigns sub-tasks.

Example: "This is a 2000-line Java file. I need the Context Compressor to shrink it, then the Logic Analyzer to map it."

Discovery Loop: The Scanner Agent reads the code. If it encounters an unknown library or obscure dependency, it uses the Google Search Tool to find documentation, rather than hallucinating functionality.

Logic Extraction: The agents identify "Business Rules" (e.g., "If User > 5 years, Discount = 10%"). These are stored in the Long-Term Memory Bank.

Synthesis: The Architect Agent drafts a modernization plan (e.g., "Convert this monolithic class into a Python Microservice").

Quality Assurance: A separate QA Agent reviews the output. If the code is hallucinated or the logic is vague, it rejects the draft and forces the Architect to try again.

🏗️ Architecture

graph TD
    User[User Input] -->|Submit Repo| Orchestrator
    Orchestrator -->|Dispatch| Scanner[Scanner Agent]
    Scanner -->|Raw Logic| Memory[Vector Memory Bank]
    Memory -->|Context| Analyst[Analyst Agent]
    Analyst -->|Draft Specs| Architect[Architect Agent]
    Architect -->|Review| QA[QA Agent]
    QA -- "Needs Revision" --> Analyst
    QA -- "Approved" --> Final[Final Report]


✅ Prerequisites

Before running LogicMapper, ensure you have the following environment set up:

System Requirements

Python 3.10+: Required for the latest LangChain/CrewAI features.

Git: For cloning the repository.

Docker (Optional): If you wish to run the agent in a sandboxed container.

API Keys Required:

You will need a .env file with the following keys:

GOOGLE_API_KEY: Access to Gemini 2.5 Pro or flash (via Vertex AI or AI Studio).

SERPER_API_KEY: For the Google Search Tool capability.

OPENAI_API_KEY: (Optional) If using OpenAI models as a fallback.

📂 Code Walkthrough

This section outlines the project structure and highlights where specific Hackathon Criteria are implemented.

Directory Structure

LogicMapper/
├── src/
│   ├── agents/              # 🤖 Multi-Agent Logic
│   │   ├── orchestrator.py  # Main entry point for task delegation
│   │   ├── scanner.py       # Code analysis agent
│   │   └── qa_engineer.py   # Self-evaluation loop agent
│   ├── tools/               # 🛠️ Agent Tools (MCP & Custom)
│   │   ├── file_reader.py   # Custom tool for safe file access
│   │   ├── google_search.py # Integration for documentation lookups
│   │   └── code_exec.py     # Sandbox for testing legacy snippets
│   ├── memory/              # 🧠 State & Context Management
│   │   ├── vector_store.py  # Long-term memory implementation
│   │   └── compressor.py    # Context compaction logic
│   └── utils/               # Observability & Logging
│       └── logger.py        # Tracing agent thoughts
├── data/                    # Sample legacy code for testing
├── main.py                  # CLI Entry point
└── app.py                   # Streamlit/Web Interface


Key Implementation Details (For Judges)

Multi-Agent System (Parallel & Sequential)

Location: src/agents/orchestrator.py

Logic: We use a state graph to manage agents. The Scanner runs in parallel to map dependencies, while the Architect runs sequentially after data is gathered.

Tools & MCP

Location: src/tools/

Logic: We implemented a custom Model Context Protocol (MCP) adapter in file_reader.py that allows the agent to "read" local enterprise directories without hallucinating file paths.

Memory & Context Engineering

Location: src/memory/compressor.py

Logic: To handle large legacy files, we implemented Context Compaction. We strip comments and whitespace and summarize functions before sending them to the LLM to save token costs and stay within the context window.

Observability

Location: src/utils/logger.py

Logic: Every "thought" the agent has is logged to the console with a timestamp, allowing us to trace the decision-making process during long-running operations.

🚀 Installation & Setup

Clone the Repository

git clone [https://github.com/yourusername/LogicMapper.git](https://github.com/yourusername/LogicMapper.git)
cd LogicMapper


Install Dependencies

pip install -r requirements.txt


Configure Environment
Create a .env file in the root:

GOOGLE_API_KEY=your_key_here
SERPER_API_KEY=your_key_here


Run the Application

For CLI mode:

python main.py --repo "[https://github.com/legacy-repo/example](https://github.com/legacy-repo/example)"


For Web UI:

streamlit run app.py
