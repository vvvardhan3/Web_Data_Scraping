from bs4 import BeautifulSoup
import requests
import json

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', class_='wikitable')
rows = table.find_all('tr')

data_list = []

for row in rows[3:]:
    cols = row.find_all('td')
    data = {}
    data['Country'] = cols[0].get_text().replace('\xa0', '')
    data['Region'] = cols[1].get_text()
    data['Year'] = cols[-1].get_text().replace('\n', '')
    data['Estimate GDP'] = cols[-2].get_text()
    data_list.append(data)

json_data = json.dumps(data_list, indent=4)

# Save JSON data to a file
with open('gdp_data.json', 'w') as json_file:
    json_file.write(json_data)

print("JSON data saved to 'gdp_data.json'")

