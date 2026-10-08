# Expense Tracker 

A simple web app for recording and managing personal expenses. Add expenses with a title, amount, category, and date; review totals and transactions; filter by category; and edit or delete records.

## Features

- Add, edit, and delete expenses
- Categorize expenses as Food, Transport, Entertainment, Shopping, Bills, Health, Education, or Other
- Filter the expense list by category
- View the total amount and transaction count for the current list
- Store expense records in a local SQLite database

## Built with

- Python and FastAPI
- SQLAlchemy and SQLite
- HTML, CSS, and JavaScript

## Requirements

- Python 3.9 or later

## Run locally

1. Clone this repository and open a terminal in the project folder.
2. Install the Python dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```
3. Start the development server:

   ```powershell
   py -m uvicorn main:app --reload
   ```
4. Open [http://localhost:8000](http://localhost:8000) in your browser.

The database and tables are created automatically when the app starts. FastAPI's interactive API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Project structure

```text
.
├── main.py              # FastAPI app, database model, and API routes
├── requirements.txt     # Python dependencies
└── static/
    ├── index.html       # Expense Tracker page
    ├── app.js           # Frontend behavior and API requests
    └── style.css        # Page styling
```

## API

| Method     | Endpoint                       | Purpose           |
| ---------- | ------------------------------ | ----------------- |
| `GET`    | `/api/expenses`              | List expenses     |
| `POST`   | `/api/expenses`              | Create an expense |
| `GET`    | `/api/expenses/{expense_id}` | Get one expense   |
| `PUT`    | `/api/expenses/{expense_id}` | Update an expense |
| `DELETE` | `/api/expenses/{expense_id}` | Delete an expense |

Example request body for creating an expense:

```json
{
  "title": "Groceries",
  "amount": 42.5,
  "category": "Food",
  "date": "2026-10-08"
}
```

## Data and privacy

Expense data is stored in `expenses.db` in the project folder. Each local copy of the app has its own database.


#### ABOUT

This is a small project we completed as part of the Software Fellowship Program by LOCUS. It was created as a hands-on activity to practice basic software development concepts and build a simple expense-tracking application.
