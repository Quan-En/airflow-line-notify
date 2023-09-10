from datetime import datetime

def check_weekday(date_stamp):
    today = datetime.strptime(date_stamp, '%Y%m%d')
    return 'is_workday' if today.isoweekday() <= 5 else 'is_holiday'