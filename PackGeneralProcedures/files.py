from PackLibrary.librarys import (	
    ExcelWriter,
    DataFrame,
    read_excel
)
from mod_variables import *


def write_file(df, path_associad, sheet_name_associad):
    
    with ExcelWriter(path_associad, engine = 'openpyxl', mode='a') as writer:  
        df.to_excel(writer, sheet_name=sheet_name_associad,index = False, freeze_panes=(1,0) )

def create (df : DataFrame, process_folder : str, process_code : str, file_name : str, sheet_name : str, folder : str, flag_file_created : bool = False):

    if folder == v_process_import_data:

        if len (process_code.split('_')) > 2:

            values_process_code = process_code.split('_')

            code = '_' + values_process_code[1] + '_' + values_process_code[2]

        path_more_filename = process_folder + '/' + process_code + '/' + folder + '/' + file_name + code + '.xlsx' 
    
    else:

        path_more_filename = process_folder + '/' + folder + '/' + file_name + process_code + '.xlsx' 
    
    if flag_file_created:
         
        write_file(df, path_more_filename, sheet_name)
    
    else:

        df.to_excel(path_more_filename, sheet_name, index = False,freeze_panes=(1,0))

    return()


def read_data_files_update (main_folder_process : str, process_code : str,folder_type_process : str, name_file : str, sheet_name : str):

    # Manage values Blank
    val_null = ['NULL', 'null', '']

    name_folder_process = v_process_sub_folder + process_code
    name_file_process = name_file + process_code + '.xlsx'

    path_file_name = './' + main_folder_process + '/' + name_folder_process + '/' + folder_type_process + '/' + name_file_process
    

    df = read_excel (path_file_name, sheet_name, dtype = 'str', keep_default_na=False, na_values=val_null)

    return(df)

def read_data_files_import (main_folder_process : str, name_folder_process : str,folder_type_process : str, name_file : str, sheet_name : str):

    # Manage values Blank
    val_null = ['NULL', 'null', '']

    code_process = '_' + name_folder_process.split('_')[1] + '_' + name_folder_process.split('_')[2]
    name_file_process = name_file + code_process + '.xlsx'

    path_file_name = './' + main_folder_process + '/' + name_folder_process + '/' + folder_type_process + '/' + name_file_process
    

    df = read_excel (path_file_name, sheet_name, dtype = 'str', keep_default_na=False, na_values=val_null)

    return(df)

def create_csv_file (df : DataFrame, path : str):

    name_file = 'CSV_Horarios.csv'
    path_to_file = path + name_file

    df.to_csv(path_to_file, index=False, encoding='iso8859-1', sep=';', na_rep='')

    return()