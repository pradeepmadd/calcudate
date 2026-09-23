import ttkbootstrap as tb
from tkinter import messagebox
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ==========================================
#          CALCULATION FUNCTIONS
# ==========================================
def calculate_date():
    try:
        base_str = f"{cb_base_year.get()}-{cb_base_month.get()}-{cb_base_day.get()}"
        base_datetime = datetime.strptime(base_str, "%Y-%m-%d")
        y = int(spin_years.get() or 0)
        mo = int(spin_months.get() or 0)
        d = int(spin_days.get() or 0)
        sign = 1 if date_operation_var.get() == "Add" else -1
        delta = relativedelta(years=sign * y, months=sign * mo, days=sign * d)
        new_date = base_datetime + delta
        label_result_date.config(text=f"Result: {new_date.strftime('%Y-%m-%d')}")
    except ValueError:
        messagebox.showerror("Error", "Invalid Date selected. Check your month/day combination.")

def calculate_time():
    try:
        base_str = f"{cb_hour.get()}:{cb_minute.get()}:{cb_second.get()} {cb_ampm.get()}"
        base_time = datetime.strptime(base_str, "%I:%M:%S %p")
        h = int(spin_hours.get() or 0)
        m = int(spin_minutes.get() or 0)
        s = int(spin_seconds.get() or 0)
        sign = 1 if time_operation_var.get() == "Add" else -1
        delta = relativedelta(hours=sign * h, minutes=sign * m, seconds=sign * s)
        new_time = base_time + delta
        label_result_time.config(text=f"Result: {new_time.strftime('%I:%M:%S %p')}")
    except ValueError:
        messagebox.showerror("Error", "Please check your time selections.")

def calculate_difference():
    try:
        start_str = f"{cb_start_year.get()}-{cb_start_month.get()}-{cb_start_day.get()}"
        end_str = f"{cb_end_year.get()}-{cb_end_month.get()}-{cb_end_day.get()}"
        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d")
        if start_date > end_date:
            start_date, end_date = end_date, start_date
            prefix = "Difference (Swapped): "
        else:
            prefix = "Difference: "
        delta = relativedelta(end_date, start_date)
        result_str = f"{prefix}\n{delta.years} Years, {delta.months} Months, {delta.days} Days"
        label_result_diff.config(text=result_str)
    except ValueError:
        messagebox.showerror("Error", "Invalid date selection.")

# ==========================================
#             MAIN WINDOW SETUP
# ==========================================
# 'darkly' is a sleek dark mode. You can change this to 'litera' or 'cosmo' for light modes!
root = tb.Window(themename="darkly") 
root.title("Date & Time Calculator Pro")
root.geometry("450x600")

notebook = tb.Notebook(root, bootstyle="info")
notebook.pack(pady=15, padx=15, expand=True, fill="both")

tab_date = tb.Frame(notebook, padding=20)
tab_time = tb.Frame(notebook, padding=20)
tab_diff = tb.Frame(notebook, padding=20)

notebook.add(tab_date, text="📅 Date Calc")
notebook.add(tab_time, text="⏱️ Time Calc")
notebook.add(tab_diff, text="🗓️ Difference")

# Setup Lists
now = datetime.now()
years_list = [str(y) for y in range(now.year - 50, now.year + 51)]
months_list = [f"{m:02d}" for m in range(1, 13)]
days_list = [f"{d:02d}" for d in range(1, 32)]

# ==========================================
#                 DATE TAB
# ==========================================
tb.Label(tab_date, text="Base Date (YYYY-MM-DD):", font=("Helvetica", 11, "bold")).pack(pady=(0, 10))
frame_d = tb.Frame(tab_date); frame_d.pack(pady=5)

cb_base_year = tb.Combobox(frame_d, values=years_list, width=6, state="readonly"); cb_base_year.pack(side="left", padx=2)
tb.Label(frame_d, text="-").pack(side="left")
cb_base_month = tb.Combobox(frame_d, values=months_list, width=4, state="readonly"); cb_base_month.pack(side="left", padx=2)
tb.Label(frame_d, text="-").pack(side="left")
cb_base_day = tb.Combobox(frame_d, values=days_list, width=4, state="readonly"); cb_base_day.pack(side="left", padx=2)
cb_base_year.set(now.year); cb_base_month.set(now.strftime("%m")); cb_base_day.set(now.strftime("%d"))

tb.Separator(tab_date, bootstyle="info").pack(fill="x", pady=15)

date_operation_var = tb.StringVar(value="Add")
frame_d_ops = tb.Frame(tab_date); frame_d_ops.pack(pady=5)
tb.Radiobutton(frame_d_ops, text="Add (+)", variable=date_operation_var, value="Add", bootstyle="success").pack(side="left", padx=10)
tb.Radiobutton(frame_d_ops, text="Subtract (-)", variable=date_operation_var, value="Subtract", bootstyle="danger").pack(side="left", padx=10)

frame_d_inputs = tb.Frame(tab_date); frame_d_inputs.pack(pady=10)
tb.Label(frame_d_inputs, text="Years").grid(row=0, column=0, pady=5, padx=5, sticky="e")
spin_years = tb.Spinbox(frame_d_inputs, from_=0, to=999, width=8); spin_years.set(0); spin_years.grid(row=0, column=1)

tb.Label(frame_d_inputs, text="Months").grid(row=1, column=0, pady=5, padx=5, sticky="e")
spin_months = tb.Spinbox(frame_d_inputs, from_=0, to=999, width=8); spin_months.set(0); spin_months.grid(row=1, column=1)

tb.Label(frame_d_inputs, text="Days").grid(row=2, column=0, pady=5, padx=5, sticky="e")
spin_days = tb.Spinbox(frame_d_inputs, from_=0, to=999, width=8); spin_days.set(0); spin_days.grid(row=2, column=1)

tb.Button(tab_date, text="Calculate Date", command=calculate_date, bootstyle="success-outline", width=20).pack(pady=15)
label_result_date = tb.Label(tab_date, text="Result: ", font=("Helvetica", 14, "bold"), bootstyle="success")
label_result_date.pack()

# ==========================================
#                 TIME TAB
# ==========================================
tb.Label(tab_time, text="Base Time (HH:MM:SS AM/PM):", font=("Helvetica", 11, "bold")).pack(pady=(0, 10))
frame_t = tb.Frame(tab_time); frame_t.pack(pady=5)

cb_hour = tb.Combobox(frame_t, values=[f"{i:02d}" for i in range(1, 13)], width=4, state="readonly"); cb_hour.pack(side="left", padx=2)
tb.Label(frame_t, text=":").pack(side="left")
cb_minute = tb.Combobox(frame_t, values=[f"{i:02d}" for i in range(60)], width=4, state="readonly"); cb_minute.pack(side="left", padx=2)
tb.Label(frame_t, text=":").pack(side="left")
cb_second = tb.Combobox(frame_t, values=[f"{i:02d}" for i in range(60)], width=4, state="readonly"); cb_second.pack(side="left", padx=2)
cb_ampm = tb.Combobox(frame_t, values=["AM", "PM"], width=5, state="readonly"); cb_ampm.pack(side="left", padx=5)
cb_hour.set(now.strftime("%I")); cb_minute.set(now.strftime("%M")); cb_second.set(now.strftime("%S")); cb_ampm.set(now.strftime("%p"))

tb.Separator(tab_time, bootstyle="info").pack(fill="x", pady=15)

time_operation_var = tb.StringVar(value="Add")
frame_t_ops = tb.Frame(tab_time); frame_t_ops.pack(pady=5)
tb.Radiobutton(frame_t_ops, text="Add (+)", variable=time_operation_var, value="Add", bootstyle="info").pack(side="left", padx=10)
tb.Radiobutton(frame_t_ops, text="Subtract (-)", variable=time_operation_var, value="Subtract", bootstyle="danger").pack(side="left", padx=10)

frame_t_inputs = tb.Frame(tab_time); frame_t_inputs.pack(pady=10)
tb.Label(frame_t_inputs, text="Hours").grid(row=0, column=0, pady=5, padx=5, sticky="e")
spin_hours = tb.Spinbox(frame_t_inputs, from_=0, to=999, width=8); spin_hours.set(0); spin_hours.grid(row=0, column=1)

tb.Label(frame_t_inputs, text="Minutes").grid(row=1, column=0, pady=5, padx=5, sticky="e")
spin_minutes = tb.Spinbox(frame_t_inputs, from_=0, to=999, width=8); spin_minutes.set(0); spin_minutes.grid(row=1, column=1)

tb.Label(frame_t_inputs, text="Seconds").grid(row=2, column=0, pady=5, padx=5, sticky="e")
spin_seconds = tb.Spinbox(frame_t_inputs, from_=0, to=999, width=8); spin_seconds.set(0); spin_seconds.grid(row=2, column=1)

tb.Button(tab_time, text="Calculate Time", command=calculate_time, bootstyle="info-outline", width=20).pack(pady=15)
label_result_time = tb.Label(tab_time, text="Result: ", font=("Helvetica", 14, "bold"), bootstyle="info")
label_result_time.pack()

# ==========================================
#            DATE DIFFERENCE TAB
# ==========================================
tb.Label(tab_diff, text="Select Start Date:", font=("Helvetica", 11, "bold")).pack(pady=(10, 10))
frame_s = tb.Frame(tab_diff); frame_s.pack()
cb_start_year = tb.Combobox(frame_s, values=years_list, width=6, state="readonly"); cb_start_year.pack(side="left", padx=2)
cb_start_month = tb.Combobox(frame_s, values=months_list, width=4, state="readonly"); cb_start_month.pack(side="left", padx=2)
cb_start_day = tb.Combobox(frame_s, values=days_list, width=4, state="readonly"); cb_start_day.pack(side="left", padx=2)
cb_start_year.set(now.year); cb_start_month.set(now.strftime("%m")); cb_start_day.set(now.strftime("%d"))

tb.Label(tab_diff, text="Select End Date:", font=("Helvetica", 11, "bold")).pack(pady=(25, 10))
frame_e = tb.Frame(tab_diff); frame_e.pack()
cb_end_year = tb.Combobox(frame_e, values=years_list, width=6, state="readonly"); cb_end_year.pack(side="left", padx=2)
cb_end_month = tb.Combobox(frame_e, values=months_list, width=4, state="readonly"); cb_end_month.pack(side="left", padx=2)
cb_end_day = tb.Combobox(frame_e, values=days_list, width=4, state="readonly"); cb_end_day.pack(side="left", padx=2)
cb_end_year.set(now.year); cb_end_month.set(now.strftime("%m")); cb_end_day.set(now.strftime("%d"))

tb.Separator(tab_diff, bootstyle="info").pack(fill="x", pady=25)

tb.Button(tab_diff, text="Calculate Difference", command=calculate_difference, bootstyle="primary", width=25).pack(pady=15)
label_result_diff = tb.Label(tab_diff, text="Difference:\n\n--", font=("Helvetica", 13, "bold"), bootstyle="primary", justify="center")
label_result_diff.pack()

root.mainloop()
