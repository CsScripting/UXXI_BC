from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *


def events_df_from_json(events : list):


    columns_df = [v_id_best, v_event_Id_BC, v_event_title_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                  v_hourBegin, v_hourEnd, v_duration, v_student_group_name, v_students_number,v_id_uxxi,v_weeks, v_event_type,
                  v_classroom_name,v_classroom_code, v_academic_year]

    df = DataFrame(columns = columns_df)
    
    for i in range (len(events)):
    
        event_id = events[i][v_id_dto]
        event_name = events[i][v_name_dto]
        event_code= events[i][v_code_dto]
        start_time = events[i][v_start_time_event_dto]
        end_time = events[i][v_end_time_event_dto]
        duration = events[i][v_duration_event_dto]
        day = events[i][v_day_event_dto]
        event_type = events[i][v_event_type_event_dto][v_name_dto]
        num_students = events[i][v_num_students_event_dto]

        wlsSectionName = events[i][v_section_name_event_dto]
        if wlsSectionName is None:
            wlsSectionConector = ''
        wlsSectionConector = events[i][v_conector_name_event_dto]
        if wlsSectionConector is None:
            wlsSectionConector = ''

        ### To iterate -- lists ###
        ## List Weeks ##
        weeks = events[i][v_weeks_event_dto]
        list_weeks = []
        for wk in range (len(weeks)):

            value_week = weeks[wk][v_start_date_dto][0:10]
            list_weeks.append(value_week)
        
        weeks_str = ','.join(list_weeks) 

        ## List Classrooms ##
        classrooms = events[i][v_classrooms_event_dto]
        list_classrooms_name = []
        list_classrooms_code = []

        if not classrooms:

            classrooms_name_str = ''
            classrooms_code_str = ''
        
        else:

            for cl in range (len(classrooms)):

                value_name_cl = classrooms[cl][v_name_dto]
                value_code_cl = classrooms[cl][v_code_dto]
                list_classrooms_name.append(value_name_cl)
                list_classrooms_code.append(value_code_cl)

            classrooms_name_str = ','.join(list_classrooms_name)
            classrooms_code_str = ','.join(list_classrooms_code)

           

        ## List St_Groups ##    
        student_groups = events[i][v_groups_event_dto]
        list_groups = []

        if not student_groups:

            groups_str = ''
        
        else:

            for sg in range (len(student_groups)):

                value_name_sg = student_groups[sg][v_name_dto]
                list_groups.append(value_name_sg)

            groups_str = ','.join(list_groups)

           
        ## List typologies ##
        typologies = events[i][v_typologies_event_dto]

        list_typologies = []

        if not typologies:

            typologies_str = ''
        
        else:
            
            for ty in range (len(typologies)):

                value_name_ty = typologies[ty][v_name_dto]
                list_typologies.append(value_name_ty)

            typologies_str = ','.join(list_typologies)
            
        
        if events[i][v_module_event_dto] is not None:

            module_name = events[i][v_module_event_dto][v_name_dto]
            module_code = events[i][v_module_event_dto][v_code_dto]

        else:
            module_name = ''
            module_code = ''


        academic_year = events[i][v_acad_year_event_dto][v_name_dto]

        if academic_year is None:
            academic_year = ''

        
        
        


        df = df.append({v_id_best : event_id, v_event_Id_BC : event_code ,v_event_title_BC : event_name, v_mod_name : module_name, v_mod_code : module_code,
                        v_mod_typologie  : typologies_str, v_section_name: wlsSectionName,  v_day : day,v_hourBegin : start_time, v_hourEnd : end_time,
                        v_duration : duration, v_student_group_name : groups_str, v_students_number : num_students,
                        v_id_uxxi : wlsSectionConector, v_weeks : weeks_str, v_event_type : event_type, v_classroom_name : classrooms_name_str,
                        v_classroom_code : classrooms_code_str , v_academic_year :academic_year
                        }, 
                        ignore_index = True)    



    return(df)