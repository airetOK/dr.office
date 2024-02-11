import googleapiclient.discovery
import os
from datetime import datetime

import service.config as config


def __get_service(service_name='sheets', api_version='v4'):
    credentials = config.get_config()
    service = googleapiclient.discovery.build(service_name, api_version, credentials=credentials)
    return service

def __convert_to_patients(spreadsheet: list[list]):
    patients = []
    for row in spreadsheet:
        patients.append({
            'fullname': row[0],
            'teeth': row[1],
            'actions': row[2],
            'price': row[3],
            'date': row[4]
        })
    return patients

def __get_current_date() -> str:
    return datetime.today().strftime('%Y-%m-%d')

def get_patients():
    service = __get_service()
    spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')
    range_name = os.getenv('GOOGLE_CELL_RANGE')
    spreadsheet = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute().get('values', [])
    return __convert_to_patients(spreadsheet)

def add_patient(form: object):
    service = __get_service()
    spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')
    range_name = os.getenv('GOOGLE_CELL_RANGE')
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, 
        range=range_name,
        valueInputOption="RAW", 
        body={'values' : [[form['fullname'], form['teeth'], form['actions'], form['price'], __get_current_date()]]}).execute()
