import os
import shutil
import time

def clean_state():
    print("🧹 Cleaning up system state...")
    
    # Files/Folders to remove
    targets = [
        "chroma_db_data",
        "project_state.json",
        "final_report.md",
        "crash.log"
    ]
    
    for target in targets:
        if os.path.exists(target):
            try:
                if os.path.isdir(target):
                    shutil.rmtree(target)
                else:
                    os.remove(target)
                print(f"✅ Removed {target}")
            except Exception as e:
                print(f"❌ Failed to remove {target}: {e}")
        else:
            print(f"ℹ️ {target} not found (already clean)")
            
    print("✨ System reset complete.")

if __name__ == "__main__":
    clean_state()
