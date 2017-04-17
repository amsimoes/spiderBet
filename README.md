# spiderBet
Scrapy spider to crawl and scrap betting tips from the biggest betting website in Portugal (www.academiadasapostas.com)

The betting tips are provided everyday to anybody who acess the website, but in order to check all the tips you must follow a tedious process of opening one link per game and also get past
some annoying ads.

This spider (Scrapy web scraper) checks the web app on the homepage which provides game information such as: Tip available, starting hour, teams playing and live/ending score.

Not every match in the webapp has a tip so it checks only the ones who have, redirecting itself to the game page and extracting only the tip from that newpage. Quick and simple. 



spreadsheet online with the daily scraping: https://docs.google.com/spreadsheets/d/1_NmlDRUS0ITWVpQ7E_ImzT01HRgX4ZHyQJ1omVA7yv4/edit?usp=sharing
