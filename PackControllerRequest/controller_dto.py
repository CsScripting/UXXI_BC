from mod_variables import *
def create_dto_courses (name : str, code : str, acronym : str):

    data = {
            v_active_dto : True,
            v_name_dto: name,
            v_code_dto : code,
            v_acronym_dto : acronym
            }



    return(data)

def create_dto_planes (name : str, code : str, year : str, course_id):

    data = {
            v_code_dto : code,
            v_course_id_dto: course_id,
            v_name_dto : name,
            v_year_dto : year,
            v_active_dto : True
            }



    return(data)


def create_dto_groups (name : str, code : str, plan_id : str, students_number : str,
                       daily_limit : str, consecutive_limit : str):

    data = {
            v_name_dto : name,
            v_students_number_dto: students_number,
            v_daily_limit_dto : daily_limit,
            v_consecutive_limit_dto : consecutive_limit,
            v_code_dto : code,
            v_curricular_plan_identifier_dto : plan_id,
            v_active_dto : True
            }



    return(data)


def create_dto_modules (name : str, code : str, acad_area_id : str, acron_name : str,
                       priotity_level : str):

    data = {
            v_acronym_dto : acron_name,
            v_code_dto: code,
            v_name_dto : name,
            v_scientif_area_id_dto : acad_area_id,
            v_importance_degree_dto : priotity_level,
            v_active_dto : True
            }



    return(data)

def create_dto_simple_search_filter (path_to_find : str, value_to_find : str):

        

        data = {
                v_filter:
                        [
                        {
                        v_type : 0,
                        v_path: path_to_find,
                        v_value_to_find : value_to_find
                        }
                        ]
                }



        return(data)
