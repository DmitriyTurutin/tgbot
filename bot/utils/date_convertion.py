from datetime import datetime 
import locale

def convert_date(date: str) -> str:
    dt = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
    date = dt.strftime("%d %B %Y %H:%M")
    return date
    