from _datetime import datetime


# assuming local PST timezone, resetting epoch timestamps to midnight to calculate number of days
def get_days(start_epoch, end_epoch):
    start_date = datetime.fromtimestamp(start_epoch).strftime("%x")
    end_date = datetime.fromtimestamp(end_epoch).strftime("%x")
    return (datetime.strptime(end_date, "%x") - datetime.strptime(start_date, "%x")).days

print(get_days(1491289199, 1491289201))
