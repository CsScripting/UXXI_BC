from PackLibrary.librarys import (	
  DataFrame,
  to_datetime,
  datetime,
  where,
  concat,
  merge
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

def group_mutual_modules_plannificacion(df : DataFrame, primer_semestre : bool):

    series_to_group = [v_cod_act_fileconect,
                       v_cod_grupo_fileconect]
    
    df['PLAN_TYPE'] = df[v_plan_fileconect].str[0]
    df['PLAN_TYPE_ID'] = where(df['PLAN_TYPE'] == 'G','1',
                         where(df['PLAN_TYPE'] == 'X','2',
                         where(df['PLAN_TYPE'] == 'M','3',
                         where(df['PLAN_TYPE'] == 'F','4','5'))))
    

    if primer_semestre:
        df['TYPE_COMPARTIDA'] = where(df[v_cred_compartida] == 'COMPARTIDA PRINCIPAL','1',
                                where(df[v_cred_compartida] == 'COMPARTIDA NO PRINCIPAL ','2',
                                 where(df[v_cred_compartida] == 'NO COMPARTIDA','3','4')))
        
    
    else:

        df['TYPE_COMPARTIDA'] = where(df[v_cred_compartida] == 'S','1',
                                where(df[v_cred_compartida] == 'N ','2',3))

                            
    
    df.sort_values(by=['TYPE_COMPARTIDA','PLAN_TYPE_ID', v_curso_fileconect, v_mod_code_fileconect], inplace=True) # ORDENADO PARA MANTER SEMPRE MESMO PLANO DOMINANTE
    df.drop(columns=['PLAN_TYPE','PLAN_TYPE_ID','TYPE_COMPARTIDA'], inplace=True)

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
    
    df = df[[v_plan_name_fileconect, v_plan_fileconect, v_year, v_mod_code, v_mod_typologie, v_student_group]].copy()
    
    df [v_identifier_gg] = df[v_student_group].str[0]

    # df [v_student_group_best] = df[v_plan_fileconect] + '_' + df [v_year] + '_' + df[v_mod_typologie] + \
                                # df[v_student_group]
    
    
    df[v_plan_code_best] = df[v_plan_fileconect] + '_' + df[v_year] + '_' + df[v_identifier_gg]
    
    df.drop(columns=[v_identifier_gg,
                     v_plan_name_fileconect,
                     v_plan_fileconect,
                     v_curso_fileconect,
                     v_mod_code], inplace=True )
    
    
    df.drop_duplicates(inplace=True)
    df['order_type_temp'] = where(df[v_mod_typologie] == 'EB', 2,
                            where(df[v_mod_typologie] == 'EPD', 1,0))
    df = df.sort_values(by=['order_type_temp'],ascending=True)


    df.drop(columns= ['order_type_temp'], inplace=True )


    series_to_group = [v_plan_code_best]
    df = manData.group_entities_to_list(df, series_to_group)


    df_iterator = df.copy()

    for row in df_iterator.itertuples():

        groups_to_btt = []
        type_groups_to_btt = []

        index_dataframe = row[0]

        groups_uxxi = getattr(row, v_student_group)

        groups_uxxi = [int(x) for x in groups_uxxi]

        for value in groups_uxxi:

            if len(str(value)) == 3:

                groups_to_btt.append(value)
                type_groups_to_btt.append('AD')


            elif len(str(value)) == 2:

                if any ([value * 10 < x < value * 10 + 9  for x in groups_to_btt] ):

                    continue

                else:

                     groups_to_btt.append(value)
                     type_groups_to_btt.append('EPD')

            elif len(str(value)) == 1:

                if groups_to_btt == []:

                    groups_to_btt.append(value)
                    type_groups_to_btt.append('EB')

                else:

                    continue
        

        df.at[index_dataframe, v_student_group] = groups_to_btt
        df.at[index_dataframe, v_mod_typologie] = type_groups_to_btt


            
    
    df[v_number_groups_plan] = df[v_student_group].apply(lambda x : len(x))


    df.drop(columns=[v_number_groups_plan], inplace=True )
    df = df.explode([v_student_group, v_mod_typologie]).reset_index(drop=True).sort_values(by=[v_plan_code_best, v_student_group])

    df[v_student_group] = df[v_student_group].astype(str)

    ## ADD NUMBER STUDENTS BY TYPE
    number_students_only_EB = '60'
    number_students_EPD = '20'


    df_EB = df[df[v_mod_typologie] == 'EB'].copy()
    df_EPD = df[df[v_mod_typologie] == 'EPD'].copy()
    df_AD = df[df[v_mod_typologie] == 'AD'].copy()

    if not df_EB.empty:
        df_EB[v_students_number_best] = number_students_only_EB

    if not df_EPD.empty:   
        df_EPD[v_students_number_best] = number_students_EPD


    if not df_AD.empty:
        df_AD['EPD_TEMP'] = df_AD[v_student_group].str[0:2]
        
        series_to_group = [v_plan_code_best,v_mod_typologie,'EPD_TEMP']

        df_AD = manData.group_entities_to_list(df_AD, series_to_group)
        df_AD[v_number_groups_plan] = df_AD[v_student_group].apply(lambda x : len(x))

        df_AD[v_students_number_best] = df_AD[v_number_groups_plan].apply(lambda x: [int(number_students_EPD)] * x)
        df_AD[v_students_number_best] = df_AD.apply(lambda x: [value//x[v_number_groups_plan] + 1
                                        if( (value % x[v_number_groups_plan] != 0 ) and (index_value + 1 <= value % x[v_number_groups_plan] ))
                                        else value//x[v_number_groups_plan]
                                        for index_value, value in enumerate(x[v_students_number_best]) ], axis = 1)

        df_AD = df_AD[[v_plan_code_best,v_mod_typologie, v_student_group,v_students_number_best]].copy()
        df_AD = df_AD.explode([v_student_group, v_students_number_best]).reset_index(drop=True).sort_values(by=[v_plan_code_best, v_student_group])
        df_AD[v_students_number_best] = df_AD[v_students_number_best].astype(str)


    df = concat([df_EB, df_EPD, df_AD], ignore_index= True)

    df_relacion_groups_plan = df.copy()

    df.rename(columns={v_student_group_best : v_name_best}, inplace=True)
    

    df [v_name_best] = df[v_plan_code_best].str.split('_').str[0] + '_' + \
                       df[v_plan_code_best].str.split('_').str[1] + '_'  + \
                       df[v_mod_typologie] + df[v_student_group]
    
    df[v_code_best] = df[v_name_best]

    df = df[[v_name_best, v_code_best, v_plan_code_best,v_students_number_best]]

    genFiles.create  (df,process_folder, process_code, v_file_curriculum_uxxi, v_sheet_st_group, v_process_manage_data, flag_file_created)

    df_relacion_groups_plan = df_relacion_groups_plan[[v_plan_code_best, v_student_group,v_students_number_best]].copy()
    series_to_group = [v_plan_code_best]
    df_relacion_groups_plan = manData.group_entities_to_list(df_relacion_groups_plan, series_to_group)

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


    df[v_mod_typologie] = df[v_mod_type_activity_fileconect]
    df.drop(columns=[v_mod_type_activity_fileconect], inplace=True )

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
    
    df[v_mod_code_dominated_to_search_module] = df[v_mod_code_fileconect].apply(lambda x: x[1:])
    df[v_mod_code_fileconect] = df[v_mod_code_fileconect].apply(lambda x: x[0])
    df[v_mod_name_fileconect] = df[v_mod_name_fileconect].apply(lambda x: x[0])
    
    # df[v_grupo_fileconect] = df[v_grupo_fileconect].apply(lambda x: x[0])


    return(df)


def create_df_info_mutual_modules_to_file (df : DataFrame,  process_folder : str, process_code : str):

    df_to_file = df.copy()

    df_to_file[v_center_plan_dominant] = df_to_file[v_cred_cod_center].apply(lambda x: x[0])
    df_to_file[v_center_plan_dominanted] = df_to_file[v_cred_cod_center].apply(lambda x: ',' .join(x[1:]))
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
    
    df_to_file.drop(columns = [v_cred_cod_center,
                               v_plan_name_fileconect,
                               v_plan_fileconect,
                               v_curso_fileconect,
                               v_grupo_fileconect,
                               v_mod_code_fileconect,
                               v_mod_name_fileconect], inplace = True)
    
    genFiles.create  (df_to_file, process_folder, process_code, v_file_mutual_modules, v_sheet_mutual_modules, v_process_manage_data)

    return (df)


def verify_number_epd_module_by_plan_to_asign_to_eb (df_data : DataFrame):

    df_data[v_plan_linea] = df_data[v_student_group].str[0]
    df = df_data[[v_plan_fileconect,
                  v_plan_linea,
                  v_mod_type_activity_fileconect,
                  v_curso_fileconect,
                  v_grupo_fileconect,
                  v_mod_code_fileconect
                  ]].copy()
    

    
    

    df = df[df[v_mod_type_activity_fileconect] == 'EPD'].copy()

    series_to_group = [ 
                        v_plan_fileconect,
                        v_plan_linea,
                        v_mod_type_activity_fileconect,
                        v_curso_fileconect,
                        v_mod_code_fileconect]
    
    


    df.sort_values(by = v_grupo_fileconect, inplace=True)
    df.drop_duplicates(inplace=True)

    df = manData.group_entities(df, series_to_group,sep=',')
    
    df[v_nr_epd_plan_module] = df[v_grupo_fileconect].str.count(',') + 1
    

    df.rename(columns={v_grupo_fileconect : v_code_epd_plan_module}, inplace=True)


    return(df)

def verify_number_groups_edp_inserted_btt (df : DataFrame):

    df[v_nr_epd_plan] = df[v_grupo_fileconect].apply(lambda x: [value for value in x if len(value) == 2 ])
    df[v_nr_epd_plan] = df[v_nr_epd_plan].apply(lambda x: len(x))
    df[v_nr_epd_plan] = df[v_nr_epd_plan].apply(lambda x: [x])

    df.rename(columns={v_grupo_fileconect : v_groups_by_plan_linea}, inplace=True)
    

    return(df)

def join_info_epd_plan (df_conector : DataFrame, df_relacion_groups_plan :DataFrame):
    

    series_to_merge = [ v_plan_code_best]


    df_conector = merge(left = df_conector, right = df_relacion_groups_plan, on = series_to_merge, how='left', indicator=True )
    df_conector.drop(columns=[v_merge], inplace=True)
    
    

    return(df_conector)

def join_info_edp_module_plan (df_conector : DataFrame, df_relacion_epd_module_linea :DataFrame):
    

    df_conector [v_plan_code_best] =  df_conector [v_plan_fileconect] + '_' + \
                                      df_conector [v_curso_fileconect] + '_' + df_conector [v_plan_linea]


    df_relacion_epd_module_linea [v_plan_code_best] =  df_relacion_epd_module_linea [v_plan_fileconect] + '_' + \
                                                       df_relacion_epd_module_linea [v_curso_fileconect] + '_' + df_relacion_epd_module_linea [v_plan_linea]

    #PASSAR APENAS NRº EPD por PLANO/LINEA
    df_relacion_epd_module_linea = df_relacion_epd_module_linea[[v_plan_code_best,
                                                                 v_mod_code_fileconect,
                                                                 v_code_epd_plan_module,
                                                                 v_nr_epd_plan_module]].copy()
    
    series_to_merge = [ v_plan_code_best,
                        v_mod_code_fileconect ]

    
    df_conector = merge(left = df_conector, right = df_relacion_epd_module_linea, on = series_to_merge, how='left', indicator=True )
    df_conector[v_nr_epd_plan_module] = where (df_conector[v_merge] == 'left_only', 0, df_conector[v_nr_epd_plan_module])
    df_conector[v_code_epd_plan_module] = where (df_conector[v_merge] == 'left_only', '0', df_conector[v_code_epd_plan_module])
    df_conector[v_nr_epd_plan_module] = df_conector[v_nr_epd_plan_module].apply(lambda x: [x])
    df_conector[v_code_epd_plan_module] = df_conector[v_code_epd_plan_module].apply(lambda x: x.split(',') if x != 0 else [x])
    
    df_conector.drop(columns=[v_merge], inplace=True)

    

    return(df_conector)




def add_groups_bullet_and_number_students (df_conector : DataFrame):
 
    df_iterator = df_conector.copy()
    df_conector[v_student_group_best] = ''

    for row in df_iterator.itertuples():

        counter = 0
        groups_to_btt = []
        index_dataframe = row[0]

        code_plan = getattr(row, v_plan_fileconect) #List
        plan_year = getattr(row, v_curso_fileconect) #List
        group_code = getattr(row, v_grupo_fileconect) #STR
        groups_plan_linea = getattr(row, v_groups_by_plan_linea)#List
        nr_epd_plan_module = getattr(row, v_nr_epd_plan_module)#List
        nr_epd_plan = getattr(row, v_nr_epd_plan)#List
        code_epd_plan_module = getattr(row, v_code_epd_plan_module)#List

        type_module = getattr(row, v_mod_type_activity_fileconect)#STR
        

        students_number_groups_plan_linea = getattr(row, v_students_number_best)

        mod_type = getattr(row, v_mod_type_activity_fileconect)
        mod_type = mod_type[0] # VALOR ESTA DENTRO DE LISTA NA SERIES

        for value_code_plan in code_plan:

            groups_to_use_btt = []
            number_students = []

            if ((nr_epd_plan[counter][0] != nr_epd_plan_module[counter][0]) & (type_module[0] == 'EB') & (nr_epd_plan_module[counter][0] != 0) & (nr_epd_plan_module[counter][0] != 0)):

                
                for groups_epd in code_epd_plan_module[counter]:

                    temp_groups_to_use_btt = [value for value in groups_plan_linea[counter] if value.startswith(str(groups_epd))]
                    groups_to_use_btt.extend(temp_groups_to_use_btt)

                    if counter == 0:  # O NUMERO DE ALUNOS APLICASSE APENAS A DOMINANTES
                        
                        # NUMERO DE ALUNOS SO DE DOMINANTE
                        index_groups_list = [index_value for index_value, value in enumerate(groups_plan_linea[counter]) if value.startswith(str(groups_epd))]
                        temp_number_students = [students_number_groups_plan_linea[counter][i] for i in index_groups_list]
                        number_students.extend(temp_number_students)
                    
                        number_students = [int(x) for x in number_students]
                        number_students_total = sum(number_students)
            
            else: #NÂO NECESSARIO COLOCAR QUANDO = 0 SE NÂO TEM NO MODULEPLAN NÂO TEM NO PLAN

                groups_plan_linea[counter] = [str(x) for x in groups_plan_linea[counter]]
                temp_groups_to_use_btt = [value for value in groups_plan_linea[counter] if value.startswith(str(group_code))]
                groups_to_use_btt.extend(temp_groups_to_use_btt)

                if counter == 0:
                    index_groups_list = [index_value for index_value, value in enumerate(groups_plan_linea[counter]) if value.startswith(str(group_code))]

                    #NUMERO DE ALUNOS RETIRADOS SEGUNDO A POSICÂO NA LISTA
                    #POSIÇÂO NA LISTA DE ACORDO COM LISTA DE GRUPOS
                    number_students = [students_number_groups_plan_linea[counter][i] for i in index_groups_list]
                    number_students = [int(x) for x in number_students]
                    number_students_total = sum(number_students)                

            

            for value in groups_to_use_btt:
                
                if len(value) == 1:

                    type_group = 'EB'
                
                elif len(value) == 2:

                    type_group = 'EPD'

                else:

                    type_group ='AD'  
                
                name_group_to_btt = code_plan[counter] + '_' + str(plan_year[counter]) + '_' + type_group + value

                groups_to_btt.append(name_group_to_btt)

            counter += 1
            
            

        df_conector.at[index_dataframe, v_student_group_best] = groups_to_btt
        df_conector.at[index_dataframe, v_students_number] = number_students_total

    df_conector[v_students_number] = df_conector[v_students_number].astype(int) 



    return(df_conector)


def create_df_w_loads_to_file (df : DataFrame,  process_folder : str, process_code : str, sub_process : str, type_file : str):

    if sub_process == v_process_update_data:
        
        if type_file == v_type_file_w_load:
        
            file_name = v_file_wloads
            v_sheet = v_sheet_wloads

        else: 

            file_name =v_file_wloads_section_overlap
            v_sheet = v_sheet_sectiones_overlap

        df[v_data_to_import_new] = 1

    else: ### NESTE CASO SERÁ O PROCESSO DE MANAGE DATA

        if type_file == v_type_file_w_load:
        
            file_name = v_file_wloads_info
            v_sheet = v_sheet_wloads

        else: 
            
            file_name = v_file_wloads_section_overlap_info
            v_sheet = v_sheet_sectiones_overlap

    genFiles.create  (df, process_folder, process_code, file_name, v_sheet, sub_process)

    return()

def create_file_validation_module_credits (df : DataFrame, sheet_name : str,  process_folder : str, process_code : str, sub_process : str):
    
    if not df.empty  &  (sheet_name != v_sheet_wrong_model_module ):

        file_name = v_file_validacion_models_credits

        if sheet_name == v_sheet_wrong_model_module:
            flag_file_created = False
        else:
            flag_file_created = True

        genFiles.create  (df, process_folder, process_code, file_name, sheet_name, sub_process,flag_file_created)
        

    return()


def verify_modeles_UXXI_conector(df : DataFrame):

    df[v_cred_model] = df[v_cred_model].apply (lambda x : set(x) )
    df[v_cred_model] = df[v_cred_model].apply (lambda x : [value for value in x if value != 'SinModelo'] )

    df[v_cred_credits] = df[v_cred_credits].apply (lambda x : set(x) )
    df[v_cred_credits] = df[v_cred_credits].apply (lambda x : [value for value in x if value != 'SinModelo'] )

    df['VALIDACION_MODELO'] = df[v_cred_model].apply (lambda x : len(x) )

    df_sin_modelo = df[df['VALIDACION_MODELO'] == 0].copy()
    df_doble_modelo = df[df['VALIDACION_MODELO'] > 1].copy()
    df = df[df['VALIDACION_MODELO'] ==  1].copy()

    df_invalid_model = concat([df_sin_modelo, df_doble_modelo], ignore_index= True)

    df_doble_modelo[v_cred_model] = df_doble_modelo[v_cred_model].apply(lambda x: x[0])
    df_doble_modelo[v_cred_credits] = df_doble_modelo[v_cred_credits].apply(lambda x: x[0])
    df[v_cred_model] = df[v_cred_model].apply (lambda x : [value for value in x ] ).str.join(',')
    df[v_cred_credits] = df[v_cred_credits].apply (lambda x : [value for value in x ] ).str.join(',')

    df = concat([df, df_doble_modelo], ignore_index= True)

    df.drop(columns='VALIDACION_MODELO', inplace=True)
    df_invalid_model.drop(columns='VALIDACION_MODELO', inplace=True)


    columns_present = [ v_cred_cod_center,
                        v_cod_act_fileconect,
                        v_cod_grupo_fileconect,
                        v_plan_fileconect,
                        v_curso_fileconect,
                        v_mod_code_fileconect,
                        v_mod_name_fileconect,
                        v_mod_type_activity_fileconect,
                        v_grupo_fileconect,
                        v_cred_model
                        ]

    df_invalid_model = df_invalid_model[columns_present]

    return(df, df_invalid_model)



def verify_modeles_UXXI_conector_segun(df : DataFrame):

    df[v_cred_model] = df[v_cred_model].apply (lambda x : set(x) )
    df[v_cred_model] = df[v_cred_model].apply (lambda x : [value for value in x if value != 'SinModelo'] )

    df[v_cred_credits] = df[v_cred_credits].apply (lambda x : set(x) )
    df[v_cred_credits] = df[v_cred_credits].apply (lambda x : [value for value in x if value != 'SinModelo'] )

    df['VALIDACION_MODELO'] = df[v_cred_model].apply (lambda x : len(x) )

    df_sin_modelo = df[df['VALIDACION_MODELO'] == 0].copy()
    df_doble_modelo = df[df['VALIDACION_MODELO'] > 1].copy()
    df = df[df['VALIDACION_MODELO'] ==  1].copy()

    df_invalid_model = concat([df_sin_modelo, df_doble_modelo], ignore_index= True)

    df_doble_modelo[v_cred_model] = df_doble_modelo[v_cred_model].apply(lambda x: x[0])
    df_doble_modelo[v_cred_credits] = df_doble_modelo[v_cred_credits].apply(lambda x: x[0])
    df[v_cred_model] = df[v_cred_model].apply (lambda x : [value for value in x ] ).str.join(',')
    df[v_cred_credits] = df[v_cred_credits].apply (lambda x : [value for value in x ] ).str.join(',')

    df = concat([df, df_doble_modelo], ignore_index= True)

    df.drop(columns='VALIDACION_MODELO', inplace=True)
    df_invalid_model.drop(columns='VALIDACION_MODELO', inplace=True)


    columns_present = [ v_cred_cod_center,
                        v_cod_act_fileconect,
                        v_cod_grupo_fileconect,
                        v_plan_fileconect,
                        v_curso_fileconect,
                        v_mod_code_fileconect,
                        v_mod_name_fileconect,
                        v_mod_type_activity_fileconect,
                        v_grupo_fileconect,
                        v_cred_model
                        ]

    df_invalid_model = df_invalid_model[columns_present]

    return(df, df_invalid_model)


def add_new_w_load_rest_hours (df : DataFrame): ### NESTE MOMENTO NÂO SE ESTA A APLICAR ESTE METODO ...

    df [v_slot_number_rest] = df[v_slot_number_rest].apply(lambda x: x[0])
     
    df_weekly_week_load = df[df[v_slot_number_rest] != 0].copy() ### ONDE SE IRÁ APLICAR A WEEKLOAD COM CARGA HORARIA QUE SOBRA
    df_reference_week_load = df[df[v_slot_number_rest] != 0].copy()
    df_unique_week_load = df[df[v_slot_number_rest] == 0].copy() ### A DISTIRIBUIÇÂO INTEIRA DE HORAS DEU RESTO ZERO

    df_weekly_week_load_EB = df_weekly_week_load[df[v_mod_typologie] == 'EB'].copy()
    df_weekly_week_load_EPD = df_weekly_week_load[df[v_mod_typologie] == 'EPD'].copy()
    df_weekly_week_load_AD = df_weekly_week_load[df[v_mod_typologie] == 'AD'].copy()

    if not df_weekly_week_load_EB.empty: # EXTRACT POSIBLE WEEKS EB
    
        weeks_upo_EB = df_weekly_week_load_EB[v_weeks].values.tolist()
        weeks_upo_EB = ",".join(weeks_upo_EB).split(",")
        unique_weeks_upo_EB = []

        for x in weeks_upo_EB:
            if x not in unique_weeks_upo_EB:
                unique_weeks_upo_EB.append(x)
    
        #CREATE DICTIONARY WITH WEEKS
        dict_unique_weeks_upo_EB = {k: v for v, k in enumerate(unique_weeks_upo_EB)} ### AS KEY DE DICIONARIO SÂO AS SEMANAS POSSIVEIS DE EB
        dict_unique_weeks_upo_EB.update({k:0 for k in dict_unique_weeks_upo_EB}) ### OS VALUES/KEY DE DICIONARIO TODOS A 0
    

    if not df_weekly_week_load_EPD.empty: # EXTRACT POSIBLE WEEKS EB
    
        weeks_upo_EPD = df_weekly_week_load_EPD[v_weeks].values.tolist()
        weeks_upo_EPD = ",".join(weeks_upo_EPD).split(",")
        unique_weeks_upo_EPD = []

        for x in weeks_upo_EPD:
            if x not in unique_weeks_upo_EPD:
                unique_weeks_upo_EPD.append(x)
    
        #CREATE DICTIONARY WITH WEEKS
        dict_unique_weeks_upo_EPD = {k: v for v, k in enumerate(unique_weeks_upo_EPD)} ### AS KEY DE DICIONARIO SÂO AS SEMANAS POSSIVEIS DE EPD
        dict_unique_weeks_upo_EPD.update({k:0 for k in dict_unique_weeks_upo_EPD}) ### OS VALUES/KEY DE DICIONARIO TODOS A 0


    if not df_weekly_week_load_AD.empty: # EXTRACT POSIBLE WEEKS AD
    
        weeks_upo_AD = df_weekly_week_load_AD[v_weeks].values.tolist()
        weeks_upo_AD = ",".join(weeks_upo_AD).split(",")
        unique_weeks_upo_AD = []

        for x in weeks_upo_AD:
            if x not in unique_weeks_upo_AD:
                unique_weeks_upo_AD.append(x)
    
        #CREATE DICTIONARY WITH WEEKS
        dict_unique_weeks_upo_AD = {k: v for v, k in enumerate(unique_weeks_upo_AD)} ### AS KEY DE DICIONARIO SÂO AS SEMANAS POSSIVEIS DE AD
        dict_unique_weeks_upo_AD.update({k:0 for k in dict_unique_weeks_upo_EPD}) ### OS VALUES/KEY DE DICIONARIO TODOS A 0

    df_weekly_week_load['NEW_WEEKS'] = ''
    
    df_weekly_week_load ['TEMP_PLAN'] = df_weekly_week_load[v_name_wload].str.split('_').str[0:3].str.join('_')
    df_weekly_week_load.sort_values(by = ['TEMP_PLAN',v_mod_typologie ], inplace=True)
    df_weekly_week_load.drop(columns=['TEMP_PLAN'], inplace=True)
    

    # AJUSTE DE HORAS A CONSIDERAR EM DATAFRAME DE WEEKLY_WEEK_LOAD
    # NUMERO DE HORAS IGUAL A HORAS DE RESTO DE DIVISÂO DE HORAS POR SEMANAS
    df_weekly_week_load[v_hours_wload] = df_weekly_week_load[v_slot_number_rest] 

    df_weekly_week_load_iterator = df_weekly_week_load.copy()
    

    #ORDENAÇÂO PARA FICAR EM SEMANAS DIFERENTES PARA MESMOS PLANOS/LINEA

    for row in df_weekly_week_load_iterator.itertuples():

        index_dataframe = row[0]
        weeks_module = getattr(row, v_weeks)
        type_module = getattr(row, v_mod_typologie)

        if type_module == 'EB':
            
            list_weeks = weeks_module.split(',') ## GUARDAR SEMANAS EM LISTA
            list_weeks_EB = list_weeks [2:] ## APENAS INSERE A APARTIR DA SEMANA 3 AS NOVAS CARGAS !!!

            filter_dictionary_EB = dict((k,dict_unique_weeks_upo_EB[k]) for k in list_weeks_EB if k in dict_unique_weeks_upo_EB)

            value_min = min(filter_dictionary_EB, key=filter_dictionary_EB.get)
            dict_unique_weeks_upo_EB[value_min] += 1


        if type_module == 'EPD':
            
            list_weeks_EPD = weeks_module.split(',') ## GUARDAR SEMANAS EM LISTA
            # list_weeks_EPD = list_weeks [2:] ## APENAS INSERE A APARTIR DA SEMANA 3 AS NOVAS CARGAS !!!

            filter_dictionary_EPD = dict((k,dict_unique_weeks_upo_EPD[k]) for k in list_weeks_EPD if k in dict_unique_weeks_upo_EPD)

            value_min = min(filter_dictionary_EPD, key=filter_dictionary_EPD.get)
            dict_unique_weeks_upo_EPD[value_min] += 1


        if type_module == 'AD':
            
            list_weeks_AD = weeks_module.split(',') ## GUARDAR SEMANAS EM LISTA
            # list_weeks_AD = list_weeks [2:] ## APENAS INSERE A APARTIR DA SEMANA 3 AS NOVAS CARGAS !!!

            filter_dictionary_AD = dict((k,dict_unique_weeks_upo_AD[k]) for k in list_weeks_AD if k in dict_unique_weeks_upo_AD)

            value_min = min(filter_dictionary_AD, key=filter_dictionary_AD.get)
            dict_unique_weeks_upo_AD[value_min] += 1
    
        df_weekly_week_load.at[index_dataframe, 'NEW_WEEKS'] = value_min
    
    df_weekly_week_load[v_weeks] = df_weekly_week_load['NEW_WEEKS']
    df_weekly_week_load.drop(columns=['NEW_WEEKS'], inplace=True)

    df_weekly_week_load[v_week_load_type] = v_week_load_weekly
    df_reference_week_load[v_week_load_type] = v_week_load_reference
    df_unique_week_load[v_week_load_type] = v_week_load_unique


    df_new = concat([df_reference_week_load, df_unique_week_load, df_weekly_week_load], ignore_index= True)

    df_new[v_name_wload] = where(df_new[v_week_load_type] == v_week_load_unique, df_new[v_name_wload] ,
                           where(df_new[v_week_load_type] == v_week_load_reference, df_new[v_name_wload]  + '_PR' ,
                                 df_new[v_name_wload] + '_PS'))
    

    return (df_new)


def create_conector_uxxi (df : DataFrame):

    df[v_file_conectores] = df[v_cod_act_fileconect] + '_' + df[v_cod_grupo_fileconect]

    return(df)

def add_session_two_facultad_expermimentales_eb (df : DataFrame):

    df[v_session_wload] = where(((df[v_center_plan_dominant] == '2') & (df[v_mod_typologie] == 'EB') & (df[v_hours_wload] % 2 == 0)),
                                2, df[v_session_wload] )
    
    df[v_hours_wload] = where(((df[v_center_plan_dominant] == '2') & (df[v_mod_typologie] == 'EB') & (df[v_hours_wload] % 2 == 0)),
                                df[v_hours_wload]/2 , df[v_hours_wload] )

    df.drop(columns=v_center_plan_dominant, inplace=True)

    return(df)


def add_alternated_weeks_EPD (df: DataFrame, df_alternated_weeks : DataFrame):

    values_weeks_par = '2,4,6,8,10,12,14'
    values_weeks_impar = '1,3,5,7,9,11,13'

    

    #Convert Data Same Type ... String OR List

    df_alternated_weeks.rename (columns={v_plan_fileconect : 'PLAN_CHECK',
                                         v_year : 'CURSO_CHECK',
                                         v_cred_cod_center : v_center_plan_dominant,
                                         v_cred_mod_code : v_mod_code,
                                         v_epd_alternatedd_linea : v_student_group
                                         }, inplace=True)

    df['CURSO_CHECK'] = df[v_year].str[0]
    df['PLAN_CHECK'] = df[v_cred_plan].str[0]
    df['TEMP_WEEKS_COUNT'] = df[v_weeks].str.count(',') + 1

    columns_merge = ['PLAN_CHECK',
                     'CURSO_CHECK',
                     v_center_plan_dominant,
                     v_mod_code,
                     v_cred_model,
                     v_student_group
                     ]

    df = merge (left=df, right=df_alternated_weeks, how = 'left', on = columns_merge, indicator=True)

    

    # REGRAS ASSOCIAR A EXCEPÇÂO DE PARES E IMPARES:
    # HORAS SEMANAIS --> SE 14 SEMANAS então MUlTIPLICAR VALOR POR 2
    df[v_hours_wload] = where(((df[v_merge] == 'both') & (df['TEMP_WEEKS_COUNT'] == 14) ) 
                              , df[v_hours_wload] * 2, df[v_hours_wload] )
    
    #NOVAS SEMANAS
    df[v_weeks] = where(((df[v_merge] == 'both') & (df[v_epd_alternatedd_weeks] == v_file_value_week_par)) ,values_weeks_par , df[v_weeks] )
    df[v_weeks] = where(((df[v_merge] == 'both') & (df[v_epd_alternatedd_weeks] == v_file_value_week_impar)) ,values_weeks_impar , df[v_weeks] )
    
    #INSERIR INDENTIFICADOR DE CARGAS SEMANAL PARES E IMPARES
    df[v_w_load_flag_alternated_week] = ''
    #NOVAS SEMANAS
    df[v_w_load_flag_alternated_week] = where(((df[v_merge] == 'both') & (df[v_epd_alternatedd_weeks] == v_file_value_week_par)) ,v_flag_week_par , df[v_w_load_flag_alternated_week] )
    df[v_w_load_flag_alternated_week] = where(((df[v_merge] == 'both') & (df[v_epd_alternatedd_weeks] == v_file_value_week_impar)) ,v_flag_week_impar , df[v_w_load_flag_alternated_week] )



    df.drop(columns=['PLAN_CHECK','CURSO_CHECK','TEMP_WEEKS_COUNT', v_epd_alternatedd_weeks,v_cred_model, v_merge], inplace=True)
      

    return(df)

def manage_data_create_xml_file_solapadas_par_impar (df : DataFrame):

    columns_present = [ v_plan_fileconect,
                        v_curso_fileconect,
                        v_mod_code_fileconect,
                        v_plan_linea,
                        v_grupo_fileconect,
                        v_name_wload,
                        v_section_name,
                        v_weeks ]
    
    df = df[columns_present].copy()
    
    series_merge = [    v_plan_fileconect,
                        v_curso_fileconect,
                        v_mod_code_fileconect,
                        v_plan_linea]

    df = manData.group_entities_to_list(df, series_merge,sep=',')

    return(df)


def filter_expermientales_to_add_w_loads_from_schedules (df : DataFrame):

    df_center_2 = df[df[v_center_plan_dominant] == '2'].copy()
    df_center_distinct_2 = df[df[v_center_plan_dominant] != '2'].copy()


    return(df_center_2, df_center_distinct_2)


def add_week_loads_center_2 (df_center_2 : DataFrame, df_w_loads : DataFrame):

    df_w_loads['PLAN_TO_MAP'] = df_w_loads['TITULACION'].str.split(' ').str[0]
    df_w_loads['DURACION_WL'] = (df_w_loads["DURACION_WL"].astype(float) * 60).astype(int)
    df_w_loads['SLOTS_WL'] = df_w_loads['DURACION_WL'].apply(lambda x: x / 30)
    df_w_loads['SLOTS_WL'] = (df_w_loads['SLOTS_WL'].astype(float)).astype(int)
    df_w_loads['SLOTS_WL'] = df_w_loads['SLOTS_WL'].astype(str)

    df_w_loads = df_w_loads[[v_mod_code,
                            v_year,
                            v_student_group,
                            'PLAN_TO_MAP',
                            'SLOTS_WL',
                            'SESSIONES_WL',
                            'SEMANA_UXXI_WL']].copy()
    
    df_w_loads.rename(columns={v_year : 'YEAR_TO_MAP'}, inplace=True)
    
    df_center_2['PLAN_TO_MAP'] = df_center_2[v_cred_plan].str[0]
    df_center_2['YEAR_TO_MAP'] = df_center_2[v_year].str[0]

    values_merge = [v_mod_code,
                    'YEAR_TO_MAP',
                    v_student_group,
                    'PLAN_TO_MAP']

    df_center_2 = merge(left=df_center_2, right = df_w_loads, on = values_merge, how='left', indicator=True)

    df_center_2_valid = df_center_2[df_center_2['_merge'] == 'both'].copy()
    df_center_2_invalid = df_center_2[df_center_2['_merge'] != 'both'].copy()


    df_center_2_valid [v_weeks] = df_center_2_valid['SEMANA_UXXI_WL']
    df_center_2_valid [v_hours_wload] = df_center_2_valid['SLOTS_WL']
    df_center_2_valid [v_session_wload] = df_center_2_valid['SESSIONES_WL']
    df_center_2_valid[v_slot_number_rest] = '0'

    # VALOR DE HORAS ADICIONAIS QUE FALTAVA ATRIBUIR FICA A 0

    df_center_2_valid.drop(columns=['PLAN_TO_MAP', 'YEAR_TO_MAP', 'SLOTS_WL','SESSIONES_WL','SEMANA_UXXI_WL', '_merge'], inplace=True)

    return(df_center_2_valid, df_center_2_invalid)


def concat_all_data_center(df_data_center_2 : DataFrame, df_data_center_distinct_2 : DataFrame):

    df_all = concat([df_data_center_2, df_data_center_distinct_2], ignore_index= True)

    return(df_all)
    


