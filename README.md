# CMS RPC Monitoring Tools

Monitoring tool for CMS RPC non-event data.

## Requirements
- Python 3.8 (or higher)
- Linux
- Tunnel or VPN to CERN network

## Setup

```console
git clone git@github.com:ftorresd/cms_rpc_monitor_tools.git`
cd cms_rpc_monitor_tools
python -m venv env
pip env/bin/activate
pip install -r requirements.txt
```

Once per session:

```console
source env/bin/activate
source oracle_env.sh
```

## Conditioning data

One should pay attention to chenge, inside the conditioning script, the starting date, ending date and the HV point.

```console
./cms_rpc_monitor_conditioning.py
./plots_conditioning.py
```
