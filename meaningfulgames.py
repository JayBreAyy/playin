import requests
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
import re

records = []
for year in range(2019, 2004, -1):
	meaningless = 0
	for conf in range(2):
		if conf == 0:
			conference = "eastern"
		else:
			conference = "western"
		url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_standings_by_date_" + conference + "_conference.html"
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		
		section = soup.find(id='div_standings_by_date')
		results = section.findNext('table')
		rows = results.find_all('tr')
		
		last = 14
		games_search = re.findall(r'[0-9]+', 
			unicodedata.normalize("NFKD", rows[-1].find('td').text.strip()))
		games = int(games_search[0]) + int(games_search[1])
		for row in rows[10:]:
			if not row.has_attr('class'):	
				cells = row.find_all('td')
				rank8 = unicodedata.normalize("NFKD", cells[7].text.strip())
				rank8wins = int(re.findall(r'[0-9]+', rank8)[0])
				
				ranklast = unicodedata.normalize("NFKD", cells[last].text.strip())
				ranklastrecord = re.findall(r'[0-9]+', ranklast)
				ranklastwins = int(ranklastrecord[0])
				ranklastgames = games - int(ranklastrecord[0]) - int(ranklastrecord[1])
				
				if (ranklastgames + ranklastwins) < (rank8wins):
					last = last - 1
					meaningless = meaningless + ranklastgames
				
				if last < 8:
					break
		
	records.append([year, meaningless])
		
data = pd.DataFrame(records, columns=['Year', 'Meaningless Games'])
print(data)
print("Without play in    :", data['Meaningless Games'].min(), data['Meaningless Games'].mean(), data['Meaningless Games'].max())

