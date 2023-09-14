import PackControllerRequest.event_request as eventRequest
import PackManageApi.glogal_variable_process_request as gl_v_request
import PackDfFromJson.EventsDf as eventDf
import PackGeneralProcedures.global_variable_process_procedures as glVarProcess
import PackExportCsv.folders_process_export_csv as folderProcessCsv

import PackManageData.bussiness_rules_uxxi as rulesUXXI

from mod_variables import *

from PackLibrary.librarys import (	
  DataFrame
)


def export_csv_steps(first_week_schedules : str, last_week_schedules : str):
    
    # Create Folder Process
    glVarProcess.gl_process_folder, glVarProcess.gl_process_code = folderProcessCsv.create_csv_folder_export_process()

    events_best = eventRequest.get_events_all(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_event_controller, first_week_schedules, last_week_schedules)

    df_events_best = eventDf.events_df_from_json(events_best)

    ## format CSV ###

    rulesUXXI.create_format_csv_uxxi(df_events_best, glVarProcess.gl_process_folder, glVarProcess.gl_process_code) 


    return()