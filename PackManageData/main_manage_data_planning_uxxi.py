import PackGeneralProcedures.global_variable_process_procedures as glVarProcess
import PackGeneralProcedures.files as genFiles
import PackManageData.folders_process_manage as folderProcess
import PackManageData.read_filter as readFilter
import PackManageData.data_uxxi as dataUxxi
from mod_variables import *



def manage_data_planning_uxxi_steps (name_file_inserted : str):


    #CREAR PASTA DE PLANIFICAÇÂO
    glVarProcess.gl_process_folder, glVarProcess.gl_process_code = folderProcess.create_main_folder_manage_process(v_process_planning_sub_folder)

    process_folder = glVarProcess.gl_process_folder
    process_code = glVarProcess.gl_process_code

    #LER DADOS
    df_planning = readFilter.read_data_file_xlsx(name_file_inserted)
    df_planning = genFiles.filter_file_not_null_values(df_planning) ## IMPORTANTE VERIFICAR NULOS POR CAUSA DOS GROUP BY

    #VERIFICAÇAO DADOS PLANIFICAÇÂO
    df_data_to_btt = df_planning.copy()
    dataUxxi.check_courses_uxxi (df_data_to_btt, process_folder, process_code, v_main_process_planning)







    return()