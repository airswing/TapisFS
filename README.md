# TapisFS
Maps Tapis files to a read-only FUSE filesystem

## Requirements
Note: Best to run in a virtual environment

`$ pip3 install agavepy fusepy` or `$ pip3 install -r requirements.txt`

## Usage
```
usage: tapisfs.py [-h] [-c CUSTOM_CONFIG] CLIENT STORAGE PATH MOUNTPOINT

positional arguments:
  CLIENT                use a client name from config.json
  STORAGE               Tapis file storage system to mount
  PATH                  path to mount within storage system
  MOUNTPOINT            path to mount filesystem

optional arguments:
  -h, --help            show this help message and exit
  -c CUSTOM_CONFIG, --custom-config CUSTOM_CONFIG
                        optional path to custom Tapis config.json
```

## Example
### Prerequisites 
- Download and run the [Tapis CLI](https://github.com/TACC-Cloud/tapis-cli-ng)
- Follow the [instructions to initialize a Tapis client](https://github.com/TACC-Cloud/tapis-cli-ng#initializing-a-tapis-client) on DesignSafe for this example
- Verify your tokens work by running: 

`tapis files list https://agave.designsafe-ci.org/files/v2/media/system/designsafe.storage.published//PRJ-2528/`
- You should get this back:
```
+--------------------------+---------------------------+-----------+
| name                     | lastModified              |    length |
+--------------------------+---------------------------+-----------+
| Wright_Powerpoint.pptx   | 2019-08-28 16:21:41-05:00 | 102330982 |
| Wright_Reaserchpaper.pdf | 2019-08-28 16:21:41-05:00 |    993994 |
| Wrigth_poster.pptx       | 2019-08-28 16:21:41-05:00 |  33740223 |
+--------------------------+---------------------------+-----------+
```
- Tapis CLI creates a `config.json` in the `~/.agave` directory by default
    - Note: You can set a custom config path by adding the `-c /custom/path/to/config.json` parameter or by specifying it in `tapisfs.json`
- Get the following ready:
    - `client_name`: Get the name from the client you just created in `config.json`
    - `storage_system`: In this example it's `designsafe.storage.published`
    - `path`: In this example it's `/PRJ-2528`
    - `mount_point`: Choose a directory path to mount to eg: `/home/username/ds_local`

### Run TapisFS
```
$ python3 tapisfs.py ds_client designsafe.storage.published /PRJ-2528 /home/username/ds_local
TapisFS running @ /home/username/ds_local ...
```