import PackGeneralProcedures.files as genFiles
import PackImportData.dataFrame_data_post as iteratePost
from mod_variables import *

def import_data_steps(name_folder_process):

    # Check File CURRICULUM_NEW, always Inserted !!!

    df_courses_to_update = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                           v_file_curriculum_import,v_sheet_courses )
    
    
    # Insert Data
    
    if not df_courses_to_update.empty: # Only to confirmacion...Irá se fazer uma validação antes !!!

        iteratePost.iterate_df_courses_and_insert (df_courses_to_update)
        


        



    return()