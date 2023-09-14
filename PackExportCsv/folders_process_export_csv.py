from PackLibrary.librarys import (
    os,
    t
)

from mod_variables import *




def create_csv_folder_export_process (): 

    path_folder = './' + v_main_folder_csv

    if not os.path.isdir(path_folder):
        
        os.mkdir(path_folder)

    timestr = t.strftime("_%Y%m%d_%H%M%S")

    process_folder= path_folder + '/' + v_csv_sub_folder + timestr

    if not os.path.isdir(process_folder):
        
        os.mkdir(process_folder) 

    process_code = timestr

    return(process_folder, process_code)