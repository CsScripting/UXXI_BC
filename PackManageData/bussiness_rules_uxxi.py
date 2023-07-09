import PackManageData.join_tuples_data as manData

from PackLibrary.librarys import (	
  DataFrame,
  where,
  merge,
  to_datetime,
  timedelta
)

from mod_variables import *
import PackGeneralProcedures.files as genFile

def group_entities(df, list_series, sep = ',', sort_flag = True):
    
    #Por vezes valores numericos tem o . (No entanto não se pode tratar aqui, pode haver campos com o .)
    # df = df.applymap(str).replace('\.0', '', regex=True)
    df.set_index (list_series, inplace=True)
    df = df.groupby (level = list_series, sort = sort_flag).agg(sep.join)
    df.reset_index(inplace=True)
    return df


def relacion_group_EPD_by_section_to_asign_to_EB(df : DataFrame):

    # See README.md    

    df_mod_plan_gr = df[[v_course_name,v_course_code, v_year, v_mod_code, v_mod_typologie,v_student_group]].copy()
    
    df_mod_plan_gr_EPD = df_mod_plan_gr[df_mod_plan_gr[v_mod_typologie] == 'EPD'].copy()

    df_mod_plan_gr_EPD [v_identifier_gg] = df_mod_plan_gr_EPD[v_student_group].str[0]

    
    df_mod_plan_gr_EPD [v_student_group_name_to_EB] = df_mod_plan_gr_EPD[v_course_code] + '_' + df_mod_plan_gr_EPD [v_year] + '_' + df_mod_plan_gr_EPD[v_mod_typologie] + \
                                                      df_mod_plan_gr_EPD[v_student_group]
    
    df_mod_plan_gr_EPD.drop_duplicates(inplace=True)

    df_mod_plan_gr_EPD = df_mod_plan_gr_EPD[[v_course_name, v_course_code, v_year, v_mod_code, v_identifier_gg,v_student_group_name_to_EB]].copy()
    
    series_to_agg = [v_course_name,v_course_code, v_year, v_mod_code, v_identifier_gg,]
    df_mod_plan_gr_EPD = group_entities(df_mod_plan_gr_EPD, series_to_agg)
    df_mod_plan_gr_EPD.rename(columns={v_identifier_gg : v_student_group}, inplace = True)
    df_mod_plan_gr_EPD[v_mod_typologie] = 'EB'
    
    return(df_mod_plan_gr_EPD)

def add_group_section_EPD (df : DataFrame):
    
    df [v_student_group_name] = where (df[v_mod_typologie] == 'EPD',
                                          df[v_course_code] + '_' + df [v_year] + '_' + df[v_mod_typologie] + df[v_student_group],
                                          'EB_To_Asign' )

    return (df)

def add_group_section_EB (df : DataFrame, df_relacion_EPD_EB : DataFrame):

    
    df = merge(left=df, right=df_relacion_EPD_EB, how = 'left', on=[v_course_name,v_course_code, v_year, v_mod_code, v_student_group,v_mod_typologie], indicator=True)

    #apenas os valores de v_merge = 'both' são relativos a EB e têm correspondencia
    #valores v_merge = 'left' e TIPO = EB, quer dizer que EB não tem EPD e fica a EPD com Nomenclatura PLAN_YEAR_EPD_GRUPO + 1
    
    df[v_student_group_name]= where(df[v_merge] == 'both', df[v_student_group_name_to_EB],
                              where((df[v_merge] == 'left_only') & (df[v_mod_typologie] == 'EB') , 
                                       df[v_course_code] + '_' + df [v_year] + '_EPD'  + df[v_student_group] + '1',         
                                       df[v_student_group_name]))


    df.drop(columns=[v_student_group_name_to_EB, v_split_weeks, v_merge], inplace=True)

    return(df)


def agg_groups_from_event (df : DataFrame):

    df[v_value_grado] = where(df[v_course_name].str[0] == 'G', '1', '0')
    df.sort_values(by=[v_value_grado, v_mod_code], ascending=[False,True], inplace=True)


    series_agg_event = [v_mod_typologie,v_student_group,v_activity_code, v_student_group_code,v_day, 
                        v_duration, v_hourBegin_split, v_hourEnd_split,v_minute_begin_split,v_minute_end_split, v_weeks, v_classroom_code, v_classroom_name]
    
    df_agg_event = group_entities (df,series_agg_event,sep= '#')

    df_agg_event.drop(columns=v_value_grado, inplace=True)

    return(df_agg_event)

def select_number_students(df : DataFrame):

    df[v_students_number] = df[v_students_number].str.split('#').str[0]

    return(df)


def add_duration_event (df : DataFrame):

    df['Hour_Begin_Temp'] = df[v_hourBegin]
    df['Hour_End_Temp'] = df[v_hourEnd]

    
    df['Hour_Begin_Temp'] = to_datetime(df['Hour_Begin_Temp'])
    df['Hour_End_Temp'] = to_datetime(df['Hour_End_Temp'])

    df[v_duration] = (df['Hour_End_Temp'] - df['Hour_Begin_Temp']).dt.total_seconds() / 3600

    df.drop(columns=['Hour_Begin_Temp', 'Hour_End_Temp'], inplace = True)

    return(df)


def create_format_csv_uxxi (df : DataFrame, path_folder, path_type_folder):

    
    df = df [[v_mod_code, v_mod_name, v_id_uxxi, v_mod_typologie,v_section_name,
           v_weeks, v_day, v_hourBegin, v_hourEnd,v_classroom_name, v_classroom_code ]].copy()
    
    df.insert(2, v_year, df[v_id_uxxi].str.split('_').str[1])
    df.insert(3, v_activity_code, df[v_id_uxxi].str.split('_').str[2])
    df.insert(4, v_student_group_code, df[v_id_uxxi].str.split('_').str[3])
    df.insert(5, v_student_group, df[v_section_name].str.split(' ').str[1])


    #Manage Weeks

    df = manData.split_by_rows(df, v_weeks, sep=',')

    df.rename(columns={v_weeks : v_week_begin}, inplace=True)
    df[v_week_begin] = to_datetime(df[v_week_begin], dayfirst = True)
    df[v_week_end] = df[v_week_begin] + timedelta(days=5)

    df[v_week_begin].apply(lambda x: x.strftime('%Y-%m-%d'))
    df[v_week_end].apply(lambda x: x.strftime('%Y-%m-%d'))
    df[v_day] = df[v_day].astype(int) + 1

    df[v_hourBegin_split] = df[v_hourBegin].str.split(':').str[0].astype(int)
    df[v_minute_begin_split] = df[v_hourBegin].str.split(':').str[-1].astype(int)

    df[v_hourEnd_split] = df[v_hourEnd].str.split(':').str[0].astype(int)
    df[v_minute_end_split] = df[v_hourEnd].str.split(':').str[-1].astype(int)

    df[v_hourBegin] = to_datetime(df[v_hourBegin])
    df[v_hourEnd] = to_datetime(df[v_hourEnd])

    df[v_duration] = (df[v_hourEnd] - df[v_hourBegin]).dt.total_seconds() / 3600

    df[v_plan_csv] = df[v_id_uxxi].str.split('_').str[0]

    df[v_code_tipo_actividad_csv] = where(df[v_mod_typologie] == 'EB', '171', '172')

    
    df = df [[v_mod_code, v_mod_name, v_year,v_mod_typologie, v_code_tipo_actividad_csv, v_activity_code,v_student_group_code,v_student_group,
              v_week_begin, v_week_end, v_day,v_hourBegin_split,v_minute_begin_split, v_hourEnd_split,v_minute_end_split, v_classroom_code,v_classroom_name, v_plan_csv]].copy()

    path_file = path_folder + '/'+ path_type_folder + '/'
    
    genFile.create_csv_file(df, path_file)
    
    return(df)


def select_type_module_uuxi(df :DataFrame):

    df[v_mod_modalidad] = df[v_mod_modalidad].str.split('#').str[0]
    df[v_mod_modalidad] = df[v_mod_modalidad].str.split(',').str[0]

    return(df) 
