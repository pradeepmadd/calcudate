from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, request

app = Flask(__name__)


def ymd(form, prefix):
    return f"{form[f'{prefix}_year']}-{form[f'{prefix}_month']}-{form[f'{prefix}_day']}"


def calc_date(form):
    base = datetime.strptime(ymd(form, "base"), "%Y-%m-%d")
    y = abs(int(form.get("years") or 0))
    mo = abs(int(form.get("months") or 0))
    d = abs(int(form.get("days") or 0))
    sign = 1 if form.get("operation") == "add" else -1
    result = base + relativedelta(years=sign * y, months=sign * mo, days=sign * d)
    op = "+" if sign == 1 else "−"
    label = f"{base.strftime('%Y-%m-%d')} {op} {y}y {mo}m {d}d"
    return {"headline": result.strftime("%Y-%m-%d"), "detail": result.strftime("%A, %d %B %Y"), "label": label}


def calc_time(form):
    stamp = f"{form['base_hour']}:{form['base_minute']}:{form['base_second']} {form['base_ampm']}"
    base = datetime.strptime(stamp, "%I:%M:%S %p")
    h = abs(int(form.get("hours") or 0))
    m = abs(int(form.get("minutes") or 0))
    s = abs(int(form.get("seconds") or 0))
    sign = 1 if form.get("operation") == "add" else -1
    result = base + relativedelta(hours=sign * h, minutes=sign * m, seconds=sign * s)
    op = "+" if sign == 1 else "−"
    label = f"{base.strftime('%I:%M:%S %p')} {op} {h}h {m}m {s}s"
    return {"headline": result.strftime("%I:%M:%S %p"), "detail": f"24-hour {result.strftime('%H:%M:%S')}", "label": label}


def calc_diff(form):
    start = datetime.strptime(ymd(form, "start"), "%Y-%m-%d")
    end = datetime.strptime(ymd(form, "end"), "%Y-%m-%d")
    swapped = start > end
    if swapped:
        start, end = end, start
    delta = relativedelta(end, start)
    total_days = (end - start).days
    headline = f"{delta.years}y {delta.months}m {delta.days}d"
    prefix = "Swapped span" if swapped else "Span"
    detail = f"{prefix} · {total_days} days · {total_days // 7}w {total_days % 7}d"
    label = f"{start.strftime('%Y-%m-%d')} → {end.strftime('%Y-%m-%d')}"
    return {"headline": headline, "detail": detail, "label": label}


@app.route("/", methods=["GET", "POST"])
def index():
    now = datetime.now()
    active_tab = request.form.get("active_tab", "date")
    result = None

    if request.method == "POST":
        try:
            if active_tab == "date":
                result = calc_date(request.form)
            elif active_tab == "time":
                result = calc_time(request.form)
            elif active_tab == "diff":
                result = calc_diff(request.form)
        except ValueError:
            result = {"headline": "—", "detail": "Invalid selection. Check the values and try again."}

    years = list(range(now.year - 50, now.year + 51))

    return render_template(
        "index.html",
        active_tab=active_tab,
        years=years,
        now_display_date=now.strftime("%a %d %b %Y"),
        now_display_time=now.strftime("%I:%M:%S %p"),
        base_year=now.year, base_month=now.month, base_day=now.day,
        base_hour=int(now.strftime("%I")), base_minute=now.minute, base_second=now.second, base_ampm=now.strftime("%p"),
        start_year=now.year, start_month=now.month, start_day=now.day,
        end_year=now.year, end_month=now.month, end_day=now.day,
        result=result,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
