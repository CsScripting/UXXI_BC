from PackLibrary.librarys import(
    requests,
    json
)


def post_search_filter_audit_log (url : str , header_request : str, controller : str, body_data : dict):

    
    url = url + controller + '/' + 'search' 
 
    response = requests.post(url, headers = header_request, json = body_data)

    dict_all_data = json.loads(response.text)

    data_values : json = dict_all_data['data']['data']   
     
    return(data_values)