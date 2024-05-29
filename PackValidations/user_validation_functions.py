from PackInterface.global_object_window import (
    names_inserted_vars
)
from PackLibrary.librarys import (
    os,
    cp
)
from mod_variables import *


# validation_folder_ConfigApi()
class ValidationFolderConfigApi(Exception):
    pass


class NoAccessToUsers(Exception):
    pass

class ForbidenAccess(Exception):
    pass

# validation_config_exist_on_folder()
class FileConfigNotInserted(Exception):
    pass 

# validation_config_exist_on_folder()
class InvalidCredentials(Exception):
    pass

class UserNotAdmin (Exception):
    pass

def get_inserted_values_user():

    user_name = names_inserted_vars[4].get()
    user_credential = names_inserted_vars[5].get()
    

    return (user_name, user_credential)

def check_filling_user_box (user_name : str, user_credential : str):

    if (user_name == '') | (user_credential == ''):
        raise InvalidCredentials



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

