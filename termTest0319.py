import re
import pandas as pd 
import random
from collections import Counter 
from pyecharts import Sankey
import time
import numpy as np
import itertools
# def Weight_Nodes(filename1, filename2, year1, year2):
def Weight_Nodes(filename1, year1):
	'''
	每次读取两个txt中的 (权值, 主题词),
	分别存入term1,term2列表中
	'''
	pattern = '([0-9.]{5})\*""([\s\S]*?)"'
	
	term = []
	with open(filename1,'r',encoding="utf-8") as f:
		content = f.readlines()
		for i in range(len(content)):
			result = re.findall(pattern, content[i])
			d = pd.DataFrame(result,columns=['value','source',]).reindex(columns=['source','value'])
			d['tag'] = '%s0%s' % (year1, i)
			term.append(d)



	return term

def generateLinks(term1, term2, year1, year2, emptyNodes):
	'''
	根据 Weight_Nodes 返回的两个列表，
	得到 year1, year2两年的links
	'''

	# 1. 初始化，及处理特殊情况
	term1 = pd.concat(term1)
	term2 = pd.concat(term2)

	space1 = year1 - 2007
	space2 = year2 - 2007

	links = []
	link =  "{'source': '%s', 'target': '%s', 'value': '0.00'}, " % (year1, year2)
	# link =  "{'source': '%s', 'target': '%s', 'value': '0.00'}, " % (' '*space1, ' '*space2)
	links.append(link)

	space = space1 - 1
	for en in emptyNodes:
		# link =  "{'source': '%s', 'target': '%s', 'value': '0.02'}, " % (en, ' '*space2)
		link =  "{'source': '%s', 'target': '%s', 'value': '0.02'}, " % (en, year2)
		emptyNodelist.append(link)
		if year1 != 2008:
			link =  "{'source': '%s', 'target': '%s', 'value': '0.02'}, " % (year1-1, en )
			# link =  "{'source': '%s', 'target': '%s', 'value': '0.02'}, " % (year1-1, en )
			# links.append(link)
			emptyNodelist.append(link)


	# 2. 计算3种情况的dataframe
	# 2.1 -- merged_t1t2 ： term1 和 term2 共有的
	merged_t1t2 = pd.merge(term1, term2, on=['source'])

	# 2.2 -- t1 : term1 - t1_t2
	t1_t2 = merged_t1t2.drop(columns = ['tag_y','value_y']) #t1
	t1_t2.rename(columns={'tag_x':'tag', 'value_x':'value'}, inplace = True) #t1
	t1 = term1.append(t1_t2)
	t1 = t1.append(t1_t2)
	t1 = t1.drop_duplicates(subset=['source', 'tag', 'value'],keep=False)
	
	# 2.3 -- t2 : term2 - t2_t1
	t2_t1 = merged_t1t2.drop(columns = ['tag_x','value_x']) #t2
	t2_t1.rename(columns={'tag_y':'tag', 'value_y':'value'}, inplace = True) #t2
	t2 = term2.append(t2_t1)
	t2 = t2.append(t2_t1)
	t2 = t2.drop_duplicates(subset=['source', 'tag', 'value'],keep=False)

	# 3. 拼接3种情况的link
	# 3.1 -- links : term1 & term2 共有的
	for _ in merged_t1t2.values:
		link =  "{'source': '%s', 'target': '%s', 'value': '%s'}, " % (_[0]+' '*space1, _[0]+' '*space2, _[1])
		links.append(link)

	# 3.2 -- links : 只有term1有的
	for t in t1.values:
		link =  "{'source': '%s', 'target': '%s', 'value': '0.0',  lineStyle:{opacity: 0 } }, " % (t[0]+' '*space1, year2)
		# link =  "{'source': '%s', 'target': '%s', 'value': '0.0',  lineStyle:{opacity: 0 } }, " % (t[0]+' '*space1, ' '*space2)
		links.append(link)

	# 3.3 -- links : 只有term2有的
	for t in t2.values:
		# print(t)
		link =  "{'source': '%s', 'target': '%s', 'value': '0.0',  lineStyle:{opacity: 0 } }, " % (year1, t[0]+' '*space2)
		# link =  "{'source': '%s', 'target': '%s', 'value': '0.0',  lineStyle:{opacity: 0 } }, " % (' '*space1, t[0]+' '*space2)
		links.append(link)

	# 4. 去重
	links = list(set(links))
	return links

def generateNodesOneByOne(term1, year1):
	'''
	根据 Weight_Nodes 返回的两个列表，
	得到 year1 的 nodes
	'''
	space1 = year1 - 2007

	emptyNodes = []

	nodes = []
	# node =  "{'name': '%s', itemStyle:{color: '#fff0',borderColor: '#fff0'} }, " % (' '*space1)
	node =  "{'name': '%s', itemStyle:{color: '#fff0',borderColor: '#fff0'} }, " % (year1)
	nodes.append(node)

	for i in term1:
		for _ in i.values:
			node =  "{'name': '%s'}, " % (_[0]+' '*space1)
			if node not in nodes:
				nodes.append(node)

		emptyNode = i['tag'][0]
		emptyNodes.append(emptyNode)
		node =  "{'name': '%s', itemStyle:{color: '#fff0', borderColor: '#fff0' }, label:{ show:false } }, " % (emptyNode)
		nodes.append(node)

	# print(len(nodes))
	# print(len(set(nodes)))
	return nodes, emptyNodes

def write2file(file, filename):
	'''
	将 generateLinks/generateNodes 的返回结果file写入文件
	'''
	with open("%s.txt" % filename, 'a', encoding='utf-8') as f:
		for i in file:
			f.write(i + '\n')

if __name__ == "__main__":
	emptyNodelist = []

	# Step 1 : 先将所有文件的 term 拿到，存放到 termYear 里
	termYear = dict()
	for i in range(2008,2015):
		try:
			term = Weight_Nodes('%s.txt'% i, i)
			termYear[i] = term
		except Exception as e:
			print("There is an error in Step 1 : " ,e)	

	# Step 2 : 每两年进行nodes生成
	years = list(termYear.keys())
	for y in range(len(termYear)-1):
		year1 = years[y]
		year2 = years[y+1]
		term1 = termYear[year1]
		term2 = termYear[year2]

		nodes,emptyNodes = generateNodesOneByOne(term1, year1)
		links = generateLinks(term1, term2, year1, year2, emptyNodes)

		write2file(nodes, 'nodes')
		write2file(links, 'links')

		print(year1,year2,'is done ...')


	links = []
	space = year2 - 2007
	nodes,emptyNodes = generateNodesOneByOne(term2, year2)
	for en in emptyNodes:
		link =  "{'source': '%s', 'target': '%s', 'value': '0.02'}, " % (year1, en)
		# link =  "{'source': '%s', 'target': '%s', 'value': '0.02'}, " % (' '*space, en)
		emptyNodelist.append(link)
	write2file(nodes, 'nodes')
	write2file(emptyNodelist, 'links')
	write2file(links, 'links')
