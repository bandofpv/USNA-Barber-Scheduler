from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

today = date.today()

date_file = "dates.txt"
log_file = "scheduler.log"

dates = []

with open(date_file, 'r') as file_object:
    lines = file_object.readlines()

for line in lines:
    dates.append(line.strip())

appt_date = dates.pop(0)
year = appt_date[0:4]
month = appt_date[5:7]
day = appt_date[8:10]

appt_day = date(int(year), int(month), int(day))
days_left = abs(appt_day - today).days

if days_left == 13:
    pass

alpha = "260477"  # input alpha code
#date = "2024-05-30"
appt_time = "12:45"  # input appointment time

# input "Male Haircut", "Deep Conditioner & Blow Dry", "Shampoo & Haircut", "Blow Dry & Flat Iron", "Braids, or
# "Facial Waxing"
service = "Male Haircut"

barber = "Sharr (Barber)"  # input "Sharr (Barber)" or "Patty (Beauty/Barber)"



driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)
driver.get("https://booknow.appointment-plus.com/7qc9ltx6/10")
driver.delete_all_cookies()

login = wait.until(ec.visibility_of_element_located((By.NAME, "loginname")))
login.clear()
login.send_keys(f"m" + alpha + "@usna.edu")
pwd = driver.find_element(By.NAME, "password")
pwd.clear()
pwd.send_keys(alpha)
pwd.send_keys(Keys.RETURN)

while True:
    wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "click here"))).click()

    try:
        driver.find_element(By.NAME, "loginname")
        break
    except NoSuchElementException:
        pass

login = driver.find_element(By.NAME, "loginname")
login.clear()
login.send_keys(f"m" + alpha + "@usna.edu")
pwd = driver.find_element(By.NAME, "password")
pwd.clear()
pwd.send_keys(alpha)
pwd.send_keys(Keys.RETURN)

acct = wait.until(ec.visibility_of_element_located((By.NAME, "account")))
acct.send_keys(Keys.RETURN)

while True:
    try:
        select = Select(driver.find_element(By.NAME, "service_id"))
        select.select_by_visible_text(service)
        break
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        pass

while True:
    try:
        select = Select(driver.find_element(By.NAME, "e_id"))
        select.select_by_visible_text(barber)
        break
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        pass

wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "calendar-available")))
available_days = driver.find_elements(By.CLASS_NAME, "calendar-available")
for available_day in available_days:
    if available_day.text == day:
        while True:
            try:
                available_day.click()
                break
            except ElementClickInterceptedException:
                pass

# wait line

found = False
time_idx = 0
for i in range(2):
    spans = driver.find_elements(By.XPATH, "//span")

    for span in spans:
        if appt_time in span.text:
            found = True
            time_idx = spans.index(span)
            break

    if i == 1 and not found:
        print(f"Your {appt_time} appointment was not available")
        break

    while not found:
        try:
            next_button = driver.find_element(By.CLASS_NAME, "button1")
            next_button.click()
            break
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            pass

    if found:
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "button-book-it")))
        book_buttons = driver.find_elements(By.CLASS_NAME, "button-book-it")

        while True:
            try:
                book_buttons[time_idx - 5].click()
                break
            except ElementClickInterceptedException as e:
                pass

# driver.close()

