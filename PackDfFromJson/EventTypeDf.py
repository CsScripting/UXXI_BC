from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *


def event_type_df_from_json(event_type : list):

    df = DataFrame(columns = [v_id_best,
                              v_name_best])
    
    for i in range (len(event_type)):
    
        id_event_type = event_type[i][v_id_dto]
        name_event_type = event_type[i][v_name_dto]
        


        df = df.append({v_id_best : id_event_type,
                        v_name_best : name_event_type}, 
                        ignore_index = True)    

    

    return(df)