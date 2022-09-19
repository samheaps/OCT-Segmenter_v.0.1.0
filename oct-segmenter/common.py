import datetime


def get_timestamp():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H_%M_%S")

    return timestamp