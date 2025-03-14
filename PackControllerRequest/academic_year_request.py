from PackLibrary.librarys import(
    requests,
    json
)

from mod_variables import v_start_date_dto, v_end_date_dto, v_total_records_dto

def get_data_academic_year_search (url : str , header_request : str, controller : str, body_data : dict):

    
    url = url + controller + '/' + 'search' 
 
    response = requests.post(url, headers = header_request, json = body_data)

    dict_all_data = json.loads(response.text)

    data_values : json = dict_all_data['data']


    event_name_total_records = data_values[v_total_records_dto]

    if event_name_total_records == 1:

        begin_date = data_values['data'][0][v_start_date_dto]
        end_date = data_values['data'][0][v_end_date_dto]

        begin_date = begin_date[0:10]
        end_date = end_date[0:10]

    else:

        begin_date = ''
        end_date = ''
     
    return( begin_date, end_date)