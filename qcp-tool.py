import oracledb
import pandas as pd
import traceback
import os
from dotenv import load_dotenv

load_dotenv()  

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dsn = os.getenv("DB_DSN")
param_id = os.getenv("PARAM_ID")

def read_multiline_input(prompt):
    print(prompt)
    print("👉 Paste your values (one per line), then press Enter twice to finish:\n")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line.strip())
    return lines

def check_jdgm_f(cursor, lot_id):
    query = """
        SELECT 1
        FROM table1
        WHERE boolean = 'F' AND LOT_ID = :lot_id
        FETCH FIRST 1 ROWS ONLY
    """
    cursor.execute(query, {"lot_id": lot_id})
    return cursor.fetchone() is not None

lot_ids = read_multiline_input("📦 Enter LOT_IDs:")
expected_values = read_multiline_input("📄 Enter EXPECTED_VALUEs (in the same order):")

if len(lot_ids) != len(expected_values):
    print("❌ The number of LOT_IDs and EXPECTED_VALUEs must match!")
    exit(1)

data_list = [{"LOT_ID": lot_id, "EXPECTED_VALUE": expected} for lot_id, expected in zip(lot_ids, expected_values)]
data = pd.DataFrame(data_list)

try:
    connection = oracledb.connect(
        user=user,
        password=password,
        dsn=dsn
    )
    print("\n✅ Successfully connected to the database!")

    cursor = connection.cursor()

    query = """
        SELECT result, boolean
        FROM (
            SELECT result, boolean
            FROM table1
            WHERE LOT_ID = :lot_id AND param = :param_id
            ORDER BY EVENT_TMST DESC
        )
        WHERE ROWNUM = 1
    """

    for index, row in data.iterrows():
        lot_id = row["LOT_ID"]
        expected_value = str(row["EXPECTED_VALUE"]).strip()

        try:
            cursor.execute(query, {"lot_id": lot_id, "param_id": param_id})
            result = cursor.fetchone()

            if result:
                db_value = str(result[0]).strip()
                if db_value != expected_value:
                    print(f"\n❌ Mismatch for LOT_ID '{lot_id}':")
                    print(f"   Expected: {expected_value}")
                    print(f"   Got     : {db_value}")
                else:
                    
                    print(f"\n✅ Match for LOT_ID '{lot_id}': Value = {db_value}")
            else:
                print(f"\n⚠️ No data found for LOT_ID '{lot_id}'.")

            if check_jdgm_f(cursor, lot_id):
                print(f"🚩 LOT_ID '{lot_id}' is flagged as 'f' due to JDGM_CODE = 'F' record.")

        except Exception:
            print(f"\n❌ Query failed for LOT_ID '{lot_id}':")
            traceback.print_exc()

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
        print("\n🔌 Database connection closed.")
