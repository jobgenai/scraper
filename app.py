from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By  # This is the missing import
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route('/scrape-article', methods=['GET'])
def scrape_article():
    try:
        # Get URL from query parameters
        url = request.args.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Load selectors from the Excel file
        excel_file = 'webdata.xlsx'  # Ensure this file is in the same directory
        selectors_df = pd.read_excel(excel_file)

        # Convert all selectors and field names to strings to avoid comparison errors
        selectors_df['Field Name'] = selectors_df['Field Name'].astype(str)
        selectors_df['Selector'] = selectors_df['Selector'].astype(str)

        # Set up Selenium WebDriver using WebDriver Manager (auto handles chromedriver)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Using WebDriver Manager to automatically download and set up chromedriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Load the dynamic page and wait for it to load fully
        driver.get(url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        page_source = driver.page_source
        driver.quit()

        # Parse the dynamically loaded page content
        soup = BeautifulSoup(page_source, 'html.parser')
        results = {}

        # Extract content based on selectors
        for _, row in selectors_df.iterrows():
            field_name = row['Field Name']
            selector = row['Selector']

            if isinstance(selector, str):  # Make sure the selector is a string
                elements = soup.select(selector)

                if elements:
                    # Collect all text from matching elements and ensure it is a string
                    results[field_name] = ' '.join([str(element.get_text(strip=True)) for element in elements])
                else:
                    results[field_name] = None  # No matching element found
            else:
                results[field_name] = None  # If selector is not a string, skip

        # Remove keys with value None (null in JSON)
        results = {key: value for key, value in results.items() if value is not None}

        # Remove duplicate values
        seen_values = set()
        results = {key: value for key, value in results.items() if value not in seen_values and not seen_values.add(value)}

        return jsonify({'success': True, 'data': results}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
