# Make sure to have a 'previous_html.html' file saved before running the code.
import requests
from bs4 import BeautifulSoup

url = "https://sandbox.oxylabs.io/products"

def fetch_html(url):
    return requests.get(url).text

# Strip the text, leaving only HTML tags and classes.
def strip_to_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for element in soup.find_all(string=True):
        element.extract()
    return soup.prettify()

def compare_structure():
    try:
        with open("previous_html.html", "r") as f:
            previous_html = f.read()
    except FileNotFoundError as e:
        print(f"Error: {e}")

    current_html = fetch_html(url)
    if strip_to_tags(previous_html) != strip_to_tags(current_html):
        with open("previous_html.html", "w") as f:
            f.write(current_html)
        print("HTML structure has changed.")
    else:
        print("No structure changes detected.")

compare_structure()