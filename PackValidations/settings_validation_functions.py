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

# check_filling_entry_box()
class FileNameNotInserted (Exception):
    pass

# validation_data_uxxi_exist_on_folder()
class FileDataUxxiNotInserted (Exception):
    pass

# validation_folder_ConfigApi()
class ValidationFolderConfigApi(Exception):
    pass

# present_on_ui_opciones_process()
class OpcionesProcessOnUI(Exception):
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

    name_file_inserted = names_inserted_vars[0].get()
    opcion_manage_data = radio_button_vars[0].get()
    opcion_update_data = radio_button_vars[1].get()
    opcion_import_data = radio_button_vars[2].get()
    

    return (name_file_inserted, opcion_manage_data, opcion_update_data,opcion_import_data)


# - Validation Variables Process - # 

def present_on_ui_opciones_process(opcion_manage_data : int, opcion_import_data : int):
    
    if ((opcion_manage_data == 0) & (opcion_import_data == 0)):

        raise OpcionesProcessOnUI
    

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


    



