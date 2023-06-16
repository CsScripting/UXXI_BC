#Extract Data API
import PackManageApi.glogal_variable_process_request as gl_v_request
import PackControllerRequest.general_requests as genRequest
import PackDfFromJson.ModulesDf as modDf

from mod_variables import *

from PackLibrary.librarys import (	
    DataFrame,
    merge,
    where,
    concat
)

def filter_df_to_import (df:DataFrame):

    df = df[df[v_data_to_import_new] == '1'].copy()
    
    return(df)

def module (df_event : DataFrame):

    # Iniciate Dataframe Invalid Data

    columns_data_frame = [v_event_Id_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                       v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code, 
                       v_year, v_student_group_name,v_students_number,v_id_uxxi,v_weeks, v_event_type, v_error_id ]

    df_invalid_events_data = DataFrame(columns = columns_data_frame)


    modules_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_module_controller)
    
    flag_need_id = True
    df_modules_best = modDf.modules_df_from_json(modules_db, flag_need_id)

    #One event can have more than un one module (Dominant/Dominated)
    
    df_event[v_mod_code_dominant] = df_event[v_mod_code].str.split("#").str[0]

    df_modules_best.rename(columns={v_code_best:v_mod_code_dominant,
                                    v_id_best : v_mod_id_dominant}, inplace=True)

    df_event[v_mod_code_dominant] = where(df_event[v_id_uxxi] == '44096_99426', '1234', df_event[v_mod_code_dominant] )

    df_event = merge(left=df_event, right=df_modules_best, on = v_mod_code_dominant, how='left', indicator = True)

    df_event_with_id_mod = df_event[df_event[v_merge] == 'both'].copy() 
    df_event_without_id_mod = df_event[df_event[v_merge] == 'left_only'].copy() 

    df_event_without_id_mod = df_event_without_id_mod [[v_event_Id_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                                                        v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code, 
                                                        v_year, v_student_group_name,v_students_number,v_id_uxxi,v_weeks, v_event_type ]].copy()
    
    df_event_without_id_mod [v_error_id] = v_error_id_mod

    df_invalid = concat([df_invalid_events_data, df_event_without_id_mod], ignore_index= True)



    return (df_event_with_id_mod, df_invalid ) 