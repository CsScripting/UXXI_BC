from PackInterface.global_object_window import (
    names_inserted_vars,
    radio_button_vars
)

from PackLibrary.librarys import (
    os
)
from mod_variables import *


### -- Exceptiones Classes from Functiones -- ###: 

# validation_folder_uxxi()
class ValidationFolderDataUxxi(Exception):
    pass

class ValidationProcessId(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

class ValidationSubFolderDataProcess(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

# validation_folder_update_data_to_import()
class ValidationFilesSchedulesUpdateData(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

# check_filling_entry_box()
class FileNameNotInserted (Exception):
    pass

# validation_data_uxxi_exist_on_folder()
class FileDataUxxiNotInserted (Exception):
    pass

# validation_data_conectores_exist_on_folder()
class FileConectoresNotInserted (Exception):
    pass


# check_extension_file()
class FileNameErrorExtensionXlsx(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

# check_event_name_exist
class EventNameNotExist (Exception):
    pass



# Algumas das Validações de Config associadas a ConfigParser !!! (não necessitam de estar defenidas)

### -- Functiones -- ###


## - Get Data Inserted - ##

def get_inserted_values_settings():

    opcion_process_to_ejecute = radio_button_vars[0].get()
    name_file_uxxi = names_inserted_vars[0].get()
    name_process_to_import = names_inserted_vars[1].get()
    event_type_process = names_inserted_vars[2].get()
    date_last_update = names_inserted_vars[3].get()

    check_opcion_first_import = radio_button_vars[1].get()
    check_opcion_conector = radio_button_vars[2].get()

    check_opcion_main_process = radio_button_vars[3].get()


    

    return (check_opcion_main_process, opcion_process_to_ejecute, name_file_uxxi, name_process_to_import,
            event_type_process,date_last_update,check_opcion_first_import, check_opcion_conector)

    

# - Validation Data UXXI - # 

def validation_folder_uxxi():

    check_directory = './' + v_folder_data_uxxi

    if not os.path.isdir(check_directory):
        
        os.mkdir(check_directory)
        raise ValidationFolderDataUxxi
    
def validation_process_id(name_inserted):

    check_directory = './' + v_main_folder_process + '/' + name_inserted

    if not os.path.isdir(check_directory):
        
        raise ValidationProcessId(name_inserted)

    
def validation_sub_folder_data_process(id_process : str,subfolder:str):

    check_directory = './' + v_main_folder_process +'/' + id_process +  '/' + subfolder

    if not os.path.isdir(check_directory):
        
        raise ValidationSubFolderDataProcess(subfolder)



def check_filling_entry_box(name_file_inserted : str):

    if (name_file_inserted == ''):
        raise FileNameNotInserted ()

def check_extension_file(name_file : str):

    file_extension = name_file.split('.')[-1]
    
    if (file_extension != 'csv'):
        raise FileNameErrorExtensionXlsx(name_file)
    
def validation_data_uxxi_exist_on_folder(file_inserted):

    path_to_file_config = './' + v_folder_data_uxxi + '/' + file_inserted
    if not os.path.exists(path_to_file_config):
        raise FileDataUxxiNotInserted
    
def validation_conector_exist_on_folder ():

    path_to_file_conector = './' + v_folder_data_uxxi + '/' + v_file_conectores + '.xlsx'
    if not os.path.exists(path_to_file_conector):
        raise FileConectoresNotInserted


    
# - Validacion Import Data - # 

def validation_files_to_import_schedules (process_name_inserted : str):

    code_process_verify_split  = process_name_inserted.split('_')

    if len (code_process_verify_split) >= 3: 
    
        code_process = '_' + process_name_inserted.split('_')[1] + '_' + process_name_inserted.split('_')[2]
    

        file_name_curriculum_update = v_file_curriculum_to_import + code_process + '.xlsx'
        file_name_schedules_update = v_file_horarios + code_process + '.xlsx'

        path_to_file_curriculum = './' + v_main_folder_process + '/' + process_name_inserted + '/' + v_process_update_data + '/' + \
                            file_name_curriculum_update
        
        path_to_file_schedules = './' + v_main_folder_process + '/' + process_name_inserted + '/' + v_process_update_data + '/' + \
                            file_name_schedules_update
        
        if not os.path.exists(path_to_file_curriculum):
            raise ValidationFilesSchedulesUpdateData (code_process)
        
        if not os.path.exists(path_to_file_schedules):
            raise ValidationFilesSchedulesUpdateData (code_process)
    else:

        raise ValidationFilesSchedulesUpdateData (code_process)
    

def verify_name_acad_year_exist(total_records_event_name_bd : int):

    if total_records_event_name_bd == 0:

        raise EventNameNotExist()
    


    

 


