from PackLibrary.librarys import (	
  DataFrame,
  datetime,
  arange
  
)
from datetime import datetime

from mod_variables import *

def update_value_day (df : DataFrame):

    df[v_day] = (df[v_day].astype(int)) - 1
    df[v_day] = df[v_day].astype(str)


    return(df)



def add_event_type(df : DataFrame):

    df[v_event_type] = 'Clases UPO'

    return(df)

def add_event_code(df : DataFrame, process_code : str):

    timestr = process_code
    df['counter'] = arange(len(df)).astype(str)
    df[v_event_Id_BC] = df[v_event_type] + '_' + df[v_mod_code].str.split('#').str[0] + timestr + '_' + df['counter']
    df.drop(columns='counter', inplace=True)

    return(df)

def add_event_section_name(df : DataFrame):

    df[v_section_name] = df[v_mod_typologie].str.split('#').str[0] + ' ' + df[v_student_group].str.split('#').str[0]

    return(df)

def add_number_week (df : DataFrame):

    df[v_number_weeks] = df[v_weeks].str.split(',').apply(lambda x: ','.join([str(datetime.strptime(e, '%Y-%m-%d').isocalendar().week)  for e in x]))

    return(df)

def add_event_connector (df : DataFrame):

    # Before ID's BD
    # df[v_plan_dominant] = df[v_course_code].str.split('#').str[0] + '_' + df[v_year].str.split('#').str[0] 
    # df[v_id_uxxi] = df[v_plan_dominant] + '_' + df[v_activity_code] + '_' + df[v_student_group_code]

    # After
    df[v_plan_dominant] = df[v_course_code].str.split('#').str[0] + '_' + df[v_year].str.split('#').str[0] 


    df[v_id_uxxi] = '{"Plan":' +  '"' + df[v_course_code].str.split('#').str[0] + '"' + \
                    ',"Cur":'  +  df[v_year].str.split('#').str[0] + \
                    ',"Act":'  +  df[v_activity_code] + \
                    ',"Gr":'   +  df[v_student_group_code] + \
                    ',"Day":'  +  df[v_day] + \
                    ',"Hour":' +  '"' + df[v_hourBegin] + '-' + df[v_hourEnd] + '"' + \
                    ',"Week":' +  '[' + df[v_number_weeks]  +']' + \
                    ',"Id":'   +  '[' + df[v_id_db] + ']' +\
                    '}'
  

    return(df)

def manage_hours (df: DataFrame):

    df[v_hourBegin_split] = df[v_hourBegin_split].str.zfill(2)
    df[v_hourEnd_split] = df[v_hourEnd_split].str.zfill(2)
    df[v_minute_begin_split] = df[v_minute_begin_split].str.zfill(2)
    df[v_minute_end_split] = df[v_minute_end_split].str.zfill(2)

    df[v_hourBegin] = df[v_hourBegin_split] + ':' + df[v_minute_begin_split]
    df[v_hourEnd] = df[v_hourEnd_split] + ':' + df[v_minute_end_split]

    df.drop(columns=[v_hourBegin_split, v_hourEnd_split, v_minute_begin_split, v_minute_end_split], inplace=True)

    return (df)