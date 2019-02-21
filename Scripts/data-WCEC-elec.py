# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Description here}

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import requests as req
import logging


def UpdateSnapshot(sensor):
    return sensor

def GetHistoricalData(): # Currently not called anywhere
    url = 'https://webservice.hobolink.com/restv2/data/custom/file'
    payload = {
        "query": "215_Last_30_Days",
        "authentication": {
            "password": "1605tilia",
            "user": "UHubDavis",
            "token": "Ei3pjgOLri",
        }
    }

    try:
        r = req.post(url, json=payload, timeout=30)
        c = 10
    except req.exceptions.Timeout:
        logging.error("Hobolink HTTP request timed out (30 seconds)")

    return

GetHistoricalData()