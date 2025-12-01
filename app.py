import streamlit as st
import asyncio
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import tempfile
import shutil
import nest_asyncio
import traceback
import zipfile

# Apply nest_asyncio to allow nested event loops in Streamlit
nest_asyncio.apply()

# LogicMapper Imports
from src.agents.orchestrator import OrchestratorAgent
from src.utils.logger import setup_logger
from src.state.project_state import ProjectState

# Setup Logger
logger = setup_logger("StreamlitUI")

# Page Config
st.set_page_config(
    page_title="LogicMapper Agent",
    page_icon="🧠",
    layout="wide"
)

# Load Environment
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def main():
    st.title("🧠 LogicMapper Agent")
    st.markdown("""
    **Autonomous Legacy Code Modernization**
    
    This agent scans your legacy code, extracts business rules, and generates a modernization strategy.
    """)
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("Configuration")
        model_name = st.selectbox(
            "Select Model",
            ["gemini-2.0-flash", "gemini-2.0-flash-lite-preview-02-05", "gemini-1.5-flash"], 
            index=0
        )
        
        st.divider()
        st.info("✅ System Status: Ready")
        if not api_key:
            st.error("❌ GOOGLE_API_KEY not found!")
        else:
            st.success("🔑 API Key Configured")

    # Main Input Area
    st.subheader("📂 Repository Input")
    
    # Input type selector
    input_type = st.radio(
        "Select input type:",
        ["Local Path", "Git Repository URL"],
        horizontal=True
    )
    
    if input_type == "Local Path":
        repo_path = st.text_input(
            "Local Repository Path",
            value="test_legacy_code.py",
            help="Enter the path to a local file or directory"
        )
    else:
        repo_path = st.text_input(
            "Git Repository URL",
            placeholder="https://github.com/username/repository.git",
            help="Enter the clone URL (not the web URL). Example: https://github.com/user/repo.git"
        )
    
    # Start Button Logic
    if st.button("🚀 Start Analysis", type="primary"):
        target_path = None
        
        # Handle input
        if repo_path:
            target_path = repo_path.strip('"').strip("'")
            
            # Convert GitHub web URLs to git clone URLs
            if "github.com" in target_path:
                if "/blob/" in target_path or "/tree/" in target_path:
                    # Extract the repo part before /blob/ or /tree/
                    for separator in ["/blob/", "/tree/"]:
                        if separator in target_path:
                            parts = target_path.split(separator)
                            target_path = parts[0]
                            break
                    st.info(f"Converted web URL to git URL: {target_path}")
                
                # Add .git if missing
                if not target_path.endswith(".git"):
                    target_path += ".git"
            
        # Validation
        if not target_path:
            st.warning("Please enter a repository path or URL.")
            return
            
        if not api_key:
            st.error("Please configure your GOOGLE_API_KEY in .env file.")
            return

        # Run the Agent
        run_analysis(target_path, model_name)

    # Display Results (Persistent View)
    # If a report was generated in a previous run, show it.
    if os.path.exists("final_report.md"):
        st.divider()
        st.subheader("📝 Modernization Report")
        
        with open("final_report.md", "r", encoding="utf-8") as f:
            report_content = f.read()
            st.markdown(report_content)
            
        st.download_button(
            label="💾 Download Report",
            data=report_content,
            file_name="modernization_plan.md",
            mime="text/markdown"
        )
        
    display_state_results()

def display_state_results():
    """Reads project_state.json and displays detailed results."""
    if os.path.exists("project_state.json"):
        try:
            with open("project_state.json", "r", encoding='utf-8') as f:
                state = json.load(f)
            
            st.divider()
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Files Scanned", len(state.get("scanned_files", [])))
            with col2:
                st.metric("Status", "Complete" if state.get("modernization_plan") else "In Progress")
            with col3:
                st.metric("Language", "Python") # Placeholder
            
            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["📄 Modernization Report", "📊 Scanned Files", "🧠 Business Rules", "🕸️ Dependency Graph"])
            
            with tab1:
                if state.get("modernization_plan"):
                    st.markdown(state["modernization_plan"])
                else:
                    st.info("No report generated yet.")
            
            with tab2:
                st.json(state.get("scanned_files", []))
                
            with tab3:
                # Display rules from analyses
                analyses = state.get("analyses", {})
                for file, data in analyses.items():
                    with st.expander(f"Rules for {file}"):
                        rules = data.get("business_rules", [])
                        if rules:
                            for rule in rules:
                                st.markdown(f"- {rule}")
                        else:
                            st.caption("No rules extracted.")
            
            with tab4:
                st.subheader("System Dependency Graph")
                mermaid_code = state.get("dependency_graph", "")
                if mermaid_code:
                    st.markdown(f"```mermaid\n{mermaid_code}\n```")
                    st.caption("If the chart doesn't render, you can copy the code above into a Mermaid live editor.")
                else:
                    st.info("No dependency graph generated.")
                            
        except Exception as e:
            st.error(f"Error loading state: {e}")

def run_analysis(repo_path, model_name):
    """Runs the agentic workflow using asyncio."""
    status_container = st.status("🕵️ Agent Working...", expanded=True)
    
    try:
        status_container.write("Initializing Agents...")
        orchestrator = OrchestratorAgent(model_name=model_name)
        
        # Check if it's a git URL and show appropriate message
        if repo_path.startswith(('http://', 'https://', 'git@', 'git://')):\
            status_container.write("📥 Cloning repository... (this may take a minute)")
        
        status_container.write("🔍 Scanning Repository...")
        status_container.write("⏳ Large repositories may take several minutes to analyze...")
        
        # --- ROBUST FIX: Handle Event Loop ---
        # Get the current event loop (Streamlit's loop) or create a new one
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        # Use run_until_complete which works with nest_asyncio
        final_report = loop.run_until_complete(orchestrator.process_repository(repo_path))
        
        status_container.update(label="✅ Analysis Complete!", state="complete", expanded=False)
        
        # Save output to file
        with open("final_report.md", "w", encoding="utf-8") as f:
            f.write(final_report)
            
        # Refresh page to show results
        st.rerun()
        
    except Exception as e:
        status_container.update(label="❌ Error Occurred", state="error")
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Streamlit Error: {e}")
        # Log traceback to crash.log
        with open("crash.log", "w") as f:
            f.write(f"Error: {str(e)}\n")
            f.write(traceback.format_exc())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Log fatal crashes to a file since stdout might be lost
        with open("crash.log", "w") as f:
            f.write(f"Fatal Crash: {str(e)}\n")
            f.write(traceback.format_exc())
        st.error("A fatal error occurred. Please check crash.log for details.")
        logger.critical(f"Fatal Crash: {e}", exc_info=True)