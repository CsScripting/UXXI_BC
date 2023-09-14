from PackLibrary.librarys import(
    ExcelFile,
    openpyxl
)
from mod_variables import *


### -- Exceptiones Classes from Functiones -- ###: 

# verify_sheet_and_columns_name_file_uxxi()
class ErrorSheetFileGeneral(Exception):
    pass

# verify_sheet_and_columns_name_file_uxxi()
class WrongColumsGeneral(Exception):
    pass

def verify_sheet_and_columns_name_file_uxxi(file_to_check : str):

    path_to_file = './' + v_folder_data_uxxi + '/' + file_to_check
    
    # - Check Sheet - #
    file_read = ExcelFile(path_to_file)
    sheets_file = file_read.sheet_names

    sheet_original = [v_sheet_data_uxxi]

    check_sheets_name =  all(elem in sheets_file for elem in sheet_original)

    if not check_sheets_name:
        
        file_read.close()
        raise ErrorSheetFileGeneral()
    
    # - Check Columns Names - #

    load_file = openpyxl.load_workbook(filename= path_to_file, read_only=True)

    sheet = load_file[v_sheet_data_uxxi] 
    columns_original = [v_id_code, v_course_code, v_course_name, v_year, v_mod_code, v_mod_name,
                        v_mod_typologie,v_student_group, v_activity_code, v_student_group_code,v_week_begin,
                        v_week_end, v_day, v_hourBegin_split,v_minute_begin_split, v_hourEnd_split, 
                        v_minute_end_split, v_duration,v_students_number,v_mod_modalidad,
                        v_classroom_code, v_classroom_name, v_id_classroom_uxxi]

    columns_file = []

    for cell in sheet[1]:

        columns_file.append(cell.value) 

    check_columns_names =  all(elem in columns_file for elem in columns_original)

    if not check_columns_names:

        error_exception = "Concat Names columns"
        load_file.close()
        raise WrongColumsGeneral(error_exception)

    load_file.close()


    return