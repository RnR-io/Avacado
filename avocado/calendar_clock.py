"""
Terminal Monthly Calendar & 12-Hour System Time Widget
Renders a clean terminal month grid highlighting today's date + 12-Hour digital clock string.
"""
import calendar
import datetime

def get_calendar_lines(year=None, month=None, highlight_today=True):
    now = datetime.datetime.now()
    if year is None: year = now.year
    if month is None: month = now.month
    today_day = now.day if highlight_today else -1

    cal = calendar.TextCalendar(calendar.SUNDAY)
    month_str = cal.formatmonth(year, month)
    raw_lines = month_str.strip().split('\n')

    formatted_lines = []
    header_title = raw_lines[0].strip()
    formatted_lines.append(f"📅 {header_title}")

    if len(raw_lines) > 1:
        formatted_lines.append(f"   {raw_lines[1]}")

    for line in raw_lines[2:]:
        idx = 0
        colored_week = ""
        while idx < len(line):
            chunk = line[idx:idx+3]
            day_str = chunk.strip()
            if day_str.isdigit() and int(day_str) == today_day:
                colored_week += f"[{int(day_str):2d}]"
            else:
                colored_week += chunk
            idx += 3
        formatted_lines.append(f"   {colored_week}")

    return formatted_lines

def get_clock_info():
    now = datetime.datetime.now()
    time_12h = now.strftime("%I:%M:%S %p")
    date_str = now.strftime("%A, %B %d, %Y")
    week_num = now.strftime("Week %U")
    return {
        "time": time_12h,
        "date": date_str,
        "week": week_num
    }
