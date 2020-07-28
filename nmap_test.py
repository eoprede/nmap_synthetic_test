import subprocess
import re
import statistics
import spectrum_config
from send_to_influxdb import send_data_to_influxDB
import json
import datetime


def figure_out_num(num):
    try:
        return float(num[1:-3])
    except:
        return None


with open("test_hosts.json") as f:
    test_hosts = json.load(f)

measurement = "network.synthetic.tests"
tag_attributes = ["hostname"]
field_attributes = ["latency", "jitter"]

for h in test_hosts:
    process = subprocess.Popen(
        ["nping", h["ip"], "-c", "10"] + h.get("args", []),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()

    sent_time = 0
    rtt = []
    for line in stdout.splitlines():
        if line.decode().startswith("SENT"):
            time_search = re.search(".*?(\(.*s\)).*", line.decode())
            if figure_out_num(time_search.group(1)):
                sent_time = figure_out_num(time_search.group(1))
        elif line.decode().startswith("RCVD"):
            time_search = re.search(".*?(\(.*s\)).*", line.decode())
            if figure_out_num(time_search.group(1)):
                rtt.append((figure_out_num(time_search.group(1)) - sent_time) * 1000)

    if rtt:
        sample_diff = []
        i = 0
        while i < len(rtt) - 1:
            sample_diff.append(abs(rtt[i] - rtt[i + 1]))
            i += 1

        jitter = sum(sample_diff) / len(sample_diff)
        print("Host " + h["name"])
        print("Average latency is {}ms".format(statistics.mean(rtt)))
        print("Jitter value is {}ms".format(jitter))

        data = {
            "hostname": h["name"],
            "latency": statistics.mean(rtt),
            "jitter": jitter,
            "time": datetime.datetime.utcnow(),
        }

        send_data_to_influxDB(
            spectrum_config.GRAFANA_HOST,
            spectrum_config.GRAFANA_PORT,
            spectrum_config.GRAFANA_UN,
            spectrum_config.GRAFANA_PW,
            spectrum_config.GRAFANA_DB,
            data,
            measurement,
            field_attributes,
            tag_attributes,
        )
    else:
        print("Could not test host " + h["name"])
