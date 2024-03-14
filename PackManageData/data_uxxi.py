from PackLibrary.librarys import (	
  DataFrame,
  to_datetime,
  datetime,
  where
)
from mod_variables import *
import PackGeneralProcedures.files as genFiles
import PackManageData.join_tuples_data as manData

def check_courses_uxxi (df : DataFrame, process_folder : str, process_code : str, main_process : str):

    if main_process == v_main_process_schedules:
    
        df = df [[v_course_name, v_course_code]].copy()

        df.drop_duplicates(inplace=True)
        df[v_acronym_best] = df[v_course_code]

        df.rename(columns={v_course_name : v_name_best,
                           v_course_code : v_code_best}, inplace=True)
        
    if main_process == v_main_process_planning:

         df = df [[v_plan_fileconect, v_plan_name_fileconect]].copy()
         df.drop_duplicates(inplace=True)
         df.rename(columns={v_plan_fileconect : v_code_best,
                            v_plan_name_fileconect : v_name_best}, inplace=True)

         df[v_acronym_best] = df[v_code_best]
 
    df = df [[v_name_best, v_acronym_best, v_code_best]].copy()

    genFiles.create  (df,process_folder,process_code, v_file_curriculum_uxxi, v_sheet_courses, v_process_manage_data)

    return()

def check_planes_uxxi (df : DataFrame, process_folder : str, process_code : str, main_process: str):

    flag_file_created = True

    df_verify_planes = df.copy()

    if main_process == v_main_process_planning:

        df_verify_planes.rename(columns={v_plan_fileconect : v_course_code,
                                         v_plan_name_fileconect : v_course_name}, inplace=True)

    #Notes README
    df_verify_planes = df_verify_planes [[v_course_name, v_course_code, v_year, v_student_group]].copy()

    df_verify_planes[v_identifier_gg] = df_verify_planes[v_student_group].str[0]
    
    df_verify_planes[v_name_best] = df_verify_planes[v_course_name] + '_' + df_verify_planes[v_year] + '_' + df_verify_planes[v_identifier_gg]
    df_verify_planes[v_code_best] = df_verify_planes[v_course_code] + '_' + df_verify_planes[v_year] + '_' + df_verify_planes[v_identifier_gg]

    df_verify_planes.rename(columns={v_year : v_year_best,
                       v_course_code : v_course_code_best}, inplace=True)

    df_verify_planes = df_verify_planes [[v_name_best,  v_code_best, v_year_best, v_course_code_best]].copy()
    df_verify_planes.drop_duplicates(inplace=True)

    genFiles.create  (df_verify_planes,process_folder,process_code, v_file_curriculum_uxxi, v_sheet_planes, v_process_manage_data, flag_file_created)


    return()

def check_planes_modules (df:DataFrame, process_folder : str, process_code : str):

    flag_file_created = True

    df.drop(columns=[v_cod_grupo_fileconect, v_cod_act_fileconect], inplace=True)
    df = df.explode([v_plan_fileconect, v_plan_name_fileconect,v_curso_fileconect, v_grupo_fileconect]).reset_index(drop=True)

    df.rename(columns={v_plan_fileconect : v_course_code,
                       v_plan_name_fileconect : v_course_name}, inplace=True)
    

    #Notes README
    df = df [[v_course_name, v_course_code, v_year, v_student_group, v_mod_code, v_mod_name]].copy()

    df[v_identifier_gg] = df[v_student_group].str[0]
    
    df[v_name_best] = df[v_course_name] + '_' + df[v_year] + '_' + df[v_identifier_gg]
    df[v_code_best] = df[v_course_code] + '_' + df[v_year] + '_' + df[v_identifier_gg]

    df.rename(columns={v_year : v_year_best,
                       v_course_code : v_course_code_best}, inplace=True)

    df = df [[v_name_best,  v_code_best, v_year_best, v_course_code_best, v_mod_code, v_mod_name]].copy()
    df.drop_duplicates(inplace=True)
    df = df.sort_values(by=v_code_best)

    genFiles.create  (df, process_folder,process_code, v_file_curriculum_uxxi, v_sheet_planes_modules, v_process_manage_data, flag_file_created)
    
    

    return(df)

def group_mutual_modules_plannificacion(df : DataFrame):

    series_to_group = [v_cod_act_fileconect,
                       v_cod_grupo_fileconect]
    
    df['PLAN_TYPE'] = df[v_plan_fileconect].str[0]
    df['PLAN_TYPE_ID'] = where(df['PLAN_TYPE'] == 'G','1',
                         where(df['PLAN_TYPE'] == 'X','2',
                         where(df['PLAN_TYPE'] == 'M','3',
                         where(df['PLAN_TYPE'] == 'F','4','5'))))
    
    df.sort_values(by=['PLAN_TYPE_ID', v_curso_fileconect, v_mod_code_fileconect], inplace=True)
    df.drop(columns=['PLAN_TYPE','PLAN_TYPE_ID'], inplace=True)

    df = manData.group_entities_to_list(df,series_to_group,sep=',')

    return(df)





def check_st_groups_uxxi_schedules (df : DataFrame, process_folder : str, process_code : str):

    flag_file_created = True

    df = df [[v_course_name, v_course_code, v_year, v_student_group, v_mod_typologie, v_students_number, v_student_group_name]].copy()

    df.rename(columns= {v_student_group_name : v_name_best}, inplace=True)

    #Create Name Plan
    df[v_identifier_gg] = df[v_student_group].str[0]

    df[v_plan_code_best] = df[v_course_code] + '_' + df[v_year] + '_' + df[v_identifier_gg]

    df = df [[v_name_best, v_plan_code_best, v_students_number]].copy()

    df = manData.split_by_rows(df, v_name_best, ',')

    df.sort_values(by=[v_name_best,v_students_number], ascending=[True, False], inplace=True)
   
    df[v_code_best] = df[v_name_best]

    df.drop_duplicates(subset=[v_name_best, v_code_best, v_plan_code_best], inplace=True)

    df.rename(columns={v_students_number : v_students_number_best}, inplace=True)

    df = df[[v_name_best, v_code_best, v_plan_code_best,v_students_number_best]]


    genFiles.create  (df,process_folder, process_code, v_file_curriculum_uxxi, v_sheet_st_group, v_process_manage_data, flag_file_created)

    return()

def create_st_group_uxxi_planning (df : DataFrame, process_folder : str, process_code : str):

    flag_file_created = True
    
    df = df[[v_plan_name_fileconect, v_plan_fileconect, v_year, v_mod_code, v_mod_typologie,v_student_group]].copy()
    
    df [v_identifier_gg] = df[v_student_group].str[0]

    # df [v_student_group_best] = df[v_plan_fileconect] + '_' + df [v_year] + '_' + df[v_mod_typologie] + \
                                # df[v_student_group]
    
    
    df[v_plan_code_best] = df[v_plan_fileconect] + '_' + df[v_year] + '_' + df[v_identifier_gg]
    
    df.drop(columns=[v_identifier_gg,
                     v_plan_name_fileconect,
                     v_plan_fileconect,
                     v_curso_fileconect,
                     v_mod_code], inplace=True )
    
    df[v_mod_id_typologie] = where(df[v_mod_typologie] == 'EB',1,
                                where(df[v_mod_typologie] == 'EPD',2,
                                where(df[v_mod_typologie] == 'AD',3,5)))
    
    df.drop_duplicates(inplace=True)
    df = df.sort_values(by=[v_mod_id_typologie],ascending=False)

    df.drop(columns=[v_mod_id_typologie,
                    v_mod_typologie], inplace=True )


    series_to_group = [v_plan_code_best]

    
    df = manData.group_entities_to_list(df, series_to_group)
    df_iterator = df.copy()

    for row in df_iterator.itertuples():

        groups_to_btt = []

        index_dataframe = row[0]

        groups_uxxi = getattr(row, v_student_group)

        groups_uxxi = [int(x) for x in groups_uxxi]

        for value in groups_uxxi:

            if len(str(value)) == 3:

                groups_to_btt.append(value)

            elif len(str(value)) == 2:

                if any ([value * 10 < x < value * 10 + 9  for x in groups_to_btt] ):

                    continue

                else:

                     groups_to_btt.append(value)

            elif len(str(value)) == 1:

                if groups_to_btt == []:

                    groups_to_btt.append(value)

                else:

                    continue

        df.at[index_dataframe, v_student_group] = groups_to_btt
            
    
    df[v_number_groups_plan] = df[v_student_group].apply(lambda x : len(x))
    # CADA LINEA (PLANO)TERÁ 60 ALUNOS A Dividir por o Maximo de Turmas 

    # EFETUADA DIVISÂO EQUITATIVA DOS ALUNOS POR GRUPOS
    number_students_linea = 60
    df[v_students_number_best] = df[v_number_groups_plan].apply(lambda x: [number_students_linea] * x)
    df[v_students_number_best] = df.apply(lambda x: [value//x[v_number_groups_plan] + 1
                                      if( (value % x[v_number_groups_plan] != 0 ) and (index_value + 1 <= value % x[v_number_groups_plan] ))
                                      else value//x[v_number_groups_plan]
                                      for index_value, value in enumerate(x[v_students_number_best]) ], axis = 1)

    df_relacion_groups_plan = df.copy()
    df.drop(columns=[v_number_groups_plan], inplace=True )
    df = df.explode([v_student_group,v_students_number_best]).reset_index(drop=True).sort_values(by=[v_plan_code_best, v_student_group])

    df[v_student_group] = df[v_student_group].astype(str)
    df[v_mod_typologie] = where(df[v_student_group].str.count(r'\d') == 1,'EB',
                          where(df[v_student_group].str.count(r'\d') == 2,'EPD', 'AD'))

    df.rename(columns={v_student_group_best : v_name_best}, inplace=True)

    df [v_name_best] = df[v_plan_code_best].str.split('_').str[0] + '_' + \
                       df[v_plan_code_best].str.split('_').str[1] + '_'  + \
                       df[v_mod_typologie] + df[v_student_group]
    
    df[v_code_best] = df[v_name_best]

    df = df[[v_name_best, v_code_best, v_plan_code_best,v_students_number_best]]

    genFiles.create  (df,process_folder, process_code, v_file_curriculum_uxxi, v_sheet_st_group, v_process_manage_data, flag_file_created)


    return(df_relacion_groups_plan)
    


def check_modules_uxxi (df : DataFrame, process_folder : str, process_code : str ,main_process: str):

    flag_file_created = True

    if main_process == v_main_process_planning:

        df.rename(columns={v_mod_name_fileconect : v_mod_name,
                           v_mod_code_fileconect : v_mod_code}, inplace=True)

    df = df [[v_mod_name, v_mod_code]].copy()
    df.drop_duplicates(inplace=True)

    df.rename(columns={v_mod_name : v_name_best,
                       v_mod_code : v_code_best}, inplace=True)
    
    df[v_acronym_best] = df [v_code_best]
    df[v_priority_mod_best] = '1'
    df[v_academic_area_best] = 'SD'

    genFiles.create  (df, process_folder, process_code, v_file_curriculum_uxxi, v_sheet_modules, v_process_manage_data, flag_file_created)


    return()


def check_typologies_uxxi (df : DataFrame, process_folder : str, process_code : str):

    flag_file_created = True

    df = df [[v_mod_typologie]].copy()
    df.drop_duplicates(inplace=True)

    df.rename(columns={v_mod_typologie : v_name_best}, inplace=True)
    df[v_description_typologie_best] = 'Add Description'

    genFiles.create  (df,process_folder, process_code, v_file_curriculum_uxxi, v_sheet_typologies, v_process_manage_data, flag_file_created)

    return()

def check_typologies_uxxi_from_file_conector (df : DataFrame):

    df['CHECK_TYPE'] = df[v_grupo_fileconect].str.len()

    df[v_mod_typologie] = where(df['CHECK_TYPE'] == 1,'EB',
                          where(df['CHECK_TYPE'] == 2, 'EPD' ,'AD'))
    
    df.drop(columns='CHECK_TYPE', inplace=True)

    return (df)


def check_classrooms_uxxi (df : DataFrame, process_folder : str, process_code : str):

    flag_file_created = True

    df = df [[v_classroom_name, v_classroom_code, v_id_classroom_uxxi]].copy()

    df = df[df[v_classroom_name] != ''].copy()
    df.drop_duplicates(inplace=True)

    df[v_classroom_code] = df[v_classroom_code] + ' - (' + df[v_id_classroom_uxxi] + ')'

    df.sort_values(by=v_classroom_name, inplace=True)

    df.drop(columns=v_id_classroom_uxxi, inplace=True)

    df.rename(columns={v_classroom_name : v_name_best,
                       v_classroom_code : v_code_best}, inplace=True)
    

    genFiles.create  (df,process_folder, process_code, v_file_curriculum_uxxi, v_sheet_classrooms, v_process_manage_data, flag_file_created)

    return()


def check_date_begin_end_schedules (df: DataFrame):

    df = df[[v_weeks]].copy()

    df[v_week_first] = df[v_weeks].str.split(',').str[0]
    df[v_week_last] = df[v_weeks].str.split(',').str[-1]

    df[v_week_first] = to_datetime(df[v_week_first],format="%Y-%m-%d", dayfirst = True)
    df[v_week_last] = to_datetime(df[v_week_last], format="%Y-%m-%d",dayfirst = True)

    value_minimum = df[v_week_first].min()
    value_higer = df[v_week_last].max()

    value_higer = value_higer + datetime.timedelta(days=7) ## When call Events ALL is by day not by Week !!!!

    value_higer = value_higer.strftime("%Y-%m-%d")
    value_minimum = value_minimum.strftime("%Y-%m-%d")

    return(value_minimum, value_higer)

def create_df_info_date_events (start_day : str, end_day : str):

    df_process = DataFrame(columns = [v_variables_process, v_variables_values])

    #Insert StartDay ### APPEND DEPRECATED
    df_process.loc[len(df_process), df_process.columns] = v_variable_start_day, start_day
    #Insert EndDAy
    df_process.loc[len(df_process), df_process.columns] = v_variable_end_day, end_day





    return(df_process)

def plans_to_btt_extract_only_dominant_modules (df:DataFrame):
    
    df[v_mod_code_fileconect] = df[v_mod_code_fileconect].apply(lambda x: x[0])
    df[v_mod_name_fileconect] = df[v_mod_name_fileconect].apply(lambda x: x[0])
    # df[v_grupo_fileconect] = df[v_grupo_fileconect].apply(lambda x: x[0])


    return(df)


def create_df_info_mutual_modules_to_file (df : DataFrame,  process_folder : str, process_code : str):

    df_to_file = df.copy()

    df_to_file[v_plan_name_dominant] = df_to_file[v_plan_name_fileconect].apply(lambda x: x[0])
    df_to_file[v_plan_name_dominated] = df_to_file[v_plan_name_fileconect].apply(lambda x: ',' .join(x[1:]))
    df_to_file[v_plan_dominant] = df_to_file[v_plan_fileconect].apply(lambda x: x[0])
    df_to_file[v_plan_dominated] = df_to_file[v_plan_fileconect].apply(lambda x: ',' .join(x[1:]))
    df_to_file[v_curso_dominant] = df_to_file[v_curso_fileconect].apply(lambda x: x[0])
    df_to_file[v_curso_dominated] = df_to_file[v_curso_fileconect].apply(lambda x: ',' .join(x[1:]))
    df_to_file[v_grupo_dominant] = df_to_file[v_grupo_fileconect].apply(lambda x: x[0])
    df_to_file[v_grupo_dominated] = df_to_file[v_grupo_fileconect].apply(lambda x: ',' .join(x[1:]))
    df_to_file[v_mod_name_dominant] = df_to_file[v_mod_name_fileconect].apply(lambda x: x[0])
    df_to_file[v_mod_name_dominated] = df_to_file[v_mod_name_fileconect].apply(lambda x: ',' .join(x[1:]))
    df_to_file[v_mod_code_dominant] = df_to_file[v_mod_code_fileconect].apply(lambda x: x[0])
    df_to_file[v_mod_code_dominated] = df_to_file[v_mod_code_fileconect].apply(lambda x: ',' .join(x[1:]))
    
    df_to_file.drop(columns = [v_plan_name_fileconect,
                       v_plan_fileconect,
                       v_curso_fileconect,
                       v_grupo_fileconect,
                       v_mod_code_fileconect,
                       v_mod_name_fileconect], inplace = True)
    
    genFiles.create  (df_to_file, process_folder, process_code, v_file_mutual_modules, v_sheet_mutual_modules, v_process_manage_data)

    return (df)


def add_groups_bullet (df_conector : DataFrame, df_groups : DataFrame):

    df_conector[v_plan_linea] = df_conector[v_student_group].str[0] 

    df_iterator = df_conector.copy()

    for row in df_iterator.itertuples():

        groups_to_btt = []
        index_dataframe = row[0]
        plan = getattr(row, v_plan_fileconect)
        plan_linea = getattr (row, v_plan_linea)
        plan_year = getattr (row, v_year)
        group_value = getattr(row, v_student_group)

        counter_list = 0

        for code_plan in plan:

            plan_to_check = code_plan + '_' + str(plan_year[counter_list]) + '_' + str(plan_linea)
            groups_plan = df_groups.loc[df_groups[v_plan_code_best] == plan_to_check ,v_student_group].iloc[0]

            groups_plan = [str(x) for x in groups_plan]
            groups_to_use_btt = [value for value in groups_plan if value.startswith(str(group_value))]

            for value in groups_to_use_btt:
                
                if len(value) == 1:

                    type_group = 'EB'
                
                elif len(value) == 2:

                    type_group = 'EPD'

                else:

                    type_group ='AD'  
                
                name_group_to_btt = code_plan + '_' + str(plan_year[counter_list]) + '_' + type_group + value

                groups_to_btt.append(name_group_to_btt)
            
            
            counter_list += 1

        df_conector.at[index_dataframe, v_student_group_best] = groups_to_btt



    return(df_conector)


def create_df_w_loads_to_file (df : DataFrame,  process_folder : str, process_code : str, sub_process : str):

    if sub_process == v_process_update_data:

        file_name = v_file_wloads
        df[v_data_to_import_new] = 1

    else: ### NESTE CASO SERÁ O PROCESSO DE MANAGE DATA

        file_name = v_file_wloads_info

    genFiles.create  (df, process_folder, process_code, file_name, v_sheet_wloads, sub_process)

    return()

    


