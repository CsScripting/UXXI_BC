from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *


def st_groups_df_from_json(st_group : list, flag_need_id : bool = False):

    df = DataFrame(columns=[v_id_best,
                            v_name_best,
                            v_code_best,
                            v_plan_code_best,
                            v_students_number_best,
                            v_daily_limit_best,
                            v_consecutive_limit_best])
    
    for i in range (len(st_group)):
    
        id_st_group = st_group[i][v_id_dto]
        name_st_group = st_group[i][v_name_dto]
        code_st_group = st_group[i][v_code_dto]
        students_st_group = st_group[i][v_students_number_dto]
        daily_st_group = st_group[i][v_daily_limit_dto]
        consecutive_st_group = st_group[i][v_consecutive_limit_dto]
        
        plan_code = st_group[i][v_curricular_plan_dto][v_code_dto]


        df = df.append({v_id_best : id_st_group, 
                        v_name_best : name_st_group, 
                        v_code_best : code_st_group,
                        v_plan_code_best : plan_code,
                        v_students_number_best : students_st_group,
                        v_daily_limit_best : daily_st_group,
                        v_consecutive_limit_best : consecutive_st_group}, 
                        ignore_index = True)    

    if not flag_need_id:

        df.drop(columns=v_id_best, inplace=True)

    else:

        df.drop(columns=[v_code_best,v_plan_code_best,v_students_number_best, v_daily_limit_best, v_consecutive_limit_best], inplace=True)


    return(df)