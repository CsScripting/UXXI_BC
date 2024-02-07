from mod_variables import *

from PackLibrary.librarys import (	
  DataFrame,
  ast,
  where,
  nan,
  concat
)

import PackUpdateData.exceptions_match_schedules as exceptMatch
import PackManageData.bussiness_rules_best as rulesBest
import PackManageData.join_tuples_data as manData



### INSERIR EM README REGRAS ASSOCIADAS A UPDATES
## CAMPOS NÂO ALTERAR:
   
   # DISCIPLINAS
   # GRUPOS ???
   # CONECTOR ???
   

def filter_by_acad_year (df : DataFrame, name_acad_year : str):

    df = df[df [v_academic_year] == name_acad_year ].copy()
    
    return(df)

def pass_str_to_dict_conector_bwp (df : DataFrame):
     
     df [v_id_uxxi] = df[v_id_uxxi].apply(ast.literal_eval)
     
     return()


def manage_conector_id_parse_to_dict (df : DataFrame):              

    df [v_id_uxxi] = df[v_id_uxxi].apply(lambda x: exceptMatch.parse_string_dict_to_dict(x))

    return(df)



def extract_values_conector_check_update(df : DataFrame):

    df [v_day_check_update_uxxi] = df[v_id_uxxi].apply(lambda x:  (exceptMatch.extract_value_dict(x,v_day_conector_bwp)))
    df [v_hour_check_update_uxxi] = df[v_id_uxxi].apply(lambda x:  (exceptMatch.extract_value_dict(x,v_hour_conector_bwp)))
    df [v_number_weeks_check_update_uxxi] = df[v_id_uxxi].apply(lambda x:  (exceptMatch.extract_value_dict(x,v_week_conector_bwp)))
    df [v_number_weeks_check_update_uxxi] =  df [v_number_weeks_check_update_uxxi].agg(lambda x: ','.join(map(str, x)))
    df [v_id_db_check_update_uxxi] = df[v_id_uxxi].apply(lambda x:  (exceptMatch.extract_value_dict(x,v_id_conector_bwp)))
    df [v_id_db_check_update_uxxi] =  df [v_id_db_check_update_uxxi].agg(lambda x: ','.join(map(str, x)))
    df [v_classroom_check_update_uxxi] = df[v_id_uxxi].apply(lambda x:  (exceptMatch.extract_value_dict(x,v_classroom_conector_bwp)))

    return (df)

def verify_updated_events (df : DataFrame):

    df [v_day_check_update] = where(df[v_day_check_update_uxxi] != df[v_day], df[v_day], '' )
    df [v_hour_check_update] = where( df[v_hour_check_update_uxxi]!= df[v_hourBegin] + '-' + df[v_hourEnd],  df[v_hourBegin] + '-' + df[v_hourEnd], '' )
    df [v_number_weeks_check_update] =  where(df[v_number_weeks_check_update_uxxi] != df[v_number_weeks], df[v_number_weeks], '' )
    df [v_classroom_name_check_update] =  where(df[v_classroom_check_update_uxxi] != df[v_classroom_name], df[v_classroom_name], '' )

  
    return (df)


def filter_events_need_update (df:DataFrame):

    need_update = False

    

    df_validation = df[(df[v_day_check_update] != '') | (df[v_number_weeks_check_update] != '') |
                       (df[v_hour_check_update] != '') | (df[v_classroom_name_check_update] != '')].copy()
    

    if not df_validation.empty:

        need_update = True


    return (df_validation, need_update)


def filter_to_reasign_values_id_uxxi_to_send_uxxi (df : DataFrame):

    columns_to_drop = [v_day_check_update_uxxi,
                       v_hour_check_update_uxxi,
                       v_number_weeks_check_update_uxxi,
                       v_classroom_check_update_uxxi,
                       v_day_check_update,
                       v_hour_check_update,
                       v_number_weeks_check_update,
                       v_classroom_name_check_update,]

    df.drop(columns=columns_to_drop, inplace=True)


    return(df)

def extract_values_conector_planificacion (df : DataFrame):

    # Manter sempre dados de PLANIFICAÇÂO UXXI - PLAN ; CURSO ; ACT ; GRUPO UXXI

    df [v_plan_conector_bwp]= df[v_id_uxxi].apply(lambda x:  (exceptMatch.extract_value_dict(x,v_plan_conector_bwp)))
    df [v_curso_conector_bwp] = df[v_id_uxxi].apply(lambda x:  (exceptMatch.extract_value_dict(x,v_curso_conector_bwp)))
    df [v_act_uxxi_conector_bwp] = df[v_id_uxxi].apply(lambda x:  (exceptMatch.extract_value_dict(x,v_act_uxxi_conector_bwp)))
    df [v_grupo_uxxi_conector_bwp] = df[v_id_uxxi].apply(lambda x:  (exceptMatch.extract_value_dict(x,v_grupo_uxxi_conector_bwp)))
    df [v_nr_grupo_uxxi_conector_bwp] = df[v_id_uxxi].apply(lambda x:  (exceptMatch.extract_value_dict(x,v_nr_grupo_uxxi_conector_bwp)))

    return (df)



def extract_id_bd_to_delete (df : DataFrame, actiontype):

    columns_filter = [v_plan_conector_bwp,v_curso_conector_bwp,
                      v_mod_code, v_mod_name,v_mod_typologie,
                      v_act_uxxi_conector_bwp, v_grupo_uxxi_conector_bwp, 
                      v_nr_grupo_uxxi_conector_bwp, v_id_db_check_update_uxxi]
                      
    df = df [columns_filter].copy()
    if actiontype == v_updated_event:

        df[v_type_action] = v_updated_event

    else:

        df[v_type_action] = v_deleted_event

    
    df = manData.split_by_rows(df,v_id_db_check_update_uxxi, sep = ',')

    df.drop_duplicates(keep= 'first',inplace=True)


    return (df)

def adicionanl_fields_event_deleted (df : DataFrame):

    df[v_mod_code] = ''
    df[v_mod_name] = ''
    df[v_mod_typologie] = ''


    return(df)

def merge_values_ids_to_delete_uxxi (df_update : DataFrame, df_delete : DataFrame):

    df_all = concat([df_update, df_delete], ignore_index= True)

    return(df_all)









