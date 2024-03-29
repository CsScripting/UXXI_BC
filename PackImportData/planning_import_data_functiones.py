import PackControllerRequest.general_requests as genRequest
import PackManageApi.global_variable_process_request as gl_v_request
import PackDfFromJson.ModulesDf as modDf
import PackDfFromJson.TypologiesDf as typeDf
import PackDfFromJson.StudentGroupsDf as stGroupDf
import PackDfFromJson.CurricularPlansDf as planDf
import PackManageData.join_tuples_data as manData

from PackLibrary.librarys import(
DataFrame,
ast
)


from mod_variables import * 

def manage_data_acad_term (data_acad_term : list):

    df = DataFrame(data_acad_term)

    columns_used_from_json = [v_id_dto,
                              v_name_dto,
                              v_start_time_acad_term_dto,
                              v_end_time_acad_term_dto,
                              v_weeks_acad_term_dto
                              ]

    #Filter DataFrame Values
    df = df [columns_used_from_json].copy()

    df[v_acad_term_id] =  df[v_id_dto]
    df[v_acad_term_name] =  df[v_name_dto]
    df[v_acad_term_star_time] = df[v_start_time_acad_term_dto].str[-8:]
    df[v_acad_term_end_time] = df[v_start_time_acad_term_dto].str[-8:]

    df[v_weeks] = df[v_weeks_acad_term_dto].apply(lambda x: [d[v_start_date_dto][0:10] for d in x])
    df[v_weeks_id] = df[v_weeks_acad_term_dto].apply(lambda x: [d[v_id_dto] for d in x])

    df.drop(columns =   [v_id_dto,
                        v_name_dto,
                        v_start_time_acad_term_dto,
                        v_end_time_acad_term_dto,
                        v_weeks_acad_term_dto], inplace=True)
    
    id_academci_year = df[v_acad_term_id].iloc[0]
    first_id_week = df[v_weeks_id].iloc[0][1]



    return(df, id_academci_year, first_id_week)


def insert_module_plan_btt (df_mod_plan :DataFrame):

    return


def collect_entities_id_to_process ():

    flag_need_id=True

    #MODULES
    modules_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_module_controller)
    df_modules_best = modDf.parse_list_mod_to_df(modules_db,flag_need_id)


    #MODULES TYPOLOGIES
    typologies_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_typologie_controller)
    df_typologies_best = typeDf.parse_list_typologies_to_df(typologies_db, flag_need_id)


    #STUDENT GROUPS
    st_groups_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_st_group_controller)
    df_st_group_best = stGroupDf.parse_list_st_groups_to_df(st_groups_db, flag_need_id)


    #CURRICULAR PLANES
    planes_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_plan_controller)
    df_plan_best = planDf.parse_list_plan_to_df(planes_db, flag_need_id)

    return (df_plan_best, df_st_group_best, df_modules_best, df_typologies_best)


def group_modules_plan (df : DataFrame):

    df_filter = df[[v_id_plan_best, v_mod_id]].copy()

    df_filter = df_filter.applymap(str)
    df_filter = manData.group_entities(df_filter, v_id_plan_best, sep=',')

    return(df_filter)

def add_id_week (df : DataFrame, first_week_id : int):

    df[v_weeks] = df [v_weeks].str.split(',').apply(lambda x: [(int(value) + first_week_id - 1 ) for value in x])
    df[v_weeks] = df[v_weeks].agg(lambda x: ','.join(map(str, x)))

    return(df)


def select_w_load_sectiones_to_import(df :DataFrame):

    df = df [df[v_data_to_import_new] == '1'].copy()
    df.drop(columns=v_data_to_import_new, inplace=True)

    return(df)

def agg_weekloads_same_pattern (df : DataFrame):

    df.drop(columns=[v_student_group_best, v_section_name], inplace=True)

    df = df.map(str)
    values_to_agg = [v_name_wload, v_mod_typologie,v_mod_id_typologie, v_hours_wload, v_session_wload, v_section_number, v_weeks]

    df = manData.group_entities(df, values_to_agg, sep = ',')

    return(df)

