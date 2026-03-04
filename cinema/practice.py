from datetime import datetime
from datetime import date , time
from datetime import timedelta

duration = timedelta(minutes=22, hours=2)
my_time = time(minute=22 , hour=23 , second=1)


start_time = '18:37:20'
start_date = '2026-03-03' 
start_datetime = datetime.fromisoformat(f"{start_date} {start_time}")

current_datetime = datetime.today()
end_datetime = start_datetime + duration 
print(start_datetime)
print(current_datetime)
print(current_datetime >= start_datetime)