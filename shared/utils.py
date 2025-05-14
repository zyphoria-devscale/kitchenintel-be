import bson
import pytz
from datetime import datetime

def generate_id():
    return str(bson.ObjectId())


def asia_jakarta_time(value):
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    return value.astimezone(jakarta_tz)

def convert_to_utc(value):
    local_dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    local_dt_aware = jakarta_tz.localize(local_dt)
    utc_dt = local_dt_aware.astimezone(pytz.UTC)
    return utc_dt