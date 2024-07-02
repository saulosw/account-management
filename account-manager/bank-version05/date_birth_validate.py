import calendar
import datetime

text_calendar = calendar.TextCalendar()

def is_valid_calendar_day(day: str, month: int, year: int) -> bool:
    try:
        formatted_month = text_calendar.formatmonth(year, month)
        return day in formatted_month
    except ValueError:
        return False

def birthdate_validate(birthdate: str) -> bool:
    if len(birthdate) != 8:
        return False
    
    day = birthdate[:2]
    month = birthdate[2:4]
    year = birthdate[4:]
    
    try:
        datetime.date(int(year), int(month), int(day))
    except ValueError:
        return False
    
    return is_valid_calendar_day(day, int(month), int(year))

def age_validate(birthdate: str) -> bool:
    if not birthdate_validate(birthdate):
        return False
    
    day = int(birthdate[:2])
    month = int(birthdate[2:4])
    year = int(birthdate[4:])
    
    birth_date = datetime.date(year, month, day)
    today = datetime.date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    if year < 1900 or age > 120:
        return False
    
    return age >= 18