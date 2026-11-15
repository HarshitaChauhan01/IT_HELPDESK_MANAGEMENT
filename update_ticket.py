import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


VALID_STATUSES = ["Open", "In Progress", "Resolved"]


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
                   Issue_Category, Priority, Status
            FROM Tickets
            ORDER BY Ticket_ID DESC
        """)

        records = cursor.fetchall()

        for index, row in enumerate(records):

            ticket_table.insert(
                "",
                tk.END,
                values=tuple(row),
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
# SELECT TICKET
# =========================

def select_ticket(event):

    selected_item = ticket_table.selection()

    if not selected_item:
        return

    ticket = ticket_table.item(selected_item[0], "values")

    ticket_id_entry.delete(0, tk.END)
    ticket_id_entry.insert(0, ticket[0])

    status_box.set(ticket[5])


# =========================
# UPDATE STATUS
# =========================

def update_status():

    ticket_id = ticket_id_entry.get().strip()
    new_status = status_box.get()

    if not ticket_id:
        messagebox.showwarning(
            "Validation Error",
            "Please select a ticket or enter a Ticket ID."
        )
        ticket_id_entry.focus()
        return

    if not ticket_id.isdigit() or int(ticket_id) <= 0:
        messagebox.showwarning(
            "Validation Error",
            "Ticket ID must be a positive number."
        )
        ticket_id_entry.focus()
        return

    if new_status not in VALID_STATUSES:
        messagebox.showwarning(
            "Validation Error",
            "Please select a valid ticket status."
        )
        status_box.focus()
        return

    conn = None

    try:
        update_button.config(state="disabled", text="Updating...")
        root.update_idletasks()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT Status FROM Tickets WHERE Ticket_ID = ?",
            (int(ticket_id),)
        )

        existing_ticket = cursor.fetchone()

        if not existing_ticket:
            messagebox.showwarning(
                "Not Found",
                "No ticket found with this Ticket ID."
            )
            return

        current_status = existing_ticket[0]

        if current_status == new_status:
            messagebox.showinfo(
                "No Changes",
                "The ticket already has this status."
            )
            return

        if new_status == "Resolved":

            query = """
                UPDATE Tickets
                SET Status = ?,
                    Resolution_Date = GETDATE()
                WHERE Ticket_ID = ?
            """

        else:

            query = """
                UPDATE Tickets
                SET Status = ?,
                    Resolution_Date = NULL
                WHERE Ticket_ID = ?
            """

        cursor.execute(query, (new_status, int(ticket_id)))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Ticket status updated successfully!"
        )

        ticket_id_entry.delete(0, tk.END)
        status_box.set("")

        load_tickets()

    except Exception as e:

        if conn:
            conn.rollback()

        messagebox.showerror(
            "Database Error",
            f"Unable to update ticket.\n\n{str(e)}"
        )

    finally:

        if conn:
            conn.close()

        update_button.config(state="normal", text="UPDATE STATUS")


# =========================
# RESET SELECTION
# =========================

def clear_selection():

    ticket_table.selection_remove(ticket_table.selection())
    ticket_id_entry.delete(0, tk.END)
    status_box.set("")


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Update Ticket Status | IT Help Desk")
root.geometry("1200x750")
root.minsize(950, 600)
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
    text="Manage Ticket Progress",
    font=("Segoe UI", 20, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w")

tk.Label(
    content,
    text="Select a ticket and update its current status.",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(5, 15))


# =========================
# TICKET SUMMARY
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
# TICKET TABLE CARD
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
    text="Select a Ticket",
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
    rowheight=36,
    font=("Segoe UI", 9),
    fieldbackground=WHITE,
    borderwidth=0
)

style.configure(
    "Treeview.Heading",
    background=NAVY,
    foreground=WHITE,
    font=("Segoe UI", 9, "bold"),
    padding=11,
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
    "Status"
)

ticket_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

column_settings = {
    "Ticket_ID": ("Ticket ID", 90),
    "Employee_Name": ("Employee Name", 180),
    "Department": ("Department", 140),
    "Issue_Category": ("Issue Category", 160),
    "Priority": ("Priority", 120),
    "Status": ("Current Status", 150)
}

for col, (heading, width) in column_settings.items():

    ticket_table.heading(col, text=heading)

    ticket_table.column(
        col,
        width=width,
        minwidth=80,
        anchor="center",
        stretch=True
    )


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

ticket_table.tag_configure("evenrow", background="#F8FAFC")
ticket_table.tag_configure("oddrow", background=WHITE)

ticket_table.bind("<<TreeviewSelect>>", select_ticket)


# =========================
# UPDATE FORM CARD
# =========================

update_frame = tk.Frame(
    content,
    bg=WHITE,
    padx=22,
    pady=20,
    highlightbackground=BORDER,
    highlightthickness=1
)

update_frame.pack(fill="x", pady=(15, 0))

tk.Label(
    update_frame,
    text="Update Ticket Status",
    font=("Segoe UI", 13, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", pady=(0, 15))


# FORM FIELDS

form_fields = tk.Frame(update_frame, bg=WHITE)
form_fields.pack(fill="x")


# Ticket ID

id_frame = tk.Frame(form_fields, bg=WHITE)
id_frame.pack(side="left", padx=(0, 25))

tk.Label(
    id_frame,
    text="Ticket ID",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w", pady=(0, 7))

ticket_id_entry = tk.Entry(
    id_frame,
    font=("Segoe UI", 10),
    width=18,
    bg="#F8FAFC",
    fg=TEXT,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=BLUE
)

ticket_id_entry.pack(ipady=8)


# Status

status_frame = tk.Frame(form_fields, bg=WHITE)
status_frame.pack(side="left", padx=(0, 25))

tk.Label(
    status_frame,
    text="New Status",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w", pady=(0, 7))

status_box = ttk.Combobox(
    status_frame,
    values=VALID_STATUSES,
    state="readonly",
    width=20,
    font=("Segoe UI", 10)
)

status_box.pack(ipady=6)


# Update Button

update_button = tk.Button(
    form_fields,
    text="UPDATE STATUS",
    font=("Segoe UI", 10, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground="#1D4ED8",
    activeforeground=WHITE,
    cursor="hand2",
    command=update_status,
    relief="flat",
    bd=0,
    padx=22,
    pady=11
)

update_button.pack(side="left", padx=(0, 10), pady=(22, 0))


# Clear Button

clear_button = tk.Button(
    form_fields,
    text="CLEAR",
    font=("Segoe UI", 10, "bold"),
    bg="#E2E8F0",
    fg=NAVY,
    activebackground="#CBD5E1",
    cursor="hand2",
    command=clear_selection,
    relief="flat",
    bd=0,
    padx=22,
    pady=11
)

clear_button.pack(side="left", pady=(22, 0))


# =========================
# REFRESH BUTTON
# =========================

bottom_frame = tk.Frame(content, bg=BG)
bottom_frame.pack(fill="x", pady=(12, 0))

tk.Label(
    bottom_frame,
    text="Select a row to automatically fill its Ticket ID and current status.",
    font=("Segoe UI", 9),
    bg=BG,
    fg=MUTED
).pack(side="left")


refresh_button = tk.Button(
    bottom_frame,
    text="REFRESH TICKETS",
    font=("Segoe UI", 9, "bold"),
    bg=NAVY,
    fg=WHITE,
    activebackground="#263F65",
    cursor="hand2",
    command=load_tickets,
    relief="flat",
    bd=0,
    padx=18,
    pady=9
)

refresh_button.pack(side="right")


# =========================
# LOAD RECORDS
# =========================

load_tickets()

root.mainloop()