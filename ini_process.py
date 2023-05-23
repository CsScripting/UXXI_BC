from mod_variables import *
from mod_library import *

import PackManageApi.get_token as modGetToken
import mod_get_data_json as modGetDataJson
# import mod_delete as modDelete
# import mod_get_data_file as  modGetDataFile
# import mod_update as modUpdate
# import mod_insert as modInsert


#Variables Identiy Process Request:
client_id = 'Integration_1'
client_secret = 'Password123!'

#URL's
url_identity = 'http://localhost:7000/'
url_api = 'http://localhost:8000/api/'

token_request = modGetToken.get_token_identity(url_identity, client_id, client_secret)
header_request = modGetToken.create_header_request(token_request)

##Read Data Events##

start_date = '2022-09-05'
end_date = '2022-12-12'

modGetDataJson.get_events_all_rows(url_api, header_request,start_date, end_date)

print ('============ End Process ===============')