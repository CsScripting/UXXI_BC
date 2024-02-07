from mod_variables import *

from PackLibrary.librarys import (	
  DataFrame,
  merge,
  nan,
  concat
)



def filter_event_empty_conect ( df: DataFrame):

    df = df [df[v_id_uxxi] == '']
  
    return(df)

def pass_empy_list_to_nan (df : DataFrame):

  
    df[v_mod_id_typologie] = df[v_mod_id_typologie].apply(lambda x: nan if len(x)==0 else x)
    df[v_mod_typologie] = df[v_mod_typologie].apply(lambda x: nan if len(x)==0 else x)
    df[v_student_group_name] = df[v_student_group_name].apply(lambda x: nan if len(x)==0 else x)
    # NÂO È NECESSARIO CLASSROOM WITH NAN, NÂO È DADO OBRIGATORIO PARA ADICIONAR CONECTOR
    # df[v_classroom_name] = df[v_classroom_name].apply(lambda x: nan if len(x)==0 else x)
    # df[v_classroom_code] = df[v_classroom_code].apply(lambda x: nan if len(x)==0 else x)

    return(df)


def filter_data_best_mandatory_fields (df : DataFrame):

    mandatory_data = [v_mod_code,
                      v_mod_name,
                      v_mod_id,
                      v_mod_typologie,
                      v_mod_id_typologie,
                      v_section_name,
                      v_student_group_name]

    df_null = df[df[mandatory_data].isnull().any (axis=1)].copy()
    df= df.dropna(axis=0, subset=mandatory_data).copy()


    return(df, df_null)




def add_conector_from_file_uxxi (df_event : DataFrame, df_conector  : DataFrame):


    df_conector.rename(columns={v_asign_fileconect: v_mod_code}, inplace=True)
    values_to_merge = [v_mod_code,v_grupo_fileconect] 

    df_event = merge(left=df_event, right= df_conector, on = values_to_merge, how='left', indicator=True)

    df_event_with_conect = df_event[df_event[v_merge == 'both']].copy
    df_event_sin_conect = df_event[df_event[v_merge != 'both']].copy

    df_event_with_conect.drop(columns = v_merge, inplace = True)
    df_event_sin_conect.drop(columns = v_merge, inplace = True)

    return(df_event_with_conect, df_event_sin_conect)

def verify_unique_typology_event (df : DataFrame):

    #Ainda por implementar
    df[v_section_name] = df[v_section_name].apply(lambda x: x[0])



def verify_name_section (df : DataFrame):

    df['SPLIT_SECTION'] = df[v_section_name].str.split(' ')
    df['NUMBER_LEN_SECTION'] = df['SPLIT_SECTION'].str.len()
    df['ALFA_VALUE'] = df['SPLIT_SECTION'].str[0].str.isalpha()
    df['NUMERIC_VALUE'] = df['SPLIT_SECTION'].str[1]
    df['NUMERIC_VALUE_CHECK'] = df['NUMERIC_VALUE'].str.isnumeric()

    

    df_values_to_filter = df.copy()

    df_valid_section_name = df_values_to_filter [(df_values_to_filter['NUMBER_LEN_SECTION'] == 2) & 
                              (df_values_to_filter['ALFA_VALUE'] == True) & 
                              (df_values_to_filter['NUMERIC_VALUE_CHECK'] == True)]

    df_invalid_section_name= df_values_to_filter[(df_values_to_filter['NUMBER_LEN_SECTION'] !=2) | 
                                                 (df_values_to_filter['ALFA_VALUE'] != True) | 
                                                 (df_values_to_filter['NUMERIC_VALUE_CHECK'] != True)]
    


    if not df_valid_section_name.empty:

        columns_to_drop_on_valid = ['NUMBER_LEN_SECTION',
                                    'ALFA_VALUE',
                                    'NUMERIC_VALUE_CHECK']
        df_valid_section_name = df_valid_section_name.drop(columns=columns_to_drop_on_valid)
        df_valid_section_name = df_valid_section_name.rename(columns={'NUMERIC_VALUE': v_grupo_fileconect})

    if not df_invalid_section_name.empty:

        columns_to_drop_on_invalid = ['NUMBER_LEN_SECTION',
                                      'ALFA_VALUE',
                                      'NUMERIC_VALUE_CHECK']
        
        df_invalid_section_name = df_invalid_section_name.drop(columns=columns_to_drop_on_invalid)

    return(df_valid_section_name, df_invalid_section_name)


def filter_event_best_with_conector (df : DataFrame):

    df_to_filter = df.copy()

    df_with_conector = df_to_filter[df_to_filter[v_merge] == 'both'].copy()
    df_without_conector = df_to_filter[df_to_filter[v_merge] != 'both'].copy()

    df_with_conector = df_with_conector.drop(columns=v_merge)
    df_without_conector = df_without_conector.drop(columns=v_merge) 




    return(df_with_conector, df_without_conector)

def update_file_columns_and_parse_data_to_filter(df : DataFrame):

    df = df.rename(columns = {v_grupo_fileconect : v_nr_grupo_uxxi_conector_bwp,
                              v_cod_act_fileconect : v_act_uxxi_conector_bwp,
                              v_cod_grupo_fileconet : v_grupo_uxxi_conector_bwp,
                              v_plan_fileconet : v_plan_conector_bwp,
                              v_curso_fileconet : v_curso_conector_bwp})
    
    
    # TO ADD NUMBER WEEKS NEXT
    df[v_weeks] = df[v_weeks].transform(lambda x: ','.join(map(str, x)))
    df[v_mod_id_typologie] = df[v_mod_id_typologie].transform(lambda x: ','.join(map(str, x)))
    

    return (df)

def manage_file_error_conector (df : DataFrame, name_error : str):

    if not df.empty:

        df.insert(0,v_column_error_conector, name_error)

        columns_to_present = [  v_column_error_conector,
                                v_event_Id_BC,
                                v_event_title_BC,
                                v_mod_code,
                                v_mod_name,
                                v_mod_typologie,
                                v_section_name,
                                v_day,
                                v_hourBegin,
                                v_hourEnd,
                                v_event_type,
                                v_student_group_name,
                                v_classroom_name,
                                v_academic_year]
            
        df = df[columns_to_present].copy()


    return(df)


def create_df_errores_conect (df_error_1, df_error_2):

    df_error_1_2 = (df_error_1.copy() if df_error_2.empty else df_error_2.copy() if df_error_1.empty
                   else concat([df_error_1, df_error_2]))

    return(df_error_1_2)