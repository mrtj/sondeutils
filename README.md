# Sonde utils

This repo contains utilty scripts for High Altitude Radiosonde tracker sites. Currently
http://tracker.om3bc.com is supported. 

## Installation

Python 2.x or 3.x is required. Install the required python libraries with

    pip install -r requirements.txt

## Usage

The `balloon.py` script downloads the tracking data from the tracker site and saves it in the following formats: `csv`, `json`, `kml`.

    python balloon.py [hwid]

where hwid is the hardware identifier of the sonda. You can find supported hwids by visiting http://tracker.om3bc.com.
