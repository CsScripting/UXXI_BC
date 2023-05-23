from PackLibrary.librarys import (
    os,
    t
)

from mod_variables import *

def create_folder_update_process (process_folder : str):


    process_folder_update_data = process_folder + '/' + v_process_update_data

    if not os.path.isdir(process_folder_update_data):
        
        os.mkdir(process_folder_update_data)

    return()