import PackValidations.settings_validation_functions as settValFunct
import PackValidations.data_uxxi_validation as dataValFunct
import PackInterface.states_objects_windows as stateObj
import PackInterface.ini_user_window as iniciateUserWindow
from PackLibrary.librarys import (
    messagebox,
    traceback,
    )
from PackInterface.global_object_window import (
    main_window
)

from mod_variables import *


def validation_settings_steps():


    try:

    
        # - GET DATA INSERTED UI - #
        opcion_process_to_ejecute, name_file_uxxi, name_process_to_import,begin_date_export_csv, end_date_export_csv = settValFunct.get_inserted_values_settings()
        
        global gl_opcion_process_to_ejecute
        gl_opcion_process_to_ejecute = opcion_process_to_ejecute
        global gl_name_file_uxxi
        gl_name_file_uxxi = name_file_uxxi
        global gl_name_process_to_import
        gl_name_process_to_import = name_process_to_import
        global gl_begin_date_export_csv
        gl_begin_date_export_csv = begin_date_export_csv
        global gl_end_date_export_csv
        gl_end_date_export_csv = end_date_export_csv


    


        # - Verify Folder to Insert Data From UXXI
        settValFunct.validation_folder_uxxi()

        if opcion_process_to_ejecute == 0:

            # Validation Data UXXI (insercion UI)
            box_to_validate = 'boxManageData'
            settValFunct.check_filling_entry_box(name_file_uxxi)
            settValFunct.check_extension_file(name_file_uxxi)
            settValFunct.validation_data_uxxi_exist_on_folder(name_file_uxxi)

            # Validation Data UXXI (file)
            dataValFunct.verify_sheet_and_columns_name_file_uxxi(name_file_uxxi)



        if (opcion_process_to_ejecute == 1):

            #ENVOLVE A IMPORTAÇÃO DE EVENTO -- AUTENTICAÇÃO LEGACY:

            
            iniciateUserWindow.start_window_user_credential()

            box_to_validate = 'boxImportData'
            settValFunct.check_filling_entry_box(name_process_to_import)
            settValFunct.validation_process_exist_on_folder(name_process_to_import)


        if (opcion_process_to_ejecute == 2):

            box_to_validate = 'boxDates'


        # After all Validation

        stateObj.enable_button_start()
        stateObj.disable_button_submit()

        #  All Opciones Disables

        stateObj.all_opciones_disables_after_submit()

        



        # Focus on Main Window
        main_window.wm_state('normal')
        

    
    except settValFunct.ValidationFolderDataUxxi:

        messagebox.showerror('Validation Folder', 'Created Folder ' + v_folder_data_uxxi + ' to Insert UXXI Files !!')
    
    except settValFunct.FileNameNotInserted:

        if (box_to_validate == 'boxManageData'):

            messagebox.showerror('Validation File', 'Fill box Data UXXI to submit !!')

        if (box_to_validate == 'boxImportData'):

            messagebox.showerror('Validation File', 'Fill box Process ID to submit !!')

    except settValFunct.FileNameErrorExtensionXlsx as e:

        file_name = e.error_value
        messagebox.showerror('Validation File', 'File ' + file_name + ' must have a .xlsx extension !!')

    except settValFunct.FileDataUxxiNotInserted:

        messagebox.showerror('Validation Folder', name_file_uxxi + ' not inserted on folder ' + v_folder_data_uxxi + ' !!')


    except dataValFunct.ErrorSheetFileGeneral:  

        messagebox.showerror('Check Data UXXI', 'Mandatory Sheet Name:\n\n' + v_sheet_data_uxxi)

    except dataValFunct.WrongColumsGeneral:  
        
        columns_file = v_id_code + '-' + v_course_code + ' - ' + v_course_name + ' - ' +   v_year + ' - ' + v_mod_code + ' - ' + v_mod_name + '\n' +  \
                       v_mod_typologie + ' - ' + v_student_group + ' - ' +   v_activity_code + ' - ' + v_student_group_code + ' - ' + v_week_begin + '\n'  + \
                       v_week_end + ' - ' + v_day + ' - ' +   v_hourBegin_split + ' - ' + v_minute_begin_split + ' - ' + v_hourEnd_split + '\n' + \
                       v_minute_end_split + ' - ' + v_duration + ' - ' +   v_students_number + '\n' + \
                       v_mod_modalidad +  ' - '+ v_classroom_code + ' - ' + v_classroom_name + ' - ' + v_id_classroom_uxxi
        messagebox.showerror('Check Data UXXI', 'Possible COLUMNS NAME:\n\n' + columns_file)

    

    except settValFunct.ValidationFolderUpdateData as e:

        data_process_code = e.error_value

        message_info_config = 'DataProcess = '  + data_process_code 
                       

        messagebox.showerror('DataProcess', 'Verify if Process Code Exist:\n' + message_info_config)

    except:
        
        messagebox.showerror('ERROR', 'If error persist please contact:\n\ninfo@bulletsolutions.com')

        #Only to debug
        print (traceback.format_exc())
    return()