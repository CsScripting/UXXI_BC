from PackLibrary.librarys import (
    os,
    t
)

from mod_variables import *

def create_folder_import_process (process_folder : str):


    process_folder_update_data = v_main_folder_process + '/' + process_folder + '/' + v_process_import_data

    if not os.path.isdir(process_folder_update_data):
        
        os.mkdir(process_folder_update_data)

    return()

def create_folder_add_conectores ():

    timestr = t.strftime("_%Y%m%d_%H%M%S")

    path_folder_conector = v_main_folder_process + '/' + v_main_folder_conector + timestr

    if not os.path.isdir(path_folder_conector):
        
        os.mkdir(path_folder_conector)

    return(path_folder_conector, timestr)