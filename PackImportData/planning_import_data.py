import PackGeneralProcedures.files as genFiles
import PackGeneralProcedures.global_variable_process_procedures as gl_v_data
import PackImportData.planning_import_data_functiones as plannImporFunct
import PackImportData.match_id_entities_planning as idEntiPlann
import PackImportData.dataFrame_planning_post as postPlan
from mod_variables import *



def planning_import_data_steps(name_folder_process):

    

    #ACADEMIC TERM
    data_academic_term = gl_v_data.gl_data_academic_term
    df_acad_term_info, id_acad_term, id_first_week_acad_term = plannImporFunct.manage_data_acad_term(data_academic_term)


    #EXTRAST ID's BEST
    df_plan, df_st_group, df_modules, df_type_mod = plannImporFunct.collect_entities_id_to_process()

    #PLAN/MODULES
    df_relacion_plan_module = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                             v_file_curriculum_to_import,v_sheet_planes_modules)
    
    df_relacion_plan_module, df_invalid = idEntiPlann.file_plan_modules_add_id_plan(df_relacion_plan_module, df_plan)
    df_relacion_plan_module, df_invalid = idEntiPlann.file_plan_modules_add_id_module(df_relacion_plan_module, df_modules, df_invalid)

    df_relacion_plan_module_ids = plannImporFunct.group_modules_plan(df_relacion_plan_module)
    postPlan.iterate_df_plan_mod_and_post(df_relacion_plan_module_ids, id_acad_term)

    #WEEKLOADS
    df_wloads = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                v_file_wloads,v_sheet_wloads )
    
    df_wloads = plannImporFunct.add_id_week (df_wloads, int(id_first_week_acad_term))
    df_wloads = plannImporFunct.select_w_load_sectiones_to_import(df_wloads)
    df_wloads = idEntiPlann.file_wloads_add_mod_id(df_wloads, df_modules)
    df_wloads = idEntiPlann.file_wloads_add_mod_type_id(df_wloads, df_type_mod)

    df_wloads_pattern = df_wloads.copy()
    df_wloads_pattern = plannImporFunct.agg_weekloads_same_pattern(df_wloads_pattern)

    postPlan.iterate_df_w_load_and_post_wload(df_wloads_pattern, id_acad_term)
    
    

    


    return()