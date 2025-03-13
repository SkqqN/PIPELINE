import hou
import sys


#Scripts
scr_folders = [
    'D:/production/WORK/_houdini_/scripts',
]

for p in scr_folders:
    sys.path.append(p)


#HDAs
hda_folders = [
    '$HH/otls/',
    'D:/production/WORK/_houdini_/hda',
]

hou.putenv('HOUDINI_OTLSCAN_PATH', ';'.join(hda_folders))
hou.hda.reloadAllFiles()
