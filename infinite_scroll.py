import time, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome()
# Visit a web page with infinite scroll.
driver.get("https://quotes.toscrape.com/scroll")
time.sleep(2)

while True:
    # Get the vertical position of the page in pixels.
    last_scroll = driver.execute_script("return window.scrollY")
    # Scroll down by a random amount of pixels between a realistic fixed interval.
    ActionChains(driver).scroll_by_amount(0, random.randint(499, 3699)).perform()
    time.sleep(2)
    # Get the new vertical position of the page in pixels after scrolling.
    new_scroll = driver.execute_script("return window.scrollY")
    # Break the loop if the page has reached its end.
    if new_scroll == last_scroll:
        break
    last_scroll = new_scroll

cards = driver.find_elements(By.CSS_SELECTOR, ".quote")
# Get the number of quote cards you've loaded. It should be 100 cards in total.
print(len(cards))
driver.quit()