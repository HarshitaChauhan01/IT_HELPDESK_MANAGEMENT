import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


# =========================
# COLOR THEME
# =========================

BG = "#F4F6FA"
NAVY = "#172B4D"
WHITE = "#FFFFFF"
TEXT = "#1E293B"
MUTED = "#64748B"
BLUE = "#2563EB"
BORDER = "#E2E8F0"


# =========================
# LOAD SEARCH RESULTS
# =========================

def display_records(records):

    for row in ticket_table.get_children():
        ticket_table.delete(row)

    for index, row in enumerate(records):

        values = list(row)

        if values[6]:
            values[6] = values[6].strftime("%d-%b-%Y %I:%M %p")

        ticket_table.insert(
            "",
            tk.END,
            values=values,
            tags=("evenrow" if index % 2 == 0 else "oddrow",)
        )

    result_count.config(text=f"Results Found: {len(records)}")


# =========================
# SEARCH TICKETS
# =========================

def search_tickets():

    search_value = search_entry.get().strip()

    if not search_value:
        messagebox.showwarning(
            "Missing Input",
            "Please enter something to search."
        )
        search_entry.focus()
        return

    conn = None

    try:

        search_button.config(state="disabled", text="Searching...")
        root.update_idletasks()

        conn = get_connection()
        cursor = conn.cursor()

        search_pattern = f"%{search_value}%"

        query = """
        SELECT Ticket_ID, Employee_Name, Department,
               Issue_Category, Priority, Status, Created_Date
        FROM Tickets
        WHERE CAST(Ticket_ID AS VARCHAR(20)) LIKE ?
           OR Employee_Name LIKE ?
           OR Department LIKE ?
           OR Issue_Category LIKE ?
           OR Priority LIKE ?
           OR Status LIKE ?
        ORDER BY Ticket_ID DESC
        """

        cursor.execute(query, (
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern
        ))

        records = cursor.fetchall()

        display_records(records)

        if not records:
            messagebox.showinfo(
                "No Results",
                "No matching tickets found."
            )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to search tickets.\n\n{str(e)}"
        )

    finally:

        if conn:
            conn.close()

        search_button.config(state="normal", text="SEARCH")


# =========================
# SHOW ALL TICKETS
# =========================

def show_all_tickets():

    conn = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Ticket_ID, Employee_Name, Department,
                   Issue_Category, Priority, Status, Created_Date
            FROM Tickets
            ORDER BY Ticket_ID DESC
        """)

        records = cursor.fetchall()

        display_records(records)

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to load tickets.\n\n{str(e)}"
        )

    finally:

        if conn:
            conn.close()


def reset_search():

    search_entry.delete(0, tk.END)
    show_all_tickets()
    search_entry.focus()


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Search Tickets | IT Help Desk")
root.geometry("1200x700")
root.minsize(950, 550)
root.configure(bg=BG)


# =========================
# HEADER
# =========================

header = tk.Frame(root, bg=NAVY, height=100)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="IT HELP DESK",
    font=("Segoe UI", 21, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(anchor="w", padx=35, pady=(18, 2))

tk.Label(
    header,
    text="SUPPORT MANAGEMENT SYSTEM",
    font=("Segoe UI", 9, "bold"),
    bg=NAVY,
    fg="#CBD5E1"
).pack(anchor="w", padx=36)


# =========================
# MAIN CONTENT
# =========================

content = tk.Frame(root, bg=BG, padx=30, pady=25)
content.pack(fill="both", expand=True)


# PAGE HEADING

tk.Label(
    content,
    text="Search Support Tickets",
    font=("Segoe UI", 20, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w")

tk.Label(
    content,
    text="Find tickets using employee details, ticket ID, category, priority or status.",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(5, 18))


# =========================
# SEARCH CARD
# =========================

search_frame = tk.Frame(
    content,
    bg=WHITE,
    padx=22,
    pady=20,
    highlightbackground=BORDER,
    highlightthickness=1
)

search_frame.pack(fill="x", pady=(0, 18))

tk.Label(
    search_frame,
    text="SEARCH TICKETS",
    font=("Segoe UI", 11, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", pady=(0, 10))

tk.Label(
    search_frame,
    text="Enter Ticket ID, Employee Name, Department, Category, Priority or Status",
    font=("Segoe UI", 9),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w", pady=(0, 10))


# Search Input and Buttons

search_controls = tk.Frame(search_frame, bg=WHITE)
search_controls.pack(fill="x")

search_entry = tk.Entry(
    search_controls,
    font=("Segoe UI", 11),
    bg="#F8FAFC",
    fg=TEXT,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=BLUE
)

search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=10,
    padx=(0, 12)
)


search_button = tk.Button(
    search_controls,
    text="SEARCH",
    font=("Segoe UI", 10, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground="#1D4ED8",
    activeforeground=WHITE,
    cursor="hand2",
    command=search_tickets,
    relief="flat",
    bd=0,
    padx=22,
    pady=11
)

search_button.pack(side="left", padx=(0, 8))


show_all_button = tk.Button(
    search_controls,
    text="SHOW ALL",
    font=("Segoe UI", 10, "bold"),
    bg=NAVY,
    fg=WHITE,
    activebackground="#263F65",
    activeforeground=WHITE,
    cursor="hand2",
    command=reset_search,
    relief="flat",
    bd=0,
    padx=22,
    pady=11
)

show_all_button.pack(side="left")


# =========================
# RESULTS SECTION
# =========================

results_header = tk.Frame(content, bg=BG)
results_header.pack(fill="x", pady=(0, 12))

tk.Label(
    results_header,
    text="Ticket Records",
    font=("Segoe UI", 13, "bold"),
    bg=BG,
    fg=TEXT
).pack(side="left")

result_count = tk.Label(
    results_header,
    text="Results Found: 0",
    font=("Segoe UI", 10, "bold"),
    bg=BG,
    fg=BLUE
)

result_count.pack(side="right")


# =========================
# TABLE CARD
# =========================

table_card = tk.Frame(
    content,
    bg=WHITE,
    padx=15,
    pady=15,
    highlightbackground=BORDER,
    highlightthickness=1
)

table_card.pack(fill="both", expand=True)


# =========================
# TABLE STYLE
# =========================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT,
    rowheight=38,
    font=("Segoe UI", 9),
    fieldbackground=WHITE,
    borderwidth=0
)

style.configure(
    "Treeview.Heading",
    background=NAVY,
    foreground=WHITE,
    font=("Segoe UI", 9, "bold"),
    padding=12,
    relief="flat"
)

style.map(
    "Treeview",
    background=[("selected", "#DBEAFE")],
    foreground=[("selected", NAVY)]
)


# =========================
# TABLE
# =========================

table_frame = tk.Frame(table_card, bg=WHITE)
table_frame.pack(fill="both", expand=True)

columns = (
    "Ticket_ID",
    "Employee_Name",
    "Department",
    "Issue_Category",
    "Priority",
    "Status",
    "Created_Date"
)

ticket_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

column_settings = {
    "Ticket_ID": ("Ticket ID", 80),
    "Employee_Name": ("Employee Name", 160),
    "Department": ("Department", 120),
    "Issue_Category": ("Issue Category", 140),
    "Priority": ("Priority", 100),
    "Status": ("Status", 120),
    "Created_Date": ("Created Date", 210)
}

for col, (heading, width) in column_settings.items():

    ticket_table.heading(col, text=heading)

    ticket_table.column(
        col,
        width=width,
        minwidth=70,
        anchor="center",
        stretch=True
    )


# Scrollbars

vertical_scroll = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=ticket_table.yview
)

horizontal_scroll = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=ticket_table.xview
)

ticket_table.configure(
    yscrollcommand=vertical_scroll.set,
    xscrollcommand=horizontal_scroll.set
)

ticket_table.grid(row=0, column=0, sticky="nsew")
vertical_scroll.grid(row=0, column=1, sticky="ns")
horizontal_scroll.grid(row=1, column=0, sticky="ew")

table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)


# Alternating Row Colors

ticket_table.tag_configure("evenrow", background="#F8FAFC")
ticket_table.tag_configure("oddrow", background=WHITE)


# =========================
# FOOTER
# =========================

tk.Label(
    content,
    text="IT Help Desk Management System",
    font=("Segoe UI", 9),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(12, 0))


# =========================
# KEYBOARD SHORTCUT
# =========================

search_entry.bind("<Return>", lambda event: search_tickets())


# LOAD ALL TICKETS INITIALLY

show_all_tickets()

search_entry.focus()

root.mainloop()