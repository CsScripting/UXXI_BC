import PackManageData.main_manage_data_uxxi as managData
import PackUpdateData.main_update_data as updateData
import PackImportData.main_import_data as importData
import PackUpdateSchedules.main_update_schedules as updateSchedules
import PackExportCsv.main_export_csv as exportCsv
import PackConector.main_add_conector as addConect





def exe_process_steps (gl_opcion_process_to_ejecute : int, gl_name_file_uxxi: str,
                       gl_name_process_to_import : str, gl_event_type_process : str, gl_date_last_update : str, gl_check_opcion_process : int, gl_opcion_conector : int):

    valid_process = False

    # OPCIONES gl_opcion_process_to_ejecute:

    # Check Data: 0
    # Import: 1
    # Export: 2

    ### Estados Eventos:
    
    # UXXI --> Implica que ja esta atualizado na duas Ferramentas
    # BWP --> Novos Eventos Onde foi Inserido conector desde este processo
    # BWP_To_UXXI_Updated (Estado Temporario --> Apenas quando envia horarios a UXXI --> Fica neste estado) --> Eventos Provenientes de UXXI
    # BWP_To_UXXI_Inserted (Estado Temporario --> Apenas quando envia horarios a UXXI --> Fica neste estado) --> Eventos Novos Criados no BWP
    # Sem Conector 


    if gl_opcion_process_to_ejecute == 0:

        first_week_schedules, last_week_schedules, df_info_events, df_events_import  = managData.manage_data_uxxi_steps(gl_name_file_uxxi)

        #UPDATE DATA -- RELATIVO A ENTIDADES DE HORARIOS --> Importante Update de Dados e não de Horarios !!!
        updateData.update_data_steps(first_week_schedules, last_week_schedules, df_info_events,df_events_import)

    if gl_opcion_process_to_ejecute == 1:

        # Processo dependente se é primeira importação HORARIOS UXXI

        if (gl_check_opcion_process == 1) & (gl_check_opcion_process ==1): #First Import

            # Importa dados Relativos a Horarios de Processo Executado Anteriormente:
            importData.import_data_steps(gl_name_process_to_import)

        elif (gl_check_opcion_process == 1) & (gl_check_opcion_process ==0): # Update de Horarios Já Existentes --> Update relativo a Conectores que recebe de UXXI

            # Atualiza Conectores(por causa de novos ID's de Base de dados de UXXI)
            # Podem ter sido enviados eventos para UXXI, por CSV de processo abaixo, que agora tem novos ID's
            
            # Dois Tipos de Conector que Procura PROCESSO:
            # BWP_To_UXXI_Updated" ---> ESTADO "UXXI" 
            # BWP_To_UXXI_Inserted" ---> ESTADO "UXXI" 

            updateSchedules.update_schedules_steps(gl_name_process_to_import)
            
        else: # Inserção de Conectores de Eventos Provenientes BTT

            addConect.add_conector_steps(gl_name_process_to_import) # VARIAVEL ENVIADA PODE GUARDAR NOME DE PROCESSO A EXECUTAR ou NOME DE ANO ACADEMICO


    if gl_opcion_process_to_ejecute == 2:

        
        # CASO 1:
        # "BWP"  ---> ESTADO "BWP_To_UXXI_Insert" --> Cria CSV
            
        # CASO 2:
        #EVENTOS COM UPDATE...ESTADO "UXXI":
        # ESTADO "UXXI"  ---> ESTADO "BWP_Updated_UXXI" --> Cria CSV

        # CASO 3:
        # BWP_To_UXXI_Update --> Cria CSV

        # CASO 4:
        # BWP_To_UXXI_Insert --> Cria CSV


        # Neste Momento Está EXPORTAR por Acad. Year --- > NO FUTURO FAZER POR TIPO DE EVENTO !!
        exportCsv.export_csv_steps(gl_event_type_process, gl_date_last_update, gl_check_opcion_process) ## EM METODO VERIFICA SE PRIMEIRA IMPORTAÇÂO OU NÂO # VALIDAR PROCESSO DE DATA


    valid_process = True

    return (valid_process)