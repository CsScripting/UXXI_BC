#Extract Data API
import PackManageApi.global_variable_process_request as gl_v_request
import PackControllerRequest.general_requests as genRequest
import PackDfFromJson.ModulesDf as modDf
import PackDfFromJson.StudentGroupsDf as stGroupDf
import PackDfFromJson.ClassroomsDf as classDf
import PackDfFromJson.TypologiesDf as typeDf
import PackDfFromJson.AcademicYearDf as acadyearDf
import PackDfFromJson.EventTypeDf as eventTypeDf
import PackDfFromJson.WeeksDf as weeksDf

from mod_variables import *

from PackLibrary.librarys import (	
    DataFrame,
    merge,
    where,
    concat,
    arange,
    isnull
)

def filter_df_to_import (df:DataFrame):

    df = df[df[v_data_to_import_new] == '1'].copy()

    df.drop(columns=v_data_to_import_new, inplace=True)
    
    return(df)

def academic_year (df_event : DataFrame):

    # Iniciate Dataframe Invalid Data

    columns_data_frame = [v_event_Id_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                          v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code, 
                          v_year, v_student_group_name,v_students_number,v_classroom_name, v_id_uxxi,v_weeks, v_event_type,v_code_request, v_message_request ]

    df_invalid_events_data = DataFrame(columns = columns_data_frame)


    academic_year_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_acad_year_controller)
    
    
    df_academic_year_best = acadyearDf.academic_year_df_from_json(academic_year_db)


    df_academic_year_best.rename(columns={v_name_best: v_academic_year,
                                          v_id_best : v_id_academic_year}, inplace=True)


    df_event = merge(left=df_event, right=df_academic_year_best, on = v_academic_year, how='left', indicator = True)

    df_event_with_id = df_event[df_event[v_merge] == 'both'].copy() 
    df_event_without_id = df_event[df_event[v_merge] == 'left_only'].copy() 

    df_event_without_id = df_event_without_id [[v_event_Id_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                                                v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code, 
                                                v_year, v_student_group_name,v_students_number,v_classroom_name, v_id_uxxi,v_weeks, v_event_type ]].copy()
    
    df_event_without_id [v_code_request] = '404' # ---> Code Entity Not Found
    df_event_without_id [v_message_request] = v_error_id_acad_year + ' - ' + v_error_id
    

    df_invalid = concat([df_invalid_events_data, df_event_without_id], ignore_index= True)

    df_event_with_id.drop(columns=v_merge, inplace=True)

    return (df_event_with_id, df_invalid )



def event_type (df_event : DataFrame, df_invalid_events_data : DataFrame):


    event_type_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_event_type_controller)
    
    
    df_event_type_best = eventTypeDf.event_type_df_from_json(event_type_db)


    df_event_type_best.rename(columns={v_name_best: v_event_type,
                                       v_id_best : v_id_event_type}, inplace=True)


    df_event = merge(left=df_event, right=df_event_type_best, on = v_event_type, how='left', indicator = True)

    df_event_with_id = df_event[df_event[v_merge] == 'both'].copy() 
    df_event_without_id = df_event[df_event[v_merge] == 'left_only'].copy() 

    df_event_without_id = df_event_without_id [[v_event_Id_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                                                        v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code, 
                                                        v_year, v_student_group_name,v_students_number,v_classroom_name, v_id_uxxi,v_weeks, v_event_type ]].copy()
    
    df_event_without_id [v_code_request] = '404' # ---> Code Entity Not Found
    df_event_without_id [v_message_request] = v_error_id_event_type + ' - ' + v_error_id
    

    df_invalid = concat([df_invalid_events_data, df_event_without_id], ignore_index= True)

    df_event_with_id.drop(columns=v_merge, inplace=True)

    return (df_event_with_id, df_invalid )

def all_module_id(df_event_with_id :DataFrame, df_horarios_invalid :DataFrame, df_modules_best :DataFrame):
    
    # Criar coluna para armazenar todos os IDs de módulos
    df_event_with_id[v_mod_id_fileconect] = ''
    df_event_to_iterate = df_event_with_id.copy()
    
    # Iterar sobre cada linha do DataFrame
    for row in df_event_to_iterate.itertuples(index=False):
        
        modules_codes = getattr(row, v_mod_code_fileconect)
        id_event_to_map = getattr(row, v_event_Id_BC)
        
        values_id_to_insert = []
        
        # Fazer split dos códigos de módulos por '#'
        if modules_codes and not isnull(modules_codes):
            module_codes_list = modules_codes.split('#')
            
            # Para cada código de módulo, buscar o ID correspondente
            for module_code in module_codes_list:
                module_code = module_code.strip()
                
                # Buscar o ID do módulo no DataFrame de módulos
                value_id = df_modules_best.loc[df_modules_best[v_code_best] == module_code, [v_id_best]]
                
                if value_id.empty:
                    # Se não encontrar o ID, adicionar mensagem de erro
                    values_id_to_insert.append(v_error_id_mod + ' - ' + v_error_id)
                else:
                    # Se encontrar, adicionar o ID
                    values_id_to_insert.append(value_id.iloc[0, 0])
            
            # Juntar todos os IDs com '#'
            values_id_to_insert = [str(i) for i in values_id_to_insert]
            values_id_to_insert_string = '#'.join(values_id_to_insert)
            df_event_with_id.loc[df_event_with_id[v_event_Id_BC] == id_event_to_map, v_mod_id_fileconect] = values_id_to_insert_string
    
    # Separar registos válidos (todos os IDs encontrados) dos inválidos (algum ID não encontrado)
    df_event_with_id[v_message_request] = where(df_event_with_id[v_mod_id_fileconect].str.contains(v_error_id_mod, na=False),
                                                  v_error_id_mod + ' - ' + v_error_id, '1')
    
    df_event_valid = df_event_with_id[df_event_with_id[v_message_request] == '1'].copy()
    df_event_invalid = df_event_with_id[df_event_with_id[v_message_request] == v_error_id_mod + ' - ' + v_error_id].copy()
    
    if not df_event_invalid.empty:
        df_event_invalid[v_code_request] = '404'
        
        # Selecionar apenas as colunas necessárias para o DataFrame de inválidos
        df_event_invalid = df_event_invalid[[v_event_Id_BC, v_mod_name, v_mod_code, v_mod_typologie, v_section_name, v_day,
                                             v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code,
                                             v_year, v_student_group_name, v_students_number, v_classroom_name, v_id_uxxi, v_weeks, v_event_type,
                                             v_code_request, v_message_request]].copy()
        
        df_horarios_invalid = concat([df_horarios_invalid, df_event_invalid], ignore_index=True)
    
    # Remover a coluna auxiliar de mensagem do DataFrame válido
    df_event_valid.drop(columns=v_message_request, inplace=True)
    
    return (df_event_valid, df_horarios_invalid)

def module_dominant (df_event : DataFrame, df_horarios_invalid : DataFrame):

    modules_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_module_controller)
    
    flag_need_id = True
    df_modules_best = modDf.parse_list_mod_to_df(modules_db, flag_need_id)

    # Criar cópia do DataFrame de módulos para usar na função all_module_id
    df_modules_for_all_ids = df_modules_best.copy()

    #One event can have more than un one module (Dominant/Dominated)
    
    df_event[v_mod_code_dominant] = df_event[v_mod_code].str.split("#").str[0]

    df_modules_best.rename(columns={v_code_best:v_mod_code_dominant,
                                    v_id_best : v_mod_id_dominant}, inplace=True)

    # Only to Debug Data
    # df_event[v_mod_code_dominant] = where(df_event[v_id_uxxi] == '44096_99426', '1234', df_event[v_mod_code_dominant] )

    df_event = merge(left=df_event, right=df_modules_best, on = v_mod_code_dominant, how='left', indicator = True)

    df_event_with_id_mod = df_event[df_event[v_merge] == 'both'].copy() 
    df_event_without_id_mod = df_event[df_event[v_merge] == 'left_only'].copy() 

    df_event_without_id_mod = df_event_without_id_mod [[v_event_Id_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                                                        v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code, 
                                                        v_year, v_student_group_name,v_students_number,v_classroom_name, v_id_uxxi,v_weeks, v_event_type ]].copy()
    
    df_event_without_id_mod [v_code_request] = '404' # ---> Code Entity Not Found
    df_event_without_id_mod [v_message_request] = v_error_id_mod + ' - ' + v_error_id
    


    df_event_with_id_mod.drop(columns=v_merge, inplace=True)

    # Chamar all_module_id para mapear todos os códigos de módulos
    df_event_with_id_mod, df_horarios_invalid = all_module_id(df_event_with_id_mod, df_horarios_invalid, df_modules_for_all_ids)

    df_invalid = concat([df_horarios_invalid, df_event_without_id_mod], ignore_index= True)

    return (df_event_with_id_mod, df_invalid )


def typologies (df_event : DataFrame, df_horarios_invalid : DataFrame):



    df_event[v_mod_type_dominant] = df_event[v_mod_typologie].str.split("#").str[0]

    typologies_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_typologie_controller)
    
    flag_need_id = True
    df_typologies_best = typeDf.parse_list_typologies_to_df(typologies_db, flag_need_id)


    df_typologies_best.rename(columns={v_name_best:v_mod_type_dominant,
                                       v_id_best : v_mod_id_typologie}, inplace=True)


    df_event = merge(left=df_event, right=df_typologies_best, on = v_mod_type_dominant, how='left', indicator = True)

    df_event_with_id_type = df_event[df_event[v_merge] == 'both'].copy() 
    df_event_without_id_type = df_event[df_event[v_merge] == 'left_only'].copy() 

    df_event_without_id_type = df_event_without_id_type [[v_event_Id_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                                                          v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code, 
                                                          v_year, v_student_group_name,v_students_number,v_classroom_name, v_id_uxxi,v_weeks, v_event_type ]].copy()
    
    
    df_event_without_id_type [v_code_request] = '404' # ---> Code Entity Not Found
    df_event_without_id_type [v_message_request] = v_error_id_type + ' - ' + v_error_id
    

    df_invalid = concat([df_horarios_invalid, df_event_without_id_type], ignore_index= True)

    df_event_with_id_type.drop(columns=v_merge, inplace=True)

    return (df_event_with_id_type, df_invalid )



def student_group (df_event : DataFrame, df_horarios_invalid : DataFrame):

    
    st_groups_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_st_group_controller)
    
    flag_need_id = True
    df_st_group_best = stGroupDf.parse_list_st_groups_to_df(st_groups_db, flag_need_id)

    df_event.insert(0, v_id_event, arange(len(df_event)))
    df_event [v_student_group_id] = ''
    df_event_to_iterate = df_event.copy()

    for row in df_event_to_iterate.itertuples(index = False):

        groups_inserted = getattr(row, v_student_group_name)
        id_event_to_map = getattr(row, v_id_event)

        groups_by_plan = groups_inserted.split('#')
        
        module_groups_ids = []

        for i in range(len(groups_by_plan)):

            name_groups  = groups_by_plan[i].split(',')
            
            group_ids_per_module = []

            for j in range (len(name_groups)):

                value_id = df_st_group_best.loc[df_st_group_best[v_name_best]==name_groups[j], [v_id_best]]

                if value_id.empty:

                    group_ids_per_module.append(v_error_id_group + ' - ' + v_error_id)
                
                else:

                    group_ids_per_module.append(str(value_id.iloc[0,0]))

            group_ids_per_module_string = ','.join(group_ids_per_module)
            module_groups_ids.append(group_ids_per_module_string)

        values_id_to_insert_string = '#'.join(module_groups_ids)
        df_event.loc[df_event[v_id_event] == id_event_to_map, v_student_group_id] = values_id_to_insert_string

    df_event[v_message_request] = where(df_event[v_student_group_id].str.contains (v_error_id_group, na = False), 
                                    v_error_id_group  + ' - ' + v_error_id, '1')
    
    df_event_with_id_st_group = df_event[df_event[v_message_request] == '1'].copy() 
    df_event_without_id_st_group = df_event[df_event[v_message_request] == v_error_id_group + ' - ' + v_error_id].copy()
    df_event_without_id_st_group [v_code_request] = '404' # ---> Code Entity Not Found

    df_event_without_id_st_group = df_event_without_id_st_group [[v_event_Id_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                                                                  v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code, 
                                                                  v_year, v_student_group_name,v_students_number,v_classroom_name, v_id_uxxi,v_weeks, v_event_type,
                                                                  v_code_request, v_message_request]].copy()
         
    df_horarios_invalid = concat([df_horarios_invalid, df_event_without_id_st_group], ignore_index= True)
    df_event_with_id_st_group.drop(columns=v_message_request, inplace=True)

    return (df_event_with_id_st_group, df_horarios_invalid)



def classrooms (df_event : DataFrame, df_horarios_invalid : DataFrame):

    
    classrooms_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_classrooms_controller)
    
    flag_need_id = True
    df_classrooms_best = classDf.parse_list_classrooms_to_df(classrooms_db, flag_need_id)

    df_event [v_id_classroom] = ''
    df_event_to_iterate = df_event.copy()

    for row in df_event_to_iterate.itertuples(index = False):

        classrooms_inserted = getattr(row, v_classroom_name)
        id_event_to_map = getattr(row, v_id_event)

        values_id_to_insert = []

        if classrooms_inserted == '' or isnull(classrooms_inserted):

            values_id_to_insert_string = ''

        else:

            classroom_value  = classrooms_inserted.split(',')

        
            for cl in range (len(classroom_value)):

                value_id = df_classrooms_best.loc[df_classrooms_best[v_name_best] == classroom_value[cl], [v_id_best]]

                if value_id.empty:

                    values_id_to_insert.append(v_error_id_classroom + ' - ' + v_error_id)
                
                else:

                    values_id_to_insert.append(value_id.iloc[0,0])


            values_id_to_insert = [str(i) for i in values_id_to_insert]
            values_id_to_insert_string = ','.join(values_id_to_insert)
            df_event.loc[df_event[v_id_event] == id_event_to_map, v_id_classroom] = values_id_to_insert_string

    df_event[v_message_request] = where(df_event[v_id_classroom].str.contains (v_error_id_classroom, na = False), 
                                    v_error_id_classroom  + ' - ' + v_error_id, '1')
    
    df_event_with_id_classrooms = df_event[df_event[v_message_request] == '1'].copy() 
    df_event_without_id_classrooms = df_event[df_event[v_message_request] == v_error_id_classroom + ' - ' + v_error_id].copy()
    df_event_without_id_classrooms [v_code_request] = '404' # ---> Code Entity Not Found

    df_event_without_id_classrooms = df_event_without_id_classrooms [[v_event_Id_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                                                                      v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code, 
                                                                      v_year, v_student_group_name,v_students_number,v_classroom_name,v_id_uxxi,v_weeks, v_event_type,v_code_request,
                                                                      v_message_request ]].copy()
         
    df_horarios_invalid = concat([df_horarios_invalid, df_event_without_id_classrooms], ignore_index= True)
    df_event_with_id_classrooms.drop(columns=v_message_request, inplace=True)

    return (df_event_with_id_classrooms, df_horarios_invalid)




def weeks (df_event : DataFrame, df_horarios_invalid : DataFrame):

    
    weeks_db = genRequest.get_entity_data(gl_v_request.gl_url_api,gl_v_request.gl_header_request, v_weeks_controller)
    
    df_weeks_best = weeksDf.parse_list_weeks_to_df(weeks_db)

    df_weeks_best[v_name_best] = df_weeks_best[v_name_best].str[0:10]

    df_event [v_id_weeks] = ''
    df_event_to_iterate = df_event.copy()

    for row in df_event_to_iterate.itertuples(index = False):

        weeks_inserted = getattr(row, v_weeks)
        id_event_to_map = getattr(row, v_id_event)

        values_id_to_insert = []

        week_value  = weeks_inserted.split(',')

        for j in range (len(week_value)):

            value_id = df_weeks_best.loc[df_weeks_best[v_name_best] == week_value[j], [v_id_best]]

            if value_id.empty:

                values_id_to_insert.append(v_error_id_week + ' - ' + v_error_id)
            
            else:

                values_id_to_insert.append(value_id.iloc[0,0])


        values_id_to_insert = [str(i) for i in values_id_to_insert]
        values_id_to_insert_string = ','.join(values_id_to_insert)
        df_event.loc[df_event[v_id_event] == id_event_to_map, v_id_weeks] = values_id_to_insert_string

    df_event[v_message_request] = where(df_event[v_id_weeks].str.contains (v_error_id_week, na = False), 
                                 v_error_id_week + ' - ' + v_error_id, '1')
    
    df_event_with_id = df_event[df_event[v_message_request] == '1'].copy() 
    df_event_without_id = df_event[df_event[v_message_request] == v_error_id_week + ' - ' + v_error_id].copy()
    df_event_without_id [v_code_request] =  '404' # ---> Code Entity Not Found

    df_event_without_id = df_event_without_id [[v_event_Id_BC, v_mod_name, v_mod_code,v_mod_typologie, v_section_name, v_day,
                                                                  v_hourBegin, v_hourEnd, v_duration, v_course_name, v_course_code, 
                                                                  v_year, v_student_group_name,v_students_number,v_classroom_name, v_id_uxxi,v_weeks, v_event_type,
                                                                  v_code_request,v_message_request ]].copy()
         
    df_horarios_invalid = concat([df_horarios_invalid, df_event_without_id], ignore_index= True)
    df_event_with_id.drop(columns=v_message_request, inplace=True)

    return (df_event_with_id, df_horarios_invalid)

