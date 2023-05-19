import PackManageData.main_manage_data_uxxi as managData

def exe_process_steps (name_file : str, opcion_manage_data: int, opcion_import_data : int):

    valid_process = False

    if opcion_manage_data == 1:

        managData.manage_data_uxxi_steps(name_file)


    valid_process = True

    return (valid_process)