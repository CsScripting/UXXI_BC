from PackLibrary.librarys import (
    os,
    t
)

from mod_variables import *

def create_main_folder_process ():

    path_folder = './' + v_main_folder_manage_data

    if not os.path.isdir(path_folder):
        
        os.mkdir(path_folder)

    timestr = t.strftime("_%Y%m%d_%H%M%S")

    process_folder= path_folder + '/' + v_process_folder_manage_data + timestr

    if not os.path.isdir(process_folder):
        
        os.mkdir(process_folder) 

    process_code = timestr

    return(process_folder, process_code)


