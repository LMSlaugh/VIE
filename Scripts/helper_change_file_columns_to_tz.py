import pandas as pd
import time as time
import datetime as dt
import pytz as tz

csvtochange = "VIE-output-REAL"

data = pd.read_csv(csvtochange + ".csv", parse_dates=["runtimedt","overallprobadt", "wifidt", "co2dt", "elecdt"])
df = data["wifidt"]
data["wifidt"] = data["wifidt"] - dt.timedelta(hours=8)
df = data["wifidt"]
df = data["co2dt"]
data["co2dt"] = data["co2dt"] - dt.timedelta(hours=8)
df = data["co2dt"]
df = data["elecdt"]
data["elecdt"] = data["elecdt"] - dt.timedelta(hours=8)
df = data["elecdt"]
df = data["overallprobadt"]
data["overallprobadt"] = data["overallprobadt"] - dt.timedelta(hours=8)
df = data["overallprobadt"]

data.to_csv(csvtochange + "UTC-8h.csv", index=False)


stopgap = "This is a stopgap"