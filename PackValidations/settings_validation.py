import PackValidations.settings_validation_functions as settValFunct
import PackValidations.data_uxxi_validation as dataValFunct
import PackInterface.states_objects_windows as stateObj
import PackControllerRequest.controller_dto as dtObj
import PackControllerRequest.academic_year_request as acadYearRequest
import PackManageApi.global_variable_process_request as gl_v_request
import PackGeneralProcedures.global_variable_process_procedures as glVarProcess
from PackLibrary.librarys import (
    messagebox,
    traceback,
    )
from PackInterface.global_object_window import (
    main_window
)

from mod_variables import *


def validation_settings_steps():


    try:

        # Disable Button Submit
        stateObj.disable_button_submit()

        #  All Opciones Disables
        stateObj.all_opciones_disables_after_submit()

    
        # - GET DATA INSERTED UI - #
        opcion_main_process ,opcion_process_to_ejecute, name_file_uxxi, name_process_to_import,event_type_process, \
        date_last_update, check_opcion_process,check_opcion_conector = settValFunct.get_inserted_values_settings()
        
        global gl_opcion_process_to_ejecute
        gl_opcion_process_to_ejecute = opcion_process_to_ejecute
        global gl_name_file_uxxi
        gl_name_file_uxxi = name_file_uxxi
        global gl_name_process_to_import
        gl_name_process_to_import = name_process_to_import
        global gl_event_type_process
        gl_event_type_process = event_type_process
        global gl_date_last_update
        gl_date_last_update = date_last_update
        global gl_check_opcion_process
        gl_check_opcion_process = check_opcion_process
        global gl_opcion_conector
        gl_opcion_conector = check_opcion_conector
        #MAIN PROCESS
        global gl_check_main_process
        gl_check_main_process = opcion_main_process

        if opcion_main_process == 1: 

            # - Verify Folder to Insert Data From UXXI
            settValFunct.validation_folder_uxxi()

            if opcion_process_to_ejecute == 0:  # OPCION CHECK DATA
    
                # Validation Data UXXI (insercion UI)
                settValFunct.check_filling_entry_box(name_file_uxxi)
                settValFunct.check_extension_file(name_file_uxxi)
                settValFunct.validation_data_uxxi_exist_on_folder(name_file_uxxi)

                # Validation Data UXXI (file) --- VERIFICAR COMO VALIDAR NOMES COLUNAS CSV 
                # dataValFunct.verify_sheet_and_columns_name_file_uxxi(name_file_uxxi)



            elif (opcion_process_to_ejecute == 1): #OPCION IMPORT


                if check_opcion_conector == 1:


                    event_type = name_process_to_import
                
                    settValFunct.check_filling_entry_box(name_process_to_import)
                    #VERIFICAR SE ACADEMIC YEAR EXISTE
                    data_object_search = dtObj.create_dto_simple_search_filter (v_search_name, event_type)
                    validacion_event_type, begin_date_acad_year, end_date_acad_year = acadYearRequest.get_data_academic_year_search (gl_v_request.gl_url_api,gl_v_request.gl_header_request, 
                                                                                                                                    v_acad_year_controller, data_object_search)
                    
                    settValFunct.verify_name_acad_year_exist(validacion_event_type)
                    
                    #GUARDADO PARA USAR EM EXECUÇÂO DE PROCESSO
                    glVarProcess.gl_begin_date_acad_year = begin_date_acad_year
                    glVarProcess.gl_end_date_acad_year = end_date_acad_year
                    
                    #VERIFICAR SE FICHEIRO DE CONECTORES EXISTE
                    settValFunct.validation_conector_exist_on_folder()
                    
                    #VERIFICAR SE CUMPRE OS REQUISITOS O FICHEIRO

                    file_name = v_file_conectores + '.xlsx'
                    dataValFunct.verify_sheet_and_columns_name_file_conector(file_name)


                else:
                
                    settValFunct.check_filling_entry_box(name_process_to_import)
                    settValFunct.validation_process_exist_on_folder(name_process_to_import)


            else: # OPCION EXPORT ---> verify validaciones

                print ('Verify Validaciones Export - Ver Excepções Abaixo')

        else: # VALIDACIONES PLANIFICACION

            print ('Validaciones PLANIFICACION')

        # After all Validation

        stateObj.enable_button_start()
        

    

        # Focus on Main Window
        main_window.wm_state('normal')
        

    
    except settValFunct.ValidationFolderDataUxxi:

        messagebox.showerror('Validation Folder', 'Created Folder ' + v_folder_data_uxxi + ' to Insert UXXI Files !!')
    
    except settValFunct.FileNameNotInserted:

        if (opcion_process_to_ejecute == 0):

            messagebox.showerror('Validation File', 'Fill box Data UXXI to submit !!')

        elif ( opcion_process_to_ejecute == 1) & (check_opcion_conector == 0) :

            messagebox.showerror('Validation File', 'Fill box Process ID to submit !!')

        elif ( opcion_process_to_ejecute == 1) & (check_opcion_conector == 1) :

            messagebox.showerror('Acad. Year', 'Insert Acad. Year Name !!')

    except settValFunct.EventNameNotExist:

        messagebox.showerror('Acad. Year',event_type +  ' not exist !!')

    except settValFunct.FileNameErrorExtensionXlsx as e:

        file_name = e.error_value
        messagebox.showerror('Validation File', 'File ' + file_name + ' must have a .csv extension !!')

    except settValFunct.FileDataUxxiNotInserted:

        messagebox.showerror('Validation Folder', name_file_uxxi + ' not inserted on folder ' + v_folder_data_uxxi + ' !!')

    except settValFunct.FileConectoresNotInserted as e:
        messagebox.showerror('Validation File', 'Insert on Folder DataUXXI:\n\n ' + v_file_conectores + '.xlsx')



    except dataValFunct.ErrorSheetFileGeneral:  

        if gl_opcion_conector == 1:

            sheet_error = v_sheet_file_conectores
            error_header = 'Conectores UXXI'

        
        else:

            sheet_error = v_sheet_schedules_data_uxxi
            error_header = 'UXXI'

        messagebox.showerror('Check Data '+ error_header, 'Mandatory Sheet Name:\n\n' + sheet_error)

    except dataValFunct.WrongColumsGeneral:  

        if gl_opcion_conector == 1:

            error_header = 'Conectores UXXI'
            columns_file = v_mod_code_fileconect + ' - ' + v_grupo_fileconect + '\n' +  \
                           v_cod_act_fileconect+ ' - ' + v_cod_grupo_fileconet 
            
        else:
        
            columns_file = v_id_code + '-' + v_course_code + ' - ' + v_course_name + ' - ' +   v_year + ' - ' + v_mod_code + ' - ' + v_mod_name + '\n' +  \
                        v_mod_typologie + ' - ' + v_student_group + ' - ' +   v_activity_code + ' - ' + v_student_group_code + ' - ' + v_week_begin + '\n'  + \
                        v_week_end + ' - ' + v_day + ' - ' +   v_hourBegin_split + ' - ' + v_minute_begin_split + ' - ' + v_hourEnd_split + '\n' + \
                        v_minute_end_split + ' - ' + v_duration + ' - ' +   v_students_number + '\n' + \
                        v_mod_modalidad +  ' - '+ v_classroom_code + ' - ' + v_classroom_name + ' - ' + v_id_classroom_uxxi
            
        messagebox.showerror('Check Data '+ error_header, 'Possible COLUMNS NAME:\n\n' + columns_file)

    

    except settValFunct.ValidationFolderUpdateData as e:

        data_process_code = e.error_value

        message_info_config = 'DataProcess = '  + data_process_code 
                       

        messagebox.showerror('DataProcess', 'Verify if Process Code Exist:\n' + message_info_config)

    except:
        
        messagebox.showerror('ERROR', 'If error persist please contact:\n\ninfo@bulletsolutions.com')

        #Only to debug
        print (traceback.format_exc())
    return()