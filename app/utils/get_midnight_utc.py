import pytz
from datetime import datetime, date, time

def get_midnight_utc(dt = None):
    
    if dt is None:
        dt = datetime.now()
        
    dt = dt.replace(hour = 0, minute=0, second=0, microsecond=0)
    
    dt = pytz.utc.localize(dt)
    
    return dt

