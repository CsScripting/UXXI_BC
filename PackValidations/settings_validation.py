import PackValidations.settings_validation_functions as settValFunct
import PackValidations.data_uxxi_validation as dataValFunct
import PackInterface.states_objects_windows as stateObj
import PackManageApi.get_token as getToken
import PackControllerRequest.GeneralRequests as genRequest
from PackLibrary.librarys import (
    messagebox,
    traceback,
    OAuth2Session,
    oauthlib, 
    requests
    )
from PackInterface.global_object_window import (
    main_window
)

from mod_variables import *

import PackManageApi.glogal_variable_process_request as glRequest

def validation_settings_steps():


    try:

    
        # - GET DATA INSERTED UI - #
        name_file_inserted, opcion_manage_data,opcion_update_data, opcion_import_data = settValFunct.get_inserted_values_settings()
        
        global gl_name_file_inserted 
        gl_name_file_inserted = name_file_inserted
        global gl_opcion_manage_data
        gl_opcion_manage_data = opcion_manage_data
        global gl_opcion_update_data
        gl_opcion_update_data = opcion_update_data
        global gl_opcion_import_data
        gl_opcion_import_data = opcion_import_data

        global check_conexion_type
        check_conexion_type = 'IS'

        
        # Opcions Process:
        settValFunct.present_on_ui_opciones_process(opcion_manage_data, opcion_import_data)

        # - Verify Folder to Insert Data From UXXI
        settValFunct.validation_folder_uxxi()

        # Values Opciones Radio Button (Selected - 1 ; Not Selected - 0 )
        if opcion_manage_data == 1:

            # Validation Data UXXI (insercion UI)
            # settValFunct.check_filling_entry_box(name_file_inserted)
            # settValFunct.check_extension_file(name_file_inserted)
            # settValFunct.validation_data_uxxi_exist_on_folder(name_file_inserted)

            # Validation Data UXXI (file)
            # dataValFunct.verify_sheet_and_columns_name_file_uxxi(name_file_inserted)

            print ('PassManageData')


        if (opcion_update_data == 1) | (opcion_import_data == 1): 
    
            settValFunct.validation_folder_config_api()
            settValFunct.validation_config_exist_on_folder()
            
            #Extract Variables API To Check Conexion
            url_api, url_identity, client_id, client_secret = settValFunct.validation_and_file_config_and_get_variables()

            value_token = getToken.get_token_identity(url_identity, client_id, client_secret)
            header_request = getToken.create_header_request (value_token)

            glRequest.gl_url_api = url_api
            glRequest.gl_header_request = header_request

            # colocar na validação se a chamada é a API ou ao IDentity......para mais tarde....A excepção será a mesma

            check_conexion_type = 'API'
            genRequest.get_entity_data(url_api, header_request, v_acad_term_controller)

        stateObj.enable_button_start()

        # Focus on Main Window
        main_window.wm_state('normal')
        

              

    except settValFunct.OpcionesProcessOnUI:

        message_info_process = 'Select Valid Opciones To Submit:\n\n' \
                       ' Opcion 1: \n' \
                       '  - Insert File Name;\n' \
                       '  - Select Manage Data;\n'\
                       '  - Select Update Data (Opcional);\n'\
                       '  - Select Import Data (Opcional).\n\n'\
                       ' Opcion 2: \n' \
                       '  - Only Select Import Data;\n'\
                       '  - Insert Process Folder already executed with Folder Update.\n'\


        messagebox.showinfo('Info Process', message_info_process)
    
    except settValFunct.ValidationFolderDataUxxi:

        messagebox.showerror('Validation Folder', 'Created Folder ' + v_folder_data_uxxi + ' to Insert UXXI Files !!')
    
    except settValFunct.FileNameNotInserted:

        messagebox.showerror('Validation File', 'Fill box Data UXXI to submit !!')

    except settValFunct.FileNameErrorExtensionXlsx as e:

        file_name = e.error_value
        messagebox.showerror('Validation File', 'File ' + file_name + ' must have a .xlsx extension !!')

    except settValFunct.FileDataUxxiNotInserted:

        messagebox.showerror('Validation Folder', name_file_inserted + ' not inserted on folder ' + v_folder_data_uxxi + ' !!')


    except dataValFunct.ErrorSheetFileGeneral:  

        messagebox.showerror('Check Data UXXI', 'Mandatory Sheet Name:\n\n' + v_sheet_data_uxxi)

    except dataValFunct.WrongColumsGeneral:  
        
        columns_file = v_course_code + ' - ' + v_course_name + ' - ' +   v_year + ' - ' + v_mod_code + ' - ' + v_mod_name + '\n' +  \
                       v_mod_typologie + ' - ' + v_student_group + ' - ' +   v_activity_code + ' - ' + v_student_group_code + ' - ' + v_week_begin + '\n'  + \
                       v_week_end + ' - ' + v_day + ' - ' +   v_hourBegin_split + ' - ' + v_minute_begin_split + ' - ' + v_hourEnd_split + '\n' + \
                       v_minute_end_split + ' - ' + v_duration + ' - ' +   v_students_number
        
        messagebox.showerror('Check Data UXXI', 'Possible COLUMNS NAME:\n\n' + columns_file)

    except settValFunct.ValidationFolderConfigApi:

        messagebox.showerror('Validation Folder', 'File config.txt not inserted on folder ' + v_folder_config_api + ' !!')

    except settValFunct.FileConfigNotInserted:

        messagebox.showerror('Validation Folder', 'File config.txt not inserted on folder ' + v_folder_config_api + ' !!')

    #error headers config
    except settValFunct.cp.NoSectionError:

        message_info_config = '\n[' + v_header_urls + ']\n\n'  + \
                       v_url_identiy + ' =\n'   + \
                       v_url_api + " =\n\n"  + \
                       '[' + v_header_credentiales + ']\n\n'  + \
                       v_client_id + ' =\n'  + \
                       v_client_secret + ' =\n\n' + \
                       "# Informacion: Names don't need " + "'' or " + '""' 
                       

        messagebox.showerror('Error config.txt', 'Format to config.txt (Folder ConfigAPI ):\n' + message_info_config)
    
    #error opciones config
    except settValFunct.cp.NoOptionError:

        message_info_config = '\n[' + v_header_urls + ']\n\n'  + \
                       v_url_identiy + ' =\n'   + \
                       v_url_api + " =\n\n"  + \
                       '[' + v_header_credentiales + ']\n\n'  + \
                       v_client_id + ' =\n'  + \
                       v_client_secret + ' =\n\n' + \
                       "# Informacion: Names don't need " + "'' or " + '""'
                       

        messagebox.showerror('Error config.txt', 'Format to config.txt (Folder ConfigAPI ):\n' + message_info_config)

    # error opciones(When Change line) config
    except settValFunct.cp.ParsingError:

        message_info_config = '\n[' + v_header_urls + ']\n\n'  + \
                       v_url_identiy + ' =\n'   + \
                       v_url_api + " =\n\n"  + \
                       '[' + v_header_credentiales + ']\n\n'  + \
                       v_client_id + ' =\n'  + \
                       v_client_secret + ' =\n\n' + \
                       "# Informacion: Names don't need " + "'' or " + '""'
                       

        messagebox.showerror('Error config.txt', 'Format to config.txt (Folder ConfigAPI ):\n' + message_info_config)
    
    
    # Errores Conection to Identity
    # Client Not Exist on Identity, or Secret not correct !!!
    except oauthlib.oauth2.rfc6749.errors.InvalidClientError:

        messagebox.showerror('Error Client IS', 'Check if: \n\n'+  ' - Client Id exist ;\n\n - Client Secret is correct.')
    
    except requests.exceptions.ConnectionError: 
         
        if check_conexion_type == 'IS':
         
            messagebox.showerror('Error URL IS', 'Check if URL ' + url_identity + ' is available !!')

        if check_conexion_type == 'API':
    
            messagebox.showerror('Error URL API', 'Check if URL ' + url_api + ' is available !!')

    except:
        
        messagebox.showerror('ERROR', 'If error persist please contact:\n\ninfo@bulletsolutions.com')

        #Only to debug
        print (traceback.format_exc())
    return()