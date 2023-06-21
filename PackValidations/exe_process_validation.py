import PackManageData.main_manage_data_uxxi as managData
import PackUpdateData.main_update_data as updateData
import PackImportData.main_import_data as importData


import PackManageApi.get_token as getToken
import PackControllerRequest.general_requests as genRequest



def exe_process_steps (name_file : str, opcion_manage_data: int,opcion_update_data :int, opcion_import_data : int, name_folder_process : str):

    valid_process = False

    if opcion_manage_data == 1:

        managData.manage_data_uxxi_steps(name_file)

    if opcion_update_data == 1:

        #Necessario verificar folder onde estão os dados, para fazer o respectivo match de dados
        updateData.update_data_steps()

    if opcion_import_data == 1:

        
        importData.import_data_steps(name_folder_process)
        

    valid_process = True

    return (valid_process)