# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


def tip_format_comma(tip):
	new_tip = ""
	if ',' in tip:
		aux = tip.split(',')
		new_tip += aux[0]
		for i in range(1,len(aux)):
			if aux[i][0] == " ":
				new_tip += ":" + aux[i][0:]
			else:
				new_tip += "." + aux[i][0:]
		return new_tip
	return tip

class SpiderbetPipeline(object):
	def process_item(self, item, spider):
		if spider.name == 'bets':
			with open('bets.txt', 'a+') as f:
				flag = False
				with open('bets.txt', 'r') as f1:
					for line in f1:
						if item['unique_id'] in line:
							flag = True
				if flag == False:
					#item['tip'] = item['tip'].replace(",", ".")
					item['tip'] = tip_format_comma(item['tip'])
					item['odd'] = '\'' + item['odd']
					f.write(item['unique_id']+" , "+item['date']+" , "+item['match']+" , "+item['tip']+" , "+item['odd']+'\n')
		else:
			return item


class ScoresPipeline(object):
	def process_item(self, item, spider):
		if spider.name == 'scores':
			with open('bets.txt', 'r') as f:
				lines = f.readlines()
			for i in range(len(lines)):
				if item['unique_id'] in lines[i] and item['score'] not in lines[i]:
					lines[i] = lines[i].rstrip('\n')+" , "+item['score']+"\n"
					break
			with open('bets.txt', 'w') as f:
				f.writelines(lines)
		else:
			return item
