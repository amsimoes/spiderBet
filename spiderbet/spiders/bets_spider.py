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
				link_game = game.xpath('./td[contains(@class,"status")]/a/@href').extract()[0]
				game_id = link_game.split("/")[-3]
				games[game_id] = []
				yield scrapy.Request(url=link_game, callback=self.parse_tip)
				time = game.xpath('./td[contains(@class,"hour")]/text()').extract()[1].strip()
				home_team = str(game.xpath('./td[contains(@class,"team-a")]/p/text()').extract())
				away_team = str(game.xpath('./td[contains(@class,"team-b")]/p/text()').extract())


	def parse_tip(self, response):
		info = response.xpath('//div[contains(@id,"stattips")]//div[\
			contains(@class,"preview_bet")]')
		odd = info.xpath('.//text()').extract()[1].split(" ")[-1]
		tip = info.xpath('.//text()').extract()[0].strip()