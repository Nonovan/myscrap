import requests, json

url = "https://km8652f2eg-dsn.algolia.net/1/indexes/Jobs_production/query"

# Request headers.
headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",  # Send data as JSON instead of 'application/x-www-form-urlencoded'.
}

# 'Query String Parameters' from the Network > Payload tab.
params = {
    "x-algolia-agent": "Algolia for JavaScript (3.33.0); Browser",
    "x-algolia-application-id": "KM8652F2EG",
    "x-algolia-api-key": "YzFhZWIwOGRhOWMyMjdhZTI5Yzc2OWM4OWFkNzc3ZTVjZGFkNDdmMThkZThiNDEzN2Y1NmI3MTQxYjM4MDI3MmZpbHRlcnM9cHJpdmF0ZSUzRDA="
}

# 'Form Data' from the Network > Payload tab.
# Modify the 'length' and 'hitsPerPage' parameters to get more listings.
# This code retrieves a total of 100 listings instead of the default 15.
data = {
    "params": "query=&aroundLatLngViaIP=true&offset=0&length=100&hitsPerPage=100&aroundPrecision=20000"
}

# Send a POST request with JSON payload.
r = requests.post(url, headers=headers, params=params, json=data)

if r.status_code == 200:
    with open("stackshare_jobs.json", "w") as f:
        json.dump(r.json(), f, indent=4)
else:
    print(f"Request failed:\n{r.status_code}\n{r.text}")