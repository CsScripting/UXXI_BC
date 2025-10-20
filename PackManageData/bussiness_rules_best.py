from PackLibrary.librarys import (	
  DataFrame,
  datetime,
  arange,
  where
  
)
from datetime import datetime
import PackManageData.join_tuples_data as manData

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

def add_event_connector_json (df : DataFrame, state_import):

    #Before ID's BD
    df[v_plan_dominant] = df[v_course_code].str.split('#').str[0] + '_' + df[v_year].str.split('#').str[0] 
    df[v_id_uxxi] = df[v_plan_dominant] + '_' + df[v_activity_code] + '_' + df[v_student_group_code]

    
    '''
    PROCESS ADD CONECTOR JSON TO INTEGRATION
    
    
    '''



    # if state_import == v_app_uxxi:

    #     df[v_plan_dominant] = df[v_course_code].str.split('#').str[0] + '_' + df[v_year].str.split('#').str[0] 

    #     state_data = v_app_uxxi

    #     df[v_id_uxxi] = '{"App":' + '"'+ state_data +'"' \
    #                     ',"Plan":' +  '"' + df[v_course_code].str.split('#').str[0] + '"' + \
    #                     ',"Cur":'  +  df[v_year].str.split('#').str[0] + \
    #                     ',"Act":'  +  df[v_activity_code] + \
    #                     ',"Gr":'   +  df[v_student_group_code] + \
    #                     ',"NrGr":'   +  df[v_student_group] + \
    #                     ',"Day":'  +  df[v_day] + \
    #                     ',"Hour":' +  '"' + df[v_hourBegin] + '-' + df[v_hourEnd] + '"' + \
    #                     ',"Class":'   +  '"' + df[v_classroom_name] + '"' +\
    #                     ',"Week":' +  '[' + df[v_number_weeks]  +']' + \
    #                     ',"Id":'   +  '[' + df[v_id_db] + ']' +\
    #                     '}'

    # elif state_import == v_app_bwp_to_uxxi:

    #     state_data = v_app_bwp_to_uxxi

    #     # Manter sempre dados de PLANIFICAÇÂO UXXI - PLAN ; CURSO ; ACT ; GRUPO UXXI

    #     df[v_id_uxxi] = '{"App":' + '"'+ state_data +'"' \
    #                     ',"Plan":' +  '"' + df[v_plan_conector_bwp] + '"' + \
    #                     ',"Cur":'  +  df[v_curso_conector_bwp] + \
    #                     ',"Act":'  +  df[v_act_uxxi_conector_bwp] + \
    #                     ',"Gr":'   +  df[v_grupo_uxxi_conector_bwp] + \
    #                     ',"NrGr":'   +  df[v_nr_grupo_uxxi_conector_bwp] + \
    #                     ',"Day":'  +  df[v_day] + \
    #                     ',"Hour":' +  '"' + df[v_hourBegin] + '-' + df[v_hourEnd] + '"' + \
    #                     ',"Class":'   +  '"' + df[v_classroom_name] + '"' +\
    #                     ',"Week":' +  '[' + df[v_number_weeks]  +']' + \
    #                     ',"Id":'   +  '[]' +\
    #                     '}'
        
    # elif state_import == v_app_bwp:

    #     state_data = v_app_bwp

    #     # Manter sempre dados de PLANIFICAÇÂO UXXI - PLAN ; CURSO ; ACT ; GRUPO UXXI

    #     df[v_id_uxxi] = '{"App":' + '"'+ state_data +'"' \
    #                     ',"Plan":' +  '"' + df[v_plan_conector_bwp] + '"' + \
    #                     ',"Cur":'  +  df[v_curso_conector_bwp] + \
    #                     ',"Act":'  +  df[v_act_uxxi_conector_bwp] + \
    #                     ',"Gr":'   +  df[v_grupo_uxxi_conector_bwp] + \
    #                     ',"NrGr":'   +  df[v_nr_grupo_uxxi_conector_bwp] + \
    #                     ',"Day":'  +  df[v_day] + \
    #                     ',"Hour":' +  '"' + df[v_hourBegin] + '-' + df[v_hourEnd] + '"' + \
    #                     ',"Class":'   +  df[v_classroom_name] +\
    #                     ',"Week":' +  '[' + df[v_number_weeks]  +']' + \
    #                     ',"Id":'   +  '[]' +\
    #                     '}'
    

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

def filter_fiels_w_loads (df : DataFrame):

    columns = [ v_center_plan_dominant, ## Apenas para atribuir session 2 Experimentales en metodo seguinte, Drop no Respectivo Metodo !!!
                v_file_conectores,
                v_plan_fileconect,
                v_curso_fileconect,
                v_mod_code,
                v_student_group,
                v_cred_model,  ## Apenas para atribuir Semanas Alternadas, Drop no respetivo Metodo !!!
                v_mod_typologie,
                v_weeks,
                v_hours_wload,
                v_plan_linea,
                v_student_group_best,
                v_students_number,
                v_slot_number_rest,
                 ]
    
    df = df [columns].copy()
    df[v_session_wload] = '1'

    return(df)

def insert_name_section (df : DataFrame):

    df[v_section_name] = df[v_mod_typologie] + df[v_student_group]

    return(df)

def insert_name_wload (df : DataFrame):

    prefix_w_load = 'L'

    df[v_plan_fileconect] = df [v_plan_fileconect].apply(lambda x : x[0])
    df[v_curso_fileconect] = df [v_curso_fileconect].apply(lambda x : x[0])
    df[v_plan_linea] = df [v_plan_linea].apply(lambda x : x[0])

    # INSERIDA EXCEPÇÂO DE NOME DE W_LOAD DE ACORDO COM SEMANAS PARES E IMPARES
    df[v_name_wload] = where (df[v_w_load_flag_alternated_week] != '', 
                              df[v_plan_fileconect] + '_' + df[v_curso_fileconect] + '_' + prefix_w_load + df[v_plan_linea] + '_' +  df[v_mod_typologie] + '_' + df[v_w_load_flag_alternated_week],
                              df[v_plan_fileconect] + '_' + df[v_curso_fileconect] + '_' + prefix_w_load + df[v_plan_linea] + '_' +  df[v_mod_typologie])
    
    df_mod_linea_par_impar = df[df[v_w_load_flag_alternated_week] != ''].copy()

    # df[v_name_wload] = where(df[v_week_load_type] == v_week_load_unique, df[v_plan_fileconect] + '_' + df[v_curso_fileconect] + '_' + prefix_w_load + df[v_plan_linea] + '_' +  df[v_mod_typologie] ,
    #                    where(df[v_week_load_type] == v_week_load_reference, df[v_plan_fileconect] + '_' + df[v_curso_fileconect] + '_' + prefix_w_load + df[v_plan_linea] + '_' +  df[v_mod_typologie]  + '_PR' ,
    #                          df[v_plan_fileconect] + '_' + df[v_curso_fileconect] + '_' + prefix_w_load + df[v_plan_linea] + '_' +  df[v_mod_typologie] + '_PS'))
    df.drop(columns=[v_plan_fileconect, v_curso_fileconect,v_w_load_flag_alternated_week], inplace = True)

    return (df, df_mod_linea_par_impar)

def insert_name_wload_segun (df : DataFrame):

    prefix_w_load = 'L'

    df_mod_linea_par_impar = DataFrame ()

    df[v_plan_fileconect] = df [v_plan_fileconect].apply(lambda x : x[0])
    df[v_curso_fileconect] = df [v_curso_fileconect].apply(lambda x : x[0])
    df[v_plan_linea] = df [v_plan_linea].apply(lambda x : x[0])

    # INSERIDA EXCEPÇÂO DE NOME DE W_LOAD DE ACORDO COM SEMANAS PARES E IMPARES
    df[v_name_wload] = df[v_plan_fileconect] + '_' + df[v_curso_fileconect] + '_' + prefix_w_load + df[v_plan_linea] + '_' +  df[v_mod_typologie] 
    

    df.drop(columns=[v_plan_fileconect, v_curso_fileconect], inplace = True)

    return (df, df_mod_linea_par_impar)


def agg_section_to_w_load (df : DataFrame):

    columns_to_drop = [v_student_group,
                       v_plan_linea]
    
    df.drop(columns=columns_to_drop, inplace=True)

    series_to_agg = [v_name_wload,
                     v_mod_code,
                     v_mod_typologie,
                     v_hours_wload,
                     v_session_wload,
                     v_weeks]

    df.sort_values(by=[v_name_wload, v_section_name], ascending=True, inplace=True)
    df = manData.group_entities_to_list(df, series_to_agg, sep = ';')

    return(df)


def count_sectiones_number (df :DataFrame):

    df[v_section_number] = df[v_section_name].apply(lambda x: len(x))

    return (df)

def add_distinct_name_w_load_same_module_type (df : DataFrame):

    df['Counter'] =df.groupby([v_name_wload,v_mod_code,v_mod_typologie])[v_mod_typologie].cumcount()

    df['Counter'] = df['Counter'] + 1
    df ['Counter'] = df ['Counter'].astype(str)
    df [v_name_wload] = where(df['Counter'] != '1',
                              df[v_name_wload] + '_M' + df['Counter'],
                              df [v_name_wload])
    
    df.drop(columns='Counter', inplace=True)

    return(df)

