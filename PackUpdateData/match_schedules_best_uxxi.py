from PackLibrary.librarys import (	
  DataFrame,
  where,
  merge,
  nan
)

from mod_variables import *
import PackUpdateData.exceptions_match_schedules as exceptMatch

def create_df_insert_data (df : DataFrame, flag_no_events : bool = False ):


    columns_df_update = [v_event_Id_BC, v_mod_name,v_mod_code,v_mod_typologie,v_section_name,
                         v_day, v_hourBegin, v_hourEnd, v_duration,v_course_name, v_course_code, v_year, v_student_group_name,
                         v_students_number, v_id_uxxi,v_weeks, v_mod_modalidad,v_classroom_name, v_classroom_code, v_event_type, v_academic_year, v_data_to_import_new]

    df [v_academic_year] = ''

    if flag_no_events:

        df[v_data_to_import_new] = 1


    df = df[columns_df_update]
        


    return(df)


def create_df_update_data ():

    

    
    

    return()

def manage_conector_id_parse_to_dict (df : DataFrame):              

    df [v_id_uxxi] = df[v_id_uxxi].apply(lambda x: exceptMatch.parse_string_dict_to_dict(x))
    df [v_id_db] = df [v_id_uxxi].apply(lambda x: (exceptMatch.extract_value_dict(x)))

    return(df)

def match_id_schedules_to_import(df_schedules_prod : DataFrame, df_schedules_to_update):


    #Pass String dict Representation to dict -- > next --> parse to dict and extract value  
    df_schedules_prod = manage_conector_id_parse_to_dict (df_schedules_prod)
    df_schedules_to_update = manage_conector_id_parse_to_dict (df_schedules_to_update)


    df_schedules_prod[v_id_db] = where (df_schedules_prod[v_id_db] != 'InvalidConector', df_schedules_prod[v_id_db].agg(lambda x: ','.join(map(str, x))), df_schedules_prod[v_id_db])
    df_schedules_to_update[v_id_db] = where (df_schedules_to_update[v_id_db] != 'InvalidConector',df_schedules_to_update[v_id_db].agg(lambda x: ','.join(map(str, x))),df_schedules_to_update[v_id_db])

    ##Pass dict to Representation String dict
    df_schedules_prod [v_id_uxxi] = df_schedules_prod[v_id_uxxi].astype(str)
    df_schedules_to_update [v_id_uxxi] = df_schedules_to_update[v_id_uxxi].astype(str)

    #COPY Datagrame to use on another method
    df_events_best = df_schedules_to_update.copy()

    ids_events_to_insert = df_schedules_to_update[v_id_db].values.tolist()

    #Values:

    # 1 - New Event
    # 2 - Posible Update

    df_schedules_prod[v_data_to_import_new] = where(df_schedules_prod[v_id_db].isin(ids_events_to_insert), 2, 1)

    df_schedules_prod_insert = df_schedules_prod[df_schedules_prod[v_data_to_import_new] == 1].copy()
    df_schedules_prod_update = df_schedules_prod[df_schedules_prod[v_data_to_import_new] == 2].copy()


    return (df_schedules_prod_insert, df_schedules_prod_update, df_events_best)


# Verify if Schedules on BC need update
def match_id_schedules_to_update(df_events_check_update : DataFrame, df_events_best : DataFrame):

    columns_df_best_to_check = [
                                v_id_best, 
                                v_event_Id_BC, 
                                v_event_title_BC,
                                v_event_type,
                                v_id_event_type,
                                v_mod_name,
                                v_mod_code,
                                v_mod_id,
                                v_mod_typologie,
                                v_mod_id_typologie,
                                v_section_name, 
                                v_day, 
                                v_hourBegin, 
                                v_hourEnd, 
                                v_student_group_name,
                                v_student_group_id,
                                v_students_number, 
                                v_id_uxxi,
                                v_weeks,
                                v_classroom_name, 
                                v_classroom_code,
                                v_id_classroom,
                                v_id_db]
    

    columns_df_uxxi_to_check = [
                                v_mod_name,
                                v_mod_code,
                                v_mod_typologie,
                                v_section_name,
                                v_day, 
                                v_hourBegin, 
                                v_hourEnd, 
                                v_duration, 
                                v_student_group_name,
                                v_students_number, 
                                v_id_uxxi,
                                v_weeks,
                                v_classroom_name, 
                                v_classroom_code,
                                v_id_db]  
    
    
    
    
    df_events_best = df_events_best[columns_df_best_to_check].copy()
    df_events_best.rename(columns = lambda name_column : name_column + v_suffix_check_update_best, inplace=True )
    df_events_best.rename(columns = {v_id_db_check_update : v_id_db}, inplace = True)


    df_events_check_update = manage_conector_id_parse_to_dict (df_events_check_update)
    df_events_check_update [v_id_uxxi] = df_events_check_update[v_id_uxxi].astype(str)
    df_events_check_update[v_id_db] = where (df_events_check_update[v_id_db] != 'InvalidConector',df_events_check_update[v_id_db].agg(lambda x: ','.join(map(str, x))), df_events_check_update[v_id_db])
    df_events_check_update = df_events_check_update[columns_df_uxxi_to_check].copy()

    df_events_best = merge(left=df_events_best, right=df_events_check_update, on=v_id_db, how = 'left', indicator=True)

    #Check Values To Update
    df_events_best[v_mod_code] = df_events_best[v_mod_code].str.split('#').str[0]
    df_events_best[v_mod_code_update] = where(df_events_best[v_mod_code_check_update] != df_events_best[v_mod_code], df_events_best[v_mod_code], '' )
    df_events_best[v_mod_typologie_update] = where(df_events_best[v_mod_typologie_check_update] != df_events_best[v_mod_typologie], df_events_best[v_mod_typologie], '' )

    
    columns_df_best_checked = [ v_id_best_check_update, v_event_Id_BC_check_update, v_event_title_BC_check_update,
                                v_mod_name_check_update,v_mod_code_check_update,v_mod_typologie_check_update,v_section_name_check_update, 
                                v_day_check_update, v_hourBegin_check_update, v_hourEnd_check_update, v_student_group_name_check_update,
                                v_students_number_check_update, v_id_uxxi_check_update,v_weeks_check_update,v_classroom_name_check_update, v_classroom_code_check_update,
                                v_mod_code_update,v_mod_typologie_update] 
    
    df_events_best = df_events_best[columns_df_best_checked].copy()

    #Remove columns Update Don´t have values to update
    df_columns_to_drop = df_events_best[[v_mod_code_update, v_mod_typologie_update]].loc[:, (df_events_best == '').all()]
    columns_to_drop = df_columns_to_drop.columns.values.tolist()

    
    df_events_best.drop(columns=columns_to_drop, inplace=True)

    
    # Verify id have columns Names to Update ---> pass above to decide if need to Write file Update 
    verify_columns_values_update = df_events_best.columns[df_events_best.columns.str.contains(v_suffix_to_update)]

    if len(verify_columns_values_update) != 0:

        
        columns_update_to_manage = [col for col in df_events_best.columns if v_suffix_to_update in col]

        #Select only rows need Update

        df_events_best.replace("", nan, inplace=True)

        df_events_best = df_events_best.dropna(axis=0, subset=columns_update_to_manage).copy()

        df_events_best.replace(nan, "", inplace=True)
         

    return (df_events_best, verify_columns_values_update)