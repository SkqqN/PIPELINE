import hou
import os
import sys
import json
from importlib import reload
from utility_scripts import main as util
reload(util)


proj_list = 'D:/production/WORK/_houdini_/config/proj_list.json'


def readJson():
    try:
        with open(proj_list, 'r') as f:
            data = json.load(f)
    except ValueError:
        data = {}

    return data


def createFolderAndVar(var, path):
    path = util.fixPath(path)
    hou.putenv(var, path)

    if not os.access(path, os.F_OK):
        os.makedirs(path)
        print('Creating ENV VARIABLE ${0} to point at folder [{1}]'.format(var, path))

    return


def unsetAllSceneVar():
    variables = [
        'SCENE',
        'SCENE_PATH',
        'INPUT_PATH',
        'SAVE_PATH',
        'OUTPUT_PATH',
        'CACHE_PATH',
        'RENDER_PATH',
        'COMP_PATH'
    ]
    for v in variables:
        hou.unsetenv(v)
    return


def projectList(kwargs):
    data = readJson()
    menu = ['-', '-']
    for k in data.keys():
        menu.append(k)
        menu.append(k)

    return menu


def sceneList(kwargs):
    menu = []
    scenes_path = hou.getenv('SCENES_PATH')
    if scenes_path and os.access(scenes_path, os.F_OK):
        for f in os.listdir(scenes_path):
            if os.path.isdir(util.fixPath(os.path.join(scenes_path, f))):
                menu.append(f)
                menu.append(f)
    return menu


def setProjectDatas(kwargs):
    node = kwargs['node']
    project_name = kwargs['script_value']
    data = readJson()

    node.parm('scene').set('')
    unsetAllSceneVar()

    if project_name == '-':
        hou.unsetenv('PROJECT')
        hou.unsetenv('CODE')
        hou.unsetenv('PROJ_FPS')
        hou.setFps(24)
        hou.unsetenv('PROJECT_PATH')
        hou.unsetenv('SCENES_PATH')
        hou.unsetenv('HDA_PATH')
        hou.unsetenv('SCRIPTS_PATH')
        node.cook(True)
        return

    try:
        project_data = data[project_name]
    except KeyError:
        util.error('Project datas not found')
        return

    #Store Datas
    project_path = project_data['PATH']
    scenes_path = os.path.join(project_path, 'SCENES')
    hda_path = os.path.join(project_path, 'HDA')
    scripts_path = os.path.join(project_path, 'SCRIPTS')

    fps = project_data['FPS']
    hou.setFps(fps)

    #Set new ENV Variables
    hou.putenv('PROJECT', project_name)
    hou.putenv('CODE', project_data['CODE'])
    hou.putenv('PROJ_FPS', str(fps))
    hou.putenv('PROJECT_PATH', project_path)
    createFolderAndVar('SCENES_PATH', scenes_path)
    createFolderAndVar('HDA_PATH', hda_path)
    createFolderAndVar('SCRIPTS_PATH', scripts_path)

    #Set HOUDINI_OTLSCAN_PATH
    hda_paths_list = [hda_path,]
    scan_path = hou.getenv('HOUDINI_OTLSCAN_PATH')
    if scan_path: #Check if it is not returning nothing
        hda_paths_list += scan_path.split(';')
    hda_paths_list = list(set(hda_paths_list)) #Kill duplicates
    hou.putenv('HOUDINI_OTLSCAN_PATH', ';'.join(hda_paths_list))
    hou.hda.reloadAllFiles()

    sys.path.append(scripts_path)

    node.cook(True)


def setSceneDatas(kwargs):
    node = kwargs['node']
    scene_name = node.evalParm('scene')

    #If null scene > unset all
    if scene_name == '':
        unsetAllSceneVar()
        node.cook(True)
        return


    #Store paths
    project_path = hou.getenv('PROJECT_PATH')
    scenes_path = hou.getenv('SCENES_PATH')

    # If no PROJECT_PATH var and dir
    if not project_path or not os.access(project_path, os.F_OK):
        util.error('Project path is invalid')
        return

    #If no SCENES_PATH var
    if not scenes_path:
        util.error('SCENES_PATH env variable not found')
        return

    #If SCENES_PATH var but no folder
    if not os.access(scenes_path, os.F_OK):
        os.makedirs(scenes_path)


    scene_path = util.fixPath(os.path.join(scenes_path, scene_name))
    #If scene folder does not exist, ask for creation
    if not os.access(scene_path, os.F_OK):
        message = ('Scene folder "{0}" does not exist.\n'
                   'Create this folder now ?'.format(scene_name))
        choice = hou.ui.displayMessage(message, severity=hou.severityType.ImportantMessage, buttons=('Yes', 'No'))
        if choice == 0:
            os.makedirs(scene_path)
        else:
            unsetAllSceneVar()
            node.cook(True)
            return

    hou.putenv('SCENE', scene_name)
    hou.putenv('SCENE_PATH', scene_path)

    createFolderAndVar('INPUT_PATH', os.path.join(scene_path, '00_INPUT'))
    createFolderAndVar('SAVE_PATH', os.path.join(scene_path, '01_WORK'))
    createFolderAndVar('OUTPUT_PATH', os.path.join(scene_path, '03_OUTPUT'))
    createFolderAndVar('CACHE_PATH', os.path.join(scene_path, '02_CACHE'))
    createFolderAndVar('RENDER_PATH', os.path.join(scene_path, '04_RENDER'))
    createFolderAndVar('COMP_PATH', os.path.join(scene_path, '05_COMP'))

    node.cook(True)


def onLoaded(kwargs):
    node = kwargs['node']
    scene = node.evalParm('scene')

    node.parm('proj').pressButton()
    if not scene == '':
        node.parm('scene').set(scene)
        if scene in sceneList({}):
            node.parm('scene').pressButton()


def onCreated(kwargs):
    node = kwargs['node']

    node.setName('SCENE_DATA', unique_name=True)

    node.setUserData('nodeshape', 'circle')
    node.setColor(hou.Color(0.58, 0.2, 0.48))
    node.setGenericFlag(hou.nodeFlag.Display, False)
    node.setGenericFlag(hou.nodeFlag.Selectable, False)

    if hou.getenv('PROJECT') and hou.getenv('SCENE'):
        node.parm('proj').set(hou.getenv('PROJECT'))
        node.parm('scene').set(hou.getenv('SCENE'))

    print('SCENE_DATA successfully created !')