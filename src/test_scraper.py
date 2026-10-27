import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

def get_company_list(page=1):
    """Fetch a single page of the company list and return the JSON data."""
    url = f"https://www.ambitionbox.com/list-of-companies?page={page}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    print(f"-> Fetching list page {page}...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', id='__NEXT_DATA__')
            if script_tag:
                data = json.loads(script_tag.string)
                companies = data['props']['pageProps']['companyListingData']
                return companies
            else:
                print("Error: __NEXT_DATA__ script not found on list page.")
        else:
            print(f"Error: Status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching list page: {e}")
    return []

def get_company_overview(url_name):
    """Fetch the company overview page and return detailed JSON data."""
    url = f"https://www.ambitionbox.com/overview/{url_name}-overview"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    print(f"  -> Fetching overview for {url_name}...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', id='__NEXT_DATA__')
            if script_tag:
                data = json.loads(script_tag.string)
                page_data = data['props']['pageProps']
                return page_data
            else:
                print(f"Error: __NEXT_DATA__ not found on overview page for {url_name}.")
        else:
            print(f"Error: Status code {response.status_code} for {url_name}")
    except Exception as e:
        print(f"Error fetching overview for {url_name}: {e}")
    return None

def test_scrape_first_3_companies():
    """Test script to scrape the first 3 companies and extract required fields."""
    companies_data = []
    
    # Step 1: Get list of companies from page 1
    companies_list = get_company_list(page=1)
    
    # Limit to first 3 companies for testing
    for rank, comp in enumerate(companies_list[:3], start=1):
        url_name = comp.get('urlName')
        
        # Step 2 & 3: Visit overview page and extract details
        overview_data = get_company_overview(url_name)
        
        if overview_data:
            # Extract basic data from header
            header = overview_data.get('companyHeaderData', {})
            meta = overview_data.get('companyMetaInformation', {})
            ratings_data = overview_data.get('aggregatedRatingsData', {})
            
            # Map factors to variables
            factors = ratings_data.get('factors', [])
            factor_dict = {f['name']: f['rating'] for f in factors}
            
            # Build company record
            record = {
                'rank': rank,
                'company_name': header.get('companyName') or meta.get('shortName'),
                'company_url': f"https://www.ambitionbox.com/overview/{url_name}-overview",
                'rating': header.get('rating'),
                'review_count': header.get('reviewsCount'),
                'industry': meta.get('primaryIndustry', [{}])[0].get('name') if meta.get('primaryIndustry') else None,
                'company_type': next((i['label'] for i in header.get('info', []) if i['type'] == 'CompanyType'), None),
                'headquarters': meta.get('hq', {}).get('cityState'),
                'employees': meta.get('globalEmployeeCount'),
                # Sub-ratings (Workplace Factors)
                'work_life_balance': factor_dict.get('Work-Life Balance'),
                'job_security': factor_dict.get('Job Security'),
                'skill_development': factor_dict.get('Skill Development'),
                'salary_benefits': factor_dict.get('Salary & Benefits'),
                'promotions_appraisals': factor_dict.get('Promotions / Appraisal'),
                'company_culture': factor_dict.get('Company Culture'),
                'work_satisfaction': factor_dict.get('Work Satisfaction'),
            }
            companies_data.append(record)
            
            # Polite delay
            time.sleep(1)

    # Step 4: Convert to DataFrame
    df = pd.DataFrame(companies_data)
    
    # Display results
    pd.set_option('display.max_columns', None)
    print("\n--- Test Scraping Results ---")
    print(df.head())
    
    # Step 5: Save raw test dataset
    df.to_csv('test_ambitionbox_raw.csv', index=False)
    print("\nSaved to test_ambitionbox_raw.csv")

if __name__ == "__main__":
    test_scrape_first_3_companies()
