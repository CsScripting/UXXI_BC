from PackLibrary.librarys import (	
    DataFrame,
    merge
)
from mod_variables import *


def compare_courses_uxxi_db (df_uxxi : DataFrame, df_best : DataFrame):

    df_best.rename(columns={v_name_best : v_name_best_match,
                            v_acronym_best : v_acronym_best_match}, inplace=True)
    

    df_uxxi = merge(left=df_uxxi, right=df_best, how = 'left', on=v_code_best, indicator=True)

    df_uxxi_to_import = df_uxxi[df_uxxi [v_merge] == 'left_only'].copy()

    df_uxxi_to_import.drop(columns=[v_name_best_match,
                                    v_acronym_best_match,
                                    v_merge], inplace=True)

    if not df_uxxi_to_import.empty:
        
        df_uxxi_to_import[v_data_to_import_new] = '1'

    return(df_uxxi_to_import)


def compare_planes_uxxi_db (df_uxxi : DataFrame, df_best : DataFrame):

    df_best.rename(columns={v_name_best : v_name_best_match,
                            v_year_best : v_year_best_match,
                            v_course_code_best : v_course_code_best_match}, inplace=True)
    

    df_uxxi = merge(left=df_uxxi, right=df_best, how = 'left', on=v_code_best, indicator=True)

    df_uxxi_to_import = df_uxxi[df_uxxi [v_merge] == 'left_only'].copy()

    df_uxxi_to_import.drop(columns=[v_name_best_match,
                                    v_year_best_match,
                                    v_course_code_best_match,
                                    v_merge], inplace=True)

    if not df_uxxi_to_import.empty:
        
        df_uxxi_to_import[v_data_to_import_new] = '1'

    return(df_uxxi_to_import)


def compare_groups_uxxi_db (df_uxxi : DataFrame, df_best : DataFrame):

    df_best.rename(columns={v_code_best : v_code_best_match,
                            v_plan_code_best : v_plan_code_best_match,
                            v_students_number_best : v_students_number_best_match}, inplace=True)
    

    df_uxxi = merge(left=df_uxxi, right=df_best, how = 'left', on=v_name_best, indicator=True)

    df_uxxi_to_import = df_uxxi[df_uxxi [v_merge] == 'left_only'].copy()

    df_uxxi_to_import.drop(columns=[v_code_best_match,
                                    v_plan_code_best_match,
                                    v_students_number_best_match,
                                    v_merge], inplace=True)

    if not df_uxxi_to_import.empty:
        
        df_uxxi_to_import[v_data_to_import_new] = '1'

    return(df_uxxi_to_import)

def compare_modules_uxxi_db (df_uxxi : DataFrame, df_best : DataFrame):

    df_best.rename(columns={v_name_best : v_name_best_match,
                            v_acronym_best : v_acronym_best_match,
                            v_priority_mod_best : v_priority_mod_best_match,
                            v_academic_area_best : v_academic_area_best_match
                            }, inplace=True)
    

    df_uxxi = merge(left=df_uxxi, right=df_best, how = 'left', on=v_code_best, indicator=True)

    df_uxxi_to_import = df_uxxi[df_uxxi [v_merge] == 'left_only'].copy()

    df_uxxi_to_import.drop(columns=[v_name_best_match,
                                    v_acronym_best_match,
                                    v_priority_mod_best_match,
                                    v_academic_area_best_match,
                                    v_merge], inplace=True)

    if not df_uxxi_to_import.empty:
        
        df_uxxi_to_import[v_data_to_import_new] = '1'

    return(df_uxxi_to_import)

def compare_typologies_uxxi_db (df_uxxi : DataFrame, df_best : DataFrame):

    df_best.rename(columns={v_description_typologie_best : v_description_typologie_best_match}, inplace=True)
    

    df_uxxi = merge(left=df_uxxi, right=df_best, how = 'left', on=v_name_best, indicator=True)

    df_uxxi_to_import = df_uxxi[df_uxxi [v_merge] == 'left_only'].copy()

    df_uxxi_to_import.drop(columns=[v_description_typologie_best_match,
                                    v_merge], inplace=True)

    if not df_uxxi_to_import.empty:
        
        df_uxxi_to_import[v_data_to_import_new] = '1'

    return(df_uxxi_to_import)


def compare_classrooms_uxxi_db (df_uxxi : DataFrame, df_best : DataFrame):

    df_best.rename(columns={v_code_best : v_classroom_code}, inplace=True)
    

    df_uxxi = merge(left=df_uxxi, right=df_best, how = 'left', on=v_name_best, indicator=True)

    df_uxxi_to_import = df_uxxi[df_uxxi [v_merge] == 'left_only'].copy()

    df_uxxi_to_import.drop(columns=[v_classroom_code,
                                    v_merge], inplace=True)

    if not df_uxxi_to_import.empty:
        
        df_uxxi_to_import[v_building_best] = ''
        df_uxxi_to_import[v_floor_best] = ''
        df_uxxi_to_import[v_capacity_class] = ''
        df_uxxi_to_import[v_capacity_exam_class] = ''
        df_uxxi_to_import[v_data_to_import_new] = '1'

    return(df_uxxi_to_import)