from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

from django.db import models

class Company(models.Model):
    website_domain = models.TextField(null=True, blank=True)
    linkedin_id = models.CharField(max_length=64, null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    linkedin_profile_url = models.TextField(null=True, blank=True)
    year_founded = models.DateField(null=True, blank=True)
    logo_url = models.TextField(null=True, blank=True)
    
    # description 
    short_description = models.TextField(null=True, blank=True)
    long_description = models.TextField(null=True, blank=True)
    linkedin_description = models.TextField(null=True, blank=True)
	
    # taxonomy 
    linkedin_specialities = ArrayField(base_field=models.TextField(), null=True, blank=True)
    linkedin_industries = ArrayField(base_field=models.TextField(), null=True, blank=True)
    categories = ArrayField(base_field=models.TextField(), null=True, blank=True)
    
    # competitors
    competitor_website_domains = ArrayField(models.TextField(), null=True, blank=True)

    # location
    hq_country = models.TextField(null=True, blank=True)
    largest_headcount_country = models.TextField(null=True, blank=True)
    hq_street_address_and_city = models.TextField(null=True, blank=True)
    all_office_addresses = models.TextField(null=True, blank=True)
    
    # financials and investment
    markets = ArrayField(models.TextField(), null=True, blank=True)
    acquisition_status = models.CharField(max_length=64, null=True, blank=True)
    last_funding_round_type = models.TextField(null=True, blank=True)
    valuation_usd = models.BigIntegerField(null=True, blank=True)
    valuation_date = models.DateField(null=True, blank=True)
    investors = ArrayField(models.TextField(), null=True, blank=True)
    total_investment_usd = models.BigIntegerField(null=True, blank=True)
    days_since_last_fundraise = models.IntegerField(null=True, blank=True)
    last_funding_round_investment_usd = models.BigIntegerField(null=True, blank=True)
    valuation_lower_bound_usd = models.BigIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('website_domain', 'linkedin_id')

class CompanyCrustdataCompanyAssociation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False, null=False, unique=True)
    crustdata_company_id = models.CharField(max_length=256, null=False, blank=False, unique=True)
