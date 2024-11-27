import PackValidations.user_validation_functions as userValFunct
import PackManageApi.get_token as getToken
import PackControllerRequest.general_requests as genRequest
import PackInterface.states_objects_windows as stateObj
import PackInterface.ini_settings_window as iniSett
import PackManageApi.global_variable_process_request as glRequest
import PackControllerRequest.controller_dto as dtObj

from PackLibrary.librarys import (
    messagebox,
    traceback,
    oauthlib, 
    requests,
    UnauthorizedClientError
    )

from mod_variables import *

def user_validation_steps ():

    
    try:

        # GET DATA USER

        user_name, user_credential= userValFunct.get_inserted_values_user()

        userValFunct.check_filling_user_box(user_name, user_credential)
        

        ## - VALIDAÇÃO DE DADOS CONFIG FILE

        # Begin Validation Connectivity CLIENT MACHINE #
        global check_conexion_type
        check_conexion_type = 'IS'

        userValFunct.validation_folder_config_api()
        userValFunct.validation_config_exist_on_folder()

        #Extract Variables API To Check Conexion
        url_api, url_identity, client_id, client_secret = userValFunct.validation_and_file_config_and_get_variables()

        value_token = getToken.get_token_identity_application_client(url_identity, client_id, client_secret)
        header_request = getToken.create_header_request (value_token)

        glRequest.gl_url_api = url_api
        

        # colocar na validação se a chamada é a API ou ao IDentity......para mais tarde....A excepção será a mesma

        check_conexion_type = 'API'
        genRequest.get_entity_data(url_api, header_request, v_acad_term_controller)

        # END Validation Connectivity API #

        # VERIFICAÇÃO CREDENCIAIS UTILIZADOR #

        value_token = getToken.get_token_identity_legacy(url_identity, client_id, client_secret,user_name, user_credential)
        header_request = getToken.create_header_request (value_token)

        glRequest.gl_url_api = url_api
        glRequest.gl_header_request = header_request

        #VERIFICAÇÃO se USER é ADMIN
        data_object_search = dtObj.create_dto_simple_search_filter (v_search_email, user_name)
        status_call, user_is_admin = genRequest.post_data_search_filter_user (url_api, header_request, v_user_controller,data_object_search)
        
        if status_call == 200:

            if user_is_admin:

                stateObj.closing_behavior_user_window()
                iniSett.start_settings_window()      

            else:

                raise userValFunct.UserNotAdmin
            
        elif status_call == 403:

            raise userValFunct.ForbidenAccess
            
        else:
           
           raise userValFunct.NoAccessToUsers



    except userValFunct.ValidationFolderConfigApi:

        messagebox.showerror('Validation Folder', 'File config.txt not inserted on folder ' + v_folder_config_api + ' !!')

    except userValFunct.FileConfigNotInserted:

        messagebox.showerror('Validation Folder', 'File config.txt not inserted on folder ' + v_folder_config_api + ' !!')

    except userValFunct.InvalidCredentials:

        messagebox.showerror('Sign In', 'Invalid Credentials !!')
        stateObj.closing_behavior_user_window()

    except userValFunct.NoAccessToUsers:

        messagebox.showerror('Sign In', 'Without Access to Users')
        stateObj.closing_behavior_user_window()

    except userValFunct.UserNotAdmin:

        messagebox.showerror('Sign In', 'Process Rules:\n\n' + 'User Must be Admin !!')
        stateObj.closing_behavior_user_window()


    except userValFunct.ForbidenAccess:

        messagebox.showerror('Sign In', 'Forbidden Access:\n\n' + 'ERROR 403')
        stateObj.closing_behavior_user_window()

    except UnauthorizedClientError as e:

        messagebox.showerror('Sign In', 'This is an UNAUTHORIZED CLIENT !!\n\n' + 'Verify in IDENTITY if client have on SETTINGS: \n\n' + 'Allowed Grant Types: password | client_credentiales' )
        stateObj.closing_behavior_user_window()

    


    #error headers config
    except userValFunct.cp.NoSectionError:

        message_info_config = '\n[' + v_header_urls + ']\n\n'  + \
                       v_url_identiy + ' =\n'   + \
                       v_url_api + " =\n\n"  + \
                       '[' + v_header_credentiales + ']\n\n'  + \
                       v_client_id + ' =\n'  + \
                       v_client_secret + ' =\n\n' + \
                       "# Informacion: Names don't need " + "'' or " + '""' 
                       

        messagebox.showerror('Error config.txt', 'Format to config.txt (Folder ConfigAPI ):\n' + message_info_config)
    
    #error opciones config
    except userValFunct.cp.NoOptionError:

        message_info_config = '\n[' + v_header_urls + ']\n\n'  + \
                       v_url_identiy + ' =\n'   + \
                       v_url_api + " =\n\n"  + \
                       '[' + v_header_credentiales + ']\n\n'  + \
                       v_client_id + ' =\n'  + \
                       v_client_secret + ' =\n\n' + \
                       "# Informacion: Names don't need " + "'' or " + '""'
                       

        messagebox.showerror('Error config.txt', 'Format to config.txt (Folder ConfigAPI ):\n' + message_info_config)

    # error opciones(When Change line) config
    except userValFunct.cp.ParsingError:

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

    except oauthlib.oauth2.rfc6749.errors.InvalidGrantError:

        messagebox.showerror('Sign In', 'Invalid Credentials !!')
        stateObj.enable_link_settings()
    
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