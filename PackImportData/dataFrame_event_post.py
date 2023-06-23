import PackManageApi.glogal_variable_process_request as gl_v_request
import PackControllerRequest.general_requests as genRequest
import PackControllerRequest.controller_dto as dtObj
from mod_variables import *

from PackLibrary.librarys import (	
    Series,
    DataFrame
)


def iterate_df_events_and_post (df : DataFrame):

    columns_to_present = [v_event_Id_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                          v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code, 
                          v_year, v_student_group_name,v_students_number,v_classroom_name, v_id_uxxi,v_weeks, v_event_type,
                          v_code_request, v_message_request]
    
    
    

    df_columns_events = list(df.columns)

    df_events_imported = DataFrame(columns = df_columns_events)
    df_events_imported[v_code_request] = ''
    df_events_imported[v_message_request] = '' 
    df_events_not_imported =  DataFrame(columns= df_columns_events)
    df_events_not_imported[v_code_request] = ''
    df_events_not_imported[v_message_request] = ''
    
    df = df.applymap(str)

    
    for row in df.itertuples(index= False):

        event_id_row = getattr (row, v_id_event)

        data_object = dtObj.create_dto_event(row)
        
        response_code, message_to_present = genRequest.post_data_to_entity(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_event_academic_controller, data_object)


    
        if response_code == 201:

            df_events_imported = df_events_imported.append([row],ignore_index=True)

            df_events_imported.loc[df_events_imported[v_id_event ] == event_id_row, v_code_request] = response_code
            df_events_imported.loc[df_events_imported[v_id_event] == event_id_row, v_message_request] = message_to_present 

        else:

            df_events_not_imported = df_events_not_imported.append([row],ignore_index=True)

            df_events_not_imported.loc[df_events_not_imported[v_id_event] == event_id_row, v_code_request] = response_code
            df_events_not_imported.loc[df_events_not_imported[v_id_event] == event_id_row, v_message_request] = message_to_present 


    df_events_imported =df_events_imported[columns_to_present]
    df_events_not_imported =df_events_not_imported[columns_to_present]
    
    return(df_events_imported, df_events_not_imported)