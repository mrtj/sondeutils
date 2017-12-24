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
    with open(filename, 'w') as csv_file:
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

def configure_kml_point(point, entry):
    try:
        name = entry['ID']
        coords = (entry['LON'], entry['LAT'], entry['ALT'])
        author = entry['UPLOADER']
        description = 'id: {ID}\nlatitude: {LAT},\nlongitude: {LON},\naltitude: {ALT},\n'\
            'datetime: {DATETIME}\nspeed: {SPEED}\nvspeed: {VSPEED}\nuploader: {UPLOADER}'\
            .format(**entry)
        point.name = name
        point.coords = [coords]
        point.altitudemode = simplekml.AltitudeMode.absolute
        point.atomauthor = author
        point.description = description
    except KeyError as exception:
        print('WARNING: expected key not found for entry.')
        print(repr(exception))

def save_to_kml(hwid, data):
    kml = simplekml.Kml()
    chunk_length = 100
    chunks = [data[i:i+chunk_length] for i in range(0, len(data), chunk_length)]
    linestyle = simplekml.LineStyle(width=2.0, color=simplekml.Color.lightblue)
    for chunk in chunks:
        try:
            point = kml.newpoint()
            configure_kml_point(point, chunk[0])
            line = kml.newlinestring()
            line.coords = [(entry['LON'], entry['LAT'], entry['ALT']) for entry in chunk]
            line.altitudemode = simplekml.AltitudeMode.absolute
            line.atomauthor = chunk[0]['UPLOADER']
            line.linestyle = linestyle
        except KeyError as exception:
            print('WARNING: expected key not found for entry.')
            print(repr(exception))
            continue
    endpoint = kml.newpoint()
    configure_kml_point(endpoint, data[-1])
    filename = hwid + '.kml'
    kml.save(filename)
    print('Written {}'.format(filename))

def process_data(hwid, data):
    if len(data) == 0:
        print('No entries found.')
        return
    save_to_json(hwid, data)
    save_to_csv(hwid, data)
    save_to_kml(hwid, data)

if __name__ == "__main__":
    main()
