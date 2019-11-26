import argparse
import json
import os
from fuse import FUSE
from tapisfuse import TapisFuse


def get_file(path):
    try:
        with open(os.path.expanduser(path), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print('No config found in %s' % path)
    except Exception as e:
        print('Undefined exception: %s' % e)


def get_client(config, client_name):
    for code in config['sessions']:
        for user in config['sessions'][code]:
            for auth_name in config['sessions'][code][user]:
                single_auth = config['sessions'][code][user][auth_name]
                if single_auth['client_name'] == client_name:
                    return single_auth


parser = argparse.ArgumentParser()
parser.add_argument('client_name', metavar='CLIENT', type=str, help='use a client name from config.json')
parser.add_argument('storage_system', metavar='STORAGE', type=str, help='Tapis file storage system to mount')
parser.add_argument('path', metavar='PATH', type=str, help='path to mount within storage system')
parser.add_argument('mount_point', metavar="MOUNTPOINT", type=str, help='path to mount filesystem')
parser.add_argument('-c', '--custom-config', help='optional path to custom Tapis config.json')
args = parser.parse_args()

if args.custom_config:
    config_dict = get_file(args.custom_config)
else:
    path = get_file('tapisfs.json')['tapis_config_path']
    config_dict = get_file(path)

auth = get_client(config_dict, args.client_name)
try:
    os.mkdir(args.mount_point)
except FileExistsError:
    pass
print('TapisFS running @ %s ...' % args.mount_point)
FUSE(TapisFuse(auth['baseurl'], args.storage_system, auth['access_token'], args.path), args.mount_point, nothreads=True, foreground=True)