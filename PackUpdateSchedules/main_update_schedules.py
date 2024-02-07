import PackImportData.folders_process_import as folderImport
import PackGeneralProcedures.files as genFiles

from mod_variables import *

def update_schedules_steps(name_folder_process):
    
    #CREATE FOLDER IMPORT
    folderImport.create_folder_import_process(name_folder_process)

    #READ FILES UXXI TO IMPORT SCHEDULES

    df_horarios = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                  v_file_horarios,v_sheet_data_uxxi)
    
    
    

    return()