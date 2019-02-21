import pandas as pd
import numpy as np
import PI_client_LMS as pc
import VieSensor as snsr


def CreateVirtualSensors(metadatabasePath):
    # Purpose: read each sensor into a list from the sensor metadatabase
    metadata = pd.read_csv(metadatabasePath)
    sensors = {} # Create sensor dictionary. Enforces unique sensor names!!
    for index, row in metadata.iterrows():
        sn = row["Sensor-Name"]
        st = row["Sensor-Type"]
        uf = row["Update-Frequency"]
        dat = row["Data-Access-Type"]
        vrt = row["Vacancy-Relationship-Type"]
        drfn = row["Data-Retrieval-File-Name"]
        ppfn = row["Preprocessing-File-Name"]
        rbfn = row["Relationship-Builder-File-Name"]
        p1 = row["Parameter-1"]
        p2 = row["Parameter-2"]
        p3 = row["Parameter-3"]
        p4 = row["Parameter-4"]
        newSensor = snsr.VieSensor(sn, st, uf, dat, vrt, drfn, ppfn, rbfn, p1, p2, p3, p4)
        sensors[newSensor.sensorname] = newSensor
    return sensors


client = pc.pi_client()
sensors = CreateVirtualSensors("VIE-sensor-metadatabase.csv") # Read sensors from file, instantiate. If missing data, fill with dummy data ("") and move on to next sensor
points = []
for k, v in sensors.items():
    points.append(v.dataaccesstype)
data = client.get_stream_by_point(points,start="2019-02-03 21:11:14", end="2019-02-07 12:30:00", interval="5m")
data.columns = ["wifi1-val", "co21-val", "elec1-val"]
data["datetimes"] = data.index
data = pd.concat([data["datetimes"],data["wifi1-val"],data["datetimes"],data["co21-val"],data["datetimes"],data["elec1-val"]], axis=1)
data.columns=["wifi1-dt","wifi1-val","co21-dt","co21-val","elec1-dt", "elec1-val"]
data.to_csv("DataFiles\\VIE-input-historical.csv", date_format='%m-%d-%Y %H:%M', index=False)

a = "this is a stopgap"