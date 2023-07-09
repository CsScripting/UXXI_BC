import PackManageData.main_manage_data_uxxi as managData
import PackUpdateData.main_update_data as updateData
import PackImportData.main_import_data as importData
import PackExportCsv.main_export_csv as exportCsv

import PackManageApi.get_token as getToken
import PackControllerRequest.general_requests as genRequest




def exe_process_steps (gl_opcion_process_to_ejecute : int, gl_name_file_uxxi: str,
                       gl_name_process_to_import : str, gl_begin_date_export_csv : str, gl_end_date_export_csv : str):

    valid_process = False

    if gl_opcion_process_to_ejecute == 0:

        first_week_schedules, last_week_schedules, df_info_events, df_events_import  = managData.manage_data_uxxi_steps(gl_name_file_uxxi)

        updateData.update_data_steps(first_week_schedules, last_week_schedules, df_info_events,df_events_import)

    if gl_opcion_process_to_ejecute == 1:

        importData.import_data_steps(gl_name_process_to_import)

    if gl_opcion_process_to_ejecute == 2:

        exportCsv.export_csv_steps(gl_begin_date_export_csv, gl_end_date_export_csv)
        
        

    valid_process = True

    return (valid_process)