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
# LOAD TICKETS
# =========================

def load_tickets():

    for row in ticket_table.get_children():
        ticket_table.delete(row)

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

        total_count.config(text=f"Total Tickets: {len(records)}")

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to load tickets.\n\n{str(e)}"
        )

    finally:
        if conn:
            conn.close()


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("View All Tickets | IT Help Desk")
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
# PAGE HEADING
# =========================

content = tk.Frame(root, bg=BG, padx=30, pady=25)
content.pack(fill="both", expand=True)

heading_frame = tk.Frame(content, bg=BG)
heading_frame.pack(fill="x", pady=(0, 20))

title_frame = tk.Frame(heading_frame, bg=BG)
title_frame.pack(side="left")

tk.Label(
    title_frame,
    text="All Support Tickets",
    font=("Segoe UI", 20, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w")

tk.Label(
    title_frame,
    text="View and monitor all support requests submitted by employees.",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(5, 0))


# =========================
# SUMMARY CARD
# =========================

summary_card = tk.Frame(
    content,
    bg=WHITE,
    padx=20,
    pady=15,
    highlightbackground=BORDER,
    highlightthickness=1
)

summary_card.pack(fill="x", pady=(0, 18))

tk.Label(
    summary_card,
    text="TICKET OVERVIEW",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w")

total_count = tk.Label(
    summary_card,
    text="Total Tickets: 0",
    font=("Segoe UI", 16, "bold"),
    bg=WHITE,
    fg=NAVY
)

total_count.pack(anchor="w", pady=(5, 0))


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

tk.Label(
    table_card,
    text="Ticket Records",
    font=("Segoe UI", 13, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", pady=(0, 12))


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

style.map(
    "Treeview.Heading",
    background=[("active", "#263F65")]
)


# =========================
# TABLE FRAME
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


# Column Configuration

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

ticket_table.tag_configure(
    "evenrow",
    background="#F8FAFC"
)

ticket_table.tag_configure(
    "oddrow",
    background=WHITE
)


# =========================
# BOTTOM ACTION BAR
# =========================

bottom_frame = tk.Frame(content, bg=BG)
bottom_frame.pack(fill="x", pady=(18, 0))

tk.Label(
    bottom_frame,
    text="IT Help Desk Management System",
    font=("Segoe UI", 9),
    bg=BG,
    fg=MUTED
).pack(side="left")


refresh_button = tk.Button(
    bottom_frame,
    text="↻  REFRESH TICKETS",
    font=("Segoe UI", 10, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground="#1D4ED8",
    activeforeground=WHITE,
    cursor="hand2",
    command=load_tickets,
    relief="flat",
    bd=0,
    padx=22,
    pady=11
)

refresh_button.pack(side="right")


def on_enter(event):
    refresh_button.config(bg="#1D4ED8")


def on_leave(event):
    refresh_button.config(bg=BLUE)


refresh_button.bind("<Enter>", on_enter)
refresh_button.bind("<Leave>", on_leave)


# =========================
# LOAD RECORDS
# =========================

load_tickets()

root.mainloop()