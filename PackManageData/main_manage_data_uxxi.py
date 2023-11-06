
import PackManageData.folders_process_manage as folderProcess
import PackManageData.read_filter as readFilter
import PackManageData.join_tuples_data as joinData
import PackManageData.bussiness_rules_uxxi as rulesUxxi
import PackManageData.bussiness_rules_best as rulesBest
import PackGeneralProcedures.global_variable_process_procedures as glVarProcess
import PackManageData.data_uxxi as dataUxxi
import PackGeneralProcedures.files as genFiles
from mod_variables import *


def manage_data_uxxi_steps(name_file_inserted : str):

    flag_file_validation_created = False
    
    # Create Folder Process
    glVarProcess.gl_process_folder, glVarProcess.gl_process_code = folderProcess.create_main_folder_manage_process()

    process_folder = glVarProcess.gl_process_folder
    process_code = glVarProcess.gl_process_code

    #read and filter data UXXI  
    df_uxxi = readFilter.read_data_file(name_file_inserted)
    df_uxxi = readFilter.select_only_columns_to_process(df_uxxi)
    df_uxxi = readFilter.cleaning_data (df_uxxi).copy()
    df_uxxi, df_uxxi_null_values = readFilter.filter_null_values(df_uxxi)
    
    if not df_uxxi_null_values.empty:

        readFilter.create_insert_validation_file(df_uxxi_null_values, process_folder, process_code,
                                                 v_sheet_null_values, flag_file_validation_created)
        flag_file_validation_created = True

    # Por agora não considera as atividades dirigidas...verificar mais tarde !!!
    df_uxxi,df_uxxi_wrong_type  = readFilter.filter_by_activity_type (df_uxxi)

    if not df_uxxi_wrong_type.empty:

        readFilter.create_insert_validation_file(df_uxxi_wrong_type, process_folder, process_code,
                                                 v_sheet_wrong_type, flag_file_validation_created)
        flag_file_validation_created= True

    
    # Split ID_BD From CODIGO

    df_uxxi = rulesUxxi.split_id_bd_from_code(df_uxxi)

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

    # Extract Curriculum From Schedules
    df_curriculum_uxxi = df_uxxi.copy()
    dataUxxi.check_courses_uxxi (df_curriculum_uxxi, process_folder, process_code)
    dataUxxi.check_planes_uxxi (df_curriculum_uxxi, process_folder, process_code)
    # dataUxxi.check_planes_modules (df_curriculum_uxxi, process_folder, process_code)
    dataUxxi.check_st_groups_uxxi (df_curriculum_uxxi, process_folder, process_code)
    dataUxxi.check_modules_uxxi (df_curriculum_uxxi, process_folder, process_code)
    dataUxxi.check_typologies_uxxi (df_curriculum_uxxi, process_folder, process_code)

    #New Code Classroom - On method check_classrooms_uxxi code saved with new Code (Concat CODIGO_AULA - (ID_AULA_UXXI))
    dataUxxi.check_classrooms_uxxi (df_curriculum_uxxi, process_folder, process_code)


    df_uxxi = rulesUxxi.agg_groups_from_event(df_uxxi)
    df_uxxi = rulesUxxi.select_number_students(df_uxxi)
    
    df_uxxi = rulesBest.update_value_day(df_uxxi)
    df_uxxi = rulesBest.add_event_type(df_uxxi)
    df_uxxi = rulesBest.add_event_code(df_uxxi, process_code)
    df_uxxi = rulesBest.add_event_section_name(df_uxxi)
    df_uxxi = rulesBest.add_number_week(df_uxxi)
    df_uxxi = rulesBest.manage_hours(df_uxxi)
    df_uxxi = rulesBest.add_event_connector(df_uxxi)
    df_uxxi = rulesUxxi.add_duration_event(df_uxxi)

    df_uxxi = rulesUxxi.select_type_module_uuxi(df_uxxi)

    #Extrat Date Schedules:

    first_week, last_week = dataUxxi.check_date_begin_end_schedules(df_uxxi)

    #Create DataFrameInfo:

    df_info_events = dataUxxi.create_df_info_date_events(first_week, last_week)



    df_uxxi_to_manage_data = df_uxxi[[v_event_Id_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                                      v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code, 
                                      v_year, v_student_group_name,v_students_number,v_id_uxxi,v_weeks,v_mod_modalidad, v_event_type,v_classroom_code, v_classroom_name ]].copy()
    
    

    #Insert File On Folder Manage Data:

    genFiles.create(df_uxxi_to_manage_data,process_folder, process_code,v_file_horarios,v_sheet_data_uxxi,v_process_manage_data)

    return(first_week, last_week, df_info_events, df_uxxi_to_manage_data)

