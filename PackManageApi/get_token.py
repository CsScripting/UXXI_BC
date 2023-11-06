from PackLibrary.librarys import(
    os,
    OAuth2Session,
    BackendApplicationClient,
    LegacyApplicationClient
)


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def get_token_identity_application_client(url_identity : str, client_id : str, client_secret : str):

    
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url= url_identity + 'connect/token', client_id=client_id,
            client_secret=client_secret)
    
    value_token = token["access_token"]


    return (value_token)


def get_token_identity_legacy (url_identity : str, client_id : str, client_secret : str, user_name : str, user_pass : str):

    
    oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id))
    token = oauth.fetch_token(token_url= url_identity + 'connect/token',
    username=user_name, password=user_pass, client_id=client_id,
        client_secret=client_secret)
    
    value_token = token["access_token"]


    return (value_token)




def create_header_request (value_token):

    header_request = {
                'Authorization': 'Bearer ' +  value_token,
                'Content-Type': 'application/json'
              }

    return(header_request)