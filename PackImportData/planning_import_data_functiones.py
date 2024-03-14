from PackLibrary.librarys import(
DataFrame,
ast
)


from mod_variables import * 

def manage_weeks_acad_term (data_acad_term : list):

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

    return(df)