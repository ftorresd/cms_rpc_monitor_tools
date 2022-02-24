#!/usr/bin/env python

import os
import csv
from tqdm import tqdm
import pprint
pp = pprint.PrettyPrinter(indent=4)

import cx_Oracle


cx_Oracle.init_oracle_client(lib_dir=f"{os.getcwd()}/lib/instantclient_19_8")

connection_str = """(
    DESCRIPTION=
    (ADDRESS= (PROTOCOL=TCP) (HOST=cmsonr3-s.cern.ch) (PORT=10121) )
    (ADDRESS= (PROTOCOL=TCP) (HOST=cmsonr4-s.cern.ch) (PORT=10121) )
    (ADDRESS= (PROTOCOL=TCP) (HOST=cmsonr2-s.cern.ch) (PORT=10121) )
    (ADDRESS= (PROTOCOL=TCP) (HOST=cmsonr1-s.cern.ch) (PORT=10121) )
    (LOAD_BALANCE=on)
    (ENABLE=BROKEN)
    (CONNECT_DATA=
        (SERVER=DEDICATED)
        (SERVICE_NAME=cms_omds_lb.cern.ch)
    )
)"""

# connection = cx_Oracle.connect(
# user="CMS_RPC_CONF", password="RPCConf_Own21", dsn=connection_str
# )
connection = cx_Oracle.connect(
    user="CMS_RPC_R", password="rpcr34d3R", dsn=connection_str
)

cursor = connection.cursor()


def query_by_dpid(cursor, dpid):
    cursor.execute(
        f"""
            SELECT CHANGE_DATE, ACTUAL_VMON 
            FROM CMS_RPC_PVSS_COND.FWCAENCHANNEL 
            WHERE dpid = {dpid} 
            AND ACTUAL_VMON IS NOT NULL 
            ORDER BY CHANGE_DATE DESC
            OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY
            """
    )
    return next(cursor)


channels = {}
with open("data/RPC_Chamber_HV_Map.csv") as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for dpid, channel in csvreader:
        channels[channel]=int(dpid)



if __name__ == "__main__":
    vmons = {}
    low_vmon = []
    for channel in tqdm(channels):
        _, vmons[channel] = query_by_dpid(cursor, channels[channel])
        if vmons[channel] < 100:
            low_vmon.append(channel)

    print("All VMONs:")
    pp.pprint(vmons)
    print("\n\n")
    


    print("Channels with VMON < 100:")
    pp.pprint(low_vmon)

