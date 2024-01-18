import csv
import requests

from bs4 import BeautifulSoup

URL = "https://www.forbes.com/lists/cloud100"


def scrape_table():
    # Make an HTTP request to the URL
    response = requests.get(URL)

    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table element
        table = soup.find(id='table')
        table_group = table.find("div", class_="table-row-group")
        rows = table_group.find_all("a")

        # Initialize an empty list to store rows
        data = []

        # Extract data from each row in the table
        for row in rows:
            # Extract data from each cell in the row
            rank = row.find("div", class_="rank").text
            organization_name = row.find("div", class_="organizationName").text
            headquarters = row.find("div", class_="headquarters").text
            employees = row.find("div", class_="employees").text
            market_value = row.find("div", class_="marketValue").text
            industry = row.find("div", class_="industry").text
            items_to_write = (rank, organization_name,
                              headquarters, employees, market_value, industry)
            data.append(items_to_write)

    with open('fobres.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


if __name__ == '__main__':
    scrape_table()
