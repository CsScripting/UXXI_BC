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

        value_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjE3NEM4ODM0OEIxNTg2MThFNEFDQkRDREMyN0ZFNThFIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2OTQ2MjUzNTMsImV4cCI6MTY5NzIxNzM1MywiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo3MDAwIiwiYXVkIjoiYmVzdGxlZ2FjeV9hcGlfcmVzb3VyY2UiLCJjbGllbnRfaWQiOiJiZXN0bGVnYWN5X2FwaV9zd2FnZ2VyIiwic3ViIjoiNzAyY2E4MDMtNDc4NC00ZmYyLWIxOWEtOWEyYjdjOTZhYzIyIiwiYXV0aF90aW1lIjoxNjk0NjI1MzUzLCJpZHAiOiJsb2NhbCIsIkFkbWluIjoiQWRtaW4iLCJuYW1lIjoiYWRtaW5AYnVsbGV0c29sdXRpb25zLmNvbSIsImVtYWlsIjoiYWRtaW5AYnVsbGV0c29sdXRpb25zLmNvbSIsInNpZCI6IjI1RjE1QzRFNkRBNjMzMEE0MTVCQzRFMzRBQTZCREQ5IiwiaWF0IjoxNjk0NjI1MzUzLCJzY29wZSI6WyJiZXN0bGVnYWN5X2FwaV9zY29wZSJdLCJhbXIiOlsicHdkIl19.JAD5iVP82ZYgZwI1VRhU9O5imyouoWjvSxHdSaBJ2SyK-fBczlX1w43_UXVXbOC_81nQ85VoKrjFCM8B2MQy1FzHLMOVaftjR8gqFzLc3R8KcfXzJHQ8MS2Q_YwUytFK1b3gleWAkx-TzlmHqAMaD4OaQMOoHl9SzrcUWQyYqqcTu_OJbqUexgXrFiXLK4ZjDERZeqF5kJvjZ1Mzq6q43HUys1DzDufZIZX7V7BpKZkfOSExFMD_iEbsXWP1DwjrLw4xxVPVAHOkx67fb6HGyN3UGCfqjHNhpVPMKVHhTK3uGoV4f3Oe1bJ5YQGDYZM-2DQU45G89Etl0eMHzzFzBA'
        # value_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkFFODczN0IyRDBDM0QxMjhCMDA3MzZBNTI3N0U0QzMxIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2ODgwMzc5NzEsImV4cCI6MTY4ODA0MTU3MSwiaXNzIjoiaHR0cHM6Ly9pcy5yZXNlcnZhcy51cG8uZXMiLCJhdWQiOiJiZXN0bGVnYWN5X2FwaV9yZXNvdXJjZSIsImNsaWVudF9pZCI6ImJlc3RsZWdhY3lfYXBpX3N3YWdnZXIiLCJzdWIiOiJlYzU0MDk3Zi1kMWQ4LTQ5Y2YtYTE5Ny03NTZiYTk2YWNjMWEiLCJhdXRoX3RpbWUiOjE2ODgwMzc5NzEsImlkcCI6ImxvY2FsIiwiQWRtaW4iOiJBZG1pbiIsIm5hbWUiOiJhZG1pbkBidWxsZXRzb2x1dGlvbnMuY29tIiwiZW1haWwiOiJhZG1pbkBidWxsZXRzb2x1dGlvbnMuY29tIiwic2lkIjoiNkE4RUFDQUU4RDJFQzE1MzNBQkFFOUQzQzBGMjJDMDAiLCJpYXQiOjE2ODgwMzc5NzEsInNjb3BlIjpbImJlc3RsZWdhY3lfYXBpX3Njb3BlIl0sImFtciI6WyJwd2QiXX0.e0xtS0CVkaj9baQRBjusW0BCWNPCJqGrxawW1QRj-jkczkllhDzm-BESWDQVFOzsq--vgDIzw_nFaDZHu0bxxZJHcv4qJytgD5iPMLeUrnw0yvwvW2aA0YUgBV8BOUy2KX7uRlaRw52Erc71214BRTHxlJExp5rS3nLIE4LHnCesYzvNhRmXOj3_HAGSDZg7Ty727Wx48JReT-CT9CpI9pVRtAD38ePH1eJEQvoWf50qXxDwKoSrt5Fglp-yftzwqazD27LIMPEtgoHDU9rQm-xzpWg9B73--5i6_NtQQITvBTDajhWiVMYBzlTiXiqXLMTVi0M2XAt0wsFLK3rLpg'

    return (value_token)


def create_header_request (value_token):

    header_request = {
                'Authorization': 'Bearer ' +  value_token,
                'Content-Type': 'application/json'
              }

    return(header_request)