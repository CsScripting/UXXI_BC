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

        counter_rows += 1


        conector_section = getattr(row, v_file_conectores)
        number_section_row = getattr(row, v_section_number)
        id_weekload = getattr (row,v_id_w_load)
        list_section_id = getattr (row,v_id_w_load_section)
        list_section_name =  getattr (row,v_section_name)
        list_number_students = getattr(row,v_students_number)
        dict_grupos = getattr (row,v_st_group_section)
        groups_add = dict_grupos.get(v_st_group_add)
        groups_remove = dict_grupos.get(v_st_group_remove)

        if nr_section_import <= number_sections_on_collection:

            nr_section_import += int(number_section_row)

            for i in range (int(number_section_row)):

                list_sectiones = dtObj.create_list_sectiones_to_wllssections(id_weekload,conector_section[i], list_section_name[i],list_number_students[i], list_section_id[i], groups_add[i], groups_remove[i])
                list_collection_section.append(list_sectiones)

        if (nr_section_import > number_sections_on_collection) or (total_rows == counter_rows):

            nr_section_import = 0
            data_object_collection = dtObj.create_wllssections_dto(list_collection_section) 
            genRequest.put_data_to_entity_collection(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_wlssectiones_update_collection, data_object_collection)

            list_collection_section = []

    return ()