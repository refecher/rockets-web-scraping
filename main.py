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
mission_name = []
rocket_name = []
price = []
mission_status = []
rocket_status = []


def get_results():
    launches = driver.find_elements(By.CSS_SELECTOR, "button[onclick*='/launches'")

    for launch in launches:
        launch.click()

        try:
            organisation_scrape = driver.find_element(
                By.XPATH, "/html/body/div/div/main/div/section[2]/div/div[1]/div/div[1]").text
            organisation.append(organisation_scrape)
        except NoSuchElementException or StaleElementReferenceException:
            organisation.append("")

        try:
            location_scrape = driver.find_element(By.XPATH, "/html/body/div/div/main/div/section[5]/div[1]/h4").text
            if len(location_scrape) <= 5:
                location_scrape = driver.find_element(By.XPATH, "/html/body/div/div/main/div/section[4]/div[1]/h4").text
                location.append(location_scrape)
            else:
                location.append(location_scrape)
        except NoSuchElementException or StaleElementReferenceException:
            location.append("")

        try:
            date_scrape = driver.find_element(By.ID, "localized").text
            date.append(date_scrape)
        except NoSuchElementException:
            date_scrape = driver.find_element(
                By.XPATH, "/html/body/div/div/main/div/section[1]/div/div/div[1]/div").text
            date.append(date_scrape.splitlines()[1])
        except StaleElementReferenceException:
            date.append("")

        try:
            mission_name_scrape = driver.find_element(By.CSS_SELECTOR, "h4.mdl-card__title-text").text
            mission_name.append(mission_name_scrape)
        except NoSuchElementException or StaleElementReferenceException:
            mission_name.append("")

        try:
            rocket_name_scrape = driver.find_element(By.CSS_SELECTOR, "div.mdl-card__title-text span").text
            rocket_name.append(rocket_name_scrape)
        except NoSuchElementException or StaleElementReferenceException:
            rocket_name.append("")

        try:
            price_scrape = driver.find_element(
                By.XPATH, "/html/body/div/div/main/div/section[2]/div/div[1]/div/div[3]").text
            if price_scrape.startswith("Price"):
                price.append(price_scrape.split(": ")[1])
            else:
                price.append("")
        except NoSuchElementException or StaleElementReferenceException:
            price.append("")

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
                   "mission_name": mission_name,
                   "rocket_name": rocket_name,
                   "price_in_million": price,
                   "mission_status": mission_status,
                   "rocket_status": rocket_status})
df.to_csv("output.csv")

driver.quit()
