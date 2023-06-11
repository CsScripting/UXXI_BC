import PackGeneralProcedures.files as genFiles
import PackImportData.dataFrame_data_post as iteratePost
import PackImportData.folders_process_import as folderImport
from mod_variables import *

def import_data_steps(name_folder_process):

    file_imported_created = False

    #Create Importacion Folder
    folderImport.create_folder_import_process(name_folder_process)

    # Check File CURRICULUM_NEW, always Inserted !!!

    ## - Courses - ##
    df_courses_to_update = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                           v_file_curriculum_to_import,v_sheet_courses )
    
    # Insert Data(if have new data)
    if not df_courses_to_update.empty: 

        df_courses_imported = iteratePost.iterate_df_courses_and_post (df_courses_to_update)
        
        genFiles.create(df_courses_imported,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_courses,v_process_import_data )
        file_imported_created = True

    else:

        # Always Inserted ImportData 
        genFiles.create(df_courses_to_update,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_courses,v_process_import_data )
        file_imported_created = True

    ## - Planes - ##
    df_planes_to_update = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                          v_file_curriculum_to_import,v_sheet_planes)
    
    if not df_planes_to_update.empty:

        df_planes_imported = iteratePost.iterate_df_planes_and_post (df_planes_to_update)
        
        genFiles.create(df_planes_imported,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_planes,v_process_import_data )
        

    else: 

        genFiles.create(df_planes_to_update,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_planes,v_process_import_data )
        

    ## - Student Groups - ##
    df_st_groups_to_update = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                             v_file_curriculum_to_import,v_sheet_st_group)
    
    if not df_st_groups_to_update.empty:

        df_st_groups_imported = iteratePost.iterate_df_groups_and_post (df_st_groups_to_update)
        
        genFiles.create(df_st_groups_imported,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_st_group,v_process_import_data )
        

    else: 

        genFiles.create(df_st_groups_imported,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_st_group,v_process_import_data )
        
    
    ## - Modules - ##
    df_modules_to_update = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                             v_file_curriculum_to_import,v_sheet_modules)
    
    if not df_modules_to_update.empty:

        df_modules_imported = iteratePost.iterate_df_modules_and_post (df_modules_to_update)
        
        genFiles.create(df_modules_imported,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_modules,v_process_import_data )
        

    else: 

        genFiles.create(df_modules_imported,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_modules,v_process_import_data )



    return()