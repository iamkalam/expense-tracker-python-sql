# Expense Tracker Application

## Overview
The Expense Tracker is a simple application designed to help users manage their expenses efficiently. It provides a user-friendly interface built with Tkinter and utilizes a database for storing expense records.

## Features
- Add, view, and delete expenses.
- User-friendly GUI for easy navigation.
- Persistent storage of expenses using a database.

## File Structure
```
expense-tracker
├── main.py               # Main application logic and GUI
├── database.py           # Database handling and operations
├── assets
│   └── icons
│       └── app_icon.ico  # Application icon
├── tests
│   ├── test_database.py   # Unit tests for database functions
│   └── test_main.py       # Unit tests for main application
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Setup Instructions
1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```
4. Run the application using:
   ```
   python main.py
   ```

## Usage
- Launch the application to view the main interface.
- Use the provided options to add new expenses, view existing ones, or delete them as needed.

## Requirements
- Python 3.x
- Tkinter
- Any additional libraries specified in `requirements.txt`

## License
This project is open-source and available for modification and distribution under the MIT License.