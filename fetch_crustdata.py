#!/usr/bin/env python
import json
import requests
import os
import sys
import django
from django.core.management import BaseCommand
from django.conf import settings
from tqdm import tqdm

# Set up Django environment
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'open_companies_database.settings_dev')
    django.setup()

from companies.models import Company, CompanyCrustdataCompanyAssociation


def convert_to_array(value, delimiter=","):
    if value:
        return [item.strip() for item in value.split(delimiter) if item.strip()]
    return []


def save_crustdata_row_in_db(crustdata_fields, crustdata_row):
    company_data = {field['api_name']: value for field, value in zip(crustdata_fields, crustdata_row)}
    company, created = Company.objects.update_or_create(
        website_domain=company_data.get('company_website_domain'),
        linkedin_id=company_data.get('linkedin_id'),
        defaults={
            'name': company_data.get('company_name'),
            'linkedin_profile_url': company_data.get('linkedin_profile_url'),
            'year_founded': company_data.get('year_founded'),
            'logo_url': company_data.get('linkedin_logo_url'),
            # 'short_description': company_data.get('short_description'),
            # 'long_description': company_data.get('long_description'),
            'linkedin_description': company_data.get('linkedin_company_description'),
            'linkedin_specialities': convert_to_array(company_data.get('linkedin_categories')),
            'linkedin_industries': convert_to_array(company_data.get('linkedin_industries')),
            'categories': convert_to_array(company_data.get('crunchbase_categories')),
            'competitor_website_domains': convert_to_array(company_data.get('competitors')),
            'hq_country': company_data.get('hq_country'),
            'largest_headcount_country': company_data.get('largest_headcount_country'),
            'hq_street_address_and_city': company_data.get('hq_street_address'),
            'all_office_addresses': company_data.get('all_office_addresses'),
            'markets': convert_to_array(company_data.get('markets')),
            'acquisition_status': company_data.get('acquisition_status'),
            'last_funding_round_type': company_data.get('last_funding_round_type'),
            'valuation_usd': company_data.get('valuation_usd'),
            'valuation_date': company_data.get('valuation_date'),
            'investors': convert_to_array(company_data.get('crunchbase_investors')),
            'total_investment_usd': company_data.get('crunchbase_total_investment_usd'),
            'days_since_last_fundraise': company_data.get('days_since_last_fundraise'),
            'last_funding_round_investment_usd': company_data.get('last_funding_round_investment_usd'),
            'valuation_lower_bound_usd': company_data.get('valuation_lower_bound_usd'),
        }
    )
    CompanyCrustdataCompanyAssociation.objects.update_or_create(
        company=company,
        defaults={'crustdata_company_id': company_data.get('company_id')}
    )


def fetch_data(config_path):
    # Load the API request configuration from the specified file
    with open(config_path, 'r') as file:
        api_request_body = json.load(file)

    auth_token = settings.CRUSTDATA_API_TOKEN
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json',
        'Origin': 'https://crustdata.com',
    }
    offset = 0
    count = 100
    progress_bar = None
    total_rows = None
    while True:
        api_request_body['offset'] = offset
        api_request_body['count'] = count
        print(f"Requesting data with offset {offset} and count {count}", flush=True)
        response = requests.post('https://api.crustdata.com/screener/screen/', headers=headers,
                                 json=api_request_body)
        response_data = response.json()
        print(f"Received response", flush=True)
        # get `total_rows`
        if total_rows is None:
            field_indices = {field['api_name']: idx for idx, field in enumerate(response_data['fields'])}
            total_rows = response_data['rows'][0][field_indices['total_rows']]
            progress_bar = tqdm(total=total_rows, desc='Fetching data from Crustdata API', file=sys.stderr, ncols=100)

        curstdata_rows = response_data.get('rows', [])
        crustdata_fields = response_data.get('fields', [])
        progress_bar.update(len(curstdata_rows))
        progress_bar.refresh()
        if not curstdata_rows:
            break
        for crustdata_row in curstdata_rows:
            save_crustdata_row_in_db(crustdata_fields, crustdata_row)
        if len(curstdata_rows) < 100:
            break

        offset += 100
    print('Successfully populated the database with Crustdata API data')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fetch data from Crustdata API and populate the database')
    parser.add_argument(
        '--request_payload',
        type=str,
        default='crustdata_request_payload.json',
        help='Path to the JSON request payload file for the Crustdata API request'
    )
    args = parser.parse_args()
    fetch_data(args.request_payload)
