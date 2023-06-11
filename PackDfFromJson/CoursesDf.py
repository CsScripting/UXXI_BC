from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *


def courses_df_from_json( course : list):

    # if empty list create a Empty Data Frame
    df = DataFrame(columns = [v_name_best,
                              v_acronym_best,
                              v_code_best])
    
    for i in range (len(course)):
    
        name_course = course[i][v_name_dto]
        acronym_course = course[i][v_acronym_dto]
        code_course = course[i][v_code_dto]


        df = df.append({v_name_best : name_course, 
                        v_acronym_best : acronym_course,
                        v_code_best : code_course}, 
                        ignore_index = True)    



    return(df)