import pandas as pd
import numpy as np
import PI_client_LMS as pc

client = pc.pi_client()
#l, d = client.search_by_point("*giedt*flow")

points = ['GIEDT.ZONE.AHU01.RM11_1.Zone Supply Air Flow','GIEDT.ZONE.AHU01.RM11_2.Zone Supply Air Flow','GIEDT.ZONE.AHU01.RM11_3.Zone Supply Air Flow']
data = client.get_stream_by_point(points,start="2018-01-15 0:00:00", end="2018-03-24 0:00:00", interval="5m")
data.to_csv("GiedtWinterExperimentData.csv")

a = "this is a stopgap"