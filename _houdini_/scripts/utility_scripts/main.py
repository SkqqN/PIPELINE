import hou
import re


def fixPath(old_path, new_sep='/'):
    regex = r'[/\\]+'
    _path = re.sub(regex, new_sep, old_path)

    if _path.endswith('/'):
        _path = _path[:-1]

    _path = _path.replace('/', new_sep)
    new_path = _path
    return new_path


def error(message='', severity=hou.severityType.Error):
    print('{severity}: {message}'.format(severity=severity.name(), message=message))
    hou.ui.displayMessage(message, severity=severity)


def printReport(header, *body):
    print('\n{header:=^50}'.format(header=header))
    for b in body:
        print('\t{0}'.format(b))
    print('='*50)
