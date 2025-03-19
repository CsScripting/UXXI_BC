from mod_variables import *
from PackLibrary.librarys import (	
  DataFrame,
  merge,
  where,
  concat
)

def filter_columns_process (df: DataFrame, process : str):


    if process == v_sheet_model_module:

        columns = [v_cred_cod_center,
                   v_cred_plan, 
                   v_cred_mod_code, 
                   v_cred_model,
                   v_cred_credits,
                   v_cred_compartida]
    

    elif process == v_sheet_credit_model:

        columns = [ 
                    v_cred_model, 
                    v_cred_credits,
                    v_cred_actividad,
                    v_cred_weeks,
                    v_cred_hours]

    elif process == v_sheet_credit_model_criterion:

        columns= [  v_cred_cod_center,
                    v_cred_plan,
                    v_cred_model,
                    v_cred_credits,
                    v_cred_period,
                    v_cred_week_EB,
                    v_cred_week_EPD,
                    v_cred_week_AD]
        
    elif process == v_sheet_alternated_weeks:

        columns= [  v_cred_cod_center,
                    v_cred_plan,
                    v_year,
                    v_cred_mod_code,
                    v_cred_model,
                    v_epd_alternatedd_linea,
                    v_epd_alternatedd_weeks]



    df = df[columns].copy()


    return(df)


def filter_null_values_credits (df : DataFrame, process: str):
    

    if process == v_sheet_model_module:

        columns_not_null_models = [v_cred_cod_center,
                                   v_cred_plan,
                                   v_cred_mod_code, 
                                   v_cred_model,
                                   v_cred_credits]

    elif process == v_sheet_credit_model:

        columns_not_null_models = [  v_cred_model, 
                                     v_cred_credits,
                                     v_cred_actividad,
                                     v_cred_weeks,
                                     v_cred_hours]

    elif process == v_sheet_credit_model_criterion:

        columns_not_null_models = [
                                    v_cred_cod_center,
                                    v_cred_plan,
                                    v_cred_model,
                                    v_cred_credits]
        


    elif process == v_sheet_alternated_weeks:

        columns_not_null_models = [ v_cred_cod_center,
                                    v_cred_plan,
                                    v_year,
                                    v_cred_mod_code,
                                    v_cred_model,
                                    v_epd_alternatedd_linea,
                                    v_epd_alternatedd_weeks]


    df_null = df[df[columns_not_null_models].isnull().any (axis=1)].copy()
    df_null.fillna('NULL', inplace = True)
    
    df = df.dropna(axis=0, subset=columns_not_null_models).copy()

    return(df, df_null) 

def verify_duplicated_data_model_credits_general( df : DataFrame, process: str):

    if process == v_sheet_model_module:

        values_to_check_duplicated = [v_cred_cod_center, v_cred_plan, v_cred_mod_code]

    elif process == v_sheet_credit_model_criterion:

        values_to_check_duplicated = [v_cred_cod_center, v_cred_plan, v_cred_model,v_cred_credits]

    elif process == v_sheet_credit_model:

        values_to_check_duplicated = [v_cred_model, v_cred_credits,v_cred_actividad ]


    elif process == v_sheet_alternated_weeks:

        values_to_check_duplicated = [v_cred_cod_center, v_cred_plan,v_year, v_cred_mod_code,v_cred_model, v_epd_alternatedd_linea]


    df_duplicated = df[df.duplicated(subset=values_to_check_duplicated,keep=False)].copy()
    df = df[~df.duplicated(subset=values_to_check_duplicated,keep=False)].copy()

    return(df, df_duplicated)

def filter_model_criterion_by_semestre(df : DataFrame, semestre : str):
    
    df = df [df[v_periodo_fileconect] == semestre].copy()

    return(df)


def update_data_to_btt (df : DataFrame):


    columns_to_drop = [v_plan_name_fileconect]
    
    df.drop(columns = columns_to_drop, inplace=True)


    df[v_mod_code_dominated_to_search_module] = df[v_mod_code_fileconect].apply(lambda x: x[1:])
    df[v_mod_code_fileconect] = df[v_mod_code_fileconect].apply(lambda x: x[0])
    df[v_mod_name_fileconect] = df[v_mod_name_fileconect].apply(lambda x: x[0])
    df[v_grupo_fileconect] = df[v_grupo_fileconect].apply(lambda x: x[0])
    df[v_plan_dominant] = df[v_plan_fileconect].apply(lambda x: x[0])
    df[v_center_plan_dominant] = df[v_cred_cod_center].apply(lambda x: x[0])


    return(df)

def add_model_module_section_conector (df_conector : DataFrame, df_model_mod : DataFrame):

    df_model_mod.rename(columns={v_cred_mod_code : v_mod_code_fileconect}, inplace=True)
    df_conector = merge(left=df_conector, right=df_model_mod, on = [v_cred_cod_center, v_plan_fileconect, v_mod_code_fileconect], how='left', indicator=True)

    df_conector[v_cred_model] = where(df_conector[v_merge] != 'both', 'SinModelo', df_conector[v_cred_model])
    df_conector[v_cred_credits] = where(df_conector[v_merge] != 'both', 'SinModelo', df_conector[v_cred_credits])
    df_conector.drop(columns=v_merge, inplace=True)


    return(df_conector)


def add_model_module_credit_section_conector (df_conector : DataFrame, df_model_cred_mod : DataFrame, flag_second_semester : bool):

    df_model_cred_mod.rename(columns={v_cred_plan : v_plan_dominant,
                                      v_cred_cod_center : v_center_plan_dominant }, inplace=True)
    
    if flag_second_semester:

        df_conector_without_week_criteria = df_conector[df_conector[v_center_plan_dominant].isin(v_center_without_default_week_criteria)]

        df_conector = df_conector[df_conector[v_center_plan_dominant].isin(v_center_with_default_week_criteria)]

        df_conector_without_week_criteria[v_cred_period] = v_period_default_week_criteria
        df_conector_without_week_criteria[v_cred_week_EB] = v_weeks_by_type_default_week_criteria
        df_conector_without_week_criteria[v_cred_week_EPD] = v_weeks_by_type_default_week_criteria
        df_conector_without_week_criteria[v_cred_week_AD] = v_weeks_by_type_default_week_criteria




    df_conector = merge(left=df_conector, right=df_model_cred_mod, on = [v_center_plan_dominant,v_plan_dominant,v_cred_model,v_cred_credits], how='left', indicator=True)

    df_conector_sin_modelo_cred = df_conector[df_conector[v_merge] != 'both'].copy()
    df_conector = df_conector[df_conector[v_merge] == 'both']

    df_conector.drop(columns=v_merge, inplace=True)
    df_conector_sin_modelo_cred.drop(columns=v_merge, inplace=True)

    columns_present = [ v_center_plan_dominant,
                        v_cod_act_fileconect,
                        v_cod_grupo_fileconect,
                        v_plan_fileconect,
                        v_curso_fileconect,
                        v_mod_code_fileconect,
                        v_mod_name_fileconect,
                        v_mod_type_activity_fileconect,
                        v_grupo_fileconect,
                        v_cred_model,
                        v_cred_credits
                        ]
    
    df_conector_sin_modelo_cred = df_conector_sin_modelo_cred[columns_present]

    if flag_second_semester:

        df_conector = concat([df_conector, df_conector_without_week_criteria], ignore_index= True)

    return(df_conector, df_conector_sin_modelo_cred)


def filter_data_center (df_data : DataFrame):

    # NEED FILTER FILE PLANNIFICACION - DISTINCT RULES TO DISTINCT CENTER
    values_1_5 = "1|5"
    values_8 = "8"  
    values_3_6_7 = "3|6|7"
    values_2 = "2"
    
    
    df_data[v_center_plan_dominant] = df_data[v_center_plan_dominant].astype(str)
    df_data ['FILTER_FILE']=  where(df_data[v_center_plan_dominant].str.contains(values_1_5, na=False), '1_5', 
                              where(df_data[v_center_plan_dominant].str.contains(values_3_6_7, na = False,), '3_6_7',
                              where(df_data[v_center_plan_dominant].str.contains(values_8, na = False,), '8',
                              where(df_data[v_center_plan_dominant].str.contains(values_2, na = False,), '2', 
                                  'SIN_CENTER'))))

    df_centro_1_5 = df_data[df_data['FILTER_FILE'] == '1_5'].copy()
    df_centro_8 = df_data[df_data['FILTER_FILE'] == '8'].copy()
    df_centro_2 = df_data[df_data['FILTER_FILE'] == '2'].copy()
    df_centro_3_6_7 = df_data[df_data['FILTER_FILE'] == '3_6_7'].copy()




    return (df_centro_1_5, df_centro_8, df_centro_2, df_centro_3_6_7)


def filter_credit_center_1_5_8 (df_model_cred_mod_1_5_8 : DataFrame):

    df_model_cred_mod_1_5_8.rename(columns={v_cred_plan : v_plan_dominant,
                                    v_cred_cod_center : v_center_plan_dominant }, inplace=True)
    
    values_1_5 = "1|5"
    df_model_cred_mod_1_5_8 ['FILTER_FILE']=  where(df_model_cred_mod_1_5_8[v_center_plan_dominant].str.contains(values_1_5, na=False), '1_5', '8') 

    df_model_cred_1_5 = df_model_cred_mod_1_5_8[df_model_cred_mod_1_5_8['FILTER_FILE'] == '1_5'].copy()
    df_model_cred_8 = df_model_cred_mod_1_5_8[df_model_cred_mod_1_5_8['FILTER_FILE'] == '8'].copy()


    return (df_model_cred_1_5, df_model_cred_8)

def add_model_credit_center_1_5 (df_data_center_1_5 : DataFrame, df_model_cred_mod_1_5 : DataFrame, df_model_cred_mod_1_3cred):

    weeks_centro_5_A0_6 = '20,21,22,23,24,25,26,27,28,29,30,32,33,35'

    df_model_cred_mod_1_5.rename(columns={v_student_group : 'GROUP_TEMP_TO_MAP' }, inplace=True)

    #Replace valores de A1b e B1b --  Serão sempre relativos a Centro 1

    df_data_center_1_5[v_cred_model] = df_data_center_1_5[v_cred_model].str.replace ('A1b', 'A1')
    df_data_center_1_5[v_cred_model] = df_data_center_1_5[v_cred_model].str.replace ('B1b', 'B1')

    
    df_centro_1_cred3 = df_data_center_1_5[df_data_center_1_5[v_cred_credits] == '3'].copy()   #COM 3 CREDITOS APENAS O CENTRO 1
    df_centro_1_5 = df_data_center_1_5[df_data_center_1_5[v_cred_credits] != '3'].copy()

    df_centro_1_5['GROUP_TEMP_TO_MAP'] = df_centro_1_5[v_mod_type_activity_fileconect].str[0]
     
    
    #MAP WEEKS CENTER 1 e 5 -- Não é necessario filtrar por linha aplicasse a todas as linhas de Centro a mesma informação Modelo/Creditos
    df_model_cred_mod_1_5 = df_model_cred_mod_1_5[[v_center_plan_dominant,v_cred_model,v_cred_credits,'GROUP_TEMP_TO_MAP',v_cred_weeks ]].copy()
    df_centro_1_5 = merge(left=df_centro_1_5, right=df_model_cred_mod_1_5, on = [v_center_plan_dominant,v_cred_model,'GROUP_TEMP_TO_MAP', v_cred_credits], how='left', indicator=True)

    ### APENAS AS DISCIPLINAS DE MODELO A0 não apresentam correspondencia
    df_centro_1_5 [v_cred_weeks] = where(df_centro_1_5['_merge'] == 'left_only', weeks_centro_5_A0_6, df_centro_1_5[v_cred_weeks])
    df_centro_1_5.drop(columns=['GROUP_TEMP_TO_MAP', '_merge'], inplace=True)

    ## Add semanas linha 1 com 3 creditos
    
    df_model_cred_mod_1_3cred.rename(columns={v_cred_plan : v_plan_dominant,
                                              v_cred_cod_center : v_center_plan_dominant,
                                              v_student_group : 'GROUP_TEMP_TO_MAP' }, inplace=True)

    df_model_cred_mod_1_3cred = df_model_cred_mod_1_3cred [[v_plan_dominant, v_center_plan_dominant, v_mod_code,'GROUP_TEMP_TO_MAP', v_cred_model, v_cred_credits, v_cred_weeks]]
    
    df_centro_1_cred3['GROUP_TEMP_TO_MAP'] = df_centro_1_cred3[v_mod_type_activity_fileconect].str[0]
    df_centro_1_cred3 = merge(left=df_centro_1_cred3, right=df_model_cred_mod_1_3cred, on = [v_plan_dominant, v_center_plan_dominant, v_mod_code,'GROUP_TEMP_TO_MAP', v_cred_model, v_cred_credits], how='left', indicator=True)

    df_centro_1_cred3.drop(columns=['GROUP_TEMP_TO_MAP', '_merge'], inplace=True)    

    df_all_centro_1_5 = concat([df_centro_1_5, df_centro_1_cred3], ignore_index= True)



    return(df_all_centro_1_5)

def add_model_credit_center_8 (df_data_center_8 : DataFrame, df_model_cred_mod_8 : DataFrame):


    df_data_center_8['GROUP_TEMP_TO_MAP'] = df_data_center_8[v_mod_type_activity_fileconect].str[0]
    df_data_center_8['LINEA'] = df_data_center_8[v_plan_linea].str[0]


    df_model_cred_mod_8.rename(columns={v_student_group : 'GROUP_TEMP_TO_MAP'}, inplace=True)
    df_model_cred_mod_8['LINEA'] = df_model_cred_mod_8['LINEA'].str[1]
    
    df_model_cred_mod_8 = df_model_cred_mod_8[[v_center_plan_dominant,v_plan_dominant, 'LINEA', v_cred_model,v_cred_credits,'GROUP_TEMP_TO_MAP',v_cred_weeks ]].copy()
     
    
    data_to_merge = [v_center_plan_dominant,v_plan_dominant, 'LINEA', v_cred_model,v_cred_credits,'GROUP_TEMP_TO_MAP']


    df_data_center_8 = merge(left=df_data_center_8, right=df_model_cred_mod_8, on = data_to_merge, how='left', indicator=True)

    df_data_center_8.drop(columns=['GROUP_TEMP_TO_MAP', 'LINEA','_merge'], inplace=True)

    

    return(df_data_center_8)

def add_model_credit_center_3_6_7 (df_data_center_3_6_7 : DataFrame):

    string_all_weeks_semester = '20,21,22,23,24,25,26,27,28,29,30,32,33,35'

    df_data_center_3_6_7[v_cred_weeks] = string_all_weeks_semester

    return(df_data_center_3_6_7)


def add_model_credit_center_2 (df_data_center_2 : DataFrame):

    string_all_weeks_semester = '20,21,22,23,24,25,26,27,28,29,30,32,33,35'

    df_data_center_2[v_cred_weeks] = string_all_weeks_semester

    return(df_data_center_2)


def concat_all_data(df_data_center_1_5 : DataFrame, df_data_center_8 : DataFrame, df_data_center_3_6_7 : DataFrame, df_data_center_2 : DataFrame):

    df_all = concat([df_data_center_1_5, df_data_center_8, df_data_center_3_6_7, df_data_center_2], ignore_index= True)



    # TO PROCESS SEGUN SEMESTRE:

    df_all[v_mod_typologie] = df_all[v_mod_type_activity_fileconect].str[0]

    return(df_all)





def select_weeks_by_typologie (df :DataFrame):

    df[v_mod_typologie] = where(df[v_student_group].str.count(r'\d') == 1,'EB',
                          where(df[v_student_group].str.count(r'\d') == 2,'EPD', 'AD'))
    
    df[v_weeks] = where(df[v_mod_typologie] == 'EB', df[v_cred_week_EB],
                  where(df[v_mod_typologie] == 'EPD', df[v_cred_week_EPD], df[v_cred_week_AD]))

    df.drop(columns = [v_cred_week_EB,v_cred_week_EPD, v_cred_week_AD], inplace=True)
    return (df)


def check_week_typologie_not_null (df : DataFrame):

    #FICHEIRO DE SEMANAS PODE APRESENTAR MODELO DE CREDITO PARA DISCIPLINA, NO ENTANTO PARA UMA TIPOLOGIA NÂO TER AS SEMANAS.


    df_null = df[df[[v_weeks,v_mod_typologie]].isnull().any(axis=1)].copy()
    df_null.fillna('NULL', inplace = True)

    columns_present = [
                        v_cod_act_fileconect,
                        v_cod_grupo_fileconect,
                        v_plan_fileconect,
                        v_curso_fileconect,
                        v_mod_code_fileconect,
                        v_mod_name_fileconect,
                        v_mod_type_activity_fileconect,
                        v_grupo_fileconect,
                        v_cred_model
                        ]

    df_null = df_null[columns_present]
    
    df = df.dropna(axis=0, subset=v_weeks).copy()

    return(df, df_null)


def add_hours_credits_model (df_conector :DataFrame, df_model_credit_hours : DataFrame):

    df_model_credit_hours.drop(columns=v_cred_weeks, inplace=True) # Inserted Second Semester

    df_model_credit_hours.rename(columns={v_cred_actividad : v_mod_typologie}, inplace=True)
    df_conector = merge(left=df_conector, right = df_model_credit_hours, on = [v_cred_model,v_cred_credits,v_mod_typologie], how='left', indicator=True)

    df_conector_sin_modelo_cred = df_conector[df_conector[v_merge] != 'both'].copy()
    df_conector = df_conector[df_conector[v_merge] == 'both']

    df_conector.drop(columns=v_merge, inplace=True)
    df_conector_sin_modelo_cred.drop(columns=v_merge, inplace=True)

    columns_present = [ v_center_plan_dominant,
                        v_cod_act_fileconect,
                        v_cod_grupo_fileconect,
                        v_plan_fileconect,
                        v_curso_fileconect,
                        v_mod_code_fileconect,
                        v_mod_name_fileconect,
                        v_mod_type_activity_fileconect,
                        v_grupo_fileconect,
                        v_cred_model
                        ]
    df_conector_sin_modelo_cred = df_conector_sin_modelo_cred[columns_present]

    return(df_conector, df_conector_sin_modelo_cred)


def hours_weeks_section (df : DataFrame):

    df[v_cred_weeks] = df[v_cred_weeks].astype(int)
    df[v_cred_hours] = df[v_cred_hours].astype(int)
    df[v_slot_number] = df[v_cred_hours] * 2

    df[v_hours_wload] = df[v_slot_number] // df[v_cred_weeks]
    df[v_slot_number_rest] = df[v_slot_number] % df[v_cred_weeks]
 
    return(df)


def manage_values_weeks(df : DataFrame):

    df[v_weeks] = df[v_cred_weeks]
    df.drop(columns=v_cred_weeks, inplace=True)

    df[v_weeks] = df[v_weeks].str.replace('.', ',')
    df[v_weeks] = df[v_weeks].str.replace(', ', ',')
    df[v_weeks] = df[v_weeks].str.replace(', ', ',')
    df[v_weeks] = df[v_weeks].apply(lambda x: x.strip())

    df[v_cred_weeks] = df[v_weeks].str.count(',') + 1



    return(df)

def replace_number_weeks_hoja_model_by_number_weeks_hoja_criterios_defecto(df : DataFrame):

    df['TEMP_WEEKS'] = df[v_weeks].str.count(',') + 1
    df[v_cred_weeks] = df['TEMP_WEEKS']

    df.drop(columns='TEMP_WEEKS', inplace=True)



    return(df)

