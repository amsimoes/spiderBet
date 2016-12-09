import scrapy

class betSpider(scrapy.Spider):
	name = "bets"
	games = dict()

	def __init__(self):
		self.games = dict()


	def start_requests(self):
		self.games = dict()
		urls = ["https://www.academiadasapostas.com"]
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
				yield scrapy.Request(url=link_game, callback=self.parse_tip, meta=g)


	def parse_tip(self, response):
		print("### PARSE TIP ###")
		game = response.meta
		info = response.xpath('//div[contains(@id,"stattips")]//div[\
			contains(@class,"preview_bet")]')
		game['odd'] = odd = info.xpath('.//text()').extract()[1].split(" ")[-1]
		game['tip'] = tip = info.xpath('.//text()').extract()[0].strip()
		return game


class Game(scrapy.Item):
	link = scrapy.Field()
	match = scrapy.Field()
	date = scrapy.Field()
	tip = scrapy.Field()
	odd = scrapy.Field()