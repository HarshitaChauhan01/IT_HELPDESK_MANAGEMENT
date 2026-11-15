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

RED = "#DC2626"
ORANGE = "#F59E0B"
GREEN = "#16A34A"


# =========================
# DATABASE REPORTS
# =========================

def get_report_data():

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Ticket summary

        cursor.execute("""
            SELECT
                COUNT(*),
                SUM(CASE WHEN Status = 'Open' THEN 1 ELSE 0 END),
                SUM(CASE WHEN Status = 'In Progress' THEN 1 ELSE 0 END),
                SUM(CASE WHEN Status = 'Resolved' THEN 1 ELSE 0 END)
            FROM Tickets
        """)

        summary = cursor.fetchone()

        # Department-wise tickets

        cursor.execute("""
            SELECT Department, COUNT(*)
            FROM Tickets
            GROUP BY Department
            ORDER BY COUNT(*) DESC
        """)

        departments = cursor.fetchall()

        # Priority-wise tickets

        cursor.execute("""
            SELECT Priority, COUNT(*)
            FROM Tickets
            GROUP BY Priority
            ORDER BY COUNT(*) DESC
        """)

        priorities = cursor.fetchall()

        # Category-wise tickets

        cursor.execute("""
            SELECT Issue_Category, COUNT(*)
            FROM Tickets
            GROUP BY Issue_Category
            ORDER BY COUNT(*) DESC
        """)

        categories = cursor.fetchall()

        # Average resolution time

        cursor.execute("""
            SELECT AVG(
                CAST(
                    DATEDIFF(MINUTE, Created_Date, Resolution_Date)
                    AS FLOAT
                )
            ) / 60.0
            FROM Tickets
            WHERE Resolution_Date IS NOT NULL
        """)

        avg_resolution = cursor.fetchone()[0]

        return summary, departments, priorities, categories, avg_resolution

    finally:

        if conn:
            conn.close()


# =========================
# DRAW BAR CHART
# =========================

def draw_bar_chart(canvas, title, records, bar_color):

    canvas.delete("all")

    canvas.update_idletasks()

    width = max(canvas.winfo_width(), 350)
    height = max(canvas.winfo_height(), 200)

    # Chart title

    canvas.create_text(
        20,
        22,
        text=title,
        anchor="w",
        font=("Segoe UI", 12, "bold"),
        fill=NAVY
    )

    canvas.create_line(
        20, 48,
        width - 20, 48,
        fill=BORDER
    )

    if not records:

        canvas.create_text(
            width // 2,
            height // 2,
            text="No data available",
            font=("Segoe UI", 10),
            fill=MUTED
        )

        return

    max_value = max(int(row[1] or 0) for row in records) or 1

    start_y = 70
    bar_height = 20
    gap = 16

    label_width = min(130, width * 0.30)
    bar_start = label_width + 15
    max_bar_width = width - bar_start - 65

    for index, row in enumerate(records):

        label = str(row[0] if row[0] is not None else "Not Assigned")
        value = int(row[1] or 0)

        y = start_y + index * (bar_height + gap)

        # Category label

        canvas.create_text(
            20,
            y + bar_height / 2,
            text=label,
            anchor="w",
            font=("Segoe UI", 9),
            fill=TEXT,
            width=label_width
        )

        # Background bar

        canvas.create_rectangle(
            bar_start,
            y,
            bar_start + max_bar_width,
            y + bar_height,
            fill="#E9EEF5",
            outline=""
        )

        # Actual bar

        bar_width = (value / max_value) * max_bar_width

        canvas.create_rectangle(
            bar_start,
            y,
            bar_start + bar_width,
            y + bar_height,
            fill=bar_color,
            outline=""
        )

        # Value

        canvas.create_text(
            bar_start + max_bar_width + 12,
            y + bar_height / 2,
            text=str(value),
            anchor="w",
            font=("Segoe UI", 9, "bold"),
            fill=TEXT
        )


# =========================
# CREATE SUMMARY CARD
# =========================

def create_card(parent, title, color):

    card = tk.Frame(
        parent,
        bg=WHITE,
        padx=16,
        pady=16,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 9, "bold"),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w")

    value_label = tk.Label(
        card,
        text="0",
        font=("Segoe UI", 25, "bold"),
        bg=WHITE,
        fg=color
    )

    value_label.pack(anchor="w", pady=(8, 0))

    return card, value_label


# =========================
# REFRESH REPORTS
# =========================

def refresh_reports():

    try:

        refresh_button.config(
            state="disabled",
            text="LOADING..."
        )

        root.update_idletasks()

        summary, departments, priorities, categories, avg_resolution = get_report_data()

        total = summary[0] or 0
        open_count = summary[1] or 0
        progress_count = summary[2] or 0
        resolved_count = summary[3] or 0

        # Update KPI cards

        total_label.config(text=str(total))
        open_label.config(text=str(open_count))
        progress_label.config(text=str(progress_count))
        resolved_label.config(text=str(resolved_count))

        if avg_resolution is None:
            resolution_label.config(text="N/A")
        else:
            resolution_label.config(
                text=f"{avg_resolution:.1f} hrs"
            )

        # Update charts

        draw_bar_chart(
            department_chart,
            "Department-wise Tickets",
            departments,
            BLUE
        )

        draw_bar_chart(
            priority_chart,
            "Priority-wise Tickets",
            priorities,
            ORANGE
        )

        draw_bar_chart(
            category_chart,
            "Issue Category Distribution",
            categories,
            GREEN
        )

        last_updated_label.config(
            text="Report data refreshed successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "Report Error",
            f"Unable to generate reports.\n\n{str(e)}"
        )

        last_updated_label.config(
            text="Unable to refresh report data."
        )

    finally:

        refresh_button.config(
            state="normal",
            text="REFRESH ANALYTICS"
        )


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("Reports & Analytics | IT Help Desk")
root.geometry("1250x850")
root.minsize(1000, 700)
root.configure(bg=BG)


# =========================
# HEADER
# =========================

header = tk.Frame(
    root,
    bg=NAVY,
    height=100
)

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
    text="Reports & Analytics",
    font=("Segoe UI", 21, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w")

tk.Label(
    content,
    text="Monitor support performance, ticket distribution and resolution time.",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(5, 18))


# =========================
# SUMMARY SECTION
# =========================

tk.Label(
    content,
    text="Performance Overview",
    font=("Segoe UI", 13, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", pady=(0, 10))


cards_frame = tk.Frame(content, bg=BG)
cards_frame.pack(fill="x")


total_card, total_label = create_card(
    cards_frame,
    "TOTAL TICKETS",
    NAVY
)

open_card, open_label = create_card(
    cards_frame,
    "OPEN TICKETS",
    RED
)

progress_card, progress_label = create_card(
    cards_frame,
    "IN PROGRESS",
    ORANGE
)

resolved_card, resolved_label = create_card(
    cards_frame,
    "RESOLVED",
    GREEN
)

resolution_card, resolution_label = create_card(
    cards_frame,
    "AVG. RESOLUTION TIME",
    BLUE
)


cards = [
    total_card,
    open_card,
    progress_card,
    resolved_card,
    resolution_card
]

for index, card in enumerate(cards):

    card.grid(
        row=0,
        column=index,
        sticky="nsew",
        padx=5
    )

    cards_frame.grid_columnconfigure(
        index,
        weight=1
    )


# =========================
# CHARTS SECTION
# =========================

charts_heading = tk.Label(
    content,
    text="Ticket Distribution Analysis",
    font=("Segoe UI", 13, "bold"),
    bg=BG,
    fg=TEXT
)

charts_heading.pack(anchor="w", pady=(25, 10))


charts_frame = tk.Frame(content, bg=BG)
charts_frame.pack(fill="both", expand=True)


def create_chart_card(parent):

    card = tk.Frame(
        parent,
        bg=WHITE,
        padx=12,
        pady=12,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    chart = tk.Canvas(
        card,
        bg=WHITE,
        highlightthickness=0,
        height=200
    )

    chart.pack(fill="both", expand=True)

    return card, chart


# Department chart

department_card, department_chart = create_chart_card(
    charts_frame
)

department_card.grid(
    row=0,
    column=0,
    padx=6,
    pady=6,
    sticky="nsew"
)


# Priority chart

priority_card, priority_chart = create_chart_card(
    charts_frame
)

priority_card.grid(
    row=0,
    column=1,
    padx=6,
    pady=6,
    sticky="nsew"
)


# Category chart

category_card, category_chart = create_chart_card(
    charts_frame
)

category_card.grid(
    row=1,
    column=0,
    columnspan=2,
    padx=6,
    pady=6,
    sticky="nsew"
)


charts_frame.grid_columnconfigure(0, weight=1)
charts_frame.grid_columnconfigure(1, weight=1)

charts_frame.grid_rowconfigure(0, weight=1)
charts_frame.grid_rowconfigure(1, weight=1)


# =========================
# FOOTER AND REFRESH
# =========================

footer = tk.Frame(content, bg=BG)
footer.pack(fill="x", pady=(12, 0))


last_updated_label = tk.Label(
    footer,
    text="Loading report data...",
    font=("Segoe UI", 9),
    bg=BG,
    fg=MUTED
)

last_updated_label.pack(side="left")


refresh_button = tk.Button(
    footer,
    text="REFRESH ANALYTICS",
    font=("Segoe UI", 9, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground="#1D4ED8",
    activeforeground=WHITE,
    cursor="hand2",
    command=refresh_reports,
    relief="flat",
    bd=0,
    padx=22,
    pady=11
)

refresh_button.pack(side="right")


# =========================
# INITIALIZE
# =========================

refresh_reports()

root.mainloop()