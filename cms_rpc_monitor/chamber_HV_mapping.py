import csv

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
