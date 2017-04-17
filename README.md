# spiderBet
Scrapy spider to crawl and scrap betting tips from the biggest betting community website in Portugal 
(PT-PT: www.academiadasapostas.com | [EN](https://www.onlinebettingacademy.com/) | [ES](https://www.academiadeapuestas.es/))

# Introduction
The betting tips are provided everyday to anybody who access the website but, in order to check all the available tips you must follow a tedious process of opening one page per tip/game and also get past some annoying ads.

This spider checks the webapp on the homepage which provides game information such as: game identifier id, tip available, starting hour, teams playing and live/ending score.

Not every match in the webapp has a betting tip available so it checks only the ones who have, redirecting itself to the game page and finally extracting only the tip from that new page. Quick and simple. 

# Process
1. Scraps tips every morning for the day matches
2. Saves them in a txt file
3. Uploads txt file to a Google Sheets using Google Drive and Google Sheets API
4. Scraps games final scores every night for the tipped matches
5. Update the online worksheet with the final scores (Not working 100%)

This last scraping to get the final score is part of a interesting feature yet to be implemented.

This feature would be an automatic way of checking if the tip was sucessful in predicting or not. With this information, every night it would calculate the day profit balance if one got to follow every tip given.

[Google Sheets spreadsheet with the daily scraping (text in Portuguese)](https://docs.google.com/spreadsheets/d/1_NmlDRUS0ITWVpQ7E_ImzT01HRgX4ZHyQJ1omVA7yv4/edit?usp=sharing)

# Usage

`$ scrapy crawl bets`

`$ scrapy crawl scores`

There are 2 different spiders, one to scrap the tips (bets) and the other to scrap the scores (scores).
I have them being called everyday using a cron script running in my server: the bets one at 10am and the scores one at 11pm after the games are finished.

Afterwards, I call a python script to upload/update the google sheets:

`$ python3 sheets.py`

In the cronscript I also include this python script after the scrapy executions.

# Issues
* Scores spider scraping with sucess but broken when run from cron
* Sometimes one scrapy crawl isn't enough to get all available data, most likely for requests failure, my fix being crawling 3 times in the cron script with 1 minute interval
* Data gathering only works for the day matches even if the webapp has tips for the next days that the user can see with some interaction
* Spreadsheet/txt file order is from older to newer games/tips scraped, for an easier view it should show last gathered data on top
