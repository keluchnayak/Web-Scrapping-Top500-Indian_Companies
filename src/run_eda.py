import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("Generating EDA charts...")

# Configure plotting style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Create output directory for charts
os.makedirs('../outputs/charts', exist_ok=True)

# Load cleaned data
df = pd.read_csv('../data/ambitionbox_top_500_cleaned.csv')
print(f"Dataset loaded: {df.shape[0]} companies, {df.shape[1]} columns.")

# 1.1 Rating Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['rating'].dropna(), bins=20, kde=True, color='skyblue')
plt.title('Distribution of Overall Company Ratings', fontsize=15)
plt.xlabel('Rating (out of 5)')
plt.ylabel('Number of Companies')
plt.axvline(df['rating'].mean(), color='red', linestyle='--', label=f'Mean: {df["rating"].mean():.2f}')
plt.legend()
plt.savefig('../outputs/charts/rating_distribution.png')
plt.close()

# 1.2 Top 10 Highest Rated Companies
top_rated = df[df['review_count'] > 5000].nlargest(10, 'rating')
if not top_rated.empty:
    plt.figure(figsize=(12, 6))
    sns.barplot(x='rating', y='company_name', data=top_rated, palette='viridis')
    plt.title('Top 10 Highest Rated Companies (>5k reviews)', fontsize=15)
    plt.xlim(3.5, 5.0)
    plt.xlabel('Rating')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('../outputs/charts/top_10_rated.png')
    plt.close()

# 1.3 Bottom 10 Rated Companies
bottom_rated = df[df['review_count'] > 5000].nsmallest(10, 'rating')
if not bottom_rated.empty:
    plt.figure(figsize=(12, 6))
    sns.barplot(x='rating', y='company_name', data=bottom_rated, palette='magma')
    plt.title('Bottom 10 Lowest Rated Companies (>5k reviews)', fontsize=15)
    plt.xlim(2.5, 4.0)
    plt.xlabel('Rating')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('../outputs/charts/bottom_10_rated.png')
    plt.close()

# 2.1 Most Reviewed Companies
top_reviewed = df.nlargest(10, 'review_count')
if not top_reviewed.empty:
    plt.figure(figsize=(12, 6))
    sns.barplot(x='review_count', y='company_name', data=top_reviewed, palette='Blues_r')
    plt.title('Top 10 Most Reviewed Companies', fontsize=15)
    plt.xlabel('Number of Reviews')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('../outputs/charts/top_10_reviewed.png')
    plt.close()

# 3.1 Industry Analysis
top_industries = df['industry'].value_counts().head(10)
if not top_industries.empty:
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_industries.values, y=top_industries.index, palette='crest')
    plt.title('Top 10 Industries by Number of Companies', fontsize=15)
    plt.xlabel('Number of Companies')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('../outputs/charts/top_industries.png')
    plt.close()

# 4. Workplace Factors Analysis
workplace_factors = ['work_life_balance', 'job_security', 'skill_development', 
                     'salary_benefits', 'promotions_appraisals', 'company_culture', 'work_satisfaction']

available_factors = [f for f in workplace_factors if f in df.columns]
if available_factors:
    factor_means = df[available_factors].mean().sort_values()
    plt.figure(figsize=(12, 6))
    sns.barplot(x=factor_means.values, y=factor_means.index, palette='mako')
    plt.title('Average Score by Workplace Factor', fontsize=15)
    plt.xlim(2.5, 4.0)
    plt.xlabel('Average Score (out of 5)')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('../outputs/charts/workplace_factors.png')
    plt.close()

print("Charts successfully generated in outputs/charts/")
