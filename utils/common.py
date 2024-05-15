import datetime
import pytz

def escape_special_chars(text):
    """Escape spezielle Zeichen für MarkdownV2"""
    escape_chars = r'\[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

def get_local_timezone(timezone='Europe/Berlin'):
    """Ermittelt die lokale Zeitzone"""
    l_timezone = pytz.timezone(timezone)
    return l_timezone

def get_current_date_time(timezone='Europe/Berlin'):
    """Ermittelt das aktuelle Datum und Uhrzeit in der angegebenen Zeitzone"""
    l_timezone = pytz.timezone(timezone)
    curr_date_time = datetime.datetime.now(l_timezone)
    return curr_date_time
