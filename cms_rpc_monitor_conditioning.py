#!/usr/bin/env python3

import os
import csv
from tqdm import tqdm
import csv

import cx_Oracle

channels = {}
with open("data/RPC_Chamber_HV_Map.csv") as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for dpid, channel in csvreader:
        channels[channel] = int(dpid)


def get_channel_meta(channel):
    region = "barrel"
    wheel_disk = channel[1:3].replace("_", "")
    if channel.startswith("R"):
        region = "endcap"
        wheel_disk = channel[2:4]
    return channel, region, wheel_disk


cx_Oracle.init_oracle_client(lib_dir=f"{os.getcwd()}/lib/instantclient_21_5")

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


def average(currents_list, last_imon):
    if len(currents_list) == 0:
        print("--> WARNING: List is empty. Checking last IMON.")
        if last_imon < 0:
            return 0
        else:
            return last_imon
    return sum(currents_list) / len(currents_list)


def process_currents_by_dpid(channel, dpid, HV_point, epsilon=70):
    dpid = 376
    cursor.execute(
        f"""SELECT CHANGE_DATE, ACTUAL_VMON, ACTUAL_IMON, ACTUAL_STATUS FROM CMS_RPC_PVSS_COND.FWCAENCHANNEL
            WHERE DPID = {dpid}
            AND CHANGE_DATE BETWEEN TO_DATE('2022/02/01 20:35:00', 'YYYY/MM/DD HH24:MI:SS') AND TO_DATE('2022/02/17 20:37:00', 'YYYY/MM/DD HH24:MI:SS')
         """
    )

    last_imon = -99
    is_stable = False
    is_good_HV = False
    currents = []
    for (
        CHANGE_DATE,
        ACTUAL_VMON,
        ACTUAL_IMON,
        ACTUAL_STATUS,
    ) in cursor:
        if ACTUAL_IMON != None:
            last_imon = ACTUAL_IMON
        vmon = ACTUAL_VMON
        if ACTUAL_VMON == None:
            vmon = 0

        if (HV_point - epsilon < vmon < HV_point + epsilon) and is_stable == False:
            is_good_HV = True
            continue

        if is_good_HV and ACTUAL_STATUS == 1:
            is_stable = True
            continue

        if is_good_HV and is_stable:
            currents.append(ACTUAL_IMON)

        if is_good_HV and is_stable and ACTUAL_STATUS == 3:
            is_stable = False
            is_good_HV = False
            break

    currents = [c for c in currents[:-3] if c != None]

    result = *get_channel_meta(channel), dpid, average(currents, last_imon)
    print(result)
    return result


def main():
    results = []
    for channel in tqdm([*channels]):
        results.append(process_currents_by_dpid(channel, channels[channel], 8000))

    with open("outputs.csv", "w") as out:
        csv_out = csv.writer(out)
        csv_out.writerow(
            ["chamber", "region", "wheel_disk", "dipid", "average_current"]
        )
        for row in results:
            csv_out.writerow(row)


if __name__ == "__main__":
    main()
