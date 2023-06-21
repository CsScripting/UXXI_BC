from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *


def typologies_df_from_json(typologie : list, flag_need_id : bool = False):

    df = DataFrame(columns = [v_id_best,
                              v_name_best,
                              v_description_typologie_best])
    
    for i in range (len(typologie)):
    
        id_typologie = typologie[i][v_id_dto]
        name_typologie = typologie[i][v_name_dto]
        description_typologie = typologie[i][v_description_dto]


        df = df.append({v_id_best : id_typologie,
                        v_name_best : name_typologie, 
                        v_description_typologie_best : description_typologie}, 
                        ignore_index = True)    

    if not flag_need_id:

        df.drop(columns=v_id_best, inplace=True)

    else:

        df.drop(columns=[v_description_typologie_best], inplace=True)

    return(df)