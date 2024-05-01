from mod_variables import *
from PackLibrary.librarys import (	
  DataFrame,
  merge,
  where
)

def filter_columns_process (df: DataFrame, process : str):


    if process == v_sheet_model_module:

        columns = [v_cred_cod_center,
                   v_cred_plan, 
                   v_cred_mod_code, 
                   v_cred_model,
                   v_cred_credits]
    

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


    df_duplicted = df[df.duplicated(subset=values_to_check_duplicated,keep=False)].copy()
    df = df[~df.duplicated(subset=values_to_check_duplicated,keep=False)].copy()

    return(df, df_duplicted)

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


def add_model_module_credit_section_conector (df_conector : DataFrame, df_model_cred_mod : DataFrame):

    df_model_cred_mod.rename(columns={v_cred_plan : v_plan_dominant,
                                      v_cred_cod_center : v_center_plan_dominant }, inplace=True)
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

    return(df_conector, df_conector_sin_modelo_cred)


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


def add_hours_credits_model (df_conector :DataFrame, df_model_credit_hours):

    df_model_credit_hours.rename(columns={v_cred_actividad : v_mod_typologie}, inplace=True)
    df_conector = merge(left=df_conector, right = df_model_credit_hours, on = [v_cred_model,v_cred_credits,v_mod_typologie], how='left', indicator=True)

    df_conector_sin_modelo_cred = df_conector[df_conector[v_merge] != 'both'].copy()
    df_conector = df_conector[df_conector[v_merge] == 'both']

    df_conector.drop(columns=v_merge, inplace=True)
    df_conector_sin_modelo_cred.drop(columns=v_merge, inplace=True)

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
    df_conector_sin_modelo_cred = df_conector_sin_modelo_cred[columns_present]

    return(df_conector, df_conector_sin_modelo_cred)


def hours_weeks_section (df : DataFrame):

    df[v_cred_weeks] = df[v_cred_weeks].astype(int)
    df[v_cred_hours] = df[v_cred_hours].astype(int)
    df[v_slot_number] = df[v_cred_hours] * 2

    df[v_hours_wload] = df[v_slot_number] // df[v_cred_weeks]
    df[v_slot_number_rest] = df[v_slot_number] % df[v_cred_weeks]
 
    return(df)

