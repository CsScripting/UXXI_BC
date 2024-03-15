import PackGeneralProcedures.files as genFiles
import PackGeneralProcedures.global_variable_process_procedures as gl_v_data
import PackImportData.planning_import_data_functiones as planImporFunct
import PackImportData.match_id_entities_planning as idEntiPlann
import PackImportData.dataFrame_planning_post as postPlan
from mod_variables import *



def planning_import_data_steps(name_folder_process):

    

    #ACADEMIC TERM
    data_academic_term = gl_v_data.gl_data_academic_term
    df_acad_term_info, id_acad_term, id_first_week_acad_term = planImporFunct.manage_data_acad_term(data_academic_term)


    #EXTRAST ID's BEST
    df_plan, df_st_group, df_modules, df_type_mod = planImporFunct.collect_entities_id_to_process()

    #PLAN/MODULES
    df_relacion_plan_module = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                             v_file_curriculum_to_import,v_sheet_planes_modules)
    
    df_relacion_plan_module, df_invalid = idEntiPlann.file_plan_modules_add_id_plan(df_relacion_plan_module, df_plan)
    df_relacion_plan_module, df_invalid = idEntiPlann.file_plan_modules_add_id_module(df_relacion_plan_module, df_modules, df_invalid)

    df_relacion_plan_module_ids = planImporFunct.group_modules_plan(df_relacion_plan_module)
    postPlan.iterate_df_plan_mod_and_post(df_relacion_plan_module_ids, id_acad_term)




    




    df_wloads = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                v_file_wloads,v_sheet_wloads )


    return()