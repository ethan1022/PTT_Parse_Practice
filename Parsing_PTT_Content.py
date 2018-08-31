#!/usr/bin/python3

# -*- coding: utf-8 -*-
import requests
import re
from requests_html import HTML
from multiprocessing import Pool

def fetch(url):
	response = requests.get(url)
	response = requests.get(url, cookies={'over18':'1'}) # cookie去哪裡找？
	return response

def parse_article_entities(doc):
	html = HTML(html=doc) #為什麼要多 html=
	post_entries = html.find('div.article-metaline')
	all_content = html.find('div')[10].text
	post_content = all_content.split("※", 1)[0].split("\n",5)[-1]
	return post_entries, post_content

def parse_article_meta(entry, content):
	meta = {
	'author':entry[0].find('span.article-meta-value', first=True).text,
	'title':entry[1].find('span.article-meta-value', first=True).text,
	'date':entry[2].find('span.article-meta-value', first=True).text,
	'content': content
	}
	return meta

url = 'https://www.ptt.cc/bbs/Beauty/M.1534515249.A.AC2.html'
resp = fetch(url)
entry, content = parse_article_entities(resp.text)
meta = parse_article_meta(entry, content)
print(meta['author'], meta['title'], meta['date'], meta['content'] )