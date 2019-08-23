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

daqnums = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
for daqnum in daqnums:
     daqname = 'Ambi-DAQ' + str(daqnum)
     #Change this to get the data you want
     print('Creating statement...')
     select_statement = sa.select([table]).where( sa.and_(table.c['DAQ Name'] == daqname, table.c['UTC Timestamp'] <= '2019-08-06 00:00:00' )).order_by(sa.asc(table.c['UTC Timestamp']))
     print('Executing statement...')
     res = conn.execute(select_statement)
     print('Capturing result in .csv format...')

     #Put the result into a dataframe
     df = pd.DataFrame(res.fetchall())
     df.columns=res.keys()
     df = pd.DataFrame(df[["UTC Timestamp","CO2","PIR","RH"]])
     df.to_csv("DataFiles\\WCEC-CO2-RH-PIR_" + daqname + ".csv", header=True, index=False)

conn.close()

#Workaround for SSH threading issue. Don't delete this:
[t.close() for t in threading.enumerate() if t.__class__.__name__ == "Transport"]
server.stop()
