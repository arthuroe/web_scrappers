import csv
import logging

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


URL = "https://www.forbes.com/lists/cloud100"


def _get_browser():
    """
    Initiate browser load
    """
    try:

        # Create custom profile to control your browser behavior
        profile = webdriver.FirefoxProfile()
        # Specify options for the browser
        options = Options()
        options.headless = True
        options.profile = profile
        # Initialize browser
        browser = webdriver.Firefox(options=options)
        return browser
    except Exception as e:
        logging.error(e)


def get_data():
    browser = _get_browser()
    browser.get(URL)

    try:
        browser.get(URL)
        logging.info("Waiting for page to load")
    except Exception as e:
        logging.error(str(e))

    table = browser.find_element(By.CLASS_NAME, "table")

    table_headers = table.find_element(By.CLASS_NAME, "header-group")
    headers = table_headers.text.split("\n")

    table_footer = browser.find_element(By.CLASS_NAME, "table-footer")
    next_page = table_footer.find_element(
        By.XPATH, "./nav/div/button[@aria-label='Next']")

    more_pages = True
    data = []

    while more_pages:
        table_row_group = table.find_element(By.CLASS_NAME, "table-row-group")
        rows = table_row_group.find_elements(By.XPATH, "./a")

        for row in rows:
            rank = row.find_element(
                By.CLASS_NAME, "rank").get_attribute("innerText")
            organization_name = row.find_element(
                By.CLASS_NAME, "organizationName").get_attribute("innerText")
            headquarters = row.find_element(
                By.CLASS_NAME, "headquarters").get_attribute("innerText")
            employees = row.find_element(
                By.CLASS_NAME, "employees").get_attribute("innerText")
            market_value = row.find_element(
                By.CLASS_NAME, "marketValue").get_attribute("innerText")
            industry = row.find_element(
                By.CLASS_NAME, "industry").get_attribute("innerText")
            items_to_write = (rank, organization_name,
                              headquarters, employees, market_value, industry)
            data.append(items_to_write)

        if not next_page.is_enabled():
            more_pages = False
        else:
            next_page.click()

    browser.quit()

    with open('fobres.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)


if __name__ == '__main__':
    get_data()
