import PackGeneralProcedures.files as genFiles
import PackImportData.dataFrame_data_post as iteratePost
import PackImportData.dataFrame_event_post as eventPost
import PackImportData.folders_process_import as folderImport
import PackImportData.match_id_entities_events as idEntities
import PackImportData.planning_import_data as planningImport

from PackLibrary.librarys import (	
 concat
)


from mod_variables import *

def import_data_steps(name_folder_process : str, main_process : str):


    ############ INICIO DE PROCESSO DE INSERÇÂO DE NOVOS DADOS #####################

    file_imported_created = False

    #Create Importacion Folder
    folderImport.create_folder_import_process(name_folder_process) #### NÂO ESQUECER GESTÂO DE FICHEIROS - PODE SE EXECUTAR PROCESSO MAIS DE UMA VEZ ##### Se Pasta existir pedir para verificar a pasta de Update

    # Check File CURRICULUM_NEW, SEMPRE INSERIDO NO PROCESSO DE UPDATA --> MESMO QUE VAZIO !!!

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
        genFiles.create(df_courses_to_update,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_courses,v_process_import_data)
        file_imported_created = True

    ## - Planes - ##
    df_planes_to_update = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                          v_file_curriculum_to_import,v_sheet_planes)
    
    if not df_planes_to_update.empty:

        df_planes_imported = iteratePost.iterate_df_planes_and_post (df_planes_to_update)
        
        genFiles.create(df_planes_imported,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_planes,v_process_import_data, file_imported_created )
        

    else: 

        genFiles.create(df_planes_to_update,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_planes,v_process_import_data, file_imported_created )
        

    ## - Student Groups - ##
    df_st_groups_to_update = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                             v_file_curriculum_to_import,v_sheet_st_group)
    
    if not df_st_groups_to_update.empty:

        df_st_groups_imported = iteratePost.iterate_df_groups_and_post (df_st_groups_to_update)
        
        genFiles.create(df_st_groups_imported,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_st_group,v_process_import_data, file_imported_created )
        

    else: 

        genFiles.create(df_st_groups_to_update,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_st_group,v_process_import_data, file_imported_created )
        
    
    ## - Modules - ##
    df_modules_to_update = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                             v_file_curriculum_to_import,v_sheet_modules)
    
    if not df_modules_to_update.empty:

        df_modules_imported = iteratePost.iterate_df_modules_and_post (df_modules_to_update)
        
        genFiles.create(df_modules_imported,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_modules,v_process_import_data, file_imported_created )
        

    else: 

        genFiles.create(df_modules_to_update,v_main_folder_process,name_folder_process,v_file_curriculum_imported,v_sheet_modules,v_process_import_data, file_imported_created  )


    ############ FIM DE PROCESSO DE INSERÇÂO DE NOVOS DADOS #####################

    ############ INICIO PROCESSO SCHEDULES/IMPORT #####################

    if main_process == v_main_process_schedules:

        #Read Files to Import Data Events

        df_horarios = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                      v_file_horarios,v_sheet_schedules_data_uxxi )
        
        # Verify Events to Import (Opcion From User) --> Value 1 To Import

        df_horarios = idEntities.filter_df_to_import(df_horarios)

        #Collect Id´s Entities to Insert  Events

        ## - AcademicTerm - ##
        df_horarios, df_horarios_invalid = idEntities.academic_year (df_horarios )

        ## - EventType - ##
        df_horarios, df_horarios_invalid = idEntities.event_type (df_horarios,df_horarios_invalid )


        ## - Modules - ##
        df_horarios, df_horarios_invalid = idEntities.module (df_horarios, df_horarios_invalid)

        #### Efetuar analise ate ao Import Events

        ## - Typologies - ##
        df_horarios, df_horarios_invalid = idEntities.typologies (df_horarios, df_horarios_invalid)

        # # - StudentGroups - #
        df_horarios, df_horarios_invalid = idEntities.student_group (df_horarios, df_horarios_invalid)

        # # - Classroooms - #
        df_horarios, df_horarios_invalid = idEntities.classrooms (df_horarios, df_horarios_invalid)


        # # - Weeks - #
        df_horarios, df_horarios_invalid = idEntities.weeks (df_horarios, df_horarios_invalid)



        ## Import Events ##
    
        ########## Verificar import sobre o mesmo processo ....erro se ficheiro ficar aberto .....


            ##################################
        # - OLD METHOD ... EVENTO POR EVENTO - #
        ###################################
        # df_events_imported, df_events_not_imported = eventPost.iterate_df_events_and_post_single_event(df_horarios)

        ##### Errores From ID and not Inserted ID
        # df_events_not_imported = concat([df_events_not_imported, df_horarios_invalid], ignore_index= True)

        # if not df_events_imported.empty:

        #     genFiles.create(df_events_imported,v_main_folder_process,name_folder_process,v_file_events_imported,v_sheet_events,v_process_import_data )

        # if not df_events_not_imported.empty:
            
        #     genFiles.create(df_events_not_imported,v_main_folder_process,name_folder_process,v_file_events_not_imported,v_sheet_events,v_process_import_data)

            ##################################
        # - OLD METHOD ... EVENTO POR EVENTO - #
            ###################################


        ##################################
        #   NEW METHOD ... COLLECTION EVENT - #
        ###################################


        eventPost.iterate_df_events_and_put_collection_event(df_horarios)


        if not df_horarios_invalid.empty:

            genFiles.create(df_horarios_invalid,v_main_folder_process,name_folder_process,v_file_events_not_imported,v_sheet_events_not_imported ,v_process_import_data )

    ############ FIM PROCESSO SCHEDULES/IMPORT #####################

    ############ INICIO PROCESSO PLANNING/IMPORT #####################

    if main_process == v_main_process_planning:

        planningImport.planning_import_data_steps(name_folder_process)



        






    return()