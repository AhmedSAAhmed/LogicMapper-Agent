# OLD SYSTEM - DO NOT TOUCH
# Author: Bob (2015)

def calc_price(user_type, amount):
    # Business Rule: VIPs get 20% off, but only if spending over 100
    if user_type == "VIP":
        if amount > 100:
            return amount * 0.80
        else:
            return amount
    
    # Business Rule: Tax is hardcoded at 5% for now
    tax = 0.05
    return amount * (1 + tax)

def legacy_db_connect():
    print("Connecting to Oracle 9i...")
```

### Step 2: Run the Main Command
Open your terminal (in VS Code) and run the entry point. We point it at the file we just created.

```bash
python main.py --repo "test_legacy_code.py"
```



### Step 3: Watch the Console Logs (The Real Test)
If the Orchestrator is working, you will see a specific sequence of logs. Here is exactly what to look for to confirm each agent is doing its job:

1.  **Scanner Check:** Look for the "Phase 1" log.
    * *Success:* `🔍 Scanning path: test_legacy_code.py`
    * *Meaning:* The **Tool** (file_system) successfully read the file from your hard drive.
2.  **Memory Check:** Look for the "Phase 2" log.
    * *Success:* `🧠 No prior memory found. Starting fresh.` (On the first run).
    * *Meaning:* The **Memory Bank** (ChromaDB) was queried successfully.
3.  **Analyst Check:** Look for the "Phase 3" log.
    * *Success:* `🧠 Analyzing logic for: test_legacy_code.py`
    * *Meaning:* The **LLM** (Gemini) received the context and is generating the report.

### Step 4: Verify the Output File
Once the script finishes, look at your file explorer. You should see a new file named **`final_report.md`**.

Open it. It should look something like this:

> **Modernization Plan**
> * **Business Rule Found:** VIP users get a 20% discount if spending > 100.
> * **Refactoring:** We recommend moving the hardcoded 5% tax to a configuration file.

### Step 5: The "Memory" Test (Crucial for Hackathon)
To prove the **Long Term Memory** works:

1.  Run the exact same command **again**: `python main.py --repo "test_legacy_code.py"`
2.  Look closely at the **Phase 2** log in the console.
3.  **Success Condition:** Instead of "No prior memory," it should now say:
    ```text
    🧠 Recalled 1 relevant business rules from Memory Bank.