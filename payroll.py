
from datetime import datetime, timedelta

time_sheet = [
    ('10:41 AM' , '5:14 PM' , 'August  1 , 2025'),
    ('10:55 AM', '7:00 PM', 'August  4 , 2025'),
    ('11:00 AM', '6:00 PM', 'August  5 , 2025'),
    ('11:00 AM', '6:00 PM', 'August  6 , 2025'),
    ('11:00 AM', '5:00 PM', 'August  7 , 2025'),
    ('11:45 AM', '5:00 PM', 'August 11 , 2025'),
    ('10:45 AM', '3:10 PM', 'August 12 , 2025'),
    ('11:30 AM', '5:00 PM', 'August 13 , 2025'),
    ('10:15 AM', '5:00 PM', 'August 14 , 2025')
]

 

DAILY_RATE = 450
HOURS_PER_DAY = 8
HOURLY_RATE = DAILY_RATE / HOURS_PER_DAY

total_income = 0

for start_str, end_str, day in time_sheet:
    start = datetime.strptime(start_str, "%I:%M %p")
    end = datetime.strptime(end_str, "%I:%M %p")
 

    # Calculate total hours worked
    hours_worked = (end - start).total_seconds() / 3600

    # Calculate pay for the day
    pay = hours_worked * HOURLY_RATE
    total_income += pay

    print(f"{start_str} → {end_str} | {hours_worked:.2f} hrs x {HOURLY_RATE:.2f} hourly rate | ₱{pay:.2f} | {day}")

print("\nTOTAL INCOME: ₱{:.2f}".format(total_income))
