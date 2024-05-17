import PackManageApi.global_variable_process_request as gl_v_request
import PackControllerRequest.general_requests as genRequest
import PackControllerRequest.controller_dto as dtObj
from mod_variables import *

from PackLibrary.librarys import (	
    DataFrame
)

def iterate_df_courses_and_post (df : DataFrame):

    df_courses_imported = DataFrame(columns = [v_name_best,
                                                v_acronym_best,
                                                v_code_best,
                                                v_code_request,
                                                v_message_request])
    
    for row in df.itertuples(index= False):

        value_to_import = getattr(row, v_data_to_import_new)

        if value_to_import == '1':

            name_course = getattr(row, v_name_best)
            acronym_course = getattr(row, v_acronym_best)
            code_course = getattr(row, v_code_best)

            data_object = dtObj.create_dto_courses(name_course, code_course, acronym_course)
            
            response_code, message_to_present = genRequest.post_data_to_entity(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_course_controller, data_object)


            df_courses_imported.loc[len(df_courses_imported), df_courses_imported.columns] =    name_course, \
                                                                                                acronym_course, \
                                                                                                code_course, \
                                                                                                response_code, \
                                                                                                message_to_present


    return(df_courses_imported)
    
    


def iterate_df_planes_and_post (df : DataFrame):

    df_planes_imported = DataFrame(columns = [v_name_best,
                                              v_code_best,
                                              v_year_best,
                                              v_course_code_best,
                                              v_code_request,
                                              v_message_request])
    
    for row in df.itertuples(index= False):

        value_to_import = getattr(row, v_data_to_import_new)

        if value_to_import == '1':

            name_plan = getattr(row, v_name_best)
            code_plan = getattr(row, v_code_best)
            year_plan = getattr(row, v_year_best)
            course_code = getattr(row, v_course_code_best)

            #Search Id Course To pass to Post Planes

            data_object_search = dtObj.create_dto_simple_search_filter (v_search_code, course_code)

            code_response_search_id_course, total_records, value_id_course = genRequest.post_data_search_filter (gl_v_request.gl_url_api, gl_v_request.gl_header_request,
                                                v_course_controller,data_object_search)
            
            if ((code_response_search_id_course == 200 ) & (total_records == 1)):
            
                data_object = dtObj.create_dto_planes(name_plan, code_plan, year_plan, value_id_course)
            
                response_code, message_to_present = genRequest.post_data_to_entity(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_plan_controller, data_object)

            else: 

                response_code = code_response_search_id_course
                message_to_present = 'CourseNotInserted'


            df_planes_imported.loc[len(df_planes_imported), df_planes_imported.columns] =   name_plan, \
                                                                                            code_plan, \
                                                                                            year_plan, \
                                                                                            course_code, \
                                                                                            response_code, \
                                                                                            message_to_present



    return(df_planes_imported)


def iterate_df_groups_and_post (df : DataFrame):

    df_st_groups_imported = DataFrame(columns = [v_name_best,
                                              v_code_best,
                                              v_plan_code_best,
                                              v_students_number_best,
                                              v_daily_limit_best,
                                              v_consecutive_limit_best,
                                              v_code_request,
                                              v_message_request])
    
    for row in df.itertuples(index= False):

        value_to_import = getattr(row, v_data_to_import_new)

        if value_to_import == '1':

            name_group = getattr(row, v_name_best)
            code_group = getattr(row, v_code_best)
            plan_code = getattr(row, v_plan_code_best)
            students_number = getattr(row, v_students_number_best)

            # Default Values Inserted
            daily_limit = v_daily_limit_default_best
            consecutive_limit = v_consecutiv_limit_default_best

            #Search Id Course To pass to Post Planes

            data_object_search = dtObj.create_dto_simple_search_filter (v_search_code, plan_code)

            code_response_search_id_plan, total_records, value_id_plan = genRequest.post_data_search_filter (gl_v_request.gl_url_api, gl_v_request.gl_header_request,
                                                                                                             v_plan_controller,data_object_search)
            
            if ((code_response_search_id_plan == 200 ) & (total_records == 1)):
            
                data_object = dtObj.create_dto_groups(name_group, code_group, value_id_plan, students_number, daily_limit, consecutive_limit)
            
                response_code, message_to_present = genRequest.post_data_to_entity(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_st_group_controller, data_object)

            else: 

                response_code = code_response_search_id_plan
                message_to_present = 'StGroupNotInserted'

            
            df_st_groups_imported.loc[len(df_st_groups_imported), df_st_groups_imported.columns] =  name_group, \
                                                                                                    code_group, \
                                                                                                    plan_code, \
                                                                                                    students_number, \
                                                                                                    v_daily_limit_default_best, \
                                                                                                    v_consecutiv_limit_default_best, \
                                                                                                    response_code, \
                                                                                                    message_to_present




    return(df_st_groups_imported)


def iterate_df_modules_and_post (df : DataFrame):

    df_modules_imported = DataFrame(columns = [v_name_best,
                                                 v_code_best,
                                                 v_acronym_best,
                                                 v_priority_mod_best,
                                                 v_academic_area_best,
                                                 v_code_request,
                                                 v_message_request])
    
    for row in df.itertuples(index= False):

        value_to_import = getattr(row, v_data_to_import_new)

        if value_to_import == '1':

            name_mod = getattr(row, v_name_best)
            code_mod = getattr(row, v_code_best)
            acron_mod = getattr(row, v_acronym_best)
            priority_mod = getattr(row, v_priority_mod_best)
            area_mod = getattr(row, v_academic_area_best)

            

            #Search Id Course To pass to Post Planes

            data_object_search = dtObj.create_dto_simple_search_filter (v_search_name, area_mod)

            code_response_search_id_acad_term, total_records, value_id_acad_area= genRequest.post_data_search_filter (gl_v_request.gl_url_api, gl_v_request.gl_header_request,
                                                                                                                      v_scientific_area_controller,data_object_search)
            
            if ((code_response_search_id_acad_term == 200 ) & (total_records == 1)):
            
                data_object = dtObj.create_dto_modules(name_mod, code_mod, value_id_acad_area, acron_mod, priority_mod)
            
                response_code, message_to_present = genRequest.post_data_to_entity(gl_v_request.gl_url_api, gl_v_request.gl_header_request, v_module_controller, data_object)

            else: 

                response_code = code_response_search_id_acad_term
                message_to_present = 'ModuleNotInserted'



            df_modules_imported.loc[len(df_modules_imported), df_modules_imported.columns] =    name_mod, \
                                                                                                   code_mod, \
                                                                                                   acron_mod, \
                                                                                                   priority_mod, \
                                                                                                   area_mod, \
                                                                                                   response_code, \
                                                                                                   message_to_present



    return(df_modules_imported)