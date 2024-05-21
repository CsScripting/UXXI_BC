import PackControllerRequest.general_requests as genRequest
import PackControllerRequest.event_request as eventRequest

import PackDfFromJson.CoursesDf as courseDf
import PackDfFromJson.CurricularPlansDf as planDf
import PackDfFromJson.StudentGroupsDf as groupDf 
import PackDfFromJson.ModulesDf as modDf
import PackDfFromJson.TypologiesDf as typeDf
import PackDfFromJson.ClassroomsDf as classDf
import PackDfFromJson.EventsDf as eventDf
import PackManageData.data_uxxi as dataUxxi


import PackManageApi.global_variable_process_request as gl_v_request
import PackGeneralProcedures.files as genFiles
import PackGeneralProcedures.global_variable_process_procedures as glVarPro
import PackUpdateData.folders_process_update as folderUpdate
import PackUpdateData.match_data_uxxi_api as matchData
import PackGeneralProcedures.files as genFiles
import PackUpdateData.match_schedules_best_uxxi as matchSche


from PackLibrary.librarys import (	
  DataFrame
)

from mod_variables import *

def update_data_steps(main_process : str, df_weekload_insert : DataFrame, df_relacion_plan_module : DataFrame,  first_week_schedules : str = '', last_week_schedules : str = '', df_info_events : DataFrame = [],
                      df_events_to_import : DataFrame = []):


    # CRIAR PASTA DE UPDATE PARA PROCESSO DE HORARIOS OU PROCESSO DE PLANIFICAÇÃO
    folderUpdate.create_folder_update_process(glVarPro.gl_process_folder)

    if main_process == 1: #SE PROCESSO DE HORARIOS

        ### extract schedules BEST ###

        events_best = eventRequest.get_events_all(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_event_controller, first_week_schedules, last_week_schedules)

        #Verify if list Events Empty or Not Empty
        if events_best: 

            # df_events_best = eventDf.events_df_from_json(events_best)
            df_events_best = eventDf.parse_list_events_to_df (events_best)

            df_uxxi_to_insert_data, df_uxxi_to_update_data, df_events_best = matchSche.match_id_schedules_to_import (df_events_to_import, df_events_best)
            
            # New Events
            df_uxxi_to_insert_data = matchSche.create_df_insert_data (df_uxxi_to_insert_data)
            
            # Verify events than exist on APP if needed Update
            if not df_uxxi_to_update_data.empty:
                
                df_events_best, verify_columns_values_update = df_uxxi_to_update_data = matchSche.match_id_schedules_to_update(df_uxxi_to_update_data, df_events_best)

            if len (verify_columns_values_update) != 0:
                
                genFiles.create(df_events_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,v_file_horarios_update,v_sheet_schedules_data_uxxi,v_process_update_data, False)




        else:
            
            df_uxxi_to_insert_data = matchSche.create_df_insert_data (df_events_to_import, True)

            
        genFiles.create(df_uxxi_to_insert_data,glVarPro.gl_process_folder,glVarPro.gl_process_code,v_file_horarios,v_sheet_schedules_data_uxxi,v_process_update_data, False)

    if main_process == 0:

        dataUxxi.create_df_w_loads_to_file (df_weekload_insert, glVarPro.gl_process_folder,glVarPro.gl_process_code, v_process_update_data, v_type_file_w_load)

    ## - Extract Data from DataBase (API) to Check Data - ##

    # - Courses - #
    courses_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_course_controller)
    df_courses_best = courseDf.parse_list_courses_to_df(courses_db)
    #Insert Course To Curriculum File
    genFiles.create (df_courses_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                        v_file_curriculum_best, v_sheet_courses,v_process_update_data)

    flag_file_created = True


    # # - Planes - #
    planes_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_plan_controller)
    df_planes_best = planDf.parse_list_plan_to_df(planes_db)
    #Insert Planes To Curriculum File
    genFiles.create (df_planes_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                        v_file_curriculum_best, v_sheet_planes,v_process_update_data, flag_file_created)

    # # - StudentGroups - #
    student_group_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_st_group_controller)
    df_st_groups_best = groupDf.parse_list_st_groups_to_df(student_group_db)
    #Insert StGroup To Curriculum File
    genFiles.create (df_st_groups_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                        v_file_curriculum_best, v_sheet_st_group,v_process_update_data, flag_file_created)

    # # - Modules - #
    modules_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_module_controller)
    df_modules_best = modDf.parse_list_mod_to_df(modules_db)

    #Insert Modules To Curriculum File
    genFiles.create (df_modules_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                        v_file_curriculum_best, v_sheet_modules,v_process_update_data, flag_file_created)


    # # - Typologies Modules - #

    typologies_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_typologie_controller)
    df_typologies_best = typeDf.parse_list_typologies_to_df (typologies_db)
    #Insert Typologies To Curriculum File
    genFiles.create (df_typologies_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                        v_file_curriculum_best, v_sheet_typologies,v_process_update_data,flag_file_created)
    
    
    if main_process == 1: # SALAS APENAS APLICAVEL PARA O PROCESSO DE HORARIOS

            # # - Classrooms - #

        classrooms_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_classrooms_controller)
        df_classrooms_best = classDf.parse_list_classrooms_to_df (classrooms_db)
        #Insert Classrooms To Curriculum File
        genFiles.create (df_classrooms_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                            v_file_curriculum_best, v_sheet_classrooms,v_process_update_data,flag_file_created)


    # - Read File CURRICULUM_UXXI - #

    # - Courses - #
    df_courses_uxxi = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                        v_file_curriculum_uxxi,v_sheet_courses, main_process )


    # # - Planes - #
    df_planes_uxxi = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                        v_file_curriculum_uxxi,v_sheet_planes,main_process )

    # # - StudentGroups - #
    df_st_groups_uxxi = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                        v_file_curriculum_uxxi,v_sheet_st_group,main_process )

    # # - Modules - #
    df_modules_uxxi = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                        v_file_curriculum_uxxi,v_sheet_modules,main_process )

    # # - Modules Typologies- #
    df_typologies_uxxi = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                            v_file_curriculum_uxxi,v_sheet_typologies,main_process )
    
    if main_process == 1: # SALAS APENAS APLICAVEL PARA O PROCESSO DE HORARIOS

        # # -Classrooms- #
        df_classrooms_uxxi = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                                v_file_curriculum_uxxi,v_sheet_classrooms,main_process )


    # - Match Data UXXI and DB - #

    #Always Insertef file Update

    #Courses
    df_courses_to_import = matchData.compare_courses_uxxi_db(df_courses_uxxi, df_courses_best)
    genFiles.create (df_courses_to_import, glVarPro.gl_process_folder,glVarPro.gl_process_code,
                        v_file_curriculum_to_import, v_sheet_courses,v_process_update_data)

    flag_file_to_import_created = True

    #Planes
    df_planes_to_import = matchData.compare_planes_uxxi_db(df_planes_uxxi, df_planes_best)
    genFiles.create (df_planes_to_import, glVarPro.gl_process_folder,glVarPro.gl_process_code,
                        v_file_curriculum_to_import, v_sheet_planes,v_process_update_data, flag_file_to_import_created)


    #Student Groups
    df_groups_to_import = matchData.compare_groups_uxxi_db(df_st_groups_uxxi, df_st_groups_best)
    genFiles.create (df_groups_to_import, glVarPro.gl_process_folder,glVarPro.gl_process_code,
                        v_file_curriculum_to_import, v_sheet_st_group,v_process_update_data, flag_file_to_import_created)


    #Modules
    df_modules_to_import = matchData.compare_modules_uxxi_db(df_modules_uxxi, df_modules_best)
    genFiles.create (df_modules_to_import, glVarPro.gl_process_folder,glVarPro.gl_process_code,
                        v_file_curriculum_to_import, v_sheet_modules,v_process_update_data, flag_file_to_import_created)

    #Typologies
    df_typologies_to_import = matchData.compare_typologies_uxxi_db(df_typologies_uxxi, df_typologies_best)
    genFiles.create (df_typologies_to_import, glVarPro.gl_process_folder,glVarPro.gl_process_code,
                        v_file_curriculum_to_import, v_sheet_typologies,v_process_update_data, flag_file_to_import_created)

    if main_process == 1: # SALAS APENAS APLICAVEL PARA O PROCESSO DE HORARIOS
        
        #Classrooms
        df_classrooms_to_import = matchData.compare_classrooms_uxxi_db(df_classrooms_uxxi, df_classrooms_best)
        genFiles.create (df_classrooms_to_import, glVarPro.gl_process_folder,glVarPro.gl_process_code,
                            v_file_curriculum_to_import, v_sheet_classrooms,v_process_update_data, flag_file_to_import_created)
        
    # Insert Relacion Plan Modules
    genFiles.create (df_relacion_plan_module, glVarPro.gl_process_folder,glVarPro.gl_process_code,
                    v_file_curriculum_to_import, v_sheet_planes_modules,v_process_update_data, flag_file_to_import_created)

    return()