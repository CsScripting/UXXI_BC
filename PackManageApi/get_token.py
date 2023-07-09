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

        value_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjE3NEM4ODM0OEIxNTg2MThFNEFDQkRDREMyN0ZFNThFIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2ODgwNTYzODAsImV4cCI6MTY5MDY0ODM4MCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo3MDAwIiwiYXVkIjoiYmVzdGxlZ2FjeV9hcGlfcmVzb3VyY2UiLCJjbGllbnRfaWQiOiJiZXN0bGVnYWN5X2FwaV9zd2FnZ2VyIiwic3ViIjoiNzAyY2E4MDMtNDc4NC00ZmYyLWIxOWEtOWEyYjdjOTZhYzIyIiwiYXV0aF90aW1lIjoxNjg4MDU2MzgwLCJpZHAiOiJsb2NhbCIsIkFkbWluIjoiQWRtaW4iLCJuYW1lIjoiYWRtaW5AYnVsbGV0c29sdXRpb25zLmNvbSIsImVtYWlsIjoiYWRtaW5AYnVsbGV0c29sdXRpb25zLmNvbSIsInNpZCI6IjNBOTcyODBFODM3M0E5OTI2MDIyRDE2NTJGMTkyRUREIiwiaWF0IjoxNjg4MDU2MzgwLCJzY29wZSI6WyJiZXN0bGVnYWN5X2FwaV9zY29wZSJdLCJhbXIiOlsicHdkIl19.TKJ6FCa3zVsT3olTYCVVBlMGGeuHUTeBIzTRo4bHuIT7Ea-Kl3_DMPSOCq5GfcpfahWkV7YrB_JWhvcmGKb9Sqh_LUU7aI0Rcz2VpWU2AZ5l0-APixZs7RySQQCFwxGvBKcBEbM4OtBsX-dr167mEjXGUrfbzdaJg8lcOFOOEr9MS9s2s9rgtdkPYu4lI4bdCnQ0n1QAlpRVK0ZIXJhAAhErDW4qahO97OosHA1xbsllrdCnBHPHLfUnNbBbAQJ38YhY6lCO6Yg627K2WGtGp6P-oa4oLXYL0QwCtW6AwLnTHqNlavu51Ytb8x-MBMYBPdA3zBPv3oSu33kRqtOiRg'
        # value_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkFFODczN0IyRDBDM0QxMjhCMDA3MzZBNTI3N0U0QzMxIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2ODgwMzc5NzEsImV4cCI6MTY4ODA0MTU3MSwiaXNzIjoiaHR0cHM6Ly9pcy5yZXNlcnZhcy51cG8uZXMiLCJhdWQiOiJiZXN0bGVnYWN5X2FwaV9yZXNvdXJjZSIsImNsaWVudF9pZCI6ImJlc3RsZWdhY3lfYXBpX3N3YWdnZXIiLCJzdWIiOiJlYzU0MDk3Zi1kMWQ4LTQ5Y2YtYTE5Ny03NTZiYTk2YWNjMWEiLCJhdXRoX3RpbWUiOjE2ODgwMzc5NzEsImlkcCI6ImxvY2FsIiwiQWRtaW4iOiJBZG1pbiIsIm5hbWUiOiJhZG1pbkBidWxsZXRzb2x1dGlvbnMuY29tIiwiZW1haWwiOiJhZG1pbkBidWxsZXRzb2x1dGlvbnMuY29tIiwic2lkIjoiNkE4RUFDQUU4RDJFQzE1MzNBQkFFOUQzQzBGMjJDMDAiLCJpYXQiOjE2ODgwMzc5NzEsInNjb3BlIjpbImJlc3RsZWdhY3lfYXBpX3Njb3BlIl0sImFtciI6WyJwd2QiXX0.e0xtS0CVkaj9baQRBjusW0BCWNPCJqGrxawW1QRj-jkczkllhDzm-BESWDQVFOzsq--vgDIzw_nFaDZHu0bxxZJHcv4qJytgD5iPMLeUrnw0yvwvW2aA0YUgBV8BOUy2KX7uRlaRw52Erc71214BRTHxlJExp5rS3nLIE4LHnCesYzvNhRmXOj3_HAGSDZg7Ty727Wx48JReT-CT9CpI9pVRtAD38ePH1eJEQvoWf50qXxDwKoSrt5Fglp-yftzwqazD27LIMPEtgoHDU9rQm-xzpWg9B73--5i6_NtQQITvBTDajhWiVMYBzlTiXiqXLMTVi0M2XAt0wsFLK3rLpg'

    return (value_token)


def create_header_request (value_token):

    header_request = {
                'Authorization': 'Bearer ' +  value_token,
                'Content-Type': 'application/json'
              }

    return(header_request)