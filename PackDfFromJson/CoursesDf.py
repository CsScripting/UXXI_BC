from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *


def parse_list_courses_to_df (course : list):

    df = DataFrame(course)

    columns_used_from_json = [
                              v_name_dto,
                              v_acronym_dto,
                              v_code_dto
                              ]
    

    #Filter DataFrame Values
    df = df [columns_used_from_json].copy()


    columns_to_rename = {   
                            
                            v_name_dto : v_name_best,
                            v_acronym_dto : v_acronym_best,
                            v_code_dto : v_code_best,
       
                        }


    df.rename(columns=columns_to_rename, inplace = True)
    

    return(df)