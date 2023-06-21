from PackLibrary.librarys import (	
    ExcelWriter,
    read_excel,
    DataFrame
)
from mod_variables import *

def read_data_file (name_file : str):

    # Manage values Blank
    val_null = ['NULL', 'null', '']

    path_file_name = './' + v_folder_data_uxxi + '/' + name_file
    sheet_name = v_sheet_data_uxxi

    df = read_excel (path_file_name, sheet_name, dtype = 'str', keep_default_na=False, na_values=val_null)

    return(df)

def write_file(df, path_associad, sheet_name_associad):
    
    with ExcelWriter(path_associad, engine = 'openpyxl', mode='a') as writer:  
        df.to_excel(writer, sheet_name=sheet_name_associad,index = False, freeze_panes=(1,0) )

def cleaning_data (df : DataFrame):
	
	df = df.apply(lambda x: x.str.strip())
	df.columns = df.columns.str.strip()
	
	return (df)

def filter_null_values (df : DataFrame):
      
    df_null = df[df.isnull().any (axis=1)].copy()
    df_null.fillna('NULL', inplace = True)

    if not df_null.empty:
         
         print ('Check what to do')
    
    df = df.dropna(axis=0, how ='any').copy()


    return(df, df_null)

def create_insert_validation_file (df : DataFrame, process_folder : str, process_code : str,sheet_name : str, flag_file_created : bool):

    path_more_filename = process_folder + '/' + v_process_manage_data + '/' + v_file_validation_data_uxxi + process_code + '.xlsx' 
    
    if flag_file_created:
         
        write_file(df, path_more_filename, sheet_name)
    
    else:

        df.to_excel(path_more_filename, sheet_name, index = False,freeze_panes=(1,0))

    return()

def filter_by_activity_type (df : DataFrame):
     
    # df_right_type = df[(df[v_mod_typologie] == 'EB') | (df[v_mod_typologie] == 'EPD') | (df[v_mod_typologie] == 'AD') ].copy()
    # df_wrong_type = df[(df[v_mod_typologie] != 'EB') & (df[v_mod_typologie] != 'EPD') & (df[v_mod_typologie] != 'AD') ].copy()

    df_right_type = df[(df[v_mod_typologie] == 'EB') | (df[v_mod_typologie] == 'EPD')].copy()
    df_wrong_type = df[(df[v_mod_typologie] != 'EB') & (df[v_mod_typologie] != 'EPD') ].copy()

    return (df_right_type, df_wrong_type)
      
