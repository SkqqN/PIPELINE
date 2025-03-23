<h1>Instructions :</h1>

- Put the 123.py file in your user preference script directory (ex: C:/Users/YourName/Documents/houdini(ver)/scripts/123.py)
- Edit line 8 to refer your working path
- _\_houdini\__ folder and its config files will be automatically created on the next houdini launch
- You can fill the folders with the one provided here to store the tools and hda
- save.py is the shelf tool to correctly save your scenes

<h3>HDA :</h3>

- SCENE_DATA : Node to setup the project, hold the variables and paths according to the pipeline

<h3>CONFIG :</h3>

- PROJ_LIST : Hold the dictionary to manage every projects infos

<h3>SCRIPTS :</h3>

- PROJECT_TOOLS : Hold every fonctions to manage projects and scenes based on the pipeline

- SCENE_DATA : Setup the pipeline for every project, create every variables, folders and files

- SAVE_SCENE : Save the scene in the right place with the right naming convention

- UTILITY SCRIPTS : Used to store fonctions used for multiple tools
</br>
</br>

Every project information will be automatically stored in the dictionary _\_houdini\_/config/proj\_list.json_<br/>
Global HDAs and scripts used for every projects will be stored in _\_houdini\_/hda_</br>
Project specific HDAs and scripts will be stored in its own project folder
