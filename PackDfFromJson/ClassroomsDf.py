from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *

def parse_list_classrooms_to_df (classroom : list, flag_need_id : bool = False):

    df = DataFrame(classroom)

    columns_used_from_json = [v_id_dto,
                              v_name_dto,
                              v_code_dto,
                              ]
    

    #Filter DataFrame Values
    df = df [columns_used_from_json].copy()

    if not df.empty:

        columns_to_rename = {   
                                
                                v_id_dto : v_id_best, 
                                v_name_dto : v_name_best,
                                v_code_dto : v_code_best,
                                
                            }


        df.rename(columns=columns_to_rename, inplace = True)

        if not flag_need_id:

            df.drop(columns=v_id_best, inplace=True)

        else:

            df.drop(columns=[v_code_best], inplace=True)

    else:

        df_columns = [v_id_best, v_name_best, v_code_best]

        df = DataFrame(columns=df_columns)

        if not flag_need_id:

            df.drop(columns=v_id_best, inplace=True)

        else:

            df.drop(columns=[v_code_best], inplace=True)


    return(df)
    

    


    
    return(df)

