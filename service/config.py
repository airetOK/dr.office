import os
from google.oauth2 import service_account


def get_config():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    account_info = {
      "private_key": os.getenv('GOOGLE_PRIVATE_KEY').replace('\\n', '\n'),
      "client_email": os.getenv('GOOGLE_CLIENT_EMAIL'),
      "token_uri": os.getenv('TOKEN_URI')
    }
    
    credentials = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
    return credentials
    
    
