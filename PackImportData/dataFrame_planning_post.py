import PackControllerRequest.controller_dto as dtObj
import PackControllerRequest.general_requests as genRequest
import PackDfFromJson.WeekLoadsDf as wLoadDf
import PackManageApi.global_variable_process_request as gl_v_request
from PackLibrary.librarys import (	
    Series,
    DataFrame,
    concat
)
from mod_variables import *



def iterate_df_plan_mod_and_post (df : DataFrame, period_btt : str):

    df = df.map(str)

    for row in df.itertuples(index= False):


        data_object = dtObj.create_dto_plan_module(row, period_btt)
        genRequest.put_data_with_parameter(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_plan_module_controller, data_object, period_btt)


    return()

def iterate_df_w_load_and_post_wload (df : DataFrame, period_btt : str):

    df = df.map(str)

    datos_weekloads_id = DataFrame()

    for row in df.itertuples(index= False):

        data_object = dtObj.create_dto_wloads_wlssectiones(row, period_btt) 
        datos_weekloads,response_code, data_to_present = genRequest.post_data_to_w_loads(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_wloads_wlssections_controller, data_object)
        datos_weekloads_id_temp = wLoadDf.parse_week_loads_df_from_json(datos_weekloads)

        datos_weekloads_id = concat([datos_weekloads_id, datos_weekloads_id_temp], ignore_index= True)

    return(datos_weekloads_id)


def iterate_df_w_load_section_post_section (df : DataFrame):

    number_sections_on_collection = 10
    total_rows = len(df.axes[0])

    nr_section_import = 0
    counter_rows = 0
    list_collection_section = []

    for row in df.itertuples(index= False):

        number_section_row = getattr(row, v_section_number)
        nr_section_import += int(number_section_row)

        counter_rows += 1

        if nr_section_import <= number_sections_on_collection:

            # data_object = dtObj.(row)   CREATE OBJECT
            list_collection_section.append()

        if (nr_section_import == number_sections_on_collection) or (total_rows == counter_rows):

            nr_section_import = 0

            # data_collection = dtObj.(list_collection_section)   CREATE OBJECT

            # genRequest.put_data_to_entity_collection(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_event_create_collection_controller, data_collection)

            list_collection_section = []

    return ()