from sshtunnel import SSHTunnelForwarder
import threading
import sqlalchemy as sa
import pandas as pd

#SSH into server
server =  SSHTunnelForwarder(
     ('server167.web-hosting.com', 21098),
     ssh_password="energyinstituteadmin215",
     ssh_username="enerkkwg",
     remote_bind_address=('127.0.0.1', 3306))

server.start()

#SQL Engine and connection string
engine = sa.create_engine('mysql+pymysql://enerkkwg_remote:westerncooling@127.0.0.1:%s/enerkkwg_data'% server.local_bind_port,echo=True)


print('Connecting...')
conn = engine.connect()
print('Getting metadata...')
#Reflect metadata
meta = sa.MetaData(engine,reflect=True)
#Get DAQ table
table = meta.tables['DAQs']

substitution_count = 0
item_count = 0

#daqnums = [1,2,3]
daqnums = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
desired_columns = ["PIR"] # Options are: "CO2", "RH", "T", "PIR"
for descol in desired_columns:
     i = 1
     # Getdata from MySQL server for all AmbiDAQ units
     for daqnum in daqnums:
          # Note that UTC Timestamp is time-shifted 3 hours ahead, so must subract 3 hours from final result to get into CA time
          select_statement=sa.text("SELECT `UTC Timestamp`,`" + descol + "` FROM `DAQs` WHERE (`UTC Timestamp` BETWEEN '2019-07-16 03:00:00' AND '2019-07-18 03:00:00') AND (`DAQ Name` LIKE 'A%Q" + str(daqnum) + "')")
          res = conn.execute(select_statement)
          if (i==1):
               df = pd.DataFrame(res.fetchall())
               df.columns=res.keys()
               df.rename(columns={descol:descol + "_" + str(daqnum)}, inplace=True)
               ind = pd.to_datetime(df["UTC Timestamp"], format="%Y-%m-%d %H:%M:%S")
               ind = ind - pd.Timedelta("3 hours")
               df.index = ind
               df.drop(["UTC Timestamp"], axis=1, inplace=True)
               i = i + 1
          else:
               df_temp = pd.DataFrame(res.fetchall())
               df_temp.columns=res.keys()
               df_temp.rename(columns={descol:descol + "_" + str(daqnum)}, inplace=True)
               ind = pd.to_datetime(df_temp["UTC Timestamp"], format="%Y-%m-%d %H:%M:%S")
               ind = ind - pd.Timedelta("3 hours")
               df_temp.index = ind
               df_temp.drop(["UTC Timestamp"], axis=1, inplace=True)
               df = pd.concat([df,df_temp], join="outer")
               i = i + 1
     # Group data according to desired timestamp resolution    
     dt = df.groupby(pd.TimeGrouper(freq="5min"))
     header_flag = 1
     prev_df = pd.DataFrame()     # Capture previous row of data to handle missing values
     for time, group in dt: # foreach 5 minute segment
          #Setting up the row
          new_cols = df.columns
          max_col = pd.Index(["Max_" + descol])
          avg_col = pd.Index(["Avg_" + descol])
          new_cols = new_cols.append(max_col)
          new_cols = new_cols.append(avg_col)
          df_row = pd.DataFrame(index=[time],columns=new_cols)
          df_row.index.name = "Timestamp"
          for col in df.columns:
               item_count = item_count + 1
               temp_df = group[col].dropna()
               temp_df.sort_index(axis=0, ascending=True,inplace=True)
               if temp_df.empty:
                    if prev_df.empty:
                         continue
                    else:
                         sustitution_count = substitution_count + 1
                         p = prev_df[col]
                         df_row.loc[time,col] = p[0]
                         t = df_row.loc[time,col]
               else:
                    v = temp_df[0] # This takes the value closest to "time" (but is actually just a little after "time"). Will need to do something different for PIR
                    df_row.loc[time,col] = v
                    row_max = max(df_row.loc[time,:])
                    row_avg = df_row.mean(axis=1)[0]
                    df_row.loc[time,"Max_" + descol] = row_max
                    df_row.loc[time,"Avg_" + descol] = row_avg
          prev_df = df_row
          if (header_flag==1):
               header_flag = 0
               df_row.to_csv("DataFiles\\AmbiDAQ_grouped_" + descol + ".csv", header=True, index=True)
          else:
               df_row.to_csv("DataFiles\\AmbiDAQ_grouped_" + descol + ".csv", mode="a", header=False, index=True)
conn.close()

#Workaround for SSH threading issue. Don't delete this:
[t.close() for t in threading.enumerate() if t.__class__.__name__ == "Transport"]
server.stop()

substitution_count = substitution_count
item_count = item_count


stopgap = "thisisastopgap"
