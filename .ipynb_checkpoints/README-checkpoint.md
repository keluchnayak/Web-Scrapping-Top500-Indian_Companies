# AmbitionBox Top 500 Companies Analysis

A complete end-to-end Data Engineering and Exploratory Data Analysis (EDA) project focused on analyzing the top 500 companies in India based on employee engagement and ratings on AmbitionBox.

## Project Structure

```text
AmbitionBox_Top_500_Analysis/
│
├── data/
│   ├── ambitionbox_top_500_raw.csv      # Raw scraped dataset
│   └── ambitionbox_top_500_cleaned.csv  # Final cleaned dataset for EDA
│
├── notebooks/
│   ├── 01_data_collection.ipynb         # (Optional) Notebook equivalent of scraper
│   ├── 02_data_cleaning.ipynb           # Notebook handling the data cleaning
│   └── 03_eda.ipynb                     # EDA and visualizations
│
├── src/
│   ├── scraper.py                       # Automated scraper script
│   └── data_cleaning.py                 # Automated data cleaning script
│
├── outputs/
│   ├── charts/                          # Exported EDA plots (.png)
│   └── insights.md                      # Final business and workplace insights
│
├── data_dictionary.md                   # Explanation of all dataset columns
└── README.md
```

## Step-by-Step Workflow

1. **Data Collection (Web Scraping)**
   - Performed using Python (`requests` and `BeautifulSoup`).
   - Extracts the structured JSON payload embedded in the `__NEXT_DATA__` tag of the AmbitionBox HTML.
   - Collects 500 companies across 25 list pages.
   - Follows each company URL to gather deep workplace factors (Job Security, Salary, Work-Life Balance, etc.).

2. **Data Cleaning**
   - Eliminates duplicate entries.
   - Cleans textual fields (e.g., stripping out excess strings from employee counts, extracting primary cities from headquarters).
   - Validates that ratings are floats.
   - Missing data points from AmbitionBox are strictly kept as `NaN` to maintain integrity.

3. **Exploratory Data Analysis (EDA)**
   - Provides visualizations for rating distributions, review volumes, industry trends, and specific workplace factors.
   - Highlights the highest and lowest-rated companies among the top 500.

4. **Insights Generation**
   - Synthesizes findings from the EDA into actionable observations for job seekers and HR professionals.

## How to Run

1. Run the scraper to gather data:
   ```bash
   python src/scraper.py
   ```
2. Clean the collected data:
   ```bash
   python src/data_cleaning.py
   ```
3. Open the Jupyter Notebooks to explore the data and visualizations:
   ```bash
   jupyter notebook notebooks/03_eda.ipynb
   ```
