from PackLibrary.librarys import (
    os,
    t
)

from mod_variables import *




def create_main_folder_manage_process (): # Create processo folder and ManageData Folder

    path_folder = './' + v_main_folder_process

    if not os.path.isdir(path_folder):
        
        os.mkdir(path_folder)

    timestr = t.strftime("_%Y%m%d_%H%M%S")

    process_folder= path_folder + '/' + v_process_sub_folder + timestr

    if not os.path.isdir(process_folder):
        
        os.mkdir(process_folder) 

    process_code = timestr

    process_folder_manage_data = process_folder + '/' + v_process_manage_data

    if not os.path.isdir(process_folder_manage_data):
        
        os.mkdir(process_folder_manage_data)

    return(process_folder, process_code)


