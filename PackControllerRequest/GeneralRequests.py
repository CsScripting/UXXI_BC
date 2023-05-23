from PackLibrary.librarys import(
    requests,
    json
)

def get_entity_data (url : str , header_request : str, controller : str):

    url = url + controller

    response = requests.request("GET", url, headers = header_request)

    dict_all_data = json.loads(response.text)

    data_values : json = dict_all_data['data']

    return(data_values)