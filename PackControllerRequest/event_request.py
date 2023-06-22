from PackLibrary.librarys import(
    requests,
    json
)



def get_events_all (url : str , header_request : str, controller : str, startDate : str, endDate :str):

    
    url = url + controller + '/all/' + startDate + '/' + endDate 
 
    response = requests.request("GET", url, headers = header_request)

    dict_all_data = json.loads(response.text)

    data_values : json = dict_all_data['data']

    return(data_values)