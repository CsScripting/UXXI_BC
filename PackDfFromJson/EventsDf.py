from PackLibrary.librarys import(
DataFrame,
ast
)
from mod_variables import *
import PackRulesExport.bussiness_rules_export as rulesExport


def events_df_from_json(events : list):


    columns_df = [v_id_best, v_event_Id_BC, v_event_title_BC, v_mod_name, v_mod_code,v_mod_typologie,v_mod_id_typologie, v_section_name, v_day,
                  v_hourBegin, v_hourEnd, v_duration, v_student_group_name, v_students_number,v_id_uxxi,v_weeks, v_event_type,v_id_event_type,
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
        event_type_id = events[i][v_event_type_event_dto][v_id_dto]
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
        list_typologies_id = []

        if not typologies:

            typologies_str = ''
        
        else:
            
            for ty in range (len(typologies)):

                value_name_ty = typologies[ty][v_name_dto]
                list_typologies.append(value_name_ty)

                value_id_ty = typologies[ty][v_id_dto]
                list_typologies_id.append(str(value_id_ty))

            typologies_str = ','.join(list_typologies)
            typologies_id_str = str(','.join(list_typologies_id))
            
        
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
                        v_mod_typologie  : typologies_str,v_mod_id_typologie : typologies_id_str, v_section_name: wlsSectionName,  v_day : day,v_hourBegin : start_time, v_hourEnd : end_time,
                        v_duration : duration, v_student_group_name : groups_str, v_students_number : num_students,
                        v_id_uxxi : wlsSectionConector, v_weeks : weeks_str, v_event_type : event_type,v_id_event_type : event_type_id, v_classroom_name : classrooms_name_str,
                        v_classroom_code : classrooms_code_str , v_academic_year :academic_year
                        }, 
                        ignore_index = True)    



    return(df)


def parse_list_events_to_df (events : list):


    df = DataFrame(events)

    columns_used_from_json = [v_id_dto,
                              v_name_dto,
                              v_code_dto,
                              v_event_type_event_dto,
                              v_start_time_event_dto,
                              v_end_time_event_dto,
                              v_duration_event_dto,
                              v_day_event_dto, 
                              v_students_number_dto,
                              v_section_name_event_dto,
                              v_conector_name_event_dto,
                              v_weeks_event_dto,
                              v_classrooms_event_dto,
                              v_groups_event_dto,
                              v_module_event_dto,
                              v_typologies_event_dto,
                              v_acad_year_dto
                              ]
    
    #Filter DataFrame Values
    df = df [columns_used_from_json].copy()

    #Extract values from object/Dict

    ## - SingleValues Dict: - ##

    

    #Module
    df[v_mod_name] =  df[v_module_event_dto].apply(lambda x: x.get(v_name_dto) if x is not None else '')
    df[v_mod_code] =  df[v_module_event_dto].apply(lambda x: x.get(v_code_dto) if x is not None else '')
    df[v_mod_id] =  df[v_module_event_dto].apply(lambda x: x.get(v_id_dto) if x is not None else '')
    
    #Event Type
    df[v_event_type] = df [v_event_type_event_dto].apply(lambda x: x.get(v_name_dto)if x is not None else '')
    df[v_id_event_type] = df [v_event_type_event_dto].apply(lambda x: x.get(v_id_dto)if x is not None else '')


    ## - NestedValues Dict: - ##

    #weeks
    df[v_weeks] = df[v_weeks_event_dto].apply(lambda x: [d[v_start_date_dto][0:10] for d in x])
    df[v_weeks] = df[v_weeks].agg(lambda x: ','.join(map(str, x)))
    
    #Typologies
    df[v_mod_id_typologie] = df[v_typologies_event_dto].apply(lambda x: [d[v_id_dto]for d in x])
    df[v_mod_typologie] = df[v_typologies_event_dto].apply(lambda x: [d[v_name_dto] for d in x])
    df[v_mod_typologie] = df[v_mod_typologie].agg(lambda x: ','.join(map(str, x)))
    df[v_mod_id_typologie] = df[v_mod_id_typologie].agg(lambda x: ','.join(map(str, x)))

    #Classrooms
    df[v_classroom_name] = df[v_classrooms_event_dto].apply(lambda x: [d[v_name_dto] for d in x])
    df[v_classroom_code] = df[v_classrooms_event_dto].apply(lambda x: [d[v_code_dto] for d in x])
    df[v_id_classroom] = df[v_classrooms_event_dto].apply(lambda x: [d[v_id_dto] for d in x])
    df[v_classroom_name] = df[v_classroom_name].agg(lambda x: ','.join(map(str, x)))
    df[v_classroom_code] = df[v_classroom_code].agg(lambda x: ','.join(map(str, x)))
    df[v_id_classroom] = df[v_id_classroom].agg(lambda x: ','.join(map(str, x)))

    #Student Groups
    df[v_student_group_name] = df[v_groups_event_dto].apply(lambda x: [d[v_name_dto] for d in x])
    df[v_student_group_id] = df[v_groups_event_dto].apply(lambda x: [d[v_id_dto] for d in x])
    df[v_student_group_name] = df[v_student_group_name].agg(lambda x: ','.join(map(str, x)))
    df[v_student_group_id] = df[v_student_group_id].agg(lambda x: ','.join(map(str, x)))

    #AcademicYear
    df[v_academic_year] = df[v_acad_year_dto].apply(lambda x: x.get(v_name_dto) if x is not None else '')
    
    #DropColumnsObjects

    columns_to_drop = [     
                        v_module_event_dto,
                        v_event_type_event_dto,
                        v_classrooms_event_dto,
                        v_groups_event_dto,
                        v_typologies_event_dto,
                        v_weeks_event_dto,
                        v_acad_year_dto
                        
                      ]

    df.drop(columns=columns_to_drop, inplace=True)

    columns_to_rename = {   
                            v_id_dto : v_id_best,
                            v_name_dto : v_event_title_BC, 
                            v_code_dto : v_event_Id_BC,
                            v_start_time_event_dto : v_hourBegin ,
                            v_end_time_event_dto : v_hourEnd,
                            v_duration_event_dto : v_duration,
                            v_day_event_dto : v_day, 
                            v_students_number_dto : v_students_number,
                            v_section_name_event_dto : v_section_name,
                            v_conector_name_event_dto : v_id_uxxi
                            
                        }


    df.rename(columns=columns_to_rename, inplace = True)

    columns_df = [v_id_best, v_event_Id_BC, v_event_title_BC, v_mod_name, v_mod_code,v_mod_typologie,v_mod_id_typologie, v_section_name, v_day,
                  v_hourBegin, v_hourEnd, v_duration, v_student_group_name, v_students_number,v_id_uxxi,v_weeks, v_event_type,v_id_event_type,
                  v_classroom_name,v_classroom_code, v_academic_year]
    
    df = df[columns_df]


    return(df)


def parse_list_events_to_df_from_audit_log (events_dict : list):

    events_deleted = False
    new_list = []
    new_list_2 = []

    

    new_list = [i[v_resourceTypaData_dto]for i in events_dict]

    for value_string in new_list:

        value_string = value_string.split('"WLSSectionConnector":')[1]
        value_string = value_string.split(',"NumStudents"')[0]
        my_dict = ast.literal_eval(value_string)

        if my_dict != '':

            new_list_2.append(my_dict)

    if new_list_2 != []:

        events_deleted = True

        df = DataFrame(new_list_2, columns= [v_id_uxxi])

        df =  rulesExport.manage_conector_id_parse_to_dict (df)

        df[v_id_db_check_update_uxxi] =  df[v_id_uxxi].apply(lambda x: x.get(v_id_conector_bwp) if x is not None else '')
        df [v_id_db_check_update_uxxi] =  df [v_id_db_check_update_uxxi].agg(lambda x: ','.join(map(str, x)))

    else:

        df = DataFrame(columns=[v_id_uxxi])
    

    return(df, events_deleted)
    


        



    print('NONE')