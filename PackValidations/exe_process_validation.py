import PackManageData.main_manage_data_uxxi as managData
import PackUpdateData.main_update_data as updateData
import PackImportData.main_import_data as importData
import PackExportCsv.main_export_csv as exportCsv





def exe_process_steps (gl_opcion_process_to_ejecute : int, gl_name_file_uxxi: str,
                       gl_name_process_to_import : str, gl_academic_year_process : str, date_last_update : str):

    valid_process = False

    if gl_opcion_process_to_ejecute == 0:

        first_week_schedules, last_week_schedules, df_info_events, df_events_import  = managData.manage_data_uxxi_steps(gl_name_file_uxxi)

        updateData.update_data_steps(first_week_schedules, last_week_schedules, df_info_events,df_events_import)

    if gl_opcion_process_to_ejecute == 1:

        process_import = 'Insert'

        if process_import == 'Insert':

            importData.import_data_steps(gl_name_process_to_import)

        else:

            print('Efectuar Processo Update')



    if gl_opcion_process_to_ejecute == 2:

        exportCsv.export_csv_steps(gl_academic_year_process, date_last_update)
        
        

    valid_process = True

    return (valid_process)