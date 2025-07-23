##This version excludes sensitive data and the .env file. This was created to speed up verifying 12,000 module data that had to be reworked. 

# 📘 How to Use the QCP Tool

## ✅ Requirements

- Python must be installed on your system.
- Ensure your `.env` file is properly configured with database access credentials.

## 🔧 Configure the `.env` File

Fill in the following parameters in your `.env` file:

DB_USER=
DB_PASSWORD=
DB_DSN=
PARAM_ID=

> 💡 If you want to test multiple parameters, change the param_id and save it.

## ▶️ Running the Script

You can run the script in one of two ways:

1. **Using an IDE (e.g. VS Code, Cursor):**

   - Open the project folder.
   - Run `qcp-tool.py`.

2. **Using a Terminal or PowerShell:**
   - Navigate to the script directory.
   - Run the script with:
     ```
     python qcp-tool.py
     ```

---

## 🧪 Using the Tool

1. **Enter LOT_IDs:**

   - Paste each `LOT_ID` on a new line.
   - Press `Enter` once after your last item, then press `Enter` again to confirm.

2. **Enter Expected Values:**
   - Paste the expected values in the same order (one per line).
   - Use the same double-enter process to submit.

---

## 📊 Output

- The script will check each `LOT_ID` and compare the actual database value to your expected value.
- You will see:
  - ✅ **Matches**
  - ❌ **Mismatches**
  - ⚠️ **Missing data**
  - 🚩 **Flags** for any `LOT_ID` that contains a `boolean = 'F'` (Out of spec)

All results will be displayed in the terminal after the script finishes running.
