#!env python
# -*- coding: utf-8 -*-

import sys
import os.path

# add taloLogger directory to module path
sys.path = [os.path.abspath('taloLogger')] + sys.path

from modules.core import configuration
from modules.core import log
from modules.datasources.ouman import oumanSerial

from influxdb import InfluxDBClient

# influxdb connection configuration
INFLUX = {
    "host": "YOUR-RASPBERRY-IP",
    "port": 8086,
    "username": "admin",
    "password": "password",
    "database": "ouman"
}

def main():
    conf = configuration.Configuration()
    conf.addConfigurable(log.Logger)
    conf.setValue('CONSOLE_LOGGING', 'true')
    LOG = log.Logger(conf)
    log.Logging.setLogger(LOG)

    serial_port = sys.argv[1]
    ouman_device = sys.argv[2]
    oser = oumanSerial.OumanSerial(serial_port, ouman_device)

    influx = InfluxDBClient(INFLUX.get("host"), INFLUX.get("port"),
                            INFLUX.get("username"), INFLUX.get("password"),
                            INFLUX.get("database"))
    influx.create_database(INFLUX.get("database"))

    measurements = []
    l1menovesi = False
    l1paluuvesi = False
    for key in oumanSerial.OUMAN_DEVICES[ouman_device]:
        data = oser.runQueryCommand(key[0])
        if len(data) > 0:
            print key[0] + ': ' + data

            try:
                data = int(data)
            except ValueError:
                try:
                    data = float(data)
                except ValueError:
                    pass

            if key[0] == "L1 menovesi":
                l1menovesi = data
            elif key[0] == "L1 paluuvesi":
                l1paluuvesi = data
            measurements.append(
                {
                    "measurement": key[0],
                    "tags": {
                        "device": ouman_device
                    },
                    "fields": {
                        "value": data
                    }
                })
        else:
            print key[0] + ': ERROR'

        if l1menovesi and l1paluuvesi:
            erotus = float(l1menovesi) - float(l1paluuvesi)
            measurements.append(
                {
                    "measurement": "L1 erotus",
                    "tags": {
                        "device": ouman_device
                    },
                    "fields": {
                        "value": erotus
                    }
                })
    influx.write_points(measurements)

if __name__ == "__main__":
    main()
