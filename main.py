import pandas as pd
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time

URL = "https://nextspaceflight.com/launches/past/"

url = Service(r"C:\Users\Zach7\Documents\pythonProject\chromedriver.exe")
# service = r"C:\Users\Zach7\Documents\Renata\chromedriver.exe"
driver = webdriver.Chrome(service=url)
driver.get(URL)

organisation = []
location = []
date = []
details = []
price = []
mission_status = []
rocket_status = []


def get_results():
    # Compute Organisation
    organisations = driver.find_elements(By.CSS_SELECTOR, ".mdl-card__title-text span")
    for organisation_scrape in organisations:
        organisation.append(organisation_scrape.text)

    # Compute Location and Date
    loc_date = driver.find_elements(By.CLASS_NAME, "mdl-card__supporting-text")
    for scrape in loc_date:
        date_scrape = scrape.text.splitlines()[0]
        date.append(date_scrape)

        location_scrape = scrape.text.splitlines()[1]
        location.append(location_scrape)

    # Compute details
    details_scrape = driver.find_elements(By.CLASS_NAME, "header-style")
    for detail in details_scrape:
        details.append(detail.text)

    launches = driver.find_elements(By.CSS_SELECTOR, "button[onclick*='/launches'")
    for launch in launches:
        launch.click()

        # Compute Price
        price_scrape = driver.find_element(
            By.XPATH, "/html/body/div/div/main/div/section[2]/div/div[1]/div/div[3]").text
        if price_scrape.startswith("Price"):
            price.append(price_scrape.split(": ")[1])
        else:
            price.append("")

        # Compute Mission Status
        try:
            mission_status_scrape = driver.find_element(
                By.XPATH, "/html/body/div/div/main/div/section[1]/h6[2]/span").text
            mission_status.append(mission_status_scrape)
        except NoSuchElementException:
            mission_status_scrape = driver.find_element(
                By.XPATH, "/html/body/div/div/main/div/section[1]/h6/span").text
            mission_status.append(mission_status_scrape)
        except StaleElementReferenceException:
            mission_status.append("")

        # Compute Rocket Status
        try:
            rocket_status_scrape = driver.find_element(
                By.XPATH, "/html/body/div/div/main/div/section[2]/div/div[1]/div/div[2]").text
            rocket_status.append(rocket_status_scrape.split()[1])
        except NoSuchElementException or StaleElementReferenceException:
            rocket_status.append("")

        time.sleep(2)

        driver.back()


while True:
    get_results()

    try:
        next_link = driver.find_element(By.XPATH, "/html/body/div/div/main/div/div[2]/div[2]/span/div/button[1]/span")
    except NoSuchElementException:
        break

    next_link.click()
    time.sleep(2)

df = pd.DataFrame({"organisation": organisation,
                   "location": location,
                   "date": date,
                   "details": details,
                   "price_in_million": price,
                   "mission_status": mission_status,
                   "rocket_status": rocket_status})
df.to_csv("output.csv")

driver.quit()
