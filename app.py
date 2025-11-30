import streamlit as st
import asyncio
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import tempfile
import zipfile
import shutil

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
            ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
            index=0
        )
        
        st.divider()
        st.info("✅ System Status: Ready")
        if not api_key:
            st.error("❌ GOOGLE_API_KEY not found!")
        else:
            st.success("🔑 API Key Configured")

    # Main Input
    col1, col2 = st.columns([1, 1])
    with col1:
        repo_path = st.text_input("Repository Path (Local Path or URL)", value="test_legacy_code.py")
    with col2:
        uploaded_file = st.file_uploader("Or Upload Code (Zip/File)", type=['zip', 'py', 'js', 'java', 'cpp', 'ts'])
    
    if st.button("🚀 Start Analysis", type="primary"):
        target_path = None
        
        # Priority to upload
        if uploaded_file:
            # Create a temp directory for the analysis
            temp_dir = tempfile.mkdtemp(prefix="logicmapper_")
            
            if uploaded_file.name.endswith('.zip'):
                # Save zip
                zip_path = os.path.join(temp_dir, uploaded_file.name)
                with open(zip_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Extract
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Use the temp dir as target
                target_path = temp_dir
                st.info(f"📂 Extracted {uploaded_file.name} for analysis")
                
            else:
                # Single file - save it inside the temp dir
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                target_path = temp_dir # Scan the folder containing the file
                st.info(f"📄 Saved {uploaded_file.name} for analysis")
                
        elif repo_path:
            # Clean the path (remove quotes if user pasted them)
            target_path = repo_path.strip('"').strip("'")
            
        if not target_path:
            st.warning("Please enter a repository path or upload a file.")
            return
            
        if not api_key:
            st.error("Please configure your GOOGLE_API_KEY in .env file.")
            return

        run_analysis(target_path, model_name)

    # Display Results if available
    display_results()

def run_analysis(repo_path, model_name):
    """Runs the agentic workflow."""
    status_container = st.status("🕵️ Agent Working...", expanded=True)
    
    try:
        # Initialize Orchestrator
        status_container.write("Initializing Agents...")
        orchestrator = OrchestratorAgent(model_name=model_name)
        
        # Run the async workflow
        # We use a new event loop for Streamlit compatibility
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        status_container.write("🔍 Scanning Repository...")
        # Note: In a real app, we'd want real-time updates from the agent.
        # For now, we await the full process.
        final_report = loop.run_until_complete(orchestrator.process_repository(repo_path))
        
        status_container.update(label="✅ Analysis Complete!", state="complete", expanded=False)
        
        # Force reload to show results
        st.rerun()
        
    except Exception as e:
        status_container.update(label="❌ Error Occurred", state="error")
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Streamlit Error: {e}")

def display_results():
    """Reads project_state.json and displays results."""
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
                st.metric("Language", "Python") # Placeholder, could be dynamic
            
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
                    # Using a simple way to render mermaid if supported, or just showing code
                    st.markdown(f"```mermaid\n{mermaid_code}\n```")
                    st.caption("If the chart doesn't render, you can copy the code above into a Mermaid live editor.")
                else:
                    st.info("No dependency graph generated.")
                            
        except Exception as e:
            st.error(f"Error loading state: {e}")

if __name__ == "__main__":
    main()
