
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
from database import get_connection


# ---------------- COLORS ----------------

BG = "#F4F6FA"
NAVY = "#172B4D"
SIDEBAR = "#1E293B"
SIDEBAR_HOVER = "#334155"
BLUE = "#2563EB"
GREEN = "#16A34A"
RED = "#DC2626"
ORANGE = "#EA8C20"
WHITE = "#FFFFFF"
TEXT = "#1F2937"
MUTED = "#64748B"


# ---------------- OPEN MODULES ----------------

def open_module(filename):

    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        filename
    )

    if not os.path.isfile(file_path):
        messagebox.showerror(
            "File Not Found",
            f"Could not find {filename}."
        )
        return

    try:
        subprocess.Popen([sys.executable, file_path])

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- DASHBOARD STATISTICS ----------------

def load_dashboard_stats():

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*),
                SUM(CASE WHEN Status = 'Open' THEN 1 ELSE 0 END),
                SUM(CASE WHEN Status = 'In Progress' THEN 1 ELSE 0 END),
                SUM(CASE WHEN Status = 'Resolved' THEN 1 ELSE 0 END)
            FROM Tickets
        """)

        result = cursor.fetchone()

        total_label.config(text=result[0] or 0)
        open_label.config(text=result[1] or 0)
        progress_label.config(text=result[2] or 0)
        resolved_label.config(text=result[3] or 0)

        # Load recent tickets
        cursor.execute("""
            SELECT TOP 8
                Ticket_ID,
                Employee_Name,
                Issue_Category,
                Priority,
                Status
            FROM Tickets
            ORDER BY Ticket_ID DESC
        """)

        records = cursor.fetchall()

        for item in recent_table.get_children():
            recent_table.delete(item)

        for record in records:

            status = record[4]

            if status == "Resolved":
                tag = "resolved"

            elif status == "In Progress":
                tag = "progress"

            else:
                tag = "open"

            recent_table.insert(
                "",
                tk.END,
                values=tuple(record),
                tags=(tag,)
            )

        connection_status.config(
            text="● Database Connected",
            fg=GREEN
        )

    except Exception as e:

        connection_status.config(
            text="● Database Connection Failed",
            fg=RED
        )

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        if conn:
            conn.close()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("IT Help Desk Management System")
root.geometry("1250x780")
root.minsize(1050, 680)
root.configure(bg=BG)


# ---------------- HEADER ----------------

header = tk.Frame(
    root,
    bg=WHITE,
    height=75
)

header.pack(fill="x")
header.pack_propagate(False)


tk.Label(
    header,
    text="IT HELP DESK",
    font=("Segoe UI", 20, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(side="left", padx=28)


tk.Label(
    header,
    text="MANAGEMENT SYSTEM",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(side="left", pady=5)


right_header = tk.Frame(header, bg=WHITE)
right_header.pack(side="right", padx=30)


tk.Label(
    right_header,
    text="ADMINISTRATOR",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="e")


connection_status = tk.Label(
    right_header,
    text="● Connecting...",
    font=("Segoe UI", 9),
    bg=WHITE,
    fg=ORANGE
)

connection_status.pack(anchor="e", pady=3)


# ---------------- MAIN LAYOUT ----------------

main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True)


# ---------------- SIDEBAR ----------------

sidebar = tk.Frame(
    main_frame,
    bg=SIDEBAR,
    width=235
)

sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)


tk.Label(
    sidebar,
    text="WORKSPACE",
    font=("Segoe UI", 10, "bold"),
    bg=SIDEBAR,
    fg="#94A3B8"
).pack(anchor="w", padx=25, pady=(30, 15))


def create_sidebar_button(text, command):

    button = tk.Button(
        sidebar,
        text=text,
        font=("Segoe UI", 10),
        bg=SIDEBAR,
        fg="#E2E8F0",
        activebackground=SIDEBAR_HOVER,
        activeforeground=WHITE,
        relief="flat",
        anchor="w",
        cursor="hand2",
        command=command,
        padx=25,
        pady=12,
        bd=0
    )

    button.pack(fill="x", padx=10, pady=2)

    button.bind(
        "<Enter>",
        lambda event: button.config(bg=SIDEBAR_HOVER)
    )

    button.bind(
        "<Leave>",
        lambda event: button.config(bg=SIDEBAR)
    )


# Navigation

create_sidebar_button(
    "▦   Dashboard",
    load_dashboard_stats
)

tk.Label(
    sidebar,
    text="TICKET MANAGEMENT",
    font=("Segoe UI", 9, "bold"),
    bg=SIDEBAR,
    fg="#94A3B8"
).pack(anchor="w", padx=25, pady=(25, 10))


create_sidebar_button(
    "＋   Add New Ticket",
    lambda: open_module("add_ticket.py")
)

create_sidebar_button(
    "▤   View All Tickets",
    lambda: open_module("view_ticket.py")
)

create_sidebar_button(
    "⌕   Search Tickets",
    lambda: open_module("search_tickets.py")
)

create_sidebar_button(
    "↻   Update Ticket Status",
    lambda: open_module("update_ticket.py")
)

create_sidebar_button(
    "✕   Delete Ticket",
    lambda: open_module("delete_ticket.py")
)

create_sidebar_button(
    "▣   Ticket Details",
    lambda: open_module("ticket_details.py")
)


tk.Label(
    sidebar,
    text="REPORTING",
    font=("Segoe UI", 9, "bold"),
    bg=SIDEBAR,
    fg="#94A3B8"
).pack(anchor="w", padx=25, pady=(25, 10))


create_sidebar_button(
    "▥   Reports & Analytics",
    lambda: open_module("reports_analytics.py")
)

create_sidebar_button(
    "⇩   Export to Excel",
    lambda: open_module("export_reports.py")
)


# Sidebar Footer

tk.Label(
    sidebar,
    text="IT HELPDESK SYSTEM\nPython | Tkinter | SQL Server",
    font=("Segoe UI", 8),
    bg=SIDEBAR,
    fg="#94A3B8",
    justify="left"
).pack(side="bottom", anchor="w", padx=22, pady=22)


# ---------------- DASHBOARD CONTENT ----------------

content = tk.Frame(
    main_frame,
    bg=BG,
    padx=30,
    pady=25
)

content.pack(side="left", fill="both", expand=True)


# Dashboard Heading

heading_frame = tk.Frame(content, bg=BG)
heading_frame.pack(fill="x")


tk.Label(
    heading_frame,
    text="Dashboard Overview",
    font=("Segoe UI", 23, "bold"),
    bg=BG,
    fg=NAVY
).pack(anchor="w")


tk.Label(
    heading_frame,
    text="Monitor, track and manage your IT support requests.",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(5, 20))


# ---------------- STATISTICS CARDS ----------------

stats_frame = tk.Frame(content, bg=BG)
stats_frame.pack(fill="x", pady=10)


def create_stat_card(parent, title, color, description):

    card = tk.Frame(
        parent,
        bg=WHITE,
        padx=18,
        pady=17,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )

    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w")

    value = tk.Label(
        card,
        text="0",
        font=("Segoe UI", 29, "bold"),
        bg=WHITE,
        fg=color
    )

    value.pack(anchor="w", pady=(8, 2))

    tk.Label(
        card,
        text=description,
        font=("Segoe UI", 9),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w")

    return card, value


total_card, total_label = create_stat_card(
    stats_frame,
    "TOTAL TICKETS",
    NAVY,
    "All registered requests"
)

open_card, open_label = create_stat_card(
    stats_frame,
    "OPEN TICKETS",
    RED,
    "Awaiting attention"
)

progress_card, progress_label = create_stat_card(
    stats_frame,
    "IN PROGRESS",
    ORANGE,
    "Currently being handled"
)

resolved_card, resolved_label = create_stat_card(
    stats_frame,
    "RESOLVED",
    GREEN,
    "Successfully completed"
)


for card in [
    total_card,
    open_card,
    progress_card,
    resolved_card
]:

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=6
    )


# ---------------- RECENT TICKETS ----------------

recent_heading = tk.Frame(content, bg=BG)
recent_heading.pack(fill="x", pady=(35, 15))


tk.Label(
    recent_heading,
    text="Recent Tickets",
    font=("Segoe UI", 16, "bold"),
    bg=BG,
    fg=NAVY
).pack(side="left")


tk.Button(
    recent_heading,
    text="VIEW ALL",
    font=("Segoe UI", 9, "bold"),
    bg=BG,
    fg=BLUE,
    relief="flat",
    cursor="hand2",
    command=lambda: open_module("view_ticket.py")
).pack(side="right")


# Table Style

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT,
    rowheight=36,
    fieldbackground=WHITE,
    font=("Segoe UI", 9)
)

style.configure(
    "Treeview.Heading",
    background="#E9EEF5",
    foreground=NAVY,
    font=("Segoe UI", 9, "bold"),
    relief="flat",
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", "#DBEAFE")],
    foreground=[("selected", NAVY)]
)


table_frame = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground="#E2E8F0",
    highlightthickness=1
)

table_frame.pack(fill="both", expand=True)


columns = (
    "Ticket ID",
    "Employee Name",
    "Issue Category",
    "Priority",
    "Status"
)


recent_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=8
)


for col in columns:

    recent_table.heading(col, text=col)

    recent_table.column(
        col,
        width=130,
        anchor="center"
    )


recent_table.column("Employee Name", width=190)
recent_table.column("Issue Category", width=160)


recent_table.tag_configure(
    "resolved",
    foreground=GREEN
)

recent_table.tag_configure(
    "progress",
    foreground=ORANGE
)

recent_table.tag_configure(
    "open",
    foreground=RED
)


scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=recent_table.yview
)

recent_table.configure(
    yscrollcommand=scrollbar.set
)

recent_table.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(side="right", fill="y")


# ---------------- QUICK ACTIONS ----------------

actions_heading = tk.Label(
    content,
    text="Quick Actions",
    font=("Segoe UI", 16, "bold"),
    bg=BG,
    fg=NAVY
)

actions_heading.pack(anchor="w", pady=(25, 12))


actions_frame = tk.Frame(content, bg=BG)
actions_frame.pack(fill="x")


def create_action_button(parent, text, color, command):

    button = tk.Button(
        parent,
        text=text,
        font=("Segoe UI", 9, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=NAVY,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        command=command,
        padx=12,
        pady=13
    )

    button.pack(
        side="left",
        fill="x",
        expand=True,
        padx=5
    )

    return button


create_action_button(
    actions_frame,
    "+ CREATE TICKET",
    BLUE,
    lambda: open_module("add_ticket.py")
)

create_action_button(
    actions_frame,
    "VIEW TICKETS",
    NAVY,
    lambda: open_module("view_ticket.py")
)

create_action_button(
    actions_frame,
    "VIEW REPORTS",
    GREEN,
    lambda: open_module("reports_analytics.py")
)


# ---------------- REFRESH BUTTON ----------------

refresh_frame = tk.Frame(content, bg=BG)
refresh_frame.pack(fill="x", pady=18)


tk.Button(
    refresh_frame,
    text="↻  REFRESH DASHBOARD",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=NAVY,
    activebackground="#E2E8F0",
    relief="flat",
    cursor="hand2",
    command=load_dashboard_stats,
    padx=18,
    pady=10
).pack(side="right")


# ---------------- FOOTER ----------------

footer = tk.Label(
    root,
    text="IT Help Desk Management System  |  Built with Python, Tkinter & SQL Server",
    font=("Segoe UI", 9),
    bg="#E9EEF5",
    fg=MUTED,
    pady=10
)

footer.pack(fill="x")


# ---------------- INITIAL LOAD ----------------

load_dashboard_stats()

root.mainloop()
