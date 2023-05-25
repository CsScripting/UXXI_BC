import PackManageApi.glogal_variable_process_request as gl_v_request
import PackControllerRequest.general_requests as genRequest
import PackControllerRequest.controller_dto as dtObj
from mod_variables import *

from PackLibrary.librarys import (	
    DataFrame
)

def iterate_df_courses_and_insert (df : DataFrame):

    for row in df.itertuples(index= False):

        value_to_import = getattr(row, v_data_to_import_new)

        if value_to_import == '1':

            name = getattr(row, v_name_best)
            acronym = getattr(row, v_acronym_best)
            code = getattr(row, v_code_best)

            data_object = dtObj.create_dto_courses(name, code, acronym)

            genRequest.post_data_to_entity(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_course_controller, data_object)



    



    return()