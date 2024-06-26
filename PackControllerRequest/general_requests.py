from PackLibrary.librarys import(
    requests,
    json
)
from mod_variables import v_id_dto, v_classrooms_controller, v_is_admin_dto

def get_entity_data (url : str , header_request : str, controller : str):

    # If DataBse Empty return a empty list ()

    if (controller == v_classrooms_controller):

        controller = controller + '/all'

    url = url + controller

    response = requests.request("GET", url, headers = header_request)

    dict_all_data = json.loads(response.text)

    data_values : json = dict_all_data['data']

    return(data_values)


def post_data_to_entity (url : str , header_request : str, controller : str, body_data : dict):

    url = url + controller 

    response = requests.post(url, headers = header_request, json = body_data)
    

    dict_data_section = json.loads(response.content)


    if( response.status_code == 201) | ( response.status_code == 200) :

        data_message : json = dict_data_section['message']

        data_to_present = data_message

    else:

        data_errors : json = dict_data_section['errors'][0]['detail']

        data_to_present = data_errors



    return (response.status_code, data_to_present)


def post_data_to_w_loads (url : str , header_request : str, controller : str, body_data : dict):

    url = url + controller 

    response = requests.post(url, headers = header_request, json = body_data)
    

    dict_data_section = json.loads(response.content)


    if ( response.status_code == 200) :

        data_message : json = dict_data_section['message']
        datos_insertados : json = dict_data_section['data']

        data_to_present = data_message

    else:

        data_errors : json = dict_data_section['errors'][0]['detail']

        data_to_present = data_errors

        datos_insertados = []



    return (datos_insertados, response.status_code, data_to_present)


def put_data_to_entity_collection (url : str , header_request : str, controller : str, body_data : dict):

    url = url + controller 

    response = requests.put(url, headers = header_request, json = body_data)
    

    dict_data_section = json.loads(response.content)


    if response.status_code == 200:

        data_message : json = dict_data_section['message']

        data_to_present = data_message

    else:

        value = 'STOP'
        print('STOP')

    #     data_errors : json = dict_data_section['errors'][0]['detail']

    #     data_to_present = data_errors

    return ()

def put_data_event_basic_information (url : str , header_request : str, controller : str, body_data : dict, id_event : str):

    url = url + controller + '/' + id_event


    response = requests.put(url, headers = header_request, json = body_data)
    

    dict_data_section = json.loads(response.content)

    return(dict_data_section)


def put_data_with_parameter (url : str , header_request : str, controller : str, body_data : dict, parameter_id : str):

    url = url + controller + '/' + str(parameter_id)

    
    response = requests.put(url, headers = header_request, json = body_data)

    dict_data_section = json.loads(response.content)

    return(dict_data_section)




def post_data_search_filter (url : str , header_request : str, controller : str, body_data : dict):

    value_id : int = 0
    url = url + controller + '/' + 'search'

    response = requests.post(url, headers = header_request, json = body_data)
    

    dict_data_section = json.loads(response.content)


    if response.status_code == 200:

        total_records = dict_data_section['data']['totalRecords']

        if total_records == 1:

            value_id = dict_data_section['data']['data'][0][v_id_dto]

        

    else:

        total_records = 0
        

    return (response.status_code, total_records, value_id)


def post_data_search_filter_user (url : str , header_request : str, controller : str, body_data : dict):

    is_admin = False

    url = url + controller + '/' + 'search'

    response = requests.post(url, headers = header_request, json = body_data)
    

    

    if response.status_code == 200:

        dict_data_section = json.loads(response.content)

        is_admin = dict_data_section['data']['data'][0][v_is_admin_dto]

     

    return (response.status_code, is_admin)
