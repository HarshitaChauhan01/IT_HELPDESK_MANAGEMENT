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

    for item in ticket_table.get_children():
        ticket_table.delete(item)

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
                values=tuple(values),
                tags=("evenrow" if index % 2 == 0 else "oddrow",)
            )

        total_count.config(text=f"Total Tickets: {len(records)}")

        clear_details()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to load tickets.\n\n{str(e)}"
        )

    finally:

        if conn:
            conn.close()


# =========================
# CLEAR DETAILS
# =========================

def clear_details():

    details_text.config(state="normal")
    details_text.delete("1.0", tk.END)

    details_text.insert(
        tk.END,
        "Select a ticket from the table to view its complete information."
    )

    details_text.config(state="disabled")

    selected_label.config(text="No ticket selected")


# =========================
# SHOW TICKET DETAILS
# =========================

def show_ticket_details(event):

    selected = ticket_table.selection()

    if not selected:
        return

    ticket_id = ticket_table.item(
        selected[0], "values"
    )[0]

    conn = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Ticket_ID, Employee_Name, Department,
                   Issue_Category, Description, Priority,
                   Status, Created_Date, Resolution_Date
            FROM Tickets
            WHERE Ticket_ID = ?
        """, (ticket_id,))

        ticket = cursor.fetchone()

        if not ticket:
            messagebox.showwarning(
                "Not Found",
                "Ticket information could not be found."
            )
            return

        fields = [
            "Ticket ID",
            "Employee Name",
            "Department",
            "Issue Category",
            "Description",
            "Priority",
            "Status",
            "Created Date",
            "Resolution Date"
        ]

        details_text.config(state="normal")
        details_text.delete("1.0", tk.END)

        for field, value in zip(fields, ticket):

            if value is None:
                display_value = "Not Available"

            elif field in ("Created Date", "Resolution Date"):
                display_value = value.strftime("%d %B %Y, %I:%M %p")

            else:
                display_value = str(value)

            details_text.insert(
                tk.END,
                f"{field}\n",
                "field"
            )

            details_text.insert(
                tk.END,
                f"{display_value}\n\n",
                "value"
            )

        details_text.config(state="disabled")

        selected_label.config(
            text=f"Viewing Ticket #{ticket_id}"
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to retrieve ticket details.\n\n{str(e)}"
        )

    finally:

        if conn:
            conn.close()


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("Ticket Details | IT Help Desk")
root.geometry("1250x800")
root.minsize(1000, 650)
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

content = tk.Frame(
    root,
    bg=BG,
    padx=30,
    pady=25
)

content.pack(fill="both", expand=True)


# PAGE HEADING

tk.Label(
    content,
    text="Ticket Details",
    font=("Segoe UI", 21, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w")

tk.Label(
    content,
    text="View and inspect complete information about support tickets.",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(5, 18))


# =========================
# SUMMARY CARD
# =========================

summary_card = tk.Frame(
    content,
    bg=WHITE,
    padx=20,
    pady=14,
    highlightbackground=BORDER,
    highlightthickness=1
)

summary_card.pack(fill="x", pady=(0, 15))

total_count = tk.Label(
    summary_card,
    text="Total Tickets: 0",
    font=("Segoe UI", 15, "bold"),
    bg=WHITE,
    fg=NAVY
)

total_count.pack(anchor="w")


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
    text="All Support Tickets",
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
    rowheight=35,
    font=("Segoe UI", 9),
    fieldbackground=WHITE,
    borderwidth=0
)

style.configure(
    "Treeview.Heading",
    background=NAVY,
    foreground=WHITE,
    font=("Segoe UI", 9, "bold"),
    padding=10,
    relief="flat"
)

style.map(
    "Treeview",
    background=[("selected", "#DBEAFE")],
    foreground=[("selected", NAVY)]
)


# =========================
# TICKET TABLE
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
    "Ticket_ID": ("Ticket ID", 85),
    "Employee_Name": ("Employee Name", 155),
    "Department": ("Department", 115),
    "Issue_Category": ("Issue Category", 135),
    "Priority": ("Priority", 95),
    "Status": ("Status", 110),
    "Created_Date": ("Created Date", 175)
}

for col, (heading, width) in column_settings.items():

    ticket_table.heading(col, text=heading)

    ticket_table.column(
        col,
        width=width,
        minwidth=75,
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

ticket_table.tag_configure(
    "evenrow",
    background="#F8FAFC"
)

ticket_table.tag_configure(
    "oddrow",
    background=WHITE
)

ticket_table.bind(
    "<<TreeviewSelect>>",
    show_ticket_details
)


# =========================
# DETAILS CARD
# =========================

details_card = tk.Frame(
    content,
    bg=WHITE,
    padx=20,
    pady=18,
    highlightbackground=BORDER,
    highlightthickness=1
)

details_card.pack(fill="both", expand=True, pady=(15, 0))


# Details Header

details_header = tk.Frame(details_card, bg=WHITE)
details_header.pack(fill="x", pady=(0, 12))

tk.Label(
    details_header,
    text="Complete Ticket Information",
    font=("Segoe UI", 14, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(side="left")

selected_label = tk.Label(
    details_header,
    text="No ticket selected",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=BLUE
)

selected_label.pack(side="right")


# Details Text Area

details_container = tk.Frame(details_card, bg=WHITE)
details_container.pack(fill="both", expand=True)

details_text = tk.Text(
    details_container,
    font=("Segoe UI", 10),
    bg="#F8FAFC",
    fg=TEXT,
    padx=18,
    pady=15,
    relief="flat",
    wrap="word",
    state="disabled",
    height=9
)

details_scroll = ttk.Scrollbar(
    details_container,
    orient="vertical",
    command=details_text.yview
)

details_text.configure(
    yscrollcommand=details_scroll.set
)

details_text.pack(side="left", fill="both", expand=True)
details_scroll.pack(side="right", fill="y")

details_text.tag_configure(
    "field",
    font=("Segoe UI", 9, "bold"),
    foreground=NAVY
)

details_text.tag_configure(
    "value",
    font=("Segoe UI", 10),
    foreground=TEXT
)


# =========================
# FOOTER
# =========================

footer = tk.Frame(content, bg=BG)
footer.pack(fill="x", pady=(12, 0))

tk.Label(
    footer,
    text="Select any row to view its complete details.",
    font=("Segoe UI", 9),
    bg=BG,
    fg=MUTED
).pack(side="left")


refresh_button = tk.Button(
    footer,
    text="REFRESH TICKETS",
    font=("Segoe UI", 9, "bold"),
    bg=NAVY,
    fg=WHITE,
    activebackground="#263F65",
    activeforeground=WHITE,
    cursor="hand2",
    command=load_tickets,
    relief="flat",
    bd=0,
    padx=20,
    pady=10
)

refresh_button.pack(side="right")


# =========================
# INITIALIZE
# =========================

clear_details()
load_tickets()

root.mainloop()