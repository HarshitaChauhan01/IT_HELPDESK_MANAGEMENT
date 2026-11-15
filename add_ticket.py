import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


# =========================
# COLOR THEME
# =========================

BG = "#F4F6FA"
NAVY = "#172B4D"
BLUE = "#2563EB"
BLUE_HOVER = "#1D4ED8"
WHITE = "#FFFFFF"
TEXT = "#1E293B"
MUTED = "#64748B"
BORDER = "#E2E8F0"


# =========================
# SUBMIT TICKET FUNCTION
# =========================

def submit_ticket():

    name = name_entry.get().strip()
    department = department_box.get()
    category = category_box.get()
    description = description_text.get("1.0", tk.END).strip()
    priority = priority_box.get()

    # Input Validation

    if not name:
        messagebox.showwarning("Validation Error", "Employee name cannot be empty.")
        name_entry.focus()
        return

    if len(name) > 100:
        messagebox.showwarning("Validation Error", "Employee name cannot exceed 100 characters.")
        return

    if not department:
        messagebox.showwarning("Validation Error", "Please select a department.")
        department_box.focus()
        return

    if not category:
        messagebox.showwarning("Validation Error", "Please select an issue category.")
        category_box.focus()
        return

    if not description:
        messagebox.showwarning("Validation Error", "Issue description cannot be empty.")
        description_text.focus()
        return

    if len(description) > 500:
        messagebox.showwarning("Validation Error", "Description cannot exceed 500 characters.")
        return

    if not priority:
        messagebox.showwarning("Validation Error", "Please select ticket priority.")
        priority_box.focus()
        return

    # Database Operation

    conn = None

    try:
        submit_button.config(state="disabled", text="Submitting...")
        root.update_idletasks()

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO Tickets
        (
            Employee_Name,
            Department,
            Issue_Category,
            Description,
            Priority,
            Status,
            Created_Date
        )
        VALUES (?, ?, ?, ?, ?, 'Open', GETDATE())
        """

        cursor.execute(
            query,
            (name, department, category, description, priority)
        )

        conn.commit()

        messagebox.showinfo(
            "Ticket Submitted",
            "Your support ticket has been created successfully!"
        )

        # Clear Form

        name_entry.delete(0, tk.END)
        department_box.set("")
        category_box.set("")
        description_text.delete("1.0", tk.END)
        priority_box.set("")

        name_entry.focus()

    except Exception as e:

        if conn:
            conn.rollback()

        messagebox.showerror(
            "Database Error",
            f"Unable to submit ticket.\n\n{str(e)}"
        )

    finally:

        if conn:
            conn.close()

        submit_button.config(state="normal", text="SUBMIT TICKET")


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("Add New Ticket | IT Help Desk")
root.geometry("720x850")
root.minsize(650, 760)
root.configure(bg=BG)


# =========================
# HEADER
# =========================

header = tk.Frame(root, bg=NAVY, height=110)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="IT HELP DESK",
    font=("Segoe UI", 21, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(anchor="w", padx=35, pady=(20, 2))

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

heading_frame = tk.Frame(root, bg=BG)
heading_frame.pack(fill="x", padx=40, pady=(25, 15))

tk.Label(
    heading_frame,
    text="Create New Ticket",
    font=("Segoe UI", 20, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w")

tk.Label(
    heading_frame,
    text="Enter the employee and issue details to raise a support request.",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(5, 0))


# =========================
# FORM CARD
# =========================

form = tk.Frame(
    root,
    bg=WHITE,
    padx=35,
    pady=25,
    highlightbackground=BORDER,
    highlightthickness=1
)

form.pack(fill="both", expand=True, padx=40, pady=(0, 25))


def create_label(text):

    tk.Label(
        form,
        text=text,
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", pady=(12, 6))


# =========================
# INPUT FIELD STYLING
# =========================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Custom.TCombobox",
    font=("Segoe UI", 10),
    padding=8,
    fieldbackground=WHITE,
    background=WHITE,
    foreground=TEXT,
    bordercolor=BORDER
)

style.map(
    "Custom.TCombobox",
    fieldbackground=[("readonly", WHITE)],
    foreground=[("readonly", TEXT)]
)


# =========================
# EMPLOYEE NAME
# =========================

create_label("Employee Name")

name_entry = tk.Entry(
    form,
    font=("Segoe UI", 11),
    bg="#F8FAFC",
    fg=TEXT,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=BLUE
)

name_entry.pack(fill="x", ipady=9)


# =========================
# DEPARTMENT
# =========================

create_label("Department")

department_box = ttk.Combobox(
    form,
    values=["IT", "HR", "Finance", "Marketing", "Sales"],
    state="readonly",
    style="Custom.TCombobox"
)

department_box.pack(fill="x")


# =========================
# ISSUE CATEGORY
# =========================

create_label("Issue Category")

category_box = ttk.Combobox(
    form,
    values=["Hardware", "Software", "Network", "Password", "Other"],
    state="readonly",
    style="Custom.TCombobox"
)

category_box.pack(fill="x")


# =========================
# ISSUE DESCRIPTION
# =========================

create_label("Issue Description")

description_text = tk.Text(
    form,
    height=5,
    font=("Segoe UI", 10),
    bg="#F8FAFC",
    fg=TEXT,
    relief="flat",
    wrap="word",
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=BLUE,
    padx=10,
    pady=8
)

description_text.pack(fill="x")


# =========================
# PRIORITY
# =========================

create_label("Ticket Priority")

priority_box = ttk.Combobox(
    form,
    values=["Low", "Medium", "High", "Critical"],
    state="readonly",
    style="Custom.TCombobox"
)

priority_box.pack(fill="x")


# =========================
# SUBMIT BUTTON
# =========================

submit_button = tk.Button(
    form,
    text="SUBMIT TICKET",
    font=("Segoe UI", 11, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=BLUE_HOVER,
    activeforeground=WHITE,
    cursor="hand2",
    command=submit_ticket,
    relief="flat",
    bd=0,
    pady=13
)

submit_button.pack(fill="x", pady=(28, 8))


def on_enter(event):
    if submit_button["state"] != "disabled":
        submit_button.config(bg=BLUE_HOVER)


def on_leave(event):
    if submit_button["state"] != "disabled":
        submit_button.config(bg=BLUE)


submit_button.bind("<Enter>", on_enter)
submit_button.bind("<Leave>", on_leave)


# =========================
# FOOTER
# =========================

tk.Label(
    root,
    text="IT Help Desk Management System  |  Support Ticket Portal",
    font=("Segoe UI", 9),
    bg=BG,
    fg=MUTED
).pack(pady=(0, 12))


name_entry.focus()

root.mainloop()