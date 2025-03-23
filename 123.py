import hou
import os
import sys
import re
import json

#CHANGE THIS TO YOUT WORKING DIRECTORY
path = 'C:/YOUR_WORKING_DIRECTORY/'


regex = r'[/\\]+'
path = re.sub(regex, '/', path)

if path.endswith('/'):
    path = path[:-1]

if not os.path.exists(path):
    os.makedirs(path)

if hou.getenv('PIPELINE_PATH'):
    hou.unsetenv('PIPELINE_PATH')
hou.putenv('PIPELINE_PATH', path)



#Config
config_path = '/'.join((path, r'_houdini_/config'))
if not os.path.exists(config_path):
    os.makedirs(config_path)

json_file = '/'.join((config_path, 'proj_list.json'))
if not os.path.isfile(json_file):
    data = {}
    with open(json_file, 'x') as file:
        json.dump(data, file)



#Scripts
scr_folders = [
    '/'.join((path, r'_houdini_/scripts')),
]

for p in scr_folders:
    if not os.path.exists(p):
        os.makedirs(p)
    sys.path.append(p)


#HDAs
hda_path = ['$HH/otls/', ]

hda_path_add = [
    '/'.join((path, r'_houdini_/hda')),
]

for h in hda_path_add:
    if not os.path.exists(h):
        os.makedirs(h)
    hda_path.append(h)


if hou.getenv('HOUDINI_OTLSCAN_PATH'):
    hou.unsetenv('HOUDINI_OTLSCAN_PATH')
hou.putenv('HOUDINI_OTLSCAN_PATH', ';'.join(hda_path))

hou.hda.reloadAllFiles()
