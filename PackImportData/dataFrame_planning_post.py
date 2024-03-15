import PackControllerRequest.controller_dto as dtObj
import PackControllerRequest.general_requests as genRequest
import PackManageApi.global_variable_process_request as gl_v_request
from PackLibrary.librarys import (	
    Series,
    DataFrame
)
from mod_variables import *



def iterate_df_plan_mod_and_post (df : DataFrame, period_btt : str):

    df = df.applymap(str)

    for row in df.itertuples(index= False):

        plan = getattr (row,v_id_plan_best)

        data_object = dtObj.create_dto_plan_module(row, period_btt)
        genRequest.put_data_with_parameter(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_plan_module_controller, data_object, period_btt)





    return()