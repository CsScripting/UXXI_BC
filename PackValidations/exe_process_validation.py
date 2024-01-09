import PackManageData.main_manage_data_uxxi as managData
import PackUpdateData.main_update_data as updateData
import PackImportData.main_import_data as importData
import PackUpdateSchedules.main_update_schedules as updateSchedules
import PackExportCsv.main_export_csv as exportCsv





def exe_process_steps (gl_opcion_process_to_ejecute : int, gl_name_file_uxxi: str,
                       gl_name_process_to_import : str, gl_academic_year_process : str, gl_date_last_update : str, gl_check_opcion_first_import : int):

    valid_process = False

    if gl_opcion_process_to_ejecute == 0:

        first_week_schedules, last_week_schedules, df_info_events, df_events_import  = managData.manage_data_uxxi_steps(gl_name_file_uxxi)

        #UPDATE DATA -- RELATIVO A ENTIDADES DE HORARIOS
        updateData.update_data_steps(first_week_schedules, last_week_schedules, df_info_events,df_events_import)

    if gl_opcion_process_to_ejecute == 1:

        if gl_check_opcion_first_import == 1:

            importData.import_data_steps(gl_name_process_to_import)

        else:

            updateSchedules.update_schedules_steps(gl_name_process_to_import)
            
            # DOIS PROCESSOS:

            # CASO 1 # UPDATE CONECTOR DE EVENTOS SEM CONECTOR --- Procura sem Conector e Atribui ESTADO "BWP"
            # ESTADO "Conector em Branco" --->  ESTADO "BWP"
            # VERIFICAÇÂO EM FICHEIRO DE CONECTORES


            # CASO 2 # UPDATE DE EVENTOS ENVIADOS A UXXI QUE AINDA NÂO TEM ID de BASE DADOS DE UXXI 
            # ESTADO "BWP_UXXI" ---> ESTADO "UXXI"
            # VERIFICAÇÂO EM FICHEIRO DE HORARIOS

            ### Estado BWP  


    if gl_opcion_process_to_ejecute == 2:

        exportCsv.export_csv_steps(gl_academic_year_process, gl_date_last_update, gl_check_opcion_first_import)

        # NO MOMENTO DE EXPORT CSV:
        
        # DOIS PROCESSOS
        
        # CASO 1 # EVENTOS COM UPDATE...ESTADO UXXI:
        # ESTADO UXXI  ---> ESTADO "BWP_UXXI"

        # CASO 2 # EVENTOS COM ESTADO BWP :
        # ESTADO BWP  ---> ESTADO "BWP_UXXI"
        
        

    valid_process = True

    return (valid_process)