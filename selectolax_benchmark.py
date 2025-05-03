import requests, time
from selectolax.parser import HTMLParser

total_time = 0
num_requests = 10

for i in range(num_requests):
    r = requests.get("https://en.wikipedia.org/wiki/List_of_minor_planet_discoverers#discovering_astronomers")
    start_time = time.time()
    tree = HTMLParser(r.text)

    rows = tree.css("table.wikitable:first-of-type tr")

    astronomers = []
    discoveries = []
    dob_dod = []

    for row in rows[1:]:
        columns = row.css("td")
        if len(columns) > 2:
            astronomers.append(columns[0].text(strip=True))
            discoveries.append(columns[1].text(strip=True))
            dob_dod.append(columns[2].text(strip=True))

    time_taken = time.time() - start_time
    total_time += time_taken
    print(f"Request {i+1} - Time taken: {time_taken} seconds")

average_time = total_time / num_requests
print(f"Average time taken: {average_time} seconds")