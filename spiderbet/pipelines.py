# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pygsheets


class SpiderbetPipeline(object):
	def process_item(self, item, spider):
		if spider.name == 'bets':
			with open('/home/bequis/spiderBet/bets.txt', 'a') as f:
				f.write(item['unique_id']+" | "+item['date']+" | "+item['match']+" | "+item['tip']+" | "+item['odd']+'\n')
		else:
			return item
