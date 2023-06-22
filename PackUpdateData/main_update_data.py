import PackControllerRequest.general_requests as genRequest
import PackControllerRequest.event_request as eventRequest

import PackDfFromJson.CoursesDf as courseDf
import PackDfFromJson.CurricularPlansDf as planDf
import PackDfFromJson.StudentGroupsDf as groupDf 
import PackDfFromJson.ModulesDf as modDf
import PackDfFromJson.TypologiesDf as typeDf
import PackDfFromJson.EventsDf as eventDf


import PackManageApi.glogal_variable_process_request as gl_v_request
import PackGeneralProcedures.files as genFiles
import PackGeneralProcedures.global_variable_process_procedures as glVarPro
import PackUpdateData.folders_process_update as folderUpdate
import PackUpdateData.match_data_uxxi_api as matchData
import PackGeneralProcedures.files as genFiles

from PackLibrary.librarys import (	
  DataFrame
)

from mod_variables import *

def update_data_steps(first_week_schedules : str, last_week_schedules : str, df_info_events : DataFrame,
                       df_events_to_import : DataFrame):


    # Create Folder Update
    folderUpdate.create_folder_update_process(glVarPro.gl_process_folder)

    genFiles.create(df_events_to_import,glVarPro.gl_process_folder,glVarPro.gl_process_code,v_file_horarios,v_sheet_data_uxxi,v_process_update_data, False)

    
    ### extract schedules BEST ###


    events_best = eventRequest.get_events_all(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_event_controller, first_week_schedules, last_week_schedules)

    df_events_best = eventDf.events_df_from_json(events_best)

    file_events_created = False
    genFiles.create (df_info_events,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_events_best, v_sheet_variables_process,v_process_update_data)
    
    file_events_created = True
    genFiles.create (df_events_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_events_best, v_sheet_events_best,v_process_update_data, file_events_created)
    


    ### -- ###

    



    
    ## - Extract Data from DataBase (API) to Check Data - ##

    # - Courses - #
    courses_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_course_controller)
    df_courses_best = courseDf.courses_df_from_json(courses_db)
    #Insert Course To Curriculum File
    genFiles.create (df_courses_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum_best, v_sheet_courses,v_process_update_data)
    
    flag_file_created = True


    # # - Planes - #
    planes_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_plan_controller)
    df_planes_best = planDf.plan_df_from_json(planes_db)
    #Insert Planes To Curriculum File
    genFiles.create (df_planes_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum_best, v_sheet_planes,v_process_update_data, flag_file_created)
    
    # # - StudentGroups - #
    student_group_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_st_group_controller)
    df_st_groups_best = groupDf.st_groups_df_from_json(student_group_db)
    #Insert StGroup To Curriculum File
    genFiles.create (df_st_groups_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum_best, v_sheet_st_group,v_process_update_data, flag_file_created)
    
    # # - Modules - #
    modules_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_module_controller)
    df_modules_best = modDf.modules_df_from_json(modules_db)
    #Insert Modules To Curriculum File
    genFiles.create (df_modules_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum_best, v_sheet_modules,v_process_update_data, flag_file_created)
    

    # # - Typologies Modules - #

    typologies_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_typologie_controller)
    df_typologies_best = typeDf.typologies_df_from_json (typologies_db)
    #Insert Typologies To Curriculum File
    genFiles.create (df_typologies_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum_best, v_sheet_typologies,v_process_update_data,flag_file_created)


    # - Read File CURRICULUM_UXXI - #

    # - Courses - #
    df_courses_uxxi = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                      v_file_curriculum_uxxi,v_sheet_courses )
    

    # # - Planes - #
    df_planes_uxxi = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                      v_file_curriculum_uxxi,v_sheet_planes )
    
    # # - StudentGroups - #
    df_st_groups_uxxi = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                      v_file_curriculum_uxxi,v_sheet_st_group )
    
    # # - Modules - #
    df_modules_uxxi = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                      v_file_curriculum_uxxi,v_sheet_modules )
    
    # # - Modules Typologies- #
    df_typologies_uxxi = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                      v_file_curriculum_uxxi,v_sheet_typologies )
    

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
    

    #Student Groups
    df_modules_to_import = matchData.compare_modules_uxxi_db(df_modules_uxxi, df_modules_best)
    genFiles.create (df_modules_to_import, glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum_to_import, v_sheet_modules,v_process_update_data, flag_file_to_import_created)
    
    #Student Groups
    df_typologies_to_import = matchData.compare_typologies_uxxi_db(df_typologies_uxxi, df_typologies_best)
    genFiles.create (df_typologies_to_import, glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum_to_import, v_sheet_typologies,v_process_update_data, flag_file_to_import_created)

    return()