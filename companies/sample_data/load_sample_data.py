#!/usr/bin/env python
import json
import os
import django
from django.conf import settings
import requests

# Set up Django environment
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'open_companies_database.settings_docker'))
    django.setup()

from companies.models import Company, CompanyCrustdataCompanyAssociation
from fetch_crustdata import save_crustdata_row_in_db, convert_to_array


# Only used when creating another copy of `sample_data.json`
def generate_sample_data_from_crustdata_api(crustdata_request_payload_path, output_path="sample_data.json"):
    # Load the API request payload from the specified file
    with open(crustdata_request_payload_path, 'r') as file:
        api_request_body = json.load(file)

    auth_token = settings.CRUSTDATA_API_TOKEN
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json',
        'Origin': 'https://crustdata.com',
    }

    all_data = {'fields': [], 'rows': []}
    offset = 0
    sample_data_num_rows = 2000
    while offset <= sample_data_num_rows:
        api_request_body['offset'] = offset
        api_request_body['count'] = 100

        response = requests.post('https://api.crustdata.com/screener/screen/', headers=headers, json=api_request_body)
        response_data = response.json()

        if not all_data['fields']:
            all_data['fields'] = response_data['fields']

        rows = response_data.get('rows', [])
        if not rows:
            break

        all_data['rows'].extend(rows)

        if len(rows) < 100:
            break

        offset += 100

    with open(output_path, 'w') as output_file:
        json.dump(all_data, output_file, indent=4)

    print(f'Successfully saved data to {output_path}')


def load_sample_data_in_db(sample_data_path):
    print("sample_data_path", sample_data_path)
    with open(sample_data_path, 'r') as file:
        response_data = json.load(file)
    crustdata_rows = response_data.get('rows', [])
    crustdata_fields = response_data.get('fields', [])

    for crustdata_row in crustdata_rows:
        save_crustdata_row_in_db(crustdata_fields=crustdata_fields, crustdata_row=crustdata_row)
    print('Successfully populated the database with sample data')


if __name__ == '__main__':
    load_sample_data_in_db(os.path.join(os.path.dirname(__file__), 'sample_data.json'))
