from PackLibrary.librarys import (	
  DataFrame
)

from mod_variables import *
import PackControllerRequest.controller_dto as dtObj
import PackManageApi.global_variable_process_request as gl_v_request
import PackControllerRequest.general_requests as genRequest

def select_columns_update_conector (df : DataFrame):

    columns_to_update_conector = [v_id_best,
                                  v_event_Id_BC,
                                  v_event_title_BC,
                                  v_id_event_type,
                                  v_mod_code,
                                  v_mod_id,
                                  v_day,
                                  v_id_academic_year,
                                  v_section_name,
                                  v_classroom_name,
                                  v_hourBegin,
                                  v_hourEnd,
                                  v_number_weeks,
                                  v_mod_id_typologie,
                                  v_plan_conector_bwp,
                                  v_curso_conector_bwp,
                                  v_act_uxxi_conector_bwp,
                                  v_grupo_uxxi_conector_bwp,
                                  v_nr_grupo_uxxi_conector_bwp,
                                  ]
    
    df = df[columns_to_update_conector].copy()

    df = df.applymap(str) # To Create Event Conector

    return(df)


def iterate_events_and_update_single_event (df : DataFrame):

 
  for row in df.itertuples(index= False):

      event_id = getattr (row, v_id_best)

      data_object = dtObj.create_dto_update_event_basic(row)
      
      response_code = genRequest.put_data_event_basic_information(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_event_controller_basic, data_object, event_id)

  return()
