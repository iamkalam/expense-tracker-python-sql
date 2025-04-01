import sqlite3
import datetime
import os

class Database:
    def __init__(self, db_name="expense_tracker.db"):
        """Initialize database connection and create tables if they don't exist"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        
    def create_tables(self):
        """Create necessary tables for the expense tracker application"""
        # Create User table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        
        # Create Expenses table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Create Income table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            source TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Add a default user if none exists for testing purposes
        self.cursor.execute("SELECT COUNT(*) FROM users")
        if self.cursor.fetchone()[0] == 0:
            self.add_user("admin", "admin123")
            
        self.conn.commit()
    
    # User management functions
    def add_user(self, username, password):
        """Add a new user to the database"""
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                               (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Username already exists
            return False
    
    def validate_user(self, username, password):
        """Validate user credentials and return user id if valid"""
        self.cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", 
                           (username, password))
        user = self.cursor.fetchone()
        return user[0] if user else None
    
    # Expense functions
    def add_expense(self, user_id, category, amount, description, date=None):
        """Add a new expense record"""
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        self.cursor.execute(
            "INSERT INTO expenses (user_id, category, date, amount, description) VALUES (?, ?, ?, ?, ?)",
            (user_id, category, date, amount, description)
        )
        self.conn.commit()
    
    def get_expenses(self, user_id):
        """Get all expenses for a user"""
        self.cursor.execute(
            "SELECT id, category, date, amount, description FROM expenses WHERE user_id = ? ORDER BY date DESC",
            (user_id,)
        )
        return self.cursor.fetchall()
    
    def delete_expense(self, expense_id):
        """Delete an expense record"""
        self.cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()
    
    # Income functions
    def add_income(self, user_id, amount, source, date=None):
        """Add a new income record"""
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        self.cursor.execute(
            "INSERT INTO income (user_id, amount, date, source) VALUES (?, ?, ?, ?)",
            (user_id, amount, date, source)
        )
        self.conn.commit()
    
    def get_income(self, user_id):
        """Get all income records for a user"""
        self.cursor.execute(
            "SELECT id, amount, date, source FROM income WHERE user_id = ? ORDER BY date DESC",
            (user_id,)
        )
        return self.cursor.fetchall()
    
    def delete_income(self, income_id):
        """Delete an income record"""
        self.cursor.execute("DELETE FROM income WHERE id = ?", (income_id,))
        self.conn.commit()
    
    # Transaction history (combines expenses and income)
    def get_transactions(self, user_id):
        """Get all transactions (expenses and income) for a user"""
        self.cursor.execute(
            "SELECT id, category, date, amount, description, 'expense' as type FROM expenses WHERE user_id = ?"
            " UNION ALL "
            "SELECT id, source, date, amount, 'Income' as description, 'income' as type FROM income WHERE user_id = ?"
            " ORDER BY date DESC",
            (user_id, user_id)
        )
        return self.cursor.fetchall()
    
    # For data visualization
    def get_expense_by_category(self, user_id):
        """Get expense totals grouped by category for charts"""
        self.cursor.execute(
            "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category",
            (user_id,)
        )
        return self.cursor.fetchall()
    
    def get_income_by_source(self, user_id):
        """Get income totals grouped by source for charts"""
        self.cursor.execute(
            "SELECT source, SUM(amount) FROM income WHERE user_id = ? GROUP BY source",
            (user_id,)
        )
        return self.cursor.fetchall()
        
    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()