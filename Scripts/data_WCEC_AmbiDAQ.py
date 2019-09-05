from sshtunnel import SSHTunnelForwarder
import threading
import sqlalchemy as sa
import pandas as pd
#import time
#import datetime
#import matplotlib.pyplot as plt
#import numpy as np
#from scipy import signal



#SSH into server
server =  SSHTunnelForwarder(
     ('server167.web-hosting.com', 21098),
     ssh_password="energyinstituteadmin215",
     ssh_username="enerkkwg",
     remote_bind_address=('127.0.0.1', 3306))

server.start()

#SQL Engine and connection string
engine = sa.create_engine('mysql+pymysql://enerkkwg_remote:westerncooling@127.0.0.1:%s/enerkkwg_data'
                       % server.local_bind_port,echo=True)


print('Connecting...')
conn = engine.connect()
print('Getting metadata...')
#Reflect metadata
meta = sa.MetaData(engine,reflect=True)
#Get DAQ table
table = meta.tables['DAQs']

#daqnums = [1,2,3]
daqnums = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
#desired_columns = ["CO2", "RH", "T"]
desired_columns = ["CO2"]
for descol in desired_columns:
     i = 1
     for daqnum in daqnums:             
          select_statement=sa.text("SELECT `UTC Timestamp`,`" + descol + "` FROM `DAQs` WHERE (`UTC Timestamp` BETWEEN '2019-07-02 00:00:00' AND '2019-08-06 00:00:00') AND (`DAQ Name` LIKE 'A%Q" + str(daqnum) + "')")
          res = conn.execute(select_statement)
          if (i==1):
               df = pd.DataFrame(res.fetchall())
               df.columns=res.keys()
               df.rename(columns={descol:descol + "_" + str(daqnum)}, inplace=True)
               ind = pd.to_datetime(df["UTC Timestamp"], format="%Y-%m-%d %H:%M:%S")
               df.index = ind
               df.drop(["UTC Timestamp"], axis=1, inplace=True)
               i = i + 1
          else:
               df_temp = pd.DataFrame(res.fetchall())
               df_temp.columns=res.keys()
               df_temp.rename(columns={descol:descol + "_" + str(daqnum)}, inplace=True)
               ind = pd.to_datetime(df_temp["UTC Timestamp"], format="%Y-%m-%d %H:%M:%S")
               df_temp.index = ind
               df_temp.drop(["UTC Timestamp"], axis=1, inplace=True)
               df = pd.concat([df,df_temp], join="outer")
               i = i + 1
          
     dt = df.groupby(pd.TimeGrouper(freq="10min"))
     header_flag = 1
     for time, group in dt:
          new_cols = df.columns
          max_col = pd.Index(["Max_" + descol])
          new_cols = new_cols.append(max_col)
          df_row = pd.DataFrame(index=[time],columns=new_cols)
          df_row.index.name = "Timestamp"
          for col in df.columns:
               temp_df = group[col].dropna()
               temp_df.sort_index(axis=0, ascending=True,inplace=True)
               if temp_df.empty:
                    continue
               v = temp_df[0] # This takes the value closest to "time" (but is actually just a little after "time"). Will need to do something different for PIR
               df_row.loc[time,col] = v
               row_max = max(df_row.loc[time,:])
               df_row.loc[time,"Max_" + descol] = row_max
          if (header_flag==1):
               header_flag = 0
               df_row.to_csv("DataFiles\\AmbiDAQ_grouped_" + descol + ".csv", mode="a", header=True, index=True)
          else:
               df_row.to_csv("DataFiles\\AmbiDAQ_grouped_" + descol + ".csv", mode="a", header=False, index=True)
     
                    

#df.to_csv("DataFiles\\WCEC-CO2-RH-PIR_" + daqname + ".csv", header=True, index=False)
conn.close()

#Workaround for SSH threading issue. Don't delete this:
[t.close() for t in threading.enumerate() if t.__class__.__name__ == "Transport"]
server.stop()
stopgap = "thisisastopgap"
