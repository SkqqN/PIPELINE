import hou
import re
import os
from importlib import reload
from utility_scripts import main as util
reload(util)


def cleanName(name):
    new_name = name.upper().strip()
    regex = r'[^a-zA-Z0-9]+'
    new_name = re.sub(regex, '-', new_name)
    if new_name.startswith('-'):
        new_name = new_name.removeprefix('-')
    if new_name.endswith('-'):
        new_name = new_name.removesuffix('-')
    return new_name


def saveScene(kwargs=None, task=None, desc=None):
    if kwargs:
        ctrl = kwargs['ctrlclick']
    else:
        ctrl = False


    # Find scene_data node
    scene_data = None
    scene_data_nodes = []
    for n in hou.node('/obj').children():
        if n.type().nameComponents()[2] == 'scene_data':
            scene_data_nodes.append(n)
    if len(scene_data_nodes) > 1:
        util.error('Multiple SCENE_DATA nodes found.\nAborting operation.')
        return
    elif len(scene_data_nodes) == 1:
        scene_data = scene_data_nodes[0]
    else:
        util.error('SCENE_DATA node not found.\nPlease create one and select a scene before saving.')
        return


    #Gather variables
    save_path = hou.getenv('SAVE_PATH')
    scene = hou.getenv('SCENE')

    if not save_path or not scene:
        util.error('Local variables not defined.\nPlease use SCENE_DATA node to set these correctly')
        return


    #Set task and description from current scene or initialize
    curr_name = hou.hipFile.basename()
    regex = (r'^(?P<scene>[a-zA-Z0-9-]+)_(?P<task>[a-zA-Z0-9-]+)_(?P<full_ver>V(?P<ver>\d{3,}))'
             r'(_(?P<desc>[a-zA-Z0-9-]+))?_(?P<user>[a-zA-Z0-9-]+)(?P<full_ext>\.(?P<ext>[a-zA-Z]+))$')

    match = re.match(regex, curr_name, flags=re.IGNORECASE)
    if match:
        if not task:
            task = match.group('task')
        if not desc:
            desc = match.group('desc')

    if not task:
        task = ''
    if not desc:
        desc = ''

    ask_input = True
    if ctrl and task != '':
        ask_input = False


    # Input Task and Description
    if ask_input:
        repeat = True
        while repeat:
            repeat = False
            message = ('Scene : {scene}\n'
                       'Path : {path}/\n\n'
                       'Enter scene description :').format(scene=scene, path=save_path)

            user_input = hou.ui.readMultiInput(message, ('Task', 'Description (optional)'),
                                               buttons=('Save', 'Cancel'),
                                               close_choice=1,
                                               title='Save Scene',
                                               initial_contents=(task, desc))

            if user_input[0] == 1:
                return

            task = user_input[1][0]
            desc = user_input[1][1]

            if task == '':
                repeat = True
                util.error('Task cannot be left blank', hou.severityType.Warning)
                continue


    #Set Version
    regex = '(?P<scene>{scene})_(?P<task>{task})_V(?P<version>\\d{{3,}})'.format(scene=scene, task=task)
    versions = []
    for f in os.listdir(save_path):
        if not os.path.isdir(f):
            match = re.match(regex, f, flags=re.IGNORECASE)
            if match:
                versions.append(int(match.group('version')))

    if len(versions) > 0:
        _ver = sorted(versions)[-1]
        ver = 'V{0:>03}'.format(_ver+1)
    else:
        ver = 'V001'


    #Set User
    user = hou.getenv('USER').upper()

    components = [scene, task, ver, desc, user]
    for i, c in enumerate(components):
        if c and c != '':
            components[i] = cleanName(c)
        else:
            del components[i]


    #Set extension
    lic_dict = {
        'Commercial' : 'hip',
        'Indie' : 'hiplc',
        'Apprentice' : 'hipnc',
        'ApprenticeHD' : 'hipnc',
        'Education' : 'hipnc'
    }
    lic = hou.licenseCategory().name()
    ext = lic_dict[lic]


    #File name
    name = '_'.join(components)
    filename = '{path}/{name}.{ext}'.format(path=save_path, name=name, ext=ext)


    #Save
    hou.hipFile.save(filename)
