import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from database import Database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import font as tkfont

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Set color scheme
        self.bg_color = "#f0f0f0"
        self.accent_color = "#4a7abc"
        self.button_color = "#4CAF50"
        self.delete_button_color = "#f44336"
        self.text_color = "#333333"
        
        self.root.configure(bg=self.bg_color)
        
        # Set fonts
        self.header_font = tkfont.Font(family="Arial", size=16, weight="bold")
        self.label_font = tkfont.Font(family="Arial", size=10)
        self.button_font = tkfont.Font(family="Arial", size=10, weight="bold")
        
        self.db = Database()
        self.current_user_id = None
        self.username = None
        
        # Start with login screen
        self.show_login_screen()

    def show_login_screen(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create a frame with some padding and a border
        frame = tk.Frame(self.root, padx=30, pady=30, bg=self.bg_color, 
                         highlightbackground=self.accent_color, highlightthickness=2)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # App title
        title_label = tk.Label(frame, text="Expense Tracker", font=("Arial", 24, "bold"), 
                               bg=self.bg_color, fg=self.accent_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Login subtitle
        login_label = tk.Label(frame, text="Login or Register", font=("Arial", 14), 
                              bg=self.bg_color, fg=self.text_color)
        login_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Username field
        tk.Label(frame, text="Username:", font=self.label_font, 
                bg=self.bg_color, fg=self.text_color).grid(row=2, column=0, sticky="e", pady=10)
        self.username_entry = tk.Entry(frame, width=25, font=self.label_font)
        self.username_entry.grid(row=2, column=1, pady=10, padx=5)
        
        # Password field
        tk.Label(frame, text="Password:", font=self.label_font, 
                bg=self.bg_color, fg=self.text_color).grid(row=3, column=0, sticky="e", pady=10)
        self.password_entry = tk.Entry(frame, width=25, show="*", font=self.label_font)
        self.password_entry.grid(row=3, column=1, pady=10, padx=5)
        
        # Button frame
        button_frame = tk.Frame(frame, bg=self.bg_color)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Login button
        login_btn = tk.Button(button_frame, text="Login", command=self.login, 
                             bg=self.accent_color, fg="white", font=self.button_font,
                             width=10, padx=10, pady=5)
        login_btn.pack(side=tk.LEFT, padx=10)
        
        # Register button
        register_btn = tk.Button(button_frame, text="Register", command=self.register, 
                               bg=self.button_color, fg="white", font=self.button_font,
                               width=10, padx=10, pady=5)
        register_btn.pack(side=tk.LEFT, padx=10)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        user_id = self.db.validate_user(username, password)
        if user_id:
            self.current_user_id = user_id
            self.username = username
            self.show_main_app()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        success = self.db.add_user(username, password)
        if success:
            messagebox.showinfo("Success", "Registration successful. You can now login.")
        else:
            messagebox.showerror("Registration Failed", "Username already exists")
            
    def show_main_app(self):
        # Clear login screen
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create top frame for user info and logout
        top_frame = tk.Frame(self.root, bg=self.accent_color, height=50)
        top_frame.pack(fill=tk.X)
        
        # Welcome message
        welcome_label = tk.Label(top_frame, text=f"Welcome, {self.username}!", 
                                font=("Arial", 12, "bold"), bg=self.accent_color, fg="white")
        welcome_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Logout button
        logout_btn = tk.Button(top_frame, text="Logout", command=self.show_login_screen, 
                             bg="white", fg=self.accent_color, font=self.button_font)
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Create notebook for tabs
        style = ttk.Style()
        style.configure("TNotebook", background=self.bg_color)
        style.configure("TNotebook.Tab", padding=[10, 5], font=('Arial', 10))
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Create tabs
        expenses_tab = ttk.Frame(notebook)
        income_tab = ttk.Frame(notebook)
        history_tab = ttk.Frame(notebook)
        charts_tab = ttk.Frame(notebook)
        
        notebook.add(expenses_tab, text="Expenses")
        notebook.add(income_tab, text="Income")
        notebook.add(history_tab, text="Transaction History")
        notebook.add(charts_tab, text="Charts")
        
        # Set up the tabs
        self.setup_expenses_tab(expenses_tab)
        self.setup_income_tab(income_tab)
        self.setup_history_tab(history_tab)
        self.setup_charts_tab(charts_tab)
        
    def setup_expenses_tab(self, parent):
        # Frame for the form with a border
        form_frame = tk.Frame(parent, padx=15, pady=15, bg=self.bg_color,
                             highlightbackground=self.accent_color, highlightthickness=1)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        tk.Label(form_frame, text="Add New Expense", font=self.header_font, 
                bg=self.bg_color, fg=self.accent_color).grid(row=0, column=0, columnspan=6, pady=(0, 15), sticky="w")
        
        # Amount input
        tk.Label(form_frame, text="Amount ($):", font=self.label_font, 
                bg=self.bg_color, fg=self.text_color).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.expense_amount_entry = tk.Entry(form_frame, width=10, font=self.label_font)
        self.expense_amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Category input
        tk.Label(form_frame, text="Category:", font=self.label_font, 
                bg=self.bg_color, fg=self.text_color).grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.expense_category_var = tk.StringVar()
        categories = ["Food", "Housing", "Transportation", "Entertainment", "Utilities", "Shopping", "Health", "Education", "Other"]
        self.expense_category_dropdown = ttk.Combobox(form_frame, textvariable=self.expense_category_var, 
                                                    values=categories, width=15, font=self.label_font)
        self.expense_category_dropdown.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.expense_category_dropdown.current(0)
        
        # Date input
        tk.Label(form_frame, text="Date:", font=self.label_font, 
                bg=self.bg_color, fg=self.text_color).grid(row=1, column=4, padx=5, pady=5, sticky="e")
        self.expense_date_entry = tk.Entry(form_frame, width=12, font=self.label_font)
        self.expense_date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.expense_date_entry.grid(row=1, column=5, padx=5, pady=5, sticky="w")
        
        # Description input
        tk.Label(form_frame, text="Description:", font=self.label_font, 
                bg=self.bg_color, fg=self.text_color).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.expense_description_entry = tk.Entry(form_frame, width=40, font=self.label_font)
        self.expense_description_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")
        
        # Button frame
        button_frame = tk.Frame(form_frame, bg=self.bg_color)
        button_frame.grid(row=2, column=4, columnspan=2, padx=5, pady=5)
        
        # Add button
        add_btn = tk.Button(button_frame, text="Add Expense", command=self.add_expense, 
                          bg=self.button_color, fg="white", font=self.button_font, padx=10, pady=2)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        reset_btn = tk.Button(button_frame, text="Reset", command=self.reset_expense_form, 
                            bg="#FF9800", fg="white", font=self.button_font, padx=10, pady=2)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Expense list frame
        list_frame = tk.Frame(parent, padx=10, pady=10)
        list_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        tk.Label(list_frame, text="Your Expenses", font=self.header_font).pack(anchor=tk.W, pady=(0, 10))
        
        # Create treeview for expenses with custom style
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 10), rowheight=25)
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        
        columns = ("id", "category", "date", "amount", "description")
        self.expense_tree = ttk.Treeview(list_frame, columns=columns, show="headings", style="Treeview")
        
        # Define headings
        self.expense_tree.heading("id", text="ID")
        self.expense_tree.heading("category", text="Category")
        self.expense_tree.heading("date", text="Date")
        self.expense_tree.heading("amount", text="Amount")
        self.expense_tree.heading("description", text="Description")
        
        # Define columns
        self.expense_tree.column("id", width=50)
        self.expense_tree.column("category", width=100)
        self.expense_tree.column("date", width=100)
        self.expense_tree.column("amount", width=100)
        self.expense_tree.column("description", width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.expense_tree.yview)
        self.expense_tree.configure(yscroll=scrollbar.set)
        
        self.expense_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Delete button frame
        delete_frame = tk.Frame(parent, bg=self.bg_color)
        delete_frame.pack(fill=tk.X, padx=10, pady=5)
        
        delete_btn = tk.Button(delete_frame, text="Delete Selected Expense", command=self.delete_expense, 
                             bg=self.delete_button_color, fg="white", font=self.button_font)
        delete_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Load expenses
        self.load_expenses()
        
    def setup_income_tab(self, parent):
        # Frame for the form with a border
        form_frame = tk.Frame(parent, padx=15, pady=15, bg=self.bg_color,
                             highlightbackground=self.accent_color, highlightthickness=1)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        tk.Label(form_frame, text="Add New Income", font=self.header_font, 
                bg=self.bg_color, fg=self.accent_color).grid(row=0, column=0, columnspan=6, pady=(0, 15), sticky="w")
        
        # Amount input
        tk.Label(form_frame, text="Amount ($):", font=self.label_font, 
                bg=self.bg_color, fg=self.text_color).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.income_amount_entry = tk.Entry(form_frame, width=10, font=self.label_font)
        self.income_amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Source input
        tk.Label(form_frame, text="Source:", font=self.label_font, 
                bg=self.bg_color, fg=self.text_color).grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.income_source_var = tk.StringVar()
        sources = ["Salary", "Freelance", "Investment", "Gift", "Bonus", "Refund", "Other"]
        self.income_source_dropdown = ttk.Combobox(form_frame, textvariable=self.income_source_var, 
                                                 values=sources, width=15, font=self.label_font)
        self.income_source_dropdown.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.income_source_dropdown.current(0)
        
        # Date input
        tk.Label(form_frame, text="Date:", font=self.label_font, 
                bg=self.bg_color, fg=self.text_color).grid(row=1, column=4, padx=5, pady=5, sticky="e")
        self.income_date_entry = tk.Entry(form_frame, width=12, font=self.label_font)
        self.income_date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.income_date_entry.grid(row=1, column=5, padx=5, pady=5, sticky="w")
        
        # Button frame
        button_frame = tk.Frame(form_frame, bg=self.bg_color)
        button_frame.grid(row=2, column=0, columnspan=6, padx=5, pady=10)
        
        # Add button
        add_btn = tk.Button(button_frame, text="Add Income", command=self.add_income, 
                          bg=self.button_color, fg="white", font=self.button_font, padx=10, pady=2)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        reset_btn = tk.Button(button_frame, text="Reset", command=self.reset_income_form, 
                            bg="#FF9800", fg="white", font=self.button_font, padx=10, pady=2)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Income list frame
        list_frame = tk.Frame(parent, padx=10, pady=10)
        list_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        tk.Label(list_frame, text="Your Income", font=self.header_font).pack(anchor=tk.W, pady=(0, 10))
        
        # Create treeview for income
        columns = ("id", "amount", "date", "source")
        self.income_tree = ttk.Treeview(list_frame, columns=columns, show="headings", style="Treeview")
        
        # Define headings
        self.income_tree.heading("id", text="ID")
        self.income_tree.heading("amount", text="Amount")
        self.income_tree.heading("date", text="Date")
        self.income_tree.heading("source", text="Source")
        
        # Define columns
        self.income_tree.column("id", width=50)
        self.income_tree.column("amount", width=100)
        self.income_tree.column("date", width=100)
        self.income_tree.column("source", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.income_tree.yview)
        self.income_tree.configure(yscroll=scrollbar.set)
        
        self.income_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Delete button frame
        delete_frame = tk.Frame(parent, bg=self.bg_color)
        delete_frame.pack(fill=tk.X, padx=10, pady=5)
        
        delete_btn = tk.Button(delete_frame, text="Delete Selected Income", command=self.delete_income, 
                             bg=self.delete_button_color, fg="white", font=self.button_font)
        delete_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Load income
        self.load_income()
        
    def setup_history_tab(self, parent):
        # Title frame
        title_frame = tk.Frame(parent, bg=self.bg_color)
        title_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        tk.Label(title_frame, text="Transaction History", font=self.header_font, 
                bg=self.bg_color, fg=self.accent_color).pack(anchor=tk.W)
        
        # Create treeview for transaction history with custom style
        history_frame = tk.Frame(parent)
        history_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        
        columns = ("type", "category", "date", "amount", "description")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", style="Treeview")
        
        # Define headings
        self.history_tree.heading("type", text="Type")
        self.history_tree.heading("category", text="Category/Source")
        self.history_tree.heading("date", text="Date")
        self.history_tree.heading("amount", text="Amount")
        self.history_tree.heading("description", text="Description")
        
        # Define columns
        self.history_tree.column("type", width=80)
        self.history_tree.column("category", width=120)
        self.history_tree.column("date", width=100)
        self.history_tree.column("amount", width=100)
        self.history_tree.column("description", width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load transaction history
        self.load_transactions()
        
    def setup_charts_tab(self, parent):
        chart_frame = tk.Frame(parent, bg=self.bg_color)
        chart_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Title
        tk.Label(chart_frame, text="Data Visualization", font=self.header_font, 
                bg=self.bg_color, fg=self.accent_color).pack(pady=(0, 20))
        
        # Buttons frame
        button_frame = tk.Frame(chart_frame, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        # Expense chart button
        expense_chart_btn = tk.Button(button_frame, text="View Expense Breakdown", 
                                    command=self.show_expense_chart, bg=self.button_color, 
                                    fg="white", font=self.button_font, padx=15, pady=10)
        expense_chart_btn.pack(side=tk.LEFT, padx=20)
        
        # Income chart button
        income_chart_btn = tk.Button(button_frame, text="View Income Breakdown", 
                                   command=self.show_income_chart, bg=self.accent_color, 
                                   fg="white", font=self.button_font, padx=15, pady=10)
        income_chart_btn.pack(side=tk.LEFT, padx=20)
        
    def add_expense(self):
        try:
            amount = float(self.expense_amount_entry.get())
            category = self.expense_category_var.get()
            date = self.expense_date_entry.get()
            description = self.expense_description_entry.get()
            
            if not category or not date:
                messagebox.showwarning("Input Error", "Please fill in all required fields")
                return
                
            self.db.add_expense(self.current_user_id, category, amount, description, date)
            
            # Clear fields
            self.reset_expense_form()
            
            # Reload data
            self.load_expenses()
            self.load_transactions()
            
            messagebox.showinfo("Success", "Expense added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            
    def add_income(self):
        try:
            amount = float(self.income_amount_entry.get())
            source = self.income_source_var.get()
            date = self.income_date_entry.get()
            
            if not source or not date:
                messagebox.showwarning("Input Error", "Please fill in all required fields")
                return
                
            self.db.add_income(self.current_user_id, amount, source, date)
            
            # Clear fields
            self.reset_income_form()
            
            # Reload data
            self.load_income()
            self.load_transactions()
            
            messagebox.showinfo("Success", "Income added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            
    def reset_expense_form(self):
        self.expense_amount_entry.delete(0, tk.END)
        self.expense_description_entry.delete(0, tk.END)
        self.expense_date_entry.delete(0, tk.END)
        self.expense_date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.expense_category_dropdown.current(0)
        
    def reset_income_form(self):
        self.income_amount_entry.delete(0, tk.END)
        self.income_date_entry.delete(0, tk.END)
        self.income_date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.income_source_dropdown.current(0)
            
    def load_expenses(self):
        # Clear current items
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)
            
        # Get expenses from database
        expenses = self.db.get_expenses(self.current_user_id)
        
        # Add to treeview
        for expense in expenses:
            # Format amount as currency
            formatted_amount = f"${expense[3]:.2f}"
            values = (expense[0], expense[1], expense[2], formatted_amount, expense[4])
            self.expense_tree.insert("", tk.END, values=values)
            
        # Add alternating row colors
        for i, item in enumerate(self.expense_tree.get_children()):
            if i % 2 == 0:
                self.expense_tree.item(item, tags=("evenrow",))
            else:
                self.expense_tree.item(item, tags=("oddrow",))
                
        self.expense_tree.tag_configure("evenrow", background="#f0f0f0")
        self.expense_tree.tag_configure("oddrow", background="#ffffff")
            
    def load_income(self):
        # Clear current items
        for item in self.income_tree.get_children():
            self.income_tree.delete(item)
            
        # Get income from database
        income = self.db.get_income(self.current_user_id)
        
        # Add to treeview
        for inc in income:
            # Format amount as currency
            formatted_amount = f"${inc[1]:.2f}"
            values = (inc[0], formatted_amount, inc[2], inc[3])
            self.income_tree.insert("", tk.END, values=values)
            
        # Add alternating row colors
        for i, item in enumerate(self.income_tree.get_children()):
            if i % 2 == 0:
                self.income_tree.item(item, tags=("evenrow",))
            else:
                self.income_tree.item(item, tags=("oddrow",))
                
        self.income_tree.tag_configure("evenrow", background="#f0f0f0")
        self.income_tree.tag_configure("oddrow", background="#ffffff")
            
    def load_transactions(self):
        # Clear current items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        # Get transactions from database
        transactions = self.db.get_transactions(self.current_user_id)
        
        # Add to treeview
        for trans in transactions:
            # Format based on transaction type
            if trans[5] == 'expense':
                amount = f"-${trans[3]:.2f}"
                tag = "expense"
                values = (trans[5].capitalize(), trans[1], trans[2], amount, trans[4])
            else:  # income
                amount = f"+${trans[3]:.2f}"
                tag = "income"
                values = (trans[5].capitalize(), trans[1], trans[2], amount, trans[4])
                
            item_id = self.history_tree.insert("", tk.END, values=values, tags=(tag,))
            
        # Add color coding
        self.history_tree.tag_configure("expense", background="#ffebee")  # Light red for expenses
        self.history_tree.tag_configure("income", background="#e8f5e9")   # Light green for income
            
    def delete_expense(self):
        selected_item = self.expense_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an expense to delete")
            return
            
        # Get the expense ID from the selected item
        expense_id = self.expense_tree.item(selected_item, "values")[0]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?")
        if not confirm:
            return
            
        # Delete from database
        self.db.delete_expense(expense_id)
        
        # Reload data
        self.load_expenses()
        self.load_transactions()
        
        messagebox.showinfo("Success", "Expense deleted successfully!")
        
    def delete_income(self):
        selected_item = self.income_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an income entry to delete")
            return
            
        # Get the income ID from the selected item
        income_id = self.income_tree.item(selected_item, "values")[0]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this income entry?")
        if not confirm:
            return
            
        # Delete from database
        self.db.delete_income(income_id)
        
        # Reload data
        self.load_income()
        self.load_transactions()
        
        messagebox.showinfo("Success", "Income deleted successfully!")
        
    def show_expense_chart(self):
        # Get expense by category data
        expense_data = self.db.get_expense_by_category(self.current_user_id)
        
        if not expense_data:
            messagebox.showinfo("No Data", "No expense data to display")
            return
            
        # Create a new top-level window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Breakdown by Category")
        chart_window.geometry("800x600")
        chart_window.configure(bg=self.bg_color)
        
        # Header
        tk.Label(chart_window, text="Expense Breakdown by Category", 
                font=("Arial", 16, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Create figure and axes
        fig = plt.Figure(figsize=(10, 8), dpi=100)
        
        # Add subplots for pie chart and bar chart
        pie_ax = fig.add_subplot(121)  # 1 row, 2 cols, 1st plot
        bar_ax = fig.add_subplot(122)  # 1 row, 2 cols, 2nd plot
        
        # Extract categories and amounts
        categories = [item[0] for item in expense_data]
        amounts = [item[1] for item in expense_data]
        
        # Create pie chart
        wedges, texts, autotexts = pie_ax.pie(amounts, autopct='%1.1f%%', startangle=90, 
                                           explode=[0.05] * len(categories),
                                           shadow=True, radius=1.1)
        
        # Style pie chart
        plt.setp(autotexts, size=9, weight="bold")
        pie_ax.set_title("Expense Breakdown (Pie Chart)")
        pie_ax.legend(wedges, categories, title="Categories", loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1))
        
        # Create bar chart
        bars = bar_ax.bar(categories, amounts, color='skyblue', width=0.6, edgecolor='grey')
        
        # Style bar chart
        bar_ax.set_title("Expense Breakdown (Bar Chart)")
        bar_ax.set_xlabel("Category")
        bar_ax.set_ylabel("Amount ($)")
        bar_ax.tick_params(axis='x', rotation=45)
        
        # Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            bar_ax.annotate(f'${height:.2f}',
                          xy=(bar.get_x() + bar.get_width() / 2, height),
                          xytext=(0, 3),  # 3 points vertical offset
                          textcoords="offset points",
                          ha='center', va='bottom', rotation=0)
        
        # Adjust layout
        fig.tight_layout()
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Close button
        close_btn = tk.Button(chart_window, text="Close", command=chart_window.destroy, 
                            bg=self.accent_color, fg="white", font=self.button_font)
        close_btn.pack(pady=10)
        
    def show_income_chart(self):
        # Get income by source data
        income_data = self.db.get_income_by_source(self.current_user_id)
        
        if not income_data:
            messagebox.showinfo("No Data", "No income data to display")
            return
            
        # Create a new top-level window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Income Breakdown by Source")
        chart_window.geometry("800x600")
        chart_window.configure(bg=self.bg_color)
        
        # Header
        tk.Label(chart_window, text="Income Breakdown by Source", 
                font=("Arial", 16, "bold"), bg=self.bg_color).pack(pady=10)
        
        # Create figure and axes
        fig = plt.Figure(figsize=(10, 8), dpi=100)
        
        # Add subplots for pie chart and histogram
        pie_ax = fig.add_subplot(121)  # 1 row, 2 cols, 1st plot
        hist_ax = fig.add_subplot(122)  # 1 row, 2 cols, 2nd plot
        
        # Extract sources and amounts
        sources = [item[0] for item in income_data]
        amounts = [item[1] for item in income_data]
        
        # Create pie chart
        wedges, texts, autotexts = pie_ax.pie(amounts, autopct='%1.1f%%', startangle=90,
                                           explode=[0.05] * len(sources),
                                           shadow=True, radius=1.1)
        
        # Style pie chart
        plt.setp(autotexts, size=9, weight="bold")
        pie_ax.set_title("Income by Source (Pie Chart)")
        pie_ax.legend(wedges, sources, title="Sources", loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1))
        
        # Create histogram
        bars = hist_ax.bar(sources, amounts, color='lightgreen', width=0.6, edgecolor='grey')
        
        # Style histogram
        hist_ax.set_title("Income by Source (Histogram)")
        hist_ax.set_xlabel("Source")
        hist_ax.set_ylabel("Amount ($)")
        hist_ax.tick_params(axis='x', rotation=45)
        
        # Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            hist_ax.annotate(f'${height:.2f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),  # 3 points vertical offset
                           textcoords="offset points",
                           ha='center', va='bottom', rotation=0)
        
        # Adjust layout
        fig.tight_layout()
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Close button
        close_btn = tk.Button(chart_window, text="Close", command=chart_window.destroy, 
                            bg=self.accent_color, fg="white", font=self.button_font)
        close_btn.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()