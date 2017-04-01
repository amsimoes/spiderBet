import scrapy
import time
import os

# TODO
# crawl the english version
# crawl the odd provider (if exists)
# bets.txt -> Google sheets
# deploy digitalocean + cron?

class betSpider(scrapy.Spider):
	name = "bets"

	def start_requests(self):
		urls = ["https://www.academiadasapostas.com/"]
		if os.path.isfile("bets.txt") == False:
			with open('bets.txt', 'w') as f:
				f.write("Data / ID , Hora , Jogo , Tip , Odd")
		with open('bets.txt', 'r') as f:
			today = time.strftime("%d/%m/%Y")
			print ("Today = " + today)
			flag = False
			for line in f:
				print ("line = " + line)
				if today in line:
					flag = True
			with open('bets.txt', 'a+') as f:
				if flag == False:
					if os.path.getsize('bets.txt') > 0:
						f.write("\n\n")
					f.write(time.strftime("%d/%m/%Y")+"\n")
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)


	def parse(self, response):
		fixtures = response.xpath('//div[contains(@id, "fh_main_tab")]')
		for game in fixtures.xpath('.//tr[contains(@type, "match")]'):
			if game.xpath('./td[contains(@class,"status")]/a').extract():
				g = Game()
				g['link'] = link_game = game.xpath('./td[contains(@class,"status")]/a/@href').extract()[0]
				g['date'] = time = game.xpath('./td[contains(@class,"hour")]/text()').extract()[1].strip()
				home_team = str(game.xpath('./td[contains(@class,"team-a")]/p/text()').extract())
				away_team = str(game.xpath('./td[contains(@class,"team-b")]/p/text()').extract())
				g['match'] = home_team[2:-2]+" X "+away_team[2:-2]
				g['unique_id'] = link_game.split("/")[-3]
				yield scrapy.Request(url=link_game, callback=self.parse_tip, meta=g)


	def parse_tip(self, response):
		print("### PARSE TIP ###")
		game = response.meta
		info = response.xpath('//div[contains(@id,"stattips")]//div[\
			contains(@class,"preview_bet")]')
		odd = info.xpath('.//text()').extract()[1].split(" ")[-1]
		#game['odd'] = odd.replace(".", ",")
		game['odd'] = odd
		game['tip'] = tip = info.xpath('.//text()').extract()[0].strip()
		return game


class Game(scrapy.Item):
	link = scrapy.Field()
	match = scrapy.Field()
	date = scrapy.Field()
	unique_id = scrapy.Field()
	tip = scrapy.Field()
	odd = scrapy.Field()
