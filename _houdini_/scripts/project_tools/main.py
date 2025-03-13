import hou
import os
import json
from importlib import reload
from utility_scripts import main as util
reload(util)


#Global variables
proj_list = 'D:/production/WORK/_houdini_/config/proj_list.json'


def readJson():
    try:
        with open(proj_list, 'r') as f:
            data = json.load(f)
    except ValueError:
        data = {}
    return data


def manageProjects():
    sel = hou.ui.displayMessage('Select an action', buttons=('Add', 'Remove', 'Details', 'Cancel'))
    if sel == 0:
        projectAdd()
    elif sel == 1:
        projectRemove()
    elif sel == 2:
        projectDetails()
    else:
        return


def projectAdd():
    #Init
    data = readJson()
    path = None
    proj_name = None
    proj_code = None
    proj_fps = None
    _proj_name = None

    #Select Project Path
    repeat = True
    while repeat:
        repeat = False

        _path = hou.ui.selectFile(title='Select Project Directory', file_type=hou.fileType.Directory)
        path = os.path.dirname(_path)

        if path == '': #Check is the user correctly selected a path
            return

        for k,v in data.items(): #Check if the path is already used
            if util.fixPath(path) == util.fixPath(v['PATH']):
                util.error('Project path is already used by project {0}\nPlease select a different path to avoid conflicts'.format(k))
                repeat = True
                break
        if repeat:
            continue

        _proj_name = os.path.split(path)[-1]


    #Select Project Datas
    repeat = True
    while repeat:
        repeat = False
        inputs = hou.ui.readMultiInput(message='Enter Project Data',
                                       input_labels=('Project Name', 'Project Code', 'FPS'),
                                       buttons=('OK', 'Cancel'),
                                       initial_contents=(_proj_name, '', '24'))

        if inputs[0] == 1:
            return

        proj_name = inputs[1][0]
        proj_code = inputs[1][1]
        proj_fps = inputs[1][2]


        # Check Values and Manage Errors
        if proj_name == '' or proj_code == '' or proj_fps == '': #Check if fields are not empty
            util.error('Please fill in all fields')
            repeat = True
            continue

        try: #Check if FPS is an integer
            proj_fps = int(proj_fps)
        except ValueError:
            util.error('FPS not set to a valid number.\nPlease enter an Integer')
            repeat = True
            continue

        for k, v in data.items():
            if proj_name == k:
                util.error('A project with the same name already exist.\nPlease use another name to avoid conflicts.')
                repeat = True
                break

            if proj_code == v['CODE']:
                util.error('A project with the same code already exist.\nPlease use another code to avoid conflicts.')
                repeat = True
                break

        if repeat:
            continue


    #Collect Datas
    if proj_name and proj_code and proj_fps: #If the value exist
        proj_data = {
            'CODE' : proj_code,
            'PATH' : path,
            'FPS' : proj_fps
        }
        data[proj_name] = proj_data

    #Write Datas in JSON File
    if data:
        with open(proj_list, 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4)


def projectRemove():
    data = readJson()
    projects = list(data.keys())
    sel = hou.ui.selectFromList(projects, message='Select project to remove',
                                title='Remove Project',
                                column_header='Projects',
                                clear_on_cancel=True)


    if len(sel) == 0: #Check if something is selected or the cancel button has been pressed
        return

    for i in sel: #Delete each project selected by the user
        key = projects[i]
        del data[key]

    with open(proj_list, 'w') as f: #Write to JSON the updated project list
        json.dump(data, f, sort_keys=True, indent=4)


def projectDetails():
    data = readJson()
    projects = list(data.keys())
    sel = hou.ui.selectFromList(projects, exclusive=True, message='Select project to view details',
                                title='Projects Details',
                                column_header='Projects',
                                clear_on_cancel=True)

    if len(sel) == 0: #Check if something is selected or the cancel button has been pressed
        return

    key = projects[sel[0]]
    proj_data = data[key]
    util.printReport('Project Details',
                'Name : {0}'.format(key),
                'Code : {0}'.format(proj_data['CODE']),
                'FPS : {0}'.format(proj_data['FPS']))
