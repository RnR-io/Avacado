"""
Terminal Monthly Calendar & Digital Clock Widget
Renders a clean terminal month grid highlighting today's date.
"""
import calendar
import datetime
import time

def get_calendar_lines(year=None, month=None, highlight_today=True):
    now = datetime.datetime.now()
    if year is None: year = now.year
    if month is None: month = now.month
    today_day = now.day if highlight_today else -1

    cal = calendar.TextCalendar(calendar.SUNDAY)
    month_str = cal.formatmonth(year, month)
    raw_lines = month_str.strip().split('\n')

    formatted_lines = []
    # Header: Month Year
    header_title = raw_lines[0].strip()
    formatted_lines.append(f"📅 {header_title}")

    # Days of week header (Su Mo Tu We Th Fr Sa)
    if len(raw_lines) > 1:
        formatted_lines.append(f"   {raw_lines[1]}")

    # Weeks grid with today highlighted
    for line in raw_lines[2:]:
        # Process 2-digit day strings
        week_days = line.split()
        colored_week = ""
        # Keep original spacing alignment
        idx = 0
        while idx < len(line):
            chunk = line[idx:idx+3]
            day_str = chunk.strip()
            if day_str.isdigit() and int(day_str) == today_day:
                # Highlight today in brackets
                colored_week += f"[{int(day_str):2d}]"
            else:
                colored_week += chunk
            idx += 3
        formatted_lines.append(f"   {colored_week}")

    return formatted_lines

def get_clock_info():
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%A, %B %d, %Y")
    week_num = now.strftime("Week %U")
    return {
        "time": time_str,
        "date": date_str,
        "week": week_num
    }
