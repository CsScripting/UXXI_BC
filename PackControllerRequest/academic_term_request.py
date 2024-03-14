from PackLibrary.librarys import(
    requests,
    json
)

from mod_variables import v_name_dto, v_total_records_dto

def get_data_academic_term_search (url : str , header_request : str, controller : str, body_data : dict):

    
    url = url + controller + '/' + 'search' 
 
    response = requests.post(url, headers = header_request, json = body_data)

    dict_all_data = json.loads(response.text)

    data_academic_term : json = dict_all_data['data']['data']
    number_records : json = dict_all_data['data'][v_total_records_dto]


    return(data_academic_term, number_records)