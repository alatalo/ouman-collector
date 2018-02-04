# Ouman EH203 data collector

Uses taloLogger to interface with Ouman EH203 over serial cable, storing measurements in InfluxDB.

I'm using a custom device descriptor for storing only the relevant measurements for my usage -- see "Install custom datatype to taloLogger" below.


## What's needed

 * Ouman EH203 connected via serial cable to (a device such as Raspberry Pi)
 * InfluxDB
 * Grafana


### SW requirements

 * taloLogger https://olammi.iki.fi/sw/taloLogger/ (tested with v1.7j)
 * Python 2.7.x


## Download and extract taloLogger

[Download taloLogger](https://olammi.iki.fi/sw/taloLogger/download.php) and extract the contents to `taloLogger/` directory.


## Setup virtualenv for running the project

On a Raspberry Pi running a fresh Raspbian:

```sh
sudo apt-get install python-pip
pip install virtualenv
python -m virtualenv ve
source ve/bin/activate
pip install -r requirements.txt
```


## Install custom datatype to taloLogger

I'm using a custom device descriptor for storing only the relevant measurements for my usage. You can use one of the datatypes taloLogger provides (see the same file as below for reference).

Overwrite OUMAN_DEVICES in `taloLogger/modules/datasources/ouman/oumanSerial.py` with the following:

```python
OUMAN_DEVICES = {
    'EH203custom': [
        ['Ulkolampotila', 18, TYPE_TEMP100, TYPE_READ, 0], \
        ['L1 menovesi', 20, TYPE_TEMP100, TYPE_READ, 0], \
        ['L1 paluuvesi', 23, TYPE_TEMP100, TYPE_READ, 0], \
        ['LV menovesi', 24, TYPE_TEMP100, TYPE_READ, 0], \
        ['LV kiertovesi', 25, TYPE_TEMP100, TYPE_READ, 0], \
        ['LV-venttiili', 51, TYPE_UINT8, TYPE_READ, 0]
    ]
}
```


## Configure InfluxDB connection

Configure InfluxDB connection details in `ouman-collector.py`.


## Run

Run the collector with:

```
python ouman-collector.py /dev/ttyS0 EH203custom
```

Crontab example, replace PIUSER with your username/path.

```
*/2 * * * * (cd /home/PIUSER/ouman-collector/; ./ve/bin/python ouman-collector.py /dev/ttyS0 EH203custom) >> /home/PIUSER/ouman-collector.log 2>&1
```
