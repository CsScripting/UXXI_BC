import PackControllerRequest.event_request as eventRequest
import PackControllerRequest.academic_year_request as acadYearRequest
import PackControllerRequest.controller_dto as dtObj
import PackManageApi.global_variable_process_request as gl_v_request
import PackDfFromJson.EventsDf as eventDf
import PackGeneralProcedures.global_variable_process_procedures as glVarProcess
import PackExportCsv.folders_process_export_csv as folderProcessCsv
import PackManageData.bussiness_rules_best as rulesBest

import PackManageData.bussiness_rules_uxxi as rulesUXXI
import PackRulesExport.bussiness_rules_export as rulesExport




from mod_variables import *

from PackLibrary.librarys import (	
  DataFrame
)


def export_csv_steps(academic_year : str, last_date_update : str):
    
  #Manage ---> First CSV or Update CSV

  if last_date_update == 'yyyy-mm-dd':

    first_csv = True

  else:
      
    first_csv = False

  # Create Folder Process
  glVarProcess.gl_process_folder, glVarProcess.gl_process_code = folderProcessCsv.create_csv_folder_export_process()

  # Get DATES ACADEMIC YEAR


  data_object_search = dtObj.create_dto_simple_search_filter (v_search_name, academic_year)

  first_week_schedules, last_week_schedules = acadYearRequest.get_data_academic_year_search (gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_acad_year_controller, data_object_search)

  events_best = eventRequest.get_events_all(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_event_controller, first_week_schedules, last_week_schedules)

  # df_events_best = eventDf.events_df_from_json(events_best)
  df_events_best = eventDf.parse_list_events_to_df (events_best)

  df_events_best = rulesExport.filter_by_acad_year(df_events_best, academic_year)
  df_events_best =  rulesExport.manage_conector_id_parse_to_dict (df_events_best)
  df_events_best = rulesExport.extract_values_conector_planificacion (df_events_best)

  if not first_csv:

      
      df_events_best = rulesExport.extract_values_conector_check_update (df_events_best)

      #Verificar Formato de conector ...
      # Só para o caso de Utilizador poder fazer alterações ao nivel de Conector.


      ## Add Number Weeks to MATCH CONECTOR

      df_events_best = rulesBest.add_number_week(df_events_best)
      df_events_best = rulesExport.verify_updated_events(df_events_best)
      df_events_best, need_update = rulesExport.filter_events_need_update (df_events_best)


      if need_update:

        #ATRIBUIR VALORES COM UPDATE PARA ENVIAR A UXXI
        df_events_best = rulesExport.filter_to_reasign_values_id_uxxi_to_send_uxxi (df_events_best)
        df_events_best = rulesExport.extract_values_conector_planificacion (df_events_best)
        df_events_best = rulesExport.reasign_values_id_uxxi_to_send_uxxi (df_events_best)

        ## format CSV ###
        df_manage_id_uxxi_to_delete = df_events_best.copy()
        

        rulesUXXI.create_format_csv_uxxi(df_events_best, glVarProcess.gl_process_folder, glVarProcess.gl_process_code,first_csv) 

        rulesExport.extract_id_bd_to_delete(df_manage_id_uxxi_to_delete, glVarProcess.gl_process_folder)
       

      
      else:
        
        print ('SinUpdates')

  else:
      
      ## format CSV ###
      rulesUXXI.create_format_csv_uxxi(df_events_best, glVarProcess.gl_process_folder, glVarProcess.gl_process_code,first_csv) 



  return()