TO WORK CORRECTLY WITH THIS TOOL :

- Put the 123.py file in your user preference script directory (ex: C:/Users/YourName/Documents/houdini(ver)/scripts/123.py)
- Edit line 7 and 17 to point to your working directory (C:/PATH_TO_WORKING_DIRECTORY/\_houdini_/scripts and C:/PATH_TO_WORKING_DIRECTORY/\_houdini_/hda)
- Put the \_houdini_ folder to your working directory
- Open \_houdini_/project_tools/main.py
- go to line 10 : proj_list = 'C:/PATH_TO_WORKING_DIRECTORY/\_houdini_/config/proj_list.json'
- replace PATH_TO_WORKING_DIRECTORY with your personal working directory
- Enjoy !

_save.py is a shelf tool script working with the pipeline only !_

Every project information will be automatically stored in the dictionary _houdini_/config/proj_list.json
Custom HDA will be accessible to \_houdini_/hda for global hda used in every projects
Project specific hda will be stored in the project folder created automatically
Same global scripts and project specific scripts
