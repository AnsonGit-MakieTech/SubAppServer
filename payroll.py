from datetime import datetime, timedelta

time_sheet = [
    ('10:40 AM' , '5:10 PM' , 'August  18 , 2025'), 
    ('10:20 AM' , '6:00 PM' , 'August  19 , 2025'), 
    ('10:03 AM' , '7:00 PM' , 'August  20 , 2025'), 
    ('10:18 AM' , '5:10 PM' , 'August  21 , 2025'), 
    ('10:30 AM' , '8:30 PM' , 'August  22 , 2025'), 
    ('10:30 AM' , '6:15 PM' , 'August  26 , 2025'), 
    ('10:40 AM' , '6:30 PM' , 'August  27 , 2025'), 
    ('10:03 AM' , '7:00 PM' , 'August  28 , 2025'), 
]

DAILY_RATE = 450
HOURS_PER_DAY = 8
HOURLY_RATE = DAILY_RATE / HOURS_PER_DAY

total_income = 0

for start_str, end_str, day in time_sheet:
    start = datetime.strptime(start_str, "%I:%M %p")
    end = datetime.strptime(end_str, "%I:%M %p")
 

    # Calculate total hours worked
    raw_hours = (end - start).total_seconds() / 3600

    # Deduct 1 hour for breaktime (but not below 0)
    hours_worked = max(0, raw_hours - 1)

    # Calculate pay for the day
    pay = hours_worked * HOURLY_RATE
    total_income += pay


    print(
        f"{start_str} → {end_str} | {raw_hours:.2f} hrs - 1 hr break = {hours_worked:.2f} hrs "
        f"x {HOURLY_RATE:.2f} | ₱{pay:.2f} | {day}"
    )

print("\nINCOME: ₱ {:.2f}".format(total_income))
print("ADVANCE : ₱ {:.2f}".format(5020))
print("\nTOTAL INCOME : ₱ {:.2f}".format(total_income - 5020))
