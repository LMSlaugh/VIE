import pandas as pd
import numpy as np
import PI_client as pc

client = pc.pi_client()
#l, d = client.search_by_point("*solar*demand*kbtu/h*")
#l, d = client.search_by_point("Actual_Campus_Demand")
#l, d = client.search_by_point("*campus*total*kwh*")
#l, d = client.search_by_point("*haring*total*elec*demand*")
l, d = client.search_by_point("*haring*")
#l, d = client.search_by_point("*roessler*electricity_demand*")
#l, d = client.search_by_point("*ap.ucd_*total*")
#l, d = client.search_by_point("*RMI_Brewery_Winery_and_Food_Pilot_Facility_MSB*elec*demand*")

points = l
#points = ['GIEDT.ZONE.AHU01.RM11_1.Zone Supply Air Flow','GIEDT.ZONE.AHU01.RM11_2.Zone Supply Air Flow','GIEDT.ZONE.AHU01.RM11_3.Zone Supply Air Flow']
#data = client.get_stream_by_point(points,start="2018-01-15 0:00:00", end="2018-03-24 0:00:00", interval="5m")
#data.to_csv("GiedtWinterExperimentData.csv")

#points = ['AP.STUD-COMM-CTR_Total_Count', 'SCC.AHU.AHU01.RM.1101A.CO2', 'SCC_Electricity_Demand_kBtu']
#points = ["RMI_Brewery_Winery_and_Food_Pilot_Facility_MSB/Electricity_Demand", "RMI_Brewery_Winery_and_Food_Pilot_Facility_MSB/Solar_PV1_Electricity", "RMI_Brewery_Winery_and_Food_Pilot_Facility_MSB/Solar_PV2_ELectricity"]
data = client.get_stream_by_point(points, calculation="calculated", start="2019-07-01 00:00:00", end="2019-07-08 00:00:00",interval="10m")
#data = client.get_stream_by_point(points, calculation="end")

data.to_csv("DataFiles\\Building_elec_w.csv", header=True, index=True)

a = "this is a stopgap"