# IT Help Desk Management System

A desktop-based IT Help Desk Management System built with **Python,
Tkinter, Microsoft SQL Server, and pyodbc**. It helps support teams
record, track, search, update, analyse, and export employee support
tickets through a graphical interface.

## Features

-   **Dashboard:** View ticket statistics and recent support requests.
-   **Add Ticket:** Record an employee's issue, department, category,
    description, and priority.
-   **View Tickets:** Browse all tickets in a tabular view.
-   **Search Tickets:** Find tickets using available ticket and employee
    details.
-   **Update Ticket:** Change a ticket's status (Open, In Progress, or
    Resolved).
-   **Delete Ticket:** Remove a ticket after confirmation.
-   **Ticket Details:** View the full information for a selected ticket.
-   **Reports & Analytics:** View ticket summaries and breakdowns by
    department, priority, and category, along with average resolution
    time.
-   **Excel Export:** Generate a formatted Excel report with ticket
    records, filters, frozen headings, and colour-coded priority/status
    values.

## Technology Stack

  Component                      Technology
  ------------------------------ ----------------------
  Programming language           Python
  Desktop GUI                    Tkinter
  Database                       Microsoft SQL Server
  Python database connectivity   pyodbc
  Excel report generation        openpyxl
  Development environment        Visual Studio Code

## Project Structure

``` text
IT_HelpDesk_System/
│
├── .venv/                  # Local Python virtual environment (not committed)
├── exports/                # Generated Excel reports
│
├── database.py             # SQL Server connection function
├── main.py                 # Main dashboard and navigation
├── add_ticket.py           # Add a new ticket
├── view_ticket.py          # View all tickets
├── search_ticket.py        # Search tickets
├── update_ticket.py        # Update ticket status
├── delete_ticket.py        # Delete tickets
├── ticket_details.py       # View complete ticket details
├── reports_analytics.py    # Ticket reports and analytics
├── export_reports.py       # Export ticket data to Excel
│
├── database_setup.sql      # Database and table setup script
├── requirements.txt        # Python package dependencies
├── .gitignore              # Files excluded from version control
└── README.md               # Project documentation
```

## Requirements

### Software

1.  Windows.
2.  Python 3.10 or later.
3.  Microsoft SQL Server (the project was configured with the
    `SQLEXPRESS` instance).
4.  SQL Server Management Studio (SSMS), or another SQL query tool.
5.  Microsoft ODBC Driver 18 for SQL Server.
6.  Visual Studio Code (recommended).

### Python packages

Install the packages listed in `requirements.txt`:

``` powershell
python -m pip install -r requirements.txt
```

Tkinter is included with standard Windows Python installations and does
not need to be installed through pip.

## Database Setup

1.  Start the SQL Server service for your SQL Server instance.
2.  Open SQL Server Management Studio and connect to your instance. The
    current local configuration uses `.\SQLEXPRESS` with Windows
    Authentication.
3.  Open and execute `database_setup.sql`.
4.  The script creates the `IT_HelpDesk` database and the `Tickets`
    table if they do not already exist.

The `Tickets` table stores:

-   Ticket ID
-   Employee name
-   Department
-   Issue category
-   Description
-   Priority
-   Status
-   Created date
-   Resolution date

> **Important:** The setup script does not insert sample data. Add
> records through the application or insert your own test records.

## Configure the Database Connection

Open `database.py` and confirm that the connection settings match your
SQL Server installation:

``` python
import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=.\\SQLEXPRESS;"
        "DATABASE=IT_HelpDesk;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return conn
```

If your SQL Server instance has a different name, update the `SERVER`
value. If you use SQL authentication instead of Windows Authentication,
update the connection string accordingly and keep credentials out of
source control.

## Run the Application

Open the project folder in Visual Studio Code.

In the VS Code PowerShell terminal, create and activate a virtual
environment (recommended):

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

``` powershell
python -m pip install -r requirements.txt
```

Start the application from the project root:

``` powershell
python main.py
```

Run an individual module for troubleshooting, if needed:

``` powershell
python add_ticket.py
python view_ticket.py
python search_ticket.py
python update_ticket.py
python delete_ticket.py
python ticket_details.py
python reports_analytics.py
python export_reports.py
```

## Excel Reports

Use the **Export Reports** option in the application to generate an
Excel workbook. Reports are saved in the project's `exports/` directory.
The workbook includes ticket records, report-generation information,
column filters, frozen headings, and colour-coded priority and status
values.

Generated reports may contain employee names and support-ticket
descriptions. Store and share them carefully.

## Ticket Status and Resolution Date

The application uses these ticket statuses:

-   `Open`
-   `In Progress`
-   `Resolved`

When a ticket is marked as Resolved, its resolution date is recorded.
When it is moved back to another status, the resolution date is cleared.

## Troubleshooting

### Cannot connect to SQL Server

-   Confirm that the SQL Server service is running.
-   Confirm the instance name in `database.py`.
-   Confirm that `IT_HelpDesk` exists and that the `Tickets` table has
    been created.
-   Confirm that Microsoft ODBC Driver 18 for SQL Server is installed.
-   Check that Windows Authentication is enabled for the configured
    connection.

### `ModuleNotFoundError: No module named 'pyodbc'`

Activate the project's virtual environment and run:

``` powershell
python -m pip install -r requirements.txt
```

### Excel export fails

Confirm that `openpyxl` is installed and that the application can write
to the project's `exports/` directory.

### A module does not open from the dashboard

Run the relevant `.py` file directly from the project root to view the
full error in the terminal. Check that the filename used by the
dashboard matches the actual filename.

## Notes

-   Run the application from the project root so that module paths
    resolve correctly.
-   The `.venv/` directory should not be uploaded to GitHub. Each user
    should create their own environment and install dependencies.
-   The `exports/` directory contains generated reports; avoid
    committing reports containing real employee information.
-   This project is intended as an academic/portfolio demonstration. Use
    appropriate access controls and data-protection practices before
    adapting it for a real organisation.

## Author

**Harshita Chauhan**\
BCA Student\
Graphic Era Hill University, Dehradun
