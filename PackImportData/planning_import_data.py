import PackGeneralProcedures.files as genFiles
import PackGeneralProcedures.global_variable_process_procedures as gl_v_data
import PackImportData.planning_import_data_functiones as planImporFunct
from mod_variables import *



def planning_import_data_steps(name_folder_process):

    df_relacion_plan_module = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                             v_file_curriculum_to_import,v_sheet_planes_modules)

    data_academic_term = gl_v_data.gl_data_academic_term

    planImporFunct.manage_weeks_acad_term(data_academic_term)

    df_wloads = genFiles.read_data_files_import(v_main_folder_process,name_folder_process, v_process_update_data, 
                                                v_file_wloads,v_sheet_wloads )


    return()