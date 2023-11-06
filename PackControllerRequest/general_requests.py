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


    if response.status_code == 201:

        data_message : json = dict_data_section['message']

        data_to_present = data_message

    else:

        data_errors : json = dict_data_section['errors'][0]['detail']

        data_to_present = data_errors



    return (response.status_code, data_to_present)

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
    

    dict_data_section = json.loads(response.content)


    if response.status_code == 200:

        is_admin = dict_data_section['data']['data'][0][v_is_admin_dto]
     

    return (response.status_code, is_admin)
