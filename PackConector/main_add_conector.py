import PackImportData.folders_process_import as folderImport
import PackGeneralProcedures.files as genFiles
import PackGeneralProcedures.global_variable_process_procedures as glVarProcess
import PackConector.manage_data_conector as dataConect
import PackControllerRequest.event_request as eventRequest
import PackManageApi.global_variable_process_request as gl_v_request
import PackDfFromJson.EventsDf as eventDf
import PackRulesDataUxxiBest.main_rules_data_uxxi_best as rulesUxxiBest
import PackManageData.bussiness_rules_best as rulesBest
import PackUpdateSchedules.update_schedules_functions as updateSched
from PackLibrary.librarys import (
    messagebox
    )


from mod_variables import *

def add_conector_steps (name_academic_year):

    #CRIAR PASTA CONECTOR
    path_folder_conector, id_process = folderImport.create_folder_add_conectores()
    
    #LER FICHEIRO UXXI CONECTORES
    df_conect = genFiles.read_file_conectores()

    #EXCLUIR VALORES NULOS DE FICHEIRO DE CONECTORES (PARA NÂO DAR PROBLEMAS NO GROUP BY)

    df_conect = genFiles.filter_file_no_null_values(df_conect)
 

    df_conect_to_agg = df_conect.copy()


    #AGREGAR CONECTORES COMUNS
    df_conect_agg = dataConect.verify_common_conect(df_conect_to_agg) 

    #GUARDAR EM FICHEIRO CONECTORES COMUNS ??
    ## Verificar se será necessarios
    

    #EXPORTAR EVENTOS DE SISTEMA
    events_best = eventRequest.get_events_all(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_event_controller, 
                                              glVarProcess.gl_begin_date_acad_year, glVarProcess.gl_end_date_acad_year)
    
    df_events_best = eventDf.parse_list_events_to_df (events_best, process_update=True)


    #FILTRAR EVENTOS ADD CONECTOR:
    #1º# - FITRAR POR EVENTOS COM CONECTOR == ''  EM JSON EMPTY STRING
    df_events_best = rulesUxxiBest.filter_event_empty_conect(df_events_best)

    #2º# - PASSAR EMPTY LIST TO nan

    df_events_best = rulesUxxiBest.pass_empy_list_to_nan(df_events_best)
    

    #3º# - AO IR BUSCAR EVENTOS FILTRA POR DATAS DE ACAD. YEAR:
    # NO ENTANTO PODE SACAR EVENTOS QUE NÂO ESTÂO ASSOCIADOS A ACAD. YEAR
    # FILTRAR AINDA POR ACADEMIC YEAR ???

    #4º# - FILTRA POR ELEMENTOS OBRIGATORIOS QUE TEM DE FIGURAR EM UXXI
    # GRUPO NÂO é OBRIGATORIO MAS SERÁ CONSIDERADO
    # PODE ADICIONAR CONECTOR NO CASO DE NÂO TER SALA

    df_events_best, df_invalid_fields_events_best = rulesUxxiBest.filter_data_best_mandatory_fields(df_events_best)
    df_invalid_fields_events_best = rulesUxxiBest.manage_file_error_conector(df_invalid_fields_events_best,v_conect_sin_fields)


    #5º# FILTRAR POR TIPOLOGIA UNICA ou Sem Tipologia

    df_events_best, df_invalid_typologiy_events_best = rulesUxxiBest.verify_unique_typology_event(df_events_best)
    df_invalid_typologiy_events_best = rulesUxxiBest.manage_file_error_conector(df_invalid_typologiy_events_best, v_conect_wrong_typologie)
    

    #6º# VERIFICAR PADRÂO NOME SECTION

    df_events_best, df_invalid_section_events_best = rulesUxxiBest.verify_name_section(df_events_best)
    df_invalid_section_events_best = rulesUxxiBest.manage_file_error_conector(df_invalid_section_events_best, v_conect_wrong_section_name)





    if not df_events_best.empty:

        df_events_best_to_add_conector, df_invalid_no_conector_events_best = rulesUxxiBest.add_conector_from_file_uxxi(df_events_best, df_conect)

        
        df_events_best_to_add_conector = rulesUxxiBest.update_file_columns_and_parse_data_to_filter (df_events_best_to_add_conector)
        df_invalid_section_events_best = rulesUxxiBest.manage_file_error_conector(df_invalid_section_events_best, v_conect_without_conector_uxxi)

        df_events_best_to_add_conector = rulesBest.add_number_week(df_events_best_to_add_conector)
        df_events_best_to_add_conector= updateSched.select_columns_update_conector(df_events_best_to_add_conector)
        df_events_best_to_add_conector = rulesBest.add_event_connector_json(df_events_best_to_add_conector, v_app_bwp)
    

        
        updateSched.iterate_events_and_update_single_event(df_events_best_to_add_conector)

        df_errores_conect = rulesUxxiBest.create_df_errores_conect(df_invalid_fields_events_best,
                                                                   df_invalid_section_events_best,
                                                                   df_invalid_typologiy_events_best,
                                                                   df_invalid_no_conector_events_best)
        

        genFiles.create_file_xlsx(df_errores_conect,
                                  path_folder_conector + '/'+ v_name_file_error_conect + id_process + '.xlsx', 
                                  v_sheet_error_conect)
        
        
    else:

        df_errores_conect = rulesUxxiBest.create_df_errores_conect(df_invalid_fields_events_best,
                                                                   df_invalid_section_events_best,
                                                                   df_invalid_typologiy_events_best,
                                                                   df_events_best)
        

        genFiles.create_file_xlsx(df_errores_conect,
                                  path_folder_conector,
                                  v_name_file_error_conect + id_process + '.xlsx', 
                                  v_sheet_error_conect)

        messagebox.showerror('Add Conector', 'No Events To Insert Connector')

    

    return()