from PackLibrary.librarys import (	
    ExcelWriter,
    DataFrame
)

def write_file(df, path_associad, sheet_name_associad):
    
    with ExcelWriter(path_associad, engine = 'openpyxl', mode='a') as writer:  
        df.to_excel(writer, sheet_name=sheet_name_associad,index = False, freeze_panes=(1,0) )

def create (df : DataFrame, process_folder : str, process_code : str,v_file_name : str, sheet_name : str, folder : str, flag_file_created : bool = False):

    path_more_filename = process_folder + '/' + folder + '/' + v_file_name + process_code + '.xlsx' 
    
    if flag_file_created:
         
        write_file(df, path_more_filename, sheet_name)
    
    else:

        df.to_excel(path_more_filename, sheet_name, index = False,freeze_panes=(1,0))

    return()