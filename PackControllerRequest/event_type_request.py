from PackLibrary.librarys import(
    requests,
    json
)
from mod_variables import v_total_records_dto

def get_data_event_type_search(url : str , header_request : str, controller : str, body_data : dict):

    url = url + controller + '/' + 'search' 

    response = requests.post(url, headers = header_request, json = body_data)

    dict_all_data = json.loads(response.text)

    data_values : json = dict_all_data['data']
    event_name_total_records = data_values[v_total_records_dto]

    return (event_name_total_records)