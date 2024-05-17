from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
import time

alpha = "260477"

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)
driver.get("https://booknow.appointment-plus.com/7qc9ltx6/10")
driver.delete_all_cookies()

elem = wait.until(ec.visibility_of_element_located((By.NAME, "loginname")))
elem.clear()
elem.send_keys(f"m" + alpha + "@usna.edu")
elem = driver.find_element(By.NAME, "password")
elem.clear()
elem.send_keys(alpha)
elem.send_keys(Keys.RETURN)

while True:
    wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "click here"))).click()

    try:
        driver.find_element(By.NAME, "loginname")
        break
    except NoSuchElementException:
        pass

elem = driver.find_element(By.NAME, "loginname")
elem.clear()
elem.send_keys(f"m" + alpha + "@usna.edu")
elem = driver.find_element(By.NAME, "password")
elem.clear()
elem.send_keys(alpha)
elem.send_keys(Keys.RETURN)

elem = wait.until(ec.visibility_of_element_located((By.NAME, "account")))
elem.send_keys(Keys.RETURN)

while True:
    try:
        select = Select(driver.find_element(By.NAME, "service_id"))
        select.select_by_visible_text("Male Haircut")
        break
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        pass

while True:
    try:
        select = Select(driver.find_element(By.NAME, "e_id"))
        select.select_by_visible_text("Sharr (Barber)")
        break
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        pass

elements = driver.find_elements(By.CLASS_NAME, "calendar-available")
for elem in elements:
    print(elem.text)
#element = driver.find_element(By.XPATH, "//@class='calendar-available'")
#driver.close()

