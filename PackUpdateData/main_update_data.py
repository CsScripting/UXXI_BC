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
    df_courses_best = courseDf.courses_df_from_json(courses_db)
    #Insert Course To Curriculum File
    genFiles.create (df_courses_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum_best, v_sheet_courses,v_process_update_data)
    
    flag_file_created = True


    # - Planes - #
    planes_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_plan_controller)
    df_planes_best = planDf.plan_df_from_json(planes_db)
    #Insert Planes To Curriculum File
    genFiles.create (df_planes_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum_best, v_sheet_planes,v_process_update_data, flag_file_created)
    
    # - StudentGroups - #
    student_group_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_st_group_controller)
    df_st_group_best = groupDf.st_groups_df_from_json(student_group_db)
    #Insert StGroup To Curriculum File
    genFiles.create (df_st_group_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum_best, v_sheet_st_group,v_process_update_data, flag_file_created)
    
    # - Modules - #
    modules_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_module_controller)
    df_modules_best = modDf.modules_df_from_json(modules_db)
    #Insert Modules To Curriculum File
    genFiles.create (df_modules_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum_best, v_sheet_modules,v_process_update_data, flag_file_created)
    

    # - Typologies Modules - #

    typologies_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_typologie_controller)
    df_typologies_best = typeDf.typologies_df_from_json (typologies_db)
    #Insert Typologies To Curriculum File
    genFiles.create (df_typologies_best,glVarPro.gl_process_folder,glVarPro.gl_process_code,
                     v_file_curriculum_best, v_sheet_typologies,v_process_update_data,flag_file_created)


    # - Read File CURRICULUM_UXXI - #

    # - Courses - #
    df_uxxi_courses = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                      v_file_curriculum_uxxi,v_sheet_courses )
    

    # - Planes - #
    df_uxxi_planes = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                      v_file_curriculum_uxxi,v_sheet_planes )
    
    # - StudentGroups - #
    df_uxxi_st_group = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                      v_file_curriculum_uxxi,v_sheet_st_group )
    
    # - Modules - #
    df_uxxi_modules = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                      v_file_curriculum_uxxi,v_sheet_modules )
    
    # - Modules Typologies- #
    df_uxxi_typologies = genFiles.read_data_files_update(v_main_folder_process,glVarPro.gl_process_code, v_process_manage_data, 
                                                      v_file_curriculum_uxxi,v_sheet_typologies )


    return()