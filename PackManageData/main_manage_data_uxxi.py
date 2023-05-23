
import PackManageData.folders_process_manage as folderProcess
import PackManageData.read_filter as readFilter
import PackManageData.join_tuples_data as joinData
import PackManageData.bussiness_rules_uxxi as rulesUxxi
import PackManageData.bussiness_rules_best as rulesBest
import PackGeneralProcedures.global_variable_process_procedures as glVarProcess
from mod_variables import *


def manage_data_uxxi_steps(name_file_inserted : str):

    flag_file_validation_created = False
    
    # Create Folder Process
    glVarProcess.gl_process_folder, glVarProcess.gl_process_code = folderProcess.create_main_folder_manage_process()

    process_folder = glVarProcess.gl_process_folder
    process_code = glVarProcess.gl_process_code

    #read and filter data UXXI  
    df_uxxi = readFilter.read_data_file(name_file_inserted)
    df_uxxi = readFilter.cleaning_data (df_uxxi).copy()
    df_uxxi, df_uxxi_null_values = readFilter.filter_null_values(df_uxxi)
    
    if not df_uxxi_null_values.empty:


        readFilter.create_insert_validation_file(df_uxxi_null_values, process_folder, process_code,
                                                 v_sheet_null_values, flag_file_validation_created)
        flag_file_validation_created = True

    df_uxxi,df_uxxi_wrong_type  = readFilter.filter_by_activity_type (df_uxxi)

    if not df_uxxi_wrong_type.empty:

        readFilter.create_insert_validation_file(df_uxxi_wrong_type, process_folder, process_code,
                                                 v_sheet_wrong_type, flag_file_validation_created)
        flag_file_validation_created= True

    df_uxxi, df_uxxi_wrong_week = joinData.manage_weeks(df_uxxi)

    if not df_uxxi_wrong_week.empty:

        readFilter.create_insert_validation_file(df_uxxi_wrong_week, process_folder, process_code,
                                                 v_sheet_wrong_week, flag_file_validation_created)
        flag_file_validation_created= True

    #Manage Groups
    df_check_groups_best_by_section = df_uxxi.copy()
    df_check_groups_best_by_section = rulesUxxi.relacion_group_EPD_by_section_to_asign_to_EB (df_check_groups_best_by_section) 
    df_uxxi = rulesUxxi.add_group_section_EPD(df_uxxi)
    df_uxxi = rulesUxxi.add_group_section_EB (df_uxxi, df_check_groups_best_by_section)
    df_uxxi = rulesUxxi.agg_groups_from_event(df_uxxi)
    df_uxxi = rulesUxxi.select_number_students(df_uxxi)
    
    df_uxxi = rulesBest.update_value_day(df_uxxi)
    df_uxxi = rulesBest.add_event_type(df_uxxi)
    df_uxxi = rulesBest.add_event_code(df_uxxi, process_code)
    df_uxxi = rulesBest.add_event_section_name(df_uxxi)
    df_uxxi = rulesBest.add_event_connector(df_uxxi)
    df_uxxi = rulesBest.manage_hours(df_uxxi)



    return()

