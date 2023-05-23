import PackControllerRequest.GeneralRequests as genRequest

import PackDfFromJson.CoursesDf as courseDf
import PackDfFromJson.CurricularPlansDf as planDf
import PackDfFromJson.StudentGroupsDf as groupDf 
import PackDfFromJson.ModulesDf as modDf
import PackDfFromJson.TypologiesDf as typeDf


import PackManageApi.glogal_variable_process_request as gl_v_request
import PackGeneralProcedures.files as genFiles
import PackGeneralProcedures.global_variable_process_procedures as glVarPro
import PackUpdateData.folders_process_update as folderUpdate

from mod_variables import *

def update_data_steps():


    # Create Folder Update
    folderUpdate.create_folder_update_process(glVarPro.gl_process_folder)

    
    ## - Extract Entities DataBase to Check Data - ##

    # - Courses - #
    courses_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_course_controller)
    df_courses = courseDf.courses_df_from_json(courses_db)
    #Insert Course To Curriculum File
    genFiles.create (df_courses,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum, v_sheet_courses,v_process_update_data)
    
    flag_file_created = True


    # - Planes - #
    planes_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_plan_controller)
    df_planes = planDf.plan_df_from_json(planes_db)
    #Insert Planes To Curriculum File
    genFiles.create (df_planes,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum, v_sheet_planes,v_process_update_data, flag_file_created)
    
    # - StudentGroups - #
    student_group_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_st_group_controller)
    df_st_group = groupDf.st_groups_df_from_json(student_group_db)
    #Insert StGroup To Curriculum File
    genFiles.create (df_st_group,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum, v_sheet_st_group,v_process_update_data, flag_file_created)
    
    # - Modules - #
    modules_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_module_controller)
    df_modules = modDf.modules_df_from_json(modules_db)
    #Insert Modules To Curriculum File
    genFiles.create (df_modules,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum, v_sheet_modules,v_process_update_data, flag_file_created)
    

    # - Typologies Modules - #

    typologies_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_typologie_controller)
    df_typologies = typeDf.typologies_df_from_json (typologies_db)
    #Insert Typologies To Curriculum File
    genFiles.create (df_typologies,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum, v_sheet_typologies,v_process_update_data,flag_file_created)

    return()