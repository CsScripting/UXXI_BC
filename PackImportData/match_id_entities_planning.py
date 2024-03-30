from PackLibrary.librarys import (	
    DataFrame,
    merge,
    concat, 
    ast
)

from mod_variables import *

def file_plan_modules_add_id_plan (df_data_plan_mod : DataFrame, df_id_plan: DataFrame):

    # Iniciate Dataframe Invalid Data

    columns_data_frame = [v_name_best, v_code_best, v_year_best,v_course_code_best, v_mod_code, v_mod_name, v_code_request, v_message_request ]

    df_invalid_planning_data = DataFrame(columns = columns_data_frame)

    df_id_plan_filter = df_id_plan[[v_id_best, v_code_best]].copy()

    
    df_data_plan_mod = merge(left=df_data_plan_mod, right = df_id_plan_filter, on = v_code_best, how='left', indicator = True)

    df_data_plan_mod_with_id_plan = df_data_plan_mod[df_data_plan_mod[v_merge] == 'both'].copy() 
    df_data_plan_mod_without_id_plan = df_data_plan_mod[df_data_plan_mod[v_merge] == 'left_only'].copy()

    #CASO DE SEGUIDA...SENDO DATAFRAME VAZIO ADICIONA AS DUAS COLUNAS ADICIONAIS; NO ENTANTO MANTEM-SE O DATAFRAME VAZIO !!! E NÂO INSERE A COLUNA DE v_merge
    df_data_plan_mod_without_id_plan [v_code_request] = '404' # ---> Code Entity Not Found
    df_data_plan_mod_without_id_plan [v_message_request] = v_error_id_plan + ' - ' + v_error_id

    if not df_data_plan_mod_without_id_plan.empty:

        df_data_plan_mod_without_id_plan.drop(columns=[v_merge, v_id_best], inplace=True)

    df_invalid = concat([df_invalid_planning_data, df_data_plan_mod_without_id_plan], ignore_index= True) ###Para poder passar ficheiro Vazio faz concat mesmo que df_data_plan_mod_without_id_plan EMPTY

    df_data_plan_mod_with_id_plan.drop(columns=v_merge, inplace=True)
    df_data_plan_mod_with_id_plan.rename(columns = {v_id_best : v_id_plan_best}, inplace=True)


    return(df_data_plan_mod_with_id_plan, df_invalid)


def file_plan_modules_add_id_module (df_data_plan_mod : DataFrame, df_id_mod: DataFrame, df_invalid : DataFrame):

    df_id_mod_filter = df_id_mod[[v_id_best, v_code_best]].copy()
    df_id_mod_filter.rename(columns = {v_code_best: v_mod_code }, inplace=True)

    
    df_data_plan_mod = merge(left=df_data_plan_mod, right = df_id_mod_filter, on = v_mod_code, how='left', indicator = True)

    df_data_plan_mod_with_id_mod = df_data_plan_mod[df_data_plan_mod[v_merge] == 'both'].copy() 
    df_data_plan_mod_without_id_mod = df_data_plan_mod[df_data_plan_mod[v_merge] == 'left_only'].copy()

    #CASO DE SEGUIDA...SENDO DATAFRAME VAZIO ADICIONA AS DUAS COLUNAS ADICIONAIS; NO ENTANTO MANTEM-SE O DATAFRAME VAZIO !!! E NÂO INSERE A COLUNA DE v_merge
    df_data_plan_mod_without_id_mod [v_code_request] = '404' # ---> Code Entity Not Found
    df_data_plan_mod_without_id_mod [v_message_request] = v_error_id_mod + ' - ' + v_error_id

    if not df_data_plan_mod_without_id_mod.empty:

        df_data_plan_mod_without_id_mod.drop(columns=[v_merge, v_id_best, v_id_plan_best], inplace=True)
        df_invalid = concat([df_invalid, df_data_plan_mod_without_id_mod], ignore_index= True)

    df_data_plan_mod_with_id_mod.drop(columns=v_merge, inplace=True)
    df_data_plan_mod_with_id_mod.rename(columns = {v_id_best : v_mod_id}, inplace=True)

    
    return (df_data_plan_mod_with_id_mod, df_invalid)


def file_wloads_add_mod_id (df_data_w_load_mod : DataFrame, df_id_mod: DataFrame):


    df_id_mod_filter = df_id_mod[[v_id_best, v_code_best]].copy()
    df_id_mod_filter.rename(columns = {v_code_best: v_mod_code }, inplace=True)

    df_data_w_load_mod = merge(left=df_data_w_load_mod, right = df_id_mod_filter, on = v_mod_code, how='left', indicator = True)


    df_data_w_load_mod = df_data_w_load_mod[df_data_w_load_mod[v_merge] == 'both'].copy() 
    df_data_w_load_mod.drop(columns=v_merge, inplace=True)
    df_data_w_load_mod.rename(columns={v_id_best : v_mod_id}, inplace= True)

    return (df_data_w_load_mod)



def file_wloads_add_mod_type_id (df_data_w_load_mod : DataFrame, df_id_mod_type: DataFrame):


    df_id_mod_filter = df_id_mod_type[[v_id_best, v_name_best]].copy()
    df_id_mod_filter.rename(columns = {v_name_best: v_mod_typologie }, inplace=True)

    df_data_w_load_mod = merge(left=df_data_w_load_mod, right = df_id_mod_filter, on = v_mod_typologie, how='left', indicator = True)
    df_data_w_load_mod = df_data_w_load_mod[df_data_w_load_mod[v_merge] == 'both'].copy() 

    df_data_w_load_mod.drop(columns=v_merge, inplace=True)
    df_data_w_load_mod.rename(columns={v_id_best : v_mod_id_typologie}, inplace=True)

    return (df_data_w_load_mod)

def verify_id_group(name_group : str, df_id_group : DataFrame):

    value_id = df_id_group.loc[df_id_group[v_name_best]==name_group, [v_id_best]]
    

    return (value_id.iloc[0,0])


def file_wloads_add_groups_id (df_data_w_load_group : DataFrame, df_id_group: DataFrame):

    df_data_w_load_group[v_student_group_best] = df_data_w_load_group[v_student_group_best].apply(lambda x: ast.literal_eval(x))

    df_data_w_load_group[v_id_st_group] = df_data_w_load_group[v_student_group_best]. \
                                         apply(lambda x:  [[verify_id_group(value, df_id_group) for value in list] for list in x])

    return(df_data_w_load_group)