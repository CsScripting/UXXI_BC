from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *


def modules_df_from_json(module : list):

    df = DataFrame(columns = [v_name_best,
                                      v_acronym_best,
                                      v_code_best,
                                      v_priority_mod_best,
                                      v_academic_area_best])
    for i in range (len(module)):
    
        name_module = module[i][v_name_dto]
        acronym_module = module[i][v_acronym_dto]
        code_module = module[i][v_code_dto]

        
        name_scientific_area = module[i][v_scientif_area_dto][v_name_dto]


        df = df.append({v_name_best : name_module, 
                                            v_acronym_best : acronym_module,
                                            v_code_best : code_module,
                                            v_priority_mod_best : '1',
                                            v_academic_area_best : name_scientific_area}, 
                                            ignore_index = True)    



    return(df)