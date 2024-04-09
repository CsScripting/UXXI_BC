import PackGeneralProcedures.global_variable_process_procedures as glVarProcess
import PackGeneralProcedures.files as genFiles
import PackManageData.folders_process_manage as folderProcess
import PackManageData.read_filter as readFilter
import PackManageData.data_uxxi as dataUxxi
import PackManageData.data_credits_uxxi as dataCredUxxi
import PackManageData.bussiness_rules_best as rulesBest
from mod_variables import *



def manage_data_planning_uxxi_steps (name_file_inserted : str):


    #CRIAR PASTA DE PLANIFICAÇÂO
    glVarProcess.gl_process_folder, glVarProcess.gl_process_code = folderProcess.create_main_folder_manage_process(v_process_planning_sub_folder)

    process_folder = glVarProcess.gl_process_folder
    process_code = glVarProcess.gl_process_code

    #LER DADOS CONECTORES
    df_planning = readFilter.read_data_file_xlsx(name_file_inserted, v_sheet_planning_data_uxxi)
    df_planning, semestre = readFilter.select_columns_to_process_planning(df_planning) # EVITAR CASOS DE FICHEIROS QUE TEM EM ALGUMA COLUNA "VAZIA" VALORES COLOCADOS POR ENGANO
    df_planning = genFiles.filter_file_not_null_values(df_planning) ## IMPORTANTE VERIFICAR NULOS POR CAUSA DOS GROUP BY

    #LER DADOS CREDITOS#
    #DISCIPLINAS MODELOS DE CREDITOS
    df_model_module = readFilter.read_data_file_xlsx(name_file_inserted, v_sheet_model_module)
    df_model_module = dataCredUxxi.filter_columns_process(df_model_module, v_sheet_model_module)
    df_model_module, df_model_module_invalid = dataCredUxxi.filter_null_values_credits(df_model_module, v_sheet_model_module) ## ENVIAR FICHEIRO DE VALIDAÇÂO
    df_model_module, df_model_module_duplicated = dataCredUxxi.verify_duplicated_data_model_credits_general(df_model_module,v_sheet_model_module) ## ENVIAR FICHEIRO DE VALIDAÇÂO

    #MODELO SEMANAS DE DISCIPLINAS
    df_model_credits_weeks =  readFilter.read_data_file_xlsx(name_file_inserted, v_sheet_credit_model_criterion)
    df_model_credits_weeks = dataCredUxxi.filter_columns_process(df_model_credits_weeks, v_sheet_credit_model_criterion)
    df_model_credits_weeks = dataCredUxxi.filter_model_criterion_by_semestre (df_model_credits_weeks, semestre)
    df_model_credits_weeks, df_model_module_credit_weeks_invalid = dataCredUxxi.filter_null_values_credits(df_model_credits_weeks, v_sheet_credit_model_criterion) ## ENVIAR FICHEIRO DE VALIDAÇÂO
    df_model_credits_weeks, df_model_module_credit_weeks_duplicated = dataCredUxxi.verify_duplicated_data_model_credits_general(df_model_credits_weeks, v_sheet_credit_model_criterion) ## ENVIAR FICHEIRO DE VALIDAÇÂO

    #MODELOS DE CREDITOS/HORAS DISCIPLINAS
    df_model_credits_hours =  readFilter.read_data_file_xlsx(name_file_inserted, v_sheet_credit_model)
    df_model_credits_hours = dataCredUxxi.filter_columns_process(df_model_credits_hours, v_sheet_credit_model)
    df_model_credits_hours, df_model_module_credit_hours_invalid = dataCredUxxi.filter_null_values_credits(df_model_credits_hours, v_sheet_credit_model) ## ENVIAR FICHEIRO DE VALIDAÇÂO
    df_model_credits_hours, df_model_module_credit_hours_duplicated = dataCredUxxi.verify_duplicated_data_model_credits_general(df_model_credits_hours,v_sheet_credit_model) ## ENVIAR FICHEIRO DE VALIDAÇÂO


    df_planning_curriculum = df_planning.copy()
    df_planning_conector = df_planning.copy()
    dataUxxi.check_courses_uxxi (df_planning_curriculum, process_folder, process_code, v_main_process_planning)
    dataUxxi.check_planes_uxxi (df_planning_curriculum, process_folder, process_code, v_main_process_planning)
    
    
    #VERIFICAÇAO DADOS PLANIFICAÇÂO
    df_planning_grouped_by_conector= dataUxxi.group_mutual_modules_plannificacion(df_planning_conector)
    df_data_to_btt = df_planning_grouped_by_conector.copy()
    
    #ESCREVER RELAÇÂO DE DOMINANTE/DOMINADAS EM FICHEIRO:
    df_planning_grouped_by_conector = dataUxxi.create_df_info_mutual_modules_to_file(df_planning_grouped_by_conector,process_folder, process_code)

    #ESCREVER RELAÇÂO DE PLANIFICAÇÂO A IMPORTAR EM BTT EM PASTA DE MANAGE DATA
    df_data_to_btt = dataUxxi.plans_to_btt_extract_only_dominant_modules(df_data_to_btt)
    dataUxxi.check_modules_uxxi (df_data_to_btt, process_folder, process_code, v_main_process_planning)
    df_relacion_plan_module = dataUxxi.check_planes_modules (df_data_to_btt, process_folder, process_code) 
    
    df_planning = dataUxxi.check_typologies_uxxi_from_file_conector(df_planning) ## MAIS TARDE INFORMAÇÂO ENVIADA EM FICHEIRO (PODERÁ SE DESCNTINUAR FUNCÂO)
    dataUxxi.check_typologies_uxxi (df_planning, process_folder, process_code)
    df_relacion_groups_plan = dataUxxi.create_st_group_uxxi_planning (df_planning, process_folder, process_code)


    
    #AO ADICIONAR FICHEIROS VERIFICAR SE HÁ DADOS PARA CONTINUAR O PROCESSO.

    dataCredUxxi.update_data_to_btt (df_planning_grouped_by_conector)
    #ADD MODEL
    df_data_import, df_asignatura_sin_modelo = dataCredUxxi.add_model_module_section_conector(df_planning_grouped_by_conector, df_model_module)
    ## ADD CREDIT MODEL Weeks
    df_data_import, df_asignatura_sin_model_credit_weeks = dataCredUxxi.add_model_module_credit_section_conector(df_data_import, df_model_credits_weeks)
    df_data_import = dataCredUxxi.select_weeks_by_typologie(df_data_import)
    df_data_import, df_data_without_weeks = dataCredUxxi.check_week_typologie_not_null(df_data_import)
    ## ADD CREDIT MODEL HOURS
    df_data_import, df_data_without_hours =  dataCredUxxi.add_hours_credits_model(df_data_import, df_model_credits_hours)

    df_data_import = dataCredUxxi.hours_weeks_section(df_data_import)
    df_data_import = dataUxxi.add_groups_bullet_and_number_students(df_data_import, df_relacion_groups_plan)
    df_data_import = rulesBest.filter_fiels_w_loads (df_data_import)
    df_data_import = rulesBest.insert_name_section(df_data_import)
    df_data_import = rulesBest.insert_name_wload (df_data_import)
    df_data_import = rulesBest.agg_section_to_w_load(df_data_import)
    df_data_import = rulesBest.count_sectiones_number(df_data_import)

    dataUxxi.create_df_w_loads_to_file (df_data_import, process_folder, process_code, v_process_manage_data)

    return(df_data_import, df_relacion_plan_module)