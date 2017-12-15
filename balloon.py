import argparse
import json

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
        data = load_from_file(args.hwid)

    process_data(data)

def load_from_file(hwid):
    ''' Loads the json data from the specified file.'''
    filename = hwid + '.json'
    with open(filename) as data_file:
        data = json.load(data_file)
    return data

def load_from_site(hwid):

    return True

def process_data(data):
    pass

if __name__ == "__main__":
    main()
