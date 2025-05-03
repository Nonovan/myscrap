from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Options for both Chrome and Firefox.
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless=new")

firefox_options = FirefoxOptions()
firefox_options.add_argument("-headless")


def check_for_error(driver):
    try:
        title = driver.title
        return "Sorry! Something went wrong!" in title
    except:
        return False

use_firefox = False

for i in range(5):
    url = f"https://www.amazon.com/s?k=adidas&page={i}"
    
    if not use_firefox:
        # Start with Chrome.
        driver = webdriver.Chrome(options=chrome_options)
        print(f"Using Chrome.")
    else:
        # Continue with Firefox if switched to it.
        driver = webdriver.Firefox(options=firefox_options)
        print(f"Using Firefox.")
    
    driver.get(url)

    # Check if there's an error and switch browsers if needed.
    if check_for_error(driver):
        driver.quit()
        use_firefox = True  # Switch to Firefox.
        print("Error detected, switching to Firefox.")
        driver = webdriver.Firefox(options=firefox_options)
        driver.get(url)

    # Wait for the element and capture the entire page.
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h2 > a > span"))
    )

    with open(f"amazon_{i + 1}.html", "w") as f:
        f.write(driver.page_source)
    
    driver.quit()