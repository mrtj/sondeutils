import argparse
import json
import csv

import requests
import simplekml

TRACKER_URL = 'http://tracker.om3bc.com/tracker_json.php'

def main():
    '''Configures and parses command line arguments.'''
    parser = argparse.ArgumentParser(description='Converts balloon tracker logs from '\
                                    'http://tracker.om3bc.com/')
    parser.add_argument('hwid', type=str,
                        help='The harware id of the tracked device')
    parser.add_argument('-f', dest='from_file', action='store_const', const=True,
                        help='If specified, the data will be read from [hwid].json '\
                        'instead of downloading from the tracker site')
    args = parser.parse_args()
    if args.from_file:
        data = load_from_file(args.hwid)
    else:
        data = load_from_site(args.hwid)

    process_data(args.hwid, data)

def load_from_file(hwid):
    ''' Loads the json data from the specified file'''
    with open(hwid + '.json') as data_file:
        data = json.load(data_file)
    return data

def load_from_site(hwid):
    ''' Loads the tracking data from the tracker site'''
    payload = {'hw': hwid, 'last': '1500'}
    print('POST {}, payload: {}'.format(TRACKER_URL, payload))
    result = requests.post(TRACKER_URL, data=payload)
    return result.json()

def save_to_csv(hwid, data):
    ''' Saves the data to csv '''
    fieldnames = ['ID', 'DATETIME', 'HW', 'TYPE', 'LAT', 'LON', 'ALT',
                  'SPEED', 'VSPEED', 'FREQ', 'UPLOADER']
    filename = hwid + '.csv'
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(data)
    print('Written {}'.format(filename))

def save_to_json(hwid, data):
    ''' Saves data to json '''
    filename = hwid + '.json'
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print('Written {}'.format(filename))

def save_to_kml(hwid, data):
    kml = simplekml.Kml()
    for entry in data:
        try:
            name = entry['ID']
            coords = (entry['LON'], entry['LAT'], entry['ALT'])
            author = entry['UPLOADER']
            description = 'datetime: {}, speed: {}, vspeed: {}' \
                .format(entry['DATETIME'], entry['SPEED'], entry['VSPEED'])
        except KeyError as exception:
            print('WARNING: expected key not found for entry.')
            print(repr(exception))
            continue
        point = kml.newpoint(name=name)
        point.coords = [coords]
        point.altitudemode = simplekml.AltitudeMode.absolute
        point.atomauthor = author
        point.description = description
    filename = hwid + '.kml'
    kml.save(filename)
    print('Written {}'.format(filename))

def process_data(hwid, data):
    save_to_json(hwid, data)
    save_to_csv(hwid, data)
    save_to_kml(hwid, data)

if __name__ == "__main__":
    main()
