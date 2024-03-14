from mod_variables import *
import PackControllerRequest.academic_term_request as acadTermRequest
import PackManageApi.global_variable_process_request as gl_v_request
import PackGeneralProcedures.global_variable_process_procedures as gl_v_data
from PackLibrary.librarys import (
    os
)

# validation_folder_update_data_to_import()
class ValidationFileWloads(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass

# validation_folder_update_data_to_import()
class ValidationNameAcademicTerm(Exception):
    def __init__(self, error_value):
        self.error_value = error_value
    pass


def validation_week_load_file_on_folder(process_name_inserted : str):

    code_process_verify_split  = process_name_inserted.split('_')

    if len (code_process_verify_split) >= 3: 
    
        code_process = '_' + process_name_inserted.split('_')[1] + '_' + process_name_inserted.split('_')[2]
    
        file_name_wloads = v_file_wloads + code_process + '.xlsx'
        file_name_curriculum_update = v_file_curriculum_to_import + code_process + '.xlsx'

        path_to_file_config = './' + v_main_folder_process + '/' + process_name_inserted + '/' + v_process_update_data + '/' + \
                            file_name_wloads
        path_to_file_curriculum = './' + v_main_folder_process + '/' + process_name_inserted + '/' + v_process_update_data + '/' + \
                            file_name_curriculum_update
        
        if not os.path.exists(path_to_file_config):
            raise ValidationFileWloads (code_process)
        
        if not os.path.exists(path_to_file_curriculum):
            raise ValidationFileWloads (code_process)
        
    else:
        raise ValidationFileWloads (code_process)
    

def validation_academic_term_planning (data_object_search : dict, name_academic_term):


    data_academic_term,validation_name =  acadTermRequest.get_data_academic_term_search (gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_acad_term_controller, data_object_search)

    gl_v_data.gl_data_academic_term = data_academic_term

    if validation_name == 0:   #validation_name É IGUAL A CAMPO DE total_records NO JSON
            raise ValidationNameAcademicTerm (name_academic_term)

    return()