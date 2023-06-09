from PackInterface.global_object_window import (
    names_inserted_vars,
    radio_button_vars
)

from PackLibrary.librarys import (
    os,
    cp
)
from mod_variables import *


### -- Exceptiones Classes from Functiones -- ###: 

# validation_folder_uxxi()
class ValidationFolderDataUxxi(Exception):
    pass

# validation_folder_update_data_to_import()
class ValidationFolderUpdateData(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

# check_filling_entry_box()
class FileNameNotInserted (Exception):
    pass

# validation_data_uxxi_exist_on_folder()
class FileDataUxxiNotInserted (Exception):
    pass

# validation_folder_ConfigApi()
class ValidationFolderConfigApi(Exception):
    pass


# check_extension_file()
class FileNameErrorExtensionXlsx(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

# validation_config_exist_on_folder()
class FileConfigNotInserted(Exception):
    pass 

# Algumas das Validações de Config associadas a ConfigParser !!! (não necessitam de estar defenidas)

### -- Functiones -- ###


## - Get Data Inserted - ##

def get_inserted_values_settings():

    opcion_process_to_ejecute = radio_button_vars[0].get()
    name_file_uxxi = radio_button_vars[0].get()
    name_process_to_import = radio_button_vars[1].get()
    begin_date_export_csv = radio_button_vars[2].get()
    end_date_export_csv = names_inserted_vars[3].get()
    

    return (opcion_process_to_ejecute, name_file_uxxi, name_process_to_import,begin_date_export_csv, end_date_export_csv)

    

# - Validation Data UXXI - # 

def validation_folder_uxxi():

    check_directory = './' + v_folder_data_uxxi

    if not os.path.isdir(check_directory):
        
        os.mkdir(check_directory)
        raise ValidationFolderDataUxxi

def check_filling_entry_box(name_file_inserted : str):

    if (name_file_inserted == ''):
        raise FileNameNotInserted ()

def check_extension_file(name_file : str):

    file_extension = name_file.split('.')[-1]
    
    if (file_extension != 'xlsx'):
        raise FileNameErrorExtensionXlsx(name_file)
    
def validation_data_uxxi_exist_on_folder(file_inserted):

    path_to_file_config = './' + v_folder_data_uxxi + '/' + file_inserted
    if not os.path.exists(path_to_file_config):
        raise FileDataUxxiNotInserted




# - Validacion Config File - # 

def validation_folder_config_api():
    
    check_directory = './' + v_folder_config_api

    if not os.path.isdir(check_directory):
        
        os.mkdir(check_directory)
        raise ValidationFolderConfigApi

def validation_config_exist_on_folder():

    path_to_file_config = './' + v_folder_config_api + '/' + v_file_name_config
    if not os.path.exists(path_to_file_config):
        raise FileConfigNotInserted
    
def validation_and_file_config_and_get_variables ():

    # If Config file not configurated raise excepciones from Confiparser

    #Manage Config File
    conf = cp.RawConfigParser()   
    path = './ConfigAPI/config.txt'
    conf.read(path) 

    # URL's
    url_identity = conf.get(v_header_urls, v_url_identiy)
    url_api = conf.get(v_header_urls, v_url_api)
    # Credenciais API
    client_id = conf.get(v_header_credentiales, v_client_id)
    client_secret = conf.get(v_header_credentiales, v_client_secret)

    return(url_api, url_identity, client_id, client_secret)

    
# - Validacion Import Data - # 

def validation_process_exist_on_folder (process_name_inserted : str):

    code_process_verify_split  = process_name_inserted.split('_')

    if len (code_process_verify_split) >= 3: 
    
        code_process = '_' + process_name_inserted.split('_')[1] + '_' + process_name_inserted.split('_')[2]
    

        file_name_update = v_file_curriculum_to_import + code_process + '.xlsx'

        path_to_file_config = './' + v_main_folder_process + '/' + process_name_inserted + '/' + v_process_update_data + '/' + \
                            file_name_update
        if not os.path.exists(path_to_file_config):
            raise ValidationFolderUpdateData (process_name_inserted)
        
    else:
        raise ValidationFolderUpdateData (process_name_inserted)


