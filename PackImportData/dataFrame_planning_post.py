import PackControllerRequest.controller_dto as dtObj
import PackControllerRequest.general_requests as genRequest
import PackDfFromJson.WeekLoadsDf as wLoadDf
import PackManageApi.global_variable_process_request as gl_v_request
from PackLibrary.librarys import (	
    Series,
    DataFrame
)
from mod_variables import *



def iterate_df_plan_mod_and_post (df : DataFrame, period_btt : str):

    df = df.map(str)

    for row in df.itertuples(index= False):


        data_object = dtObj.create_dto_plan_module(row, period_btt)
        genRequest.put_data_with_parameter(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_plan_module_controller, data_object, period_btt)


    return()

def iterate_df_w_load_and_post_wload (df : DataFrame, period_btt : StopAsyncIteration):

    df = df.map(str)

    for row in df.itertuples(index= False):

        data_object = dtObj.create_dto_wloads_wlssectiones(row, period_btt) 
        datos_weekloads,response_code, data_to_present = genRequest.post_data_to_w_loads(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_wloads_wlssections_controller, data_object)
        wLoadDf.parse_week_loads_df_from_json(datos_weekloads)

    return()