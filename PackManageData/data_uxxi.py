from PackLibrary.librarys import (	
  DataFrame,
)
from mod_variables import *
import PackGeneralProcedures.files as genFiles

def check_courses_uxxi (df : DataFrame, process_folder : str, process_code : str):

    df = df [[v_course_name, v_course_code]].copy()

    df.drop_duplicates(inplace=True)
    df[v_acronym_best] = df[v_course_code]

    df.rename(columns={v_course_name : v_name_best,
                       v_course_code : v_code_best}, inplace=True)
    
    df = df [[v_name_best, v_acronym_best, v_code_best]].copy()

    genFiles.create  (df,process_folder,process_code, v_file_curriculum_uxxi, v_sheet_courses, v_process_manage_data)

    return()

def check_planes_uxxi (df : DataFrame, process_folder : str, process_code : str):

    flag_file_created = True

    #Notes README
    df = df [[v_course_name, v_course_code, v_year, v_student_group]].copy()

    df[v_identifier_gg] = df[v_student_group].str[0]
    
    df[v_name_best] = df[v_course_name] + '_' + df[v_year] + '_' + df[v_identifier_gg]
    df[v_code_best] = df[v_course_code] + '_' + df[v_year] + '_' + df[v_identifier_gg]

    df.rename(columns={v_year : v_year_best,
                       v_course_code : v_course_code_best}, inplace=True)

    df = df [[v_name_best,  v_code_best, v_year_best, v_course_code_best]].copy()
    df.drop_duplicates(inplace=True)

    genFiles.create  (df,process_folder,process_code, v_file_curriculum_uxxi, v_sheet_planes, v_process_manage_data, flag_file_created)


    return()


def check_st_groups_uxxi (df : DataFrame, process_folder : str, process_code : str):

    flag_file_created = True

    df = df [[v_course_name, v_course_code, v_year, v_student_group, v_mod_typologie, v_students_number]].copy()

    df = df[df[v_mod_typologie] == 'EPD'].copy()

    # Create Name Group
    df[v_name_best] = df[v_course_code] + '_' + df[v_year] + '_' + df[v_mod_typologie] + df[v_student_group]
    df[v_code_best] = df[v_course_code] + '_' + df[v_year] + '_' + df[v_mod_typologie] + df[v_student_group]

    #Create Name Plan
    df[v_identifier_gg] = df[v_student_group].str[0]

    df[v_plan_code_best] = df[v_course_code] + '_' + df[v_year] + '_' + df[v_identifier_gg]

    df = df [[v_name_best, v_code_best, v_plan_code_best, v_students_number]]

    df.sort_values(by=[v_name_best,v_students_number], ascending=[True, False], inplace=True)
    df.drop_duplicates(subset=[v_name_best, v_code_best, v_plan_code_best], inplace=True)

    df.rename(columns={v_students_number : v_students_number_best}, inplace=True)


    genFiles.create  (df,process_folder, process_code, v_file_curriculum_uxxi, v_sheet_st_group, v_process_manage_data, flag_file_created)

    return()


def check_modules_uxxi (df : DataFrame, process_folder : str, process_code : str):

    flag_file_created = True

    df = df [[v_mod_name, v_mod_code]].copy()
    df.drop_duplicates(inplace=True)

    df.rename(columns={v_mod_name : v_name_best,
                       v_mod_code : v_code_best}, inplace=True)
    
    df[v_acronym_best] = df [v_code_best]
    df[v_priority_mod_best] = '1'
    df[v_academic_area_best] = 'SD'

    genFiles.create  (df,process_folder, process_code, v_file_curriculum_uxxi, v_sheet_modules, v_process_manage_data, flag_file_created)


    return()


def check_typologies_uxxi (df : DataFrame, process_folder : str, process_code : str):

    flag_file_created = True

    df = df [[v_mod_typologie]].copy()
    df.drop_duplicates(inplace=True)

    df.rename(columns={v_mod_typologie : v_name_best}, inplace=True)
    df[v_description_typologie_best] = 'Add Description'

    genFiles.create  (df,process_folder, process_code, v_file_curriculum_uxxi, v_sheet_typologies, v_process_manage_data, flag_file_created)

    return()