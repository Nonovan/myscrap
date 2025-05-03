import os
import random
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from urllib.parse import urlparse, urljoin
import datetime # For date handling (though filtering is complex)

# --- Configuration ---
# List of realistic User-Agents
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0',
]

# --- Flask App Setup ---
app = Flask(__name__)
# Optional: Set a secret key for session management if you add features later
# app.secret_key = os.urandom(24)

# --- Helper Functions ---
def is_valid_url(url):
    """Basic URL validation."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def parse_input_list(input_string):
    """Splits comma-separated input and strips whitespace."""
    if not input_string:
        return []
    return [item.strip() for item in input_string.split(',') if item.strip()]

# --- Scraping Logic ---
def perform_scrape(target_url, terms, phrases, start_date_str, end_date_str):
    """
    Performs the scraping operation for a single URL.
    Returns a dictionary with results or error information.
    """
    print(f"Scraping: {target_url}") # Log activity
    results = {'matches': [], 'status': 'pending', 'message': ''}
    headers = {'User-Agent': random.choice(USER_AGENTS)}

    # --- !!! Advanced Technique Integration Points !!! ---
    # 1. Proxy Setup (Example structure - requires actual proxy service)
    # proxies = {
    #     'http': 'http://user:password@proxyserver:port',
    #     'https': 'http://user:password@proxyserver:port',
    # }
    proxies = None # Set to None if not using proxies

    # 2. Respecting Robots.txt (Conceptual - needs library like 'reppy' or manual check)
    # print(f"Note: Check {urljoin(target_url, '/robots.txt')} before scraping extensively.")

    # 3. Rate Limiting
    time.sleep(random.uniform(1, 3)) # Be polite! Wait 1-3 seconds

    try:
        # Make the request
        response = requests.get(target_url, headers=headers, proxies=proxies, timeout=15) # Added timeout
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        # Parse HTML
        soup = BeautifulSoup(response.content, 'lxml') # Using lxml parser

        # Extract text content (consider relevant tags like <p>, <h1>, <h2>, <li>, <td> etc.)
        # This is a VERY basic text extraction. Real-world scenarios need more specific selectors.
        page_text = soup.get_text(separator=' ', strip=True).lower() # Lowercase for case-insensitive search

        found_content = []

        # --- Search Logic ---
        # Simple check if terms/phrases exist anywhere on the page
        match_found = False
        search_items = terms + phrases # Combine search criteria

        if not search_items: # If no terms/phrases, maybe just extract all paragraphs?
             paragraphs = soup.find_all('p')
             found_content = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
             if found_content:
                 match_found = True # Consider finding any paragraph a "match" in this case
        else:
            # Check for individual terms
            for term in terms:
                if term.lower() in page_text:
                    match_found = True
                    # More sophisticated: Find the specific sentence/paragraph containing the term
                    elements_with_term = soup.find_all(string=lambda text: term.lower() in text.lower())
                    for element in elements_with_term:
                       # Find the nearest relevant parent tag (e.g., <p>, <div>)
                       parent = element.find_parent(['p', 'div', 'li', 'td'])
                       if parent:
                           found_content.append(parent.get_text(strip=True))
                       else:
                           found_content.append(str(element).strip()) # Fallback

            # Check for exact phrases
            for phrase in phrases:
                if phrase.lower() in page_text:
                     match_found = True
                     # Similar logic as above to find context
                     elements_with_phrase = soup.find_all(string=lambda text: phrase.lower() in text.lower())
                     for element in elements_with_phrase:
                        parent = element.find_parent(['p', 'div', 'li', 'td'])
                        if parent:
                           found_content.append(parent.get_text(strip=True))
                        else:
                           found_content.append(str(element).strip()) # Fallback


        # --- Date Filtering (Highly Complex & Site-Specific) ---
        # This is a placeholder. Real date filtering requires identifying date elements
        # on the page (e.g., <time datetime="...">, specific text patterns) and parsing them.
        # It's often unreliable without custom logic per site.
        if start_date_str or end_date_str:
            print(f"Date filtering requested ({start_date_str} - {end_date_str}) - Note: Basic implementation doesn't filter by date effectively.")
            # You would need logic here to find date tags/text, parse them,
            # and compare against the provided range.

        # Store unique matches
        results['matches'] = list(set(found_content)) # Remove duplicates
        if not results['matches'] and match_found: # If terms were found but context extraction failed
             results['matches'] = ["Match found, but context extraction needs refinement for this site."]

        results['status'] = 'success'


    # 4. Error Handling
    except requests.exceptions.Timeout:
        results['status'] = 'error'
        results['message'] = 'Request timed out.'
        print(f"Error scraping {target_url}: Timeout")
    except requests.exceptions.HTTPError as e:
        results['status'] = 'error'
        results['message'] = f'HTTP Error: {e.response.status_code}'
        print(f"Error scraping {target_url}: HTTP {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        results['status'] = 'error'
        results['message'] = f'Request Error: {e}'
        print(f"Error scraping {target_url}: {e}")
    except Exception as e: # Catch other potential errors (e.g., parsing)
        results['status'] = 'error'
        results['message'] = f'An unexpected error occurred: {e}'
        print(f"Error scraping {target_url}: Unexpected error - {e}")

    return results


# --- Flask Routes ---
@app.route('/')
def index():
    """Displays the main form."""
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    """Handles the form submission and initiates scraping."""
    form_data = request.form
    urls_input = form_data.get('websites', '')
    terms_input = form_data.get('terms', '')
    phrases_input = form_data.get('phrases', '')
    start_date_str = form_data.get('start_date', '') # Keep as string for now
    end_date_str = form_data.get('end_date', '')   # Keep as string for now

    urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
    terms = parse_input_list(terms_input)
    phrases = parse_input_list(phrases_input)

    valid_urls = [url for url in urls if is_valid_url(url)]
    invalid_urls = [url for url in urls if not is_valid_url(url)]

    if not valid_urls:
        return render_template('index.html', error="No valid URLs provided.")

    if invalid_urls:
         print(f"Ignoring invalid URLs: {invalid_urls}") # Log invalid ones

    # --- !!! Handling JavaScript-Heavy Sites (Placeholder) !!! ---
    # If a site needs JS rendering, you'd switch to Selenium/Playwright here
    # for specific URLs or based on an initial check. This adds complexity.
    # Example idea:
    # if 'some-javascript-heavy-site.com' in target_url:
    #     result = scrape_with_selenium(target_url, ...) # Separate function needed
    # else:
    #     result = perform_scrape(...)

    all_results = {}
    for url in valid_urls:
        # Pass date strings directly; parsing/filtering happens within scrape logic if implemented
        all_results[url] = perform_scrape(url, terms, phrases, start_date_str, end_date_str)

    return render_template('index.html', results=all_results, request=request) # Pass request back to repopulate form


# --- Run the App ---
if __name__ == '__main__':
    # Note: Debug mode is insecure for production!
    app.run(debug=True)
    # For production, use a proper WSGI server like Gunicorn or Waitress:
    # gunicorn -w 4 app:app
    # waitress-serve --host 127.0.0.1 --port 5000 app:app