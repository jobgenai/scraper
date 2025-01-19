from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import pandas as pd
import requests

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

        # Fetch the page content using requests
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({'error': f'Failed to fetch URL, status code: {response.status_code}'}), 500

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        results = {}

        # Extract content based on selectors
        for _, row in selectors_df.iterrows():
            field_name = row['Field Name']
            selector = row['Selector']

            if isinstance(selector, str):  # Make sure the selector is a string
                elements = soup.select(selector)

                if elements:
                    # Collect all text from matching elements
                    results[field_name] = ' '.join([element.get_text(strip=True) for element in elements])
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
