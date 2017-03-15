import scrapy


class betScore(scrapy.Spider):
	name = "scores"

	def start_requests(self):
		urls = ["https://www.academiadasapostas.com"]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		fixtures = response.xpath('//div[contains(@id, "fh_main_tab")]')
		for game in fixtures.xpath('.//tr[contains(@type, "match")]'):
			score = Score()
			link_game = game.xpath('./td[contains(@class,"stats")]/a/@href').extract()[0]
			status = str(game.xpath('./td[contains(@class, "status")]/span/text()').extract()[0].strip())
			if status != "Terminado":
				continue
			score['status'] = status
			home_score = str(game.xpath('./td[contains(@class,"score")]/a//span/text()').extract()[0].strip())
			away_score = str(game.xpath('./td[contains(@class,"score")]/a//span/text()').extract()[2].strip())
			score['unique_id'] = link_game.split("/")[-3]
			print(score['unique_id']+" | "+home_score+" - "+away_score)
			score['score'] = home_score + " - " + away_score
			yield score



class Score(scrapy.Item):
	unique_id = scrapy.Field()
	score = scrapy.Field()
	status = scrapy.Field()