


def quarter_hour_down_rounder(original_time):

    time_minute = original_time.minute

    if time_minute >= 0 and time_minute < 15:
        new_minute = 0
    elif time_minute >= 15 and time_minute < 30:
        new_minute = 15
    elif time_minute >= 30 and time_minute < 45:
        new_minute = 30
    elif time_minute >= 45 and time_minute < 60:
        new_minute = 45
    else:
        raise "Invalid time error"

    new_time = original_time.replace(minute=new_minute,second=0)
    return new_time

