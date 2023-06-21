from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *


def weeks_df_from_json(weeks : list):

    df = DataFrame(columns = [v_id_best,
                              v_name_best])
    
    for i in range (len(weeks)):
    
        id_weeks = weeks[i][v_id_dto]
        name_weeks = weeks[i][v_start_date_dto]
        


        df = df.append({v_id_best : id_weeks,
                        v_name_best : name_weeks}, 
                        ignore_index = True)    

    

    return(df)