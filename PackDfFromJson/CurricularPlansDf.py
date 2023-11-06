from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *

def parse_list_plan_to_df (plan : list):

    df = DataFrame(plan)

    columns_used_from_json = [v_id_dto,
                              v_name_dto,
                              v_code_dto,
                              v_year_dto,
                              v_course_dto
                              ]
    

    #Filter DataFrame Values
    df = df [columns_used_from_json].copy()

    #Extract values from object/Dict

    ## - SingleValues Dict: - ##

    #Course
    df[v_course_code_best] =  df[v_course_dto].apply(lambda x: x.get(v_code_dto))

    #DropColumnsObjects

    columns_to_drop = [     
                        v_course_dto
                        
                      ]

    df.drop(columns=columns_to_drop, inplace=True)

    columns_to_rename = {   
                            
                            v_name_dto : v_name_best, 
                            v_code_dto : v_code_best,
                            v_year_dto : v_year_best,
                               
                        }


    df.rename(columns=columns_to_rename, inplace = True)
    

    order_columns_df = [ 
                        v_name_best, 
                        v_code_best,
                        v_year_best,
                        v_course_code_best
                        ]


    df = df [order_columns_df].copy()


    
    return(df)