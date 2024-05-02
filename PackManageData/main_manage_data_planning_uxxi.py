import PackGeneralProcedures.global_variable_process_procedures as glVarProcess
import PackGeneralProcedures.files as genFiles
import PackManageData.folders_process_manage as folderProcess
import PackManageData.read_filter as readFilter
import PackManageData.data_uxxi as dataUxxi
import PackManageData.data_credits_uxxi as dataCredUxxi
import PackManageData.bussiness_rules_best as rulesBest
from mod_variables import *



def manage_data_planning_uxxi_steps (name_file_inserted : str):

    manage_weekly_weekload = False

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

    #VALIDAÇÂO DE MODELOS CREDITOS PARA FICHEIRO:

    dataUxxi.create_file_validation_module_credits (df_model_module_invalid,v_sheet_wrong_model_module, process_folder, process_code, v_process_manage_data)
    dataUxxi.create_file_validation_module_credits (df_model_module_duplicated,v_sheet_duplicated_model_module, process_folder, process_code, v_process_manage_data)
    dataUxxi.create_file_validation_module_credits (df_model_module_credit_weeks_invalid,v_sheet_wrong_model_credit, process_folder, process_code, v_process_manage_data)
    dataUxxi.create_file_validation_module_credits (df_model_module_credit_weeks_duplicated,v_sheet_duplicated_model_credit, process_folder, process_code, v_process_manage_data)
    dataUxxi.create_file_validation_module_credits (df_model_module_credit_hours_invalid,v_sheet_wrong_credit_week, process_folder, process_code, v_process_manage_data)
    dataUxxi.create_file_validation_module_credits (df_model_module_credit_hours_duplicated,v_sheet_duplicated_credit_week, process_folder, process_code, v_process_manage_data)



    df_planning_curriculum = df_planning.copy()
    df_planning_conector = df_planning.copy()
    dataUxxi.check_courses_uxxi (df_planning_curriculum, process_folder, process_code, v_main_process_planning)
    dataUxxi.check_planes_uxxi (df_planning_curriculum, process_folder, process_code, v_main_process_planning)
    df_planning = dataUxxi.check_typologies_uxxi_from_file_conector(df_planning)
    dataUxxi.check_typologies_uxxi (df_planning, process_folder, process_code)
    df_relacion_groups_plan = dataUxxi.create_st_group_uxxi_planning (df_planning, process_folder, process_code)
    
    
    #VERIFICAÇAO DADOS PLANIFICAÇÂO
    #ADD MODEL (ADICIONADO LOGO MODELO DE DISCIPLINA PARA NÂO TER DE FAZER ITERAÇÔES DEPOIS DE AGRUPADO)
    #ADD MODEL --> NESTE CASO SO SERA NECESSARIO FAZER O MERGE
    df_planning_conector= dataCredUxxi.add_model_module_section_conector(df_planning_conector, df_model_module)
    #VERIFICAR NUMERO DE EPD POR DISCIPLINA PLANO
    df_relacion_epd_module_linea = dataUxxi.verify_number_epd_module_by_plan_to_asign_to_eb(df_planning_conector)
    df_planning_conector = dataUxxi.join_info_edp_module_plan(df_planning_conector, df_relacion_epd_module_linea)
    #VERIFICAR NUMERO DE EPD POR PLANO INSERIDO NO BTT
    df_relacion_groups_plan = dataUxxi.verify_number_groups_edp_inserted_btt(df_relacion_groups_plan)
    df_planning_conector = dataUxxi.join_info_epd_plan(df_planning_conector, df_relacion_groups_plan)

    df_planning_grouped_by_conector= dataUxxi.group_mutual_modules_plannificacion(df_planning_conector)
    df_planning_grouped_by_conector,df_asignatura_sin_modelo  = dataUxxi.verify_modeles_UXXI_conector(df_planning_grouped_by_conector)
    dataUxxi.create_file_validation_module_credits (df_asignatura_sin_modelo,v_sheet_section_sin_modelo, process_folder, process_code, v_process_manage_data)
    
    
    df_data_to_btt = df_planning_grouped_by_conector.copy()
    
    #ESCREVER RELAÇÂO DE DOMINANTE/DOMINADAS EM FICHEIRO:
    df_planning_grouped_by_conector = dataUxxi.create_df_info_mutual_modules_to_file(df_planning_grouped_by_conector,process_folder, process_code)

    #ESCREVER RELAÇÂO DE PLANIFICAÇÂO A IMPORTAR EM BTT EM PASTA DE MANAGE DATA
    df_data_to_btt = dataUxxi.plans_to_btt_extract_only_dominant_modules(df_data_to_btt)
    dataUxxi.check_modules_uxxi (df_data_to_btt, process_folder, process_code, v_main_process_planning)
    df_relacion_plan_module = dataUxxi.check_planes_modules (df_data_to_btt, process_folder, process_code) 
    


    
    #AO ADICIONAR FICHEIROS VERIFICAR SE HÁ DADOS PARA CONTINUAR O PROCESSO.
    
    dataCredUxxi.update_data_to_btt (df_planning_grouped_by_conector)
    
    ## ADD CREDIT MODEL Weeks
    df_data_import, df_asignatura_sin_model_credit_weeks = dataCredUxxi.add_model_module_credit_section_conector(df_planning_grouped_by_conector, df_model_credits_weeks)
    dataUxxi.create_file_validation_module_credits (df_asignatura_sin_model_credit_weeks,v_sheet_section_sin_credit_weeks, process_folder, process_code, v_process_manage_data)
    df_data_import = dataCredUxxi.select_weeks_by_typologie(df_data_import)
    df_data_import, df_data_without_weeks = dataCredUxxi.check_week_typologie_not_null(df_data_import)
    dataUxxi.create_file_validation_module_credits (df_data_without_weeks,v_sheet_section_sin_type_weeks, process_folder, process_code, v_process_manage_data)
    ## ADD CREDIT MODEL HOURS
    df_data_import, df_data_without_hours =  dataCredUxxi.add_hours_credits_model(df_data_import, df_model_credits_hours)
    dataUxxi.create_file_validation_module_credits (df_data_without_hours,v_sheet_section_sin_credit_hours, process_folder, process_code, v_process_manage_data)

    df_data_import = dataCredUxxi.manage_values_weeks(df_data_import)##COMO É DADO DE ENTRADA DE USUARIO(GESTÂO MANUAL) NECESSARIO TRATAR DADOS
    df_data_import = dataCredUxxi.replace_number_weeks_hoja_model_by_number_weeks_hoja_criterios_defecto (df_data_import)
    df_data_import = dataCredUxxi.hours_weeks_section(df_data_import)
    df_data_import = dataUxxi.add_groups_bullet_and_number_students(df_data_import)


    ## INSERIR CARGA COM HORAS RESTANTES (BEGIN) ##

    # if manage_weekly_weekload:
    
    #     df_data_import = dataUxxi.add_new_w_load_rest_hours(df_data_import)

    # else:

    #     df_data_import[v_week_load_type] = v_week_load_unique

    ## INSERIR CARGA COM HORAS RESTANTES (END) ##

    
    df_data_import = dataUxxi.create_conector_uxxi(df_data_import)
    df_data_import = rulesBest.filter_fiels_w_loads (df_data_import)
    df_data_import = rulesBest.insert_name_section(df_data_import)
    df_data_import = rulesBest.insert_name_wload (df_data_import)
    df_data_import = rulesBest.agg_section_to_w_load(df_data_import)
    df_data_import = rulesBest.count_sectiones_number(df_data_import)

    if manage_weekly_weekload:
    
        df_data_import = dataUxxi.add_new_w_load_rest_hours(df_data_import)

    dataUxxi.create_df_w_loads_to_file (df_data_import, process_folder, process_code, v_process_manage_data)

    return(df_data_import, df_relacion_plan_module)