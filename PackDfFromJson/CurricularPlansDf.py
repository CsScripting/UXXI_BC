from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *

def plan_df_from_json(plan : list):

    df = DataFrame(columns = [v_name_best,
                              v_code_best,
                              v_year_best,
                              v_course_code_best])
    
    for i in range (len(plan)):
    
        name_plan = plan[i][v_name_dto]
        code_plan = plan[i][v_code_dto]
        year_plan = plan[i][v_year_dto]

        course_code = plan[i][v_course_dto][v_code_dto]
        


        df = df.append({v_name_best : name_plan,
                        v_code_best : code_plan,
                        v_year_best : year_plan,
                        v_course_code_best : course_code}, 
                        ignore_index = True)    



    return(df)