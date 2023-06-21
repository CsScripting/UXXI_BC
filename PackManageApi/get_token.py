from PackLibrary.librarys import(
    os,
    OAuth2Session
)


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def get_token_identity(url_identity : str, client_id : str, client_secret : str, events : bool = False):

    from oauthlib.oauth2 import BackendApplicationClient
    from requests_oauthlib import OAuth2Session
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url= url_identity + 'connect/token', client_id=client_id,
            client_secret=client_secret)
    
    value_token = token["access_token"]

    if events:

        value_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjE3NEM4ODM0OEIxNTg2MThFNEFDQkRDREMyN0ZFNThFIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2ODcyNTIwNDcsImV4cCI6MTY4OTg0NDA0NywiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo3MDAwIiwiYXVkIjoiYmVzdGxlZ2FjeV9hcGlfcmVzb3VyY2UiLCJjbGllbnRfaWQiOiJiZXN0bGVnYWN5X2FwaV9zd2FnZ2VyIiwic3ViIjoiNzAyY2E4MDMtNDc4NC00ZmYyLWIxOWEtOWEyYjdjOTZhYzIyIiwiYXV0aF90aW1lIjoxNjg3MjUxOTk2LCJpZHAiOiJsb2NhbCIsIkFkbWluIjoiQWRtaW4iLCJuYW1lIjoiYWRtaW5AYnVsbGV0c29sdXRpb25zLmNvbSIsImVtYWlsIjoiYWRtaW5AYnVsbGV0c29sdXRpb25zLmNvbSIsInNpZCI6IjY4RjcwOTAyNkMxOTA4M0VBNDYxRUYyQUJENDc4RERDIiwiaWF0IjoxNjg3MjUyMDQ3LCJzY29wZSI6WyJiZXN0bGVnYWN5X2FwaV9zY29wZSJdLCJhbXIiOlsicHdkIl19.tGVT5IdM-Tub9WOMZBNFGc14lF0Iaurc58Tjm2tDgQQC94NZCO5OpoXDGORKux8cJgA-60Gcdj8yWGOIGWaP-waux3Fc-kuWqEU5qyo8Q4mqKwjSk0zCsreg2dPIkhsO2gQ9uh8JBiLejddxZlBdRsu-k3arnFkagnCESYSL59WtCI1_zsMo-y2kENxJX5gBEujUYxeMmCalIztCf-Rc3J-kgrgf4ZYWrpNuFDdY1_iIyW1ada3mFn6p6htUIMauhiLRI6M1-LvE8nNdi_fwoERh-UG5eJ4QEHHrRxhRiXx7WoVKMM1Gu83Wd4veYrRljBkHSGnt-wTWoIkj0VgAjQ'

    return (value_token)


def create_header_request (value_token):

    header_request = {
                'Authorization': 'Bearer ' +  value_token,
                'Content-Type': 'application/json'
              }

    return(header_request)