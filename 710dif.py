import requests
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
import re

within = 0
total = 0
for year in range(2019, 2004, -1):
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
		
		row = rows[-1]
		if not row.has_attr('class'):	
			cells = row.find_all('td')
			rank7 = unicodedata.normalize("NFKD", cells[6].text.strip())
			rank7wins = int(re.findall(r'[0-9]+', rank7)[0])
			
			rank10 = unicodedata.normalize("NFKD", cells[9].text.strip())
			rank10wins = int(re.findall(r'[0-9]+', rank10)[0])
			
			total += 1
			if (rank7wins - rank10wins <= 6):
				within += 1
			print(year, conference, rank7wins - rank10wins)
	

print(within, total)