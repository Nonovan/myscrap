from selenium import webdriver
from selenium.webdriver import ChromeOptions


chrome_options = ChromeOptions(); chrome_options.add_argument("--headless=new")

# Disable Chrome features that reveal the presence of automation.
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# Hide the "Chrome is being controlled by automated test software" notification bar.
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# Disable the automation extension in Chrome, which is usually injected by Selenium.
chrome_options.add_experimental_option('useAutomationExtension', False)


driver = webdriver.Chrome(options=chrome_options)
# Modify the navigator object to hide the presence of WebDriver.
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# Visit a website.
driver.get("https://sandbox.oxylabs.io/products")

with open(f"website_html.html", "w") as f:
    f.write(driver.page_source)
driver.quit()