import PackManageData.join_tuples_data as manData
from mod_variables import *
from PackLibrary.librarys import (	
  DataFrame
)


def verify_common_conect (df : DataFrame ):

    series_to_group = [v_cod_act_fileconect, v_cod_grupo_fileconect]
    df = manData.group_entities(df, series_to_group)

    return(df)