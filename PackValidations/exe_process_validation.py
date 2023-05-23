import PackManageData.main_manage_data_uxxi as managData
import PackUpdateData.main_update_data as updateData



def exe_process_steps (name_file : str, opcion_manage_data: int,opcion_update_data :int, opcion_import_data : int):

    valid_process = False

    if opcion_manage_data == 1:

        managData.manage_data_uxxi_steps(name_file)

    if opcion_update_data == 1:

        #Necessario verificar folder onde estão os dados, para fazer o respectivo match de dados
        updateData.update_data_steps()



    valid_process = True

    return (valid_process)