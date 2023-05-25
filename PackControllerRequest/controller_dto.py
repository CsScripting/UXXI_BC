from mod_variables import *
def create_dto_courses (name : str, code : str, acronym : str):

    data = {
            v_active_dto : True,
            v_name_dto: name,
            v_code_dto : code,
            v_acronym_dto : acronym
            }



    return(data)
