import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import os

def get_company_list(page):
    """Fetch a single page of the company list and return the JSON data."""
    url = f"https://www.ambitionbox.com/list-of-companies?page={page}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    print(f"Fetching list page {page}...")
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
            print(f"Error on page {page}: Status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching list page {page}: {e}")
    return []

def get_company_overview(url_name):
    """Fetch the company overview page and return detailed JSON data."""
    url = f"https://www.ambitionbox.com/overview/{url_name}-overview"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', id='__NEXT_DATA__')
            if script_tag:
                data = json.loads(script_tag.string)
                return data['props']['pageProps']
    except Exception as e:
        print(f"Error fetching overview for {url_name}: {e}")
    return None

def main():
    print("Starting AmbitionBox Top 500 Company Scraper...")
    companies_data = []
    total_companies_target = 500
    companies_per_page = 20
    pages_to_fetch = total_companies_target // companies_per_page
    
    rank = 1
    
    for page in range(1, pages_to_fetch + 1):
        companies_list = get_company_list(page)
        
        for comp in companies_list:
            url_name = comp.get('urlName')
            safe_name = comp.get('name', '').encode('cp1252', errors='replace').decode('cp1252')
            print(f"[{rank}/{total_companies_target}] Scraping: {safe_name}")
            
            overview_data = get_company_overview(url_name)
            
            if overview_data:
                header = overview_data.get('companyHeaderData', {})
                meta = overview_data.get('companyMetaInformation', {})
                
                # Navigate into ratingDistribution -> data -> ratings
                rating_dist = overview_data.get('aggregatedRatingsData', {}).get('ratingDistribution', {})
                ratings_dict = rating_dist.get('data', {}).get('ratings', {})
                
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
                    
                    # Workplace Factors
                    'work_life_balance': ratings_dict.get('workLifeRating'),
                    'job_security': ratings_dict.get('jobSecurityRating'),
                    'skill_development': ratings_dict.get('skillDevelopmentRating'),
                    'salary_benefits': ratings_dict.get('compensationBenefitsRating'),
                    'promotions_appraisals': ratings_dict.get('careerGrowthRating'),
                    'company_culture': ratings_dict.get('companyCultureRating'),
                    'work_satisfaction': ratings_dict.get('workSatisfactionRating'),
                }
                companies_data.append(record)
            
            rank += 1
            time.sleep(0.1) # Polite delay
            
        time.sleep(0.5) # Delay between pages
        
        # Save periodically
        pd.DataFrame(companies_data).to_csv('../data/ambitionbox_top_500_raw.csv', index=False)
        
    print(f"\nScraping complete! Collected {len(companies_data)} companies.")
    
    # Save to CSV
    df = pd.DataFrame(companies_data)
    
    # Check if data dir exists
    out_dir = '../data'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    csv_path = os.path.join(out_dir, 'ambitionbox_top_500_raw.csv')
    df.to_csv(csv_path, index=False)
    print(f"Raw data saved to {csv_path}")
    
    # Try saving to Excel as well
    try:
        excel_path = os.path.join(out_dir, 'ambitionbox_top_500_raw.xlsx')
        df.to_excel(excel_path, index=False)
        print(f"Raw data saved to {excel_path}")
    except Exception as e:
        print(f"Note: Could not save to Excel format ({e}). Ensure openpyxl is installed.")

if __name__ == "__main__":
    main()
