#!/usr/bin/env python

import os
import csv
from tqdm import tqdm
import pprint
import datetime

pp = pprint.PrettyPrinter(indent=4)


# from prompt_toolkit import PromptSession
# from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
# from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit import prompt

# from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import FuzzyWordCompleter

import matplotlib.dates as mdates
import matplotlib.pyplot as plt


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


def query_by_dpid(cursor, dpid):
    initial_date = datetime.datetime(2022, 1, 1).isoformat().replace("T", " ")
    end_date = datetime.datetime(2023, 5, 28).isoformat().replace("T", " ")

    cursor.execute(
        f"""
      SELECT CHANGE_DATE, ACTUAL_VMON, ACTUAL_IMON, ACTUAL_STATUS 
      FROM CMS_RPC_PVSS_COND.FWCAENCHANNEL 
      WHERE dpid = {dpid}       
      AND CHANGE_DATE BETWEEN TO_DATE('{initial_date} 'YYYY/MM/DD HH24:MI:SS') AND TO_DATE('{end_date} 'YYYY/MM/DD HH24:MI:SS')
      """
    )
    return cursor


def clear_list(list_to_clear, dates_list):
    new_list = []
    new_dates = []
    for item, date in zip(list_to_clear, dates_list):
        if iten != None:
            new_list.append(item)
            new_dates.append(date)
    ## TODO:  append to the front and to the back!!
    return new_list, new_dates


def plot_results(CHANGE_DATES, ACTUAL_VMONS, ACTUAL_IMONS, ACTUAL_STATUSES):
    x_values = CHANGE_DATES
    y_values = ACTUAL_IMONS

    ax = plt.gca()

    # formatter = mdates.DateFormatter("%d/%m/%y %H:%M:%S")
    # ax.xaxis.set_major_formatter(formatter)

    # locator = mdates.DayLocator()
    # ax.xaxis.set_major_locator(locator)

    dates = mdates.date2num(x_values)

    # plt.plot(x_values, y_values, fmt='')
    plt.plot_date(dates, y_values, fmt="b", drawstyle="steps")
    plt.show()


def main():
    # Create some history.
    # channels_history = InMemoryHistory()
    channels_for_completer = []
    channels = {}
    with open("data/RPC_Chamber_HV_Map.csv") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for dpid, channel in csvreader:
            # channels[channel.replace('+ 'p').replace('- 'm')] = int(dpid)
            # channels_for_completer.append(channel.replace('+ 'p').replace('- 'm'))
            channels[channel] = int(dpid)
            channels_for_completer.append(channel)

    # get HV Channel
    print("What HV channel to query?")

    selected_hv_channel = prompt(
        "HV channel:",
        completer=FuzzyWordCompleter(channels_for_completer, WORD=True),
        complete_while_typing=True,
    )

    # connection = cx_Oracle.connect(
    # user="CMS_RPC_CONF", password="RPCConf_Own21", dsn=connection_str
    # )
    connection = cx_Oracle.connect(
        user="CMS_RPC_R", password="rpcr34d3R", dsn=connection_str
    )

    cursor = connection.cursor()

    results = query_by_dpid(cursor, channels[selected_hv_channel])

    CHANGE_DATES = []
    ACTUAL_VMONS = []
    ACTUAL_IMONS = []
    ACTUAL_STATUSES = []

    # Loop over the results
    for CHANGE_DATE, ACTUAL_VMON, ACTUAL_IMON, ACTUAL_STATUS in results:
        CHANGE_DATES.append(CHANGE_DATE)
        ACTUAL_VMONS.append(ACTUAL_VMON)
        ACTUAL_IMONS.append(ACTUAL_IMON)
        ACTUAL_STATUSES.append(ACTUAL_STATUS)

    # print(CHANGE_DATES)
    # print(ACTUAL_IMONS)


if __name__ == "__main__":
    main()
