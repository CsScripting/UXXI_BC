from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *


def typologies_df_from_json(typologie : list):

    df = DataFrame(columns = [v_name_best,
                              v_description_typologie_best])
    for i in range (len(typologie)):
    
        name_typologie = typologie[i][v_name_dto]
        description_typologie = typologie[i][v_description_dto]


        df = df.append({v_name_best : name_typologie, 
                        v_description_typologie_best : description_typologie}, 
                        ignore_index = True)    



    return(df)