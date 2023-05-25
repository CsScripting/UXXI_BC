from PackLibrary.librarys import (	
    DataFrame,
    merge
)
from mod_variables import *


def compare_courses_uxxi_db (df_uxxi : DataFrame, df_best : DataFrame):

    df_best.rename(columns={v_name_best : v_name_best_match,
                            v_acronym_best : v_acronym_best_match}, inplace=True)
    

    df_uxxi = merge(left=df_uxxi, right=df_best, how = 'left', on=v_code_best, indicator=True)

    df_uxxi_to_import = df_uxxi[df_uxxi [v_merge] == 'left_only'].copy()

    if not df_uxxi_to_import.empty:
    
        df_uxxi_to_import.drop(columns=[v_name_best_match,
                                        v_acronym_best_match,
                                        v_merge], inplace=True)
        
        df_uxxi_to_import[v_data_to_import_new] = '1'

    return(df_uxxi_to_import)