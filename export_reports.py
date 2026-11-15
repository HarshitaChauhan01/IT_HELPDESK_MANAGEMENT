import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

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
# FETCH TICKET RECORDS
# =========================

def fetch_tickets():

    conn = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                Ticket_ID,
                Employee_Name,
                Department,
                Issue_Category,
                Description,
                Priority,
                Status,
                Created_Date,
                Resolution_Date
            FROM Tickets
            ORDER BY Ticket_ID DESC
        """)

        records = cursor.fetchall()

        return records

    finally:

        if conn:
            conn.close()


# =========================
# CREATE EXCEL REPORT
# =========================

def create_excel_report(records):

    workbook = Workbook()

    sheet = workbook.active
    sheet.title = "Help Desk Tickets"

    # Workbook properties

    workbook.properties.title = "IT Help Desk Ticket Report"
    workbook.properties.subject = "Support Ticket Records"
    workbook.properties.creator = "IT Help Desk Management System"

    # =========================
    # REPORT TITLE
    # =========================

    sheet.merge_cells("A1:I1")

    title_cell = sheet["A1"]

    title_cell.value = "IT HELP DESK - TICKET REPORT"

    title_cell.font = Font(
        name="Arial",
        size=16,
        bold=True,
        color="FFFFFF"
    )

    title_cell.fill = PatternFill(
        start_color="172B4D",
        end_color="172B4D",
        fill_type="solid"
    )

    title_cell.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    sheet.row_dimensions[1].height = 38

    # =========================
    # REPORT INFORMATION
    # =========================

    sheet["A2"] = "Generated On:"
    sheet["B2"] = datetime.now().strftime("%d-%m-%Y %H:%M")

    sheet["A3"] = "Total Tickets:"
    sheet["B3"] = len(records)

    for cell in ["A2", "A3"]:

        sheet[cell].font = Font(
            bold=True,
            color="172B4D"
        )

    # =========================
    # COLUMN HEADINGS
    # =========================

    headers = [
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

    header_row = 5

    for col_num, heading in enumerate(headers, start=1):

        cell = sheet.cell(
            row=header_row,
            column=col_num,
            value=heading
        )

        cell.font = Font(
            bold=True,
            color="FFFFFF",
            size=10
        )

        cell.fill = PatternFill(
            start_color="30475E",
            end_color="30475E",
            fill_type="solid"
        )

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    sheet.row_dimensions[header_row].height = 28

    # =========================
    # INSERT TICKET RECORDS
    # =========================

    for row_num, record in enumerate(
        records,
        start=header_row + 1
    ):

        for col_num, value in enumerate(record, start=1):

            if isinstance(value, datetime):
                value = value.strftime("%d-%m-%Y %H:%M")

            cell = sheet.cell(
                row=row_num,
                column=col_num,
                value=value
            )

            cell.alignment = Alignment(
                vertical="center",
                wrap_text=True
            )

            # Alternating row colors

            if row_num % 2 == 0:

                cell.fill = PatternFill(
                    start_color="F1F5F9",
                    end_color="F1F5F9",
                    fill_type="solid"
                )

            else:

                cell.fill = PatternFill(
                    start_color="FFFFFF",
                    end_color="FFFFFF",
                    fill_type="solid"
                )

        sheet.row_dimensions[row_num].height = 32

    # =========================
    # COLOR-CODE PRIORITY
    # =========================

    priority_colors = {
        "Low": "DCFCE7",
        "Medium": "FEF3C7",
        "High": "FFEDD5",
        "Critical": "FEE2E2"
    }

    for row_num in range(header_row + 1, header_row + len(records) + 1):

        priority_cell = sheet.cell(
            row=row_num,
            column=6
        )

        priority = priority_cell.value

        if priority in priority_colors:

            priority_cell.fill = PatternFill(
                start_color=priority_colors[priority],
                end_color=priority_colors[priority],
                fill_type="solid"
            )

            priority_cell.font = Font(
                bold=True,
                color="172B4D"
            )

    # =========================
    # COLOR-CODE STATUS
    # =========================

    status_colors = {
        "Open": "FEE2E2",
        "In Progress": "FEF3C7",
        "Resolved": "DCFCE7"
    }

    for row_num in range(header_row + 1, header_row + len(records) + 1):

        status_cell = sheet.cell(
            row=row_num,
            column=7
        )

        status = status_cell.value

        if status in status_colors:

            status_cell.fill = PatternFill(
                start_color=status_colors[status],
                end_color=status_colors[status],
                fill_type="solid"
            )

            status_cell.font = Font(
                bold=True,
                color="172B4D"
            )

    # =========================
    # COLUMN WIDTHS
    # =========================

    column_widths = [
        12, 22, 18, 20, 45, 15, 18, 22, 22
    ]

    for index, width in enumerate(column_widths, start=1):

        sheet.column_dimensions[
            get_column_letter(index)
        ].width = width

    # =========================
    # BORDERS
    # =========================

    thin_border = Border(
        bottom=Side(
            style="thin",
            color="D9E1F2"
        )
    )

    last_row = header_row + len(records)

    for row in sheet.iter_rows(
        min_row=header_row,
        max_row=last_row,
        min_col=1,
        max_col=9
    ):

        for cell in row:
            cell.border = thin_border

    # =========================
    # FILTERS AND FREEZE PANES
    # =========================

    sheet.freeze_panes = "A6"

    sheet.auto_filter.ref = f"A5:I{last_row}"

    # =========================
    # SAVE EXCEL FILE
    # =========================

    project_folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    export_folder = os.path.join(
        project_folder,
        "exports"
    )

    os.makedirs(export_folder, exist_ok=True)

    filename = (
        "IT_HelpDesk_Report_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".xlsx"
    )

    file_path = os.path.join(
        export_folder,
        filename
    )

    workbook.save(file_path)

    return file_path


# =========================
# EXPORT FUNCTION
# =========================

def export_to_excel():

    try:

        export_button.config(
            state="disabled",
            text="GENERATING REPORT..."
        )

        root.update_idletasks()

        records = fetch_tickets()

        if not records:

            messagebox.showinfo(
                "No Records",
                "There are no tickets available to export."
            )

            return

        file_path = create_excel_report(records)

        export_status.config(
            text="Excel report generated successfully!",
            fg="#16A34A"
        )

        messagebox.showinfo(
            "Export Successful",
            f"Your Excel report has been generated!\n\n"
            f"Total Tickets: {len(records)}\n\n"
            f"File Location:\n{file_path}"
        )

    except Exception as e:

        export_status.config(
            text="Report generation failed.",
            fg="#DC2626"
        )

        messagebox.showerror(
            "Export Error",
            f"Unable to export report.\n\n{str(e)}"
        )

    finally:

        export_button.config(
            state="normal",
            text="EXPORT TO EXCEL"
        )


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("Excel Export | IT Help Desk")
root.geometry("850x600")
root.minsize(700, 500)
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
    padx=35,
    pady=30
)

content.pack(fill="both", expand=True)


# PAGE HEADING

tk.Label(
    content,
    text="Export Reports to Excel",
    font=("Segoe UI", 22, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w")

tk.Label(
    content,
    text="Generate and save a professionally formatted report of all support tickets.",
    font=("Segoe UI", 10),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(6, 22))


# =========================
# EXPORT CARD
# =========================

export_card = tk.Frame(
    content,
    bg=WHITE,
    padx=30,
    pady=30,
    highlightbackground=BORDER,
    highlightthickness=1
)

export_card.pack(fill="both", expand=True)


tk.Label(
    export_card,
    text="EXCEL REPORT GENERATOR",
    font=("Segoe UI", 14, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w", pady=(0, 8))


tk.Label(
    export_card,
    text="Your report will include:",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", pady=(12, 8))


# REPORT CONTENT LIST

report_items = [
    "Complete ticket records",
    "Employee and department information",
    "Issue category and description",
    "Priority and ticket status",
    "Created date and resolution date",
    "Formatted Excel columns and filters"
]

for item in report_items:

    tk.Label(
        export_card,
        text=f"•  {item}",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w", pady=4)


# =========================
# EXPORT BUTTON
# =========================

export_button = tk.Button(
    export_card,
    text="EXPORT TO EXCEL",
    font=("Segoe UI", 11, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground="#1D4ED8",
    activeforeground=WHITE,
    cursor="hand2",
    command=export_to_excel,
    relief="flat",
    bd=0,
    padx=30,
    pady=14
)

export_button.pack(pady=(28, 12))


# =========================
# STATUS MESSAGE
# =========================

export_status = tk.Label(
    export_card,
    text="Ready to generate your Excel report.",
    font=("Segoe UI", 9),
    bg=WHITE,
    fg=MUTED
)

export_status.pack(pady=5)


# =========================
# FOOTER
# =========================

tk.Label(
    content,
    text="Reports are automatically saved inside the project's exports folder.",
    font=("Segoe UI", 9),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(15, 0))


root.mainloop()