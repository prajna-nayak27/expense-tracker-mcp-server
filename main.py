from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

CATEGORY_FILE_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

# Create FastMCP server instance
mcp = FastMCP(name="ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            date TEXT NOT NULL,
            description TEXT DEFAULT ''
        )""")
        conn.commit()

init_db()

@mcp.tool
def add_expense(date, amount, category, subcategory="", description=""):
    """Add a new expense to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("""
                INSERT INTO expenses (date, amount, category, subcategory, description)
                VALUES (?, ?, ?, ?, ?)""", (date, amount, category, subcategory, description))
        conn.commit()
    return {"status": "success", "expense_id": cur.lastrowid}


@mcp.tool
def list_all_expenses():
    """List all expenses in the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT * FROM expenses")
        rows = cur.fetchall()
    return [dict(id=row[0], amount=row[1], category=row[2], subcategory=row[3], date=row[4], description=row[5]) for row in rows]

@mcp.tool
def delete_expense(expense_id):
    """Delete an expense by its ID."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
    return {"status": "success", "deleted_expense_id": expense_id}

@mcp.tool
def add_credit(date, amount, description=""):
    """Add a credit entry to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("""
                INSERT INTO expenses (date, amount, category, description)
                VALUES (?, ?, 'credit', ?)""", (date, amount, description))
        conn.commit()
    return {"status": "success", "credit_id": cur.lastrowid}

@mcp.tool
def edit_expense(expense_id, date=None, amount=None, category=None, subcategory=None, description=None):
    """Edit an existing expense."""
    fields = []
    params = []
    if date is not None:
        fields.append("date = ?")
        params.append(date)
    if amount is not None:
        fields.append("amount = ?")
        params.append(amount)
    if category is not None:
        fields.append("category = ?")
        params.append(category)
    if subcategory is not None:
        fields.append("subcategory = ?")
        params.append(subcategory)
    if description is not None:
        fields.append("description = ?")
        params.append(description)

    params.append(expense_id)
    query = f"UPDATE expenses SET {', '.join(fields)} WHERE id = ?"

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query, params)
        conn.commit()
    return {"status": "success", "edited_expense_id": expense_id}

@mcp.tool
def get_expense_summary(start_date=None, end_date=None):
    """Get a summary of expenses grouped by category."""
    query = "SELECT category, SUM(amount) FROM expenses WHERE 1=1"
    params = []
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    query += " GROUP BY category"

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(query, params)
        rows = cur.fetchall()
    return {row[0]: row[1] for row in rows}

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    #Read categories from a static JSON file
    with open(CATEGORY_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run(host="0.0.0.0", port=8000, transport="http")