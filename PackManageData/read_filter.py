from PackLibrary.librarys import (	
    ExcelWriter,
    read_excel,
    read_csv,
    DataFrame
)
from mod_variables import *

def read_data_file (name_file : str):

    # Manage values Blank
    val_null = ['NULL', 'null', '']

    path_file_name = './' + v_folder_data_uxxi + '/' + name_file
    sheet_name = v_sheet_schedules_data_uxxi


    df = read_csv (path_file_name, sep= ';',encoding = 'UTF-8' , dtype = 'str')

    # df = read_excel (path_file_name, sheet_name, dtype = 'str', keep_default_na=False, na_values=val_null)

    # values_modules = ['504011','902019' ]
    # df = df[df[v_mod_code].isin(values_modules)].copy()
    # df = df[( df[v_activity_code] == '40238') & (df[v_student_group_code] == '78451')].copy()

    return(df)

def read_data_file_xlsx (name_file :str, sheet_name : str):

    # Manage values Blank
    val_null = ['NULL', 'null', '']

    path_file_name = './' + v_folder_data_uxxi + '/' + name_file

    df = read_excel (path_file_name, sheet_name, dtype = 'str', keep_default_na=False, na_values=val_null)

    return(df)

def write_file(df, path_associad, sheet_name_associad):
    
    with ExcelWriter(path_associad, engine = 'openpyxl', mode='a') as writer:  
        df.to_excel(writer, sheet_name=sheet_name_associad,index = False, freeze_panes=(1,0) )

def cleaning_data (df : DataFrame):
	
	df = df.apply(lambda x: x.str.strip())
	df.columns = df.columns.str.strip()
	
	return (df)

def select_only_columns_to_process( df : DataFrame):

    df = df [[v_id_code, v_course_code, v_course_name, v_year, v_mod_code, v_mod_name,
              v_mod_typologie,v_student_group, v_activity_code, v_student_group_code,v_week_begin,
              v_week_end, v_day, v_hourBegin_split,v_minute_begin_split, v_hourEnd_split, 
              v_minute_end_split, v_duration, v_students_number,v_mod_modalidad, v_classroom_code, v_classroom_name, v_id_classroom_uxxi]].copy()


    return(df)

def filter_null_values (df : DataFrame):
    
    columns_not_null = [v_id_code, v_course_code, v_course_name,v_year,
                        v_mod_code,v_mod_name, v_mod_typologie,
                        v_student_group, v_activity_code,v_student_group_code,
                        v_week_begin, v_week_end, v_day, v_hourBegin_split,
                        v_minute_begin_split, v_hourEnd_split, v_minute_end_split,
                        v_duration,v_mod_modalidad, v_students_number
                        ]

    df_null = df[df[columns_not_null].isnull().any (axis=1)].copy()
    df_null.fillna('NULL', inplace = True)
    
    df = df.dropna(axis=0, subset=columns_not_null).copy()

    #Apenas Aplicado a Salas
    df.fillna('', inplace=True)


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
      


def select_columns_to_process_planning( df : DataFrame):

    semestre_planificacion = df[v_periodo_fileconect].iloc[0]
    df = df[[v_plan_name_fileconect,
             v_plan_fileconect,
             v_curso_fileconect,
             v_mod_code_fileconect,
             v_mod_name_fileconect,
             v_grupo_fileconect,
             v_cod_act_fileconect,
             v_cod_grupo_fileconect]].copy()
    
    return(df, semestre_planificacion)