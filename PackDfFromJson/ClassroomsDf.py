from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *



def classrooms_df_from_json(classroom : list, flag_need_id : bool = False):

    df = DataFrame(columns=[v_id_best,
                            v_name_best,
                            v_code_best
                            ])
    
    for i in range (len(classroom)):
    
        id_class = classroom[i][v_id_dto]
        name_class = classroom[i][v_name_dto]
        code_class = classroom[i][v_code_dto]


        df = df.append({v_id_best : id_class, 
                        v_name_best : name_class, 
                        v_code_best : code_class
                         }, 
                        ignore_index = True)    

    if not flag_need_id:

        df.drop(columns=v_id_best, inplace=True)

    else:

        df.drop(columns=[v_code_best], inplace=True)


    return(df)

