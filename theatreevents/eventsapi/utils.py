from django.db import IntegrityError, DatabaseError
import pytz


def get_client_code(client_name):
    import datetime
    words = client_name.split()
    if len(words) > 1:
        initials = [word[0].upper() for word in words[:2]]
    else:
        initials = [word[:2].upper() for word in words]

    now_utc = datetime.datetime.utcnow()
    local_timezone = pytz.timezone('Africa/Nairobi')  # should be timezone of the server
    now = now_utc.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    minute = str(now.minute).zfill(2)
    hour = str(now.hour).zfill(2)
    month = str(now.month).zfill(2)
    date = str(now.day).zfill(2)

    return initials[0] + minute + hour + month + date + initials[1]


def save_instance(model_instance):
    try:
        model_instance.save()
        return True
    except IntegrityError | DatabaseError:
        return False
