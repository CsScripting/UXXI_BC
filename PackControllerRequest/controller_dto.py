from mod_variables import *
from PackLibrary.librarys import (	
    Series,
    isnull
)

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

def create_dto_event (event_data : Series):

        # Insert Name Event 
        type_module_uxxi = getattr (event_data,v_mod_modalidad)
        code_titulacion_dominant = getattr (event_data,v_course_code)

        name_event = code_titulacion_dominant + '_' + type_module_uxxi



        #Manage Weeks
        weeks_event = getattr (event_data, v_id_weeks).split(',')
        list_weeks =[]

        for i in range (len(weeks_event)):

         list_weeks.append(       { 
                                        "model": {
                                                "identifier": weeks_event[i]
                                                 },
                                                 "status": 1
                                  })  

        #Manage students Groups
        st_groups_event = getattr (event_data, v_student_group_id).split(',')
        list_groups =[]

        for j in range (len(st_groups_event)):

         list_groups.append(       { 
                                        "model": {
                                                "identifier": st_groups_event[j]
                                                 },
                                                 "status": 1
                                  }) 

         #Manage typologies
        typologie = getattr (event_data, v_mod_id_typologie).split(',')
        list_typologies =[]

        for k in range (len(typologie)):

         list_typologies.append(       { 
                                        "model": {
                                                "identifier": typologie[k]
                                                 },
                                                 "status": 1
                                  }) 

        #ManageTeachers   
        list_teachers =[]  

        #ManageClassrooms 


        classrooms = getattr (event_data, v_id_classroom)
        
        if classrooms == '' or isnull(classrooms) or None:
        
                list_classrooms = []
        else:
                
                classrooms = classrooms.split(',') 
                list_classrooms =[]  

                for cl in range (len(classrooms)):

                        list_classrooms.append(       { 
                                                        "model": {
                                                                "identifier": classrooms[cl]
                                                                },
                                                                "status": 1
                                                })  

        data = {
                
                v_name_dto : name_event,
                v_code_dto : getattr (event_data,v_event_Id_BC),
                v_start_time_event_dto : getattr (event_data,v_hourBegin),
                v_end_time_event_dto :  getattr (event_data,v_hourEnd),
                v_day_event_dto : getattr (event_data,v_day),
                v_section_name_event_dto : getattr (event_data,v_section_name),
                v_conector_name_event_dto : getattr( event_data, v_id_uxxi),
                v_event_type_id_event_dto : getattr (event_data,v_id_event_type),
                v_mod_id_event_dto : getattr (event_data,v_mod_id_dominant),
                v_acad_year_id_event_dto :getattr ( event_data,v_id_academic_year),
                v_students_number_dto : getattr (event_data,v_students_number),
                v_weeks_event_dto: list_weeks,
                v_groups_event_dto : list_groups,
                v_teachers_event_dto : list_teachers,
                v_classrooms_event_dto : list_classrooms,
                v_typologies_event_dto : list_typologies,

                v_constrains_event: True

                }

        return(data)
