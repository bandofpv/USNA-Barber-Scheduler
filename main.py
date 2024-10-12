import logging
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, WebDriverException, StaleElementReferenceException

# INPUT FULL_FILEPATH ==> full file path to USNA_Barber_Scheduler directory ex: /home/pi/USNA_Barber_Scheduler
filepath = "FULL_FILEPATH"

# INPUT: ALPHACODE ==> your alpha code
alpha = "ALPHACODE"

# INPUT: "Male Haircut", "Deep Conditioner & Blow Dry", "Shampoo & Haircut", "Blow Dry & Flat Iron", "Braids, or
# "Facial Waxing"
service = "Male Haircut"

# INPUT: "Sharr (Barber)" or "Patty (Beauty/Barber)"
barber = "Sharr (Barber)"

# UNCOMMENT below line when using computer
# driver = webdriver.Firefox()

# UNCOMMENT below lines when using RPI
selenium_service = webdriver.FirefoxService(executable_path='/usr/local/bin/geckodriver')
driver = webdriver.Firefox(service=selenium_service)

# Create and configure logger
logging.basicConfig(filename=f"{filepath}/scheduler.log", format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger()

today = date.today()  # grab today's date

date_file = f"{filepath}/dates.txt"  # filename of date text file

dates = []

with open(date_file, 'r') as file_object:  # open date_file and read each line
    lines = file_object.readlines()

for line in lines:  # append each line in date_file into dates list
    dates.append(line.strip())

dates = [d for d in dates if d.strip()]  # remove empty lines from dates list

appt_date = dates.pop(0)  # grab the first date in dates list

# grab the year, month, day, and time given the "YEAR-MN-DY HR:MN" digit format
year = appt_date[0:4]
month = appt_date[5:7]
day = appt_date[8:10]
appt_time = appt_date[11:16]

appt_day = date(int(year), int(month), int(day))  # convert appt_date into a date object
days_left = (appt_day - today).days  # calculate the number of days between appointment and today

if 0 < days_left <= 13:  # 13 days is the earliest you can schedule an appointment

    wait = WebDriverWait(driver, 10)  # create a wait object
    try:  # try to open appointment website
        driver.get("https://booknow.appointment-plus.com/7qc9ltx6/10")
    except WebDriverException:  # if the website is unreachable, log it
        logger.info("Webpage unreachable")

        driver.close()  # close the driver to break rest of code

    driver.delete_all_cookies()  # delete any cookies to force a new login

    # locate login input element and login using usna email
    login = wait.until(ec.visibility_of_element_located((By.NAME, "loginname")))
    login.clear()
    login.send_keys(f"m" + alpha + "@usna.edu")

    # locate password input element and login using 260477
    pwd = driver.find_element(By.NAME, "password")
    pwd.clear()
    pwd.send_keys(alpha)
    pwd.send_keys(Keys.RETURN)

    # Click on the "click here" hyperlink
    # Note: the while loops and try/excepts are used to wait for the loading screen to disappear
    while True:
        wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "click here"))).click()

        try:  # break out of loop once the login input element is found
            driver.find_element(By.NAME, "loginname")
            break
        except NoSuchElementException:
            pass

    # locate login input element and login using usna email
    login = wait.until(ec.visibility_of_element_located((By.NAME, "loginname")))
    login.clear()
    login.send_keys(f"m" + alpha + "@usna.edu")

    # locate password input element and login using 260477
    pwd = driver.find_element(By.NAME, "password")
    pwd.clear()
    pwd.send_keys(alpha)
    pwd.send_keys(Keys.RETURN)

    # locate account input element and press the enter key to reach next menu
    acct = wait.until(ec.visibility_of_element_located((By.NAME, "account")))
    acct.send_keys(Keys.RETURN)

    # locate the "Select service" drop down and select the service desired
    while True:
        try:  # break out of loop once desired service is selected
            select = Select(driver.find_element(By.NAME, "service_id"))
            select.select_by_visible_text(service)
            break
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            pass

    # locate the "Select Barber/beautician" drop down and select the barber/beautician desired
    while True:
        try:  # break out of loop once desired barber/beautician is selected
            select = Select(driver.find_element(By.NAME, "e_id"))
            select.select_by_visible_text(barber)
            break
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            pass

    available = False

    # wait for calendar to load and grab available appointment days
    wait.until(ec.visibility_of_element_located((By.ID, "calendar")))
    available_days = driver.find_elements(By.CLASS_NAME, "calendar-available")
    for available_day in available_days:  # loop through all available appointment days
        try:
            if available_day.text == day:  # find desired appointment day
                while True:
                    try:  # break once desired appointment day is selected
                        available_day.click()
                        break
                    except ElementClickInterceptedException:
                        pass
                available = True
        except StaleElementReferenceException:
            pass

    if available:  # if the desired appointment day is available, attempt to book appointment
        found = False
        time_idx = 0
        for i in range(2):  # loop only 2 times to avoid unnecessary web queries
            # wait for appointment times to load
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "appointment-list-header")))

            spans = driver.find_elements(By.XPATH, "//span")  # grab available appointment times

            for span in spans:  # loop through all available appointment times and log index of desired time
                if appt_time in span.text:
                    found = True
                    time_idx = spans.index(span)
                    break

            # if second time looping and desired appointment time is unavailable, log it
            if i == 1 and not found:
                logger.info(f"Your desired appointment time on {appt_date} is unavailable")

                break

            # if desired appointment time isn't visible, navigate to next menu
            while not found:
                try:  # break once "Next" button is clicked
                    next_button = driver.find_element(By.CLASS_NAME, "button1")
                    next_button.click()
                    break
                except (NoSuchElementException, ElementClickInterceptedException) as e:
                    pass

            # if desired appointment time is available, book it
            if found:
                wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "button-book-it")))
                book_buttons = driver.find_elements(By.CLASS_NAME, "button-book-it")

                while True:
                    try:  # break once corresponding "book it" button is clicked
                        book_buttons[time_idx - 6].click()
                        break
                    except ElementClickInterceptedException as e:
                        pass

                wait.until(ec.visibility_of_element_located((By.XPATH, '//input[@name="send_sms" and @value="no"]')))
                radio_button = driver.find_element(By.XPATH, '//input[@name="send_sms" and @value="no"]')

                while True:
                    try:  # wait until radio_button is clicked
                        radio_button.click()
                        break
                    except ElementClickInterceptedException as e:
                        pass

                wait.until(ec.visibility_of_element_located((By.NAME, 'finalize_appt')))
                finalize_button = driver.find_element(By.NAME, 'finalize_appt')

                while True:
                    try:  # wait until finalize_button is clicked
                        finalize_button.click()
                        break
                    except ElementClickInterceptedException as e:
                        pass

                logger.info(f"Your appointment on {appt_date} was booked")

                break

        # add a "\n" to the end of each element in dates list
        for i in range(len(dates)):
            dates[i] = dates[i] + "\n"

        # write dates list onto date_file
        with open(date_file, 'w') as file_object:
            file_object.writelines(dates)

    else:  # if the desired appointment day is unavailable, add date back to dates.txt file and log it
        # re-add desired appointment date to start of dates list
        dates.insert(0, appt_date)

        # add a "\n" to the end of each element in dates list
        for i in range(len(dates)):
            dates[i] = dates[i] + "\n"

        # write dates list onto date_file
        with open(date_file, 'w') as file_object:
            file_object.writelines(dates)

        logger.info(f"Your desired appointment day on {appt_date} is unavailable")

# if desired appointment date is after current date, write over date_file excluding desired appointment date due to pop
elif days_left < 0:
    # add a "\n" to the end of each element in dates list
    for i in range(len(dates)):
        dates[i] = dates[i] + "\n"

    # write dates list onto date_file
    with open(date_file, 'w') as file_object:
        file_object.writelines(dates)

    logger.info(f"Your appointment date on {appt_date} is overdue")

# if desired appointment date is not released yet
else:
    # re-add desired appointment date to start of dates list
    dates.insert(0, appt_date)

    # add a "\n" to the end of each element in dates list
    for i in range(len(dates)):
        dates[i] = dates[i] + "\n"

    # write dates list onto date_file
    with open(date_file, 'w') as file_object:
        file_object.writelines(dates)

driver.close()  # close driver

