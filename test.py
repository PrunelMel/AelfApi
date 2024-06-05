import datetime

start_dt = datetime.date(int("2022"), 6, 10)
end_dt = datetime.date(2022, 6, 15)

# difference between current and previous date
delta = datetime.timedelta(days=1)

# store the dates between two dates in a list
dates = []

while start_dt <= end_dt:
    # add current date to list by converting  it to iso format
    dates.append(start_dt.isoformat())
    # increment start date by timedelta
    start_dt += delta

print('Dates between', start_dt, 'and', end_dt)
print(dates)
print(datetime.date.today().strftime("%d %B, %Y"))