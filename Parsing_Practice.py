#!/usr/bin/python3

# -*- coding: utf-8 -*-
import requests
import re
from requests_html import HTML

domain = 'https://www.ptt.cc'
search_endpoint_url = 'https://www.ptt.cc/bbs/Beauty/search'

def fetch(url):
	response = requests.get(url)
	response = requests.get(url, cookies={'over18':'1'}) # cookie去哪裡找？
	return response

def parse_article_entities(doc):
	html = HTML(html=doc) #為什麼要多 html=
	post_entries = html.find('div.r-ent')
	return post_entries

def parse_article_meta(entry):
	meta = {
		'title':entry.find('div.title', first=True).text,
		'push':entry.find('div.nrec', first=True).text,
		'date':entry.find('div.date', first=True).text, # first=True 什麼意思？
	}

	try:
		meta['author'] = entry.find('div.author', first=True).text
		meta['link'] = domain + entry.find('div.title > a', first=True).attrs['href']
	except AttributeError:
		if '(本文已被刪除)' in meta['title']:
			match_author = re.search('\[(\w*)\]', meta['title']) #這是在爬 [haudai] 這個字
			if match_author:
				meta['author'] = match_author.group(1)
		elif re.search('已被\w*刪除', meta['title']):
			match_author = re.search('\<(\w*)\>', meta['title']) #這是在爬 <edisonchu> 這個字
			if match_author:
				meta['author'] = match_author.group(1)
		meta['link'] = ""
	return meta

def get_metadata_from(url):

	def parse_next_link(doc):
		html = HTML(html=doc)
		controls = html.find('.action-bar a.btn.wide')
		link = controls[1].attrs['href']
		return domain + link

	resp = fetch(url)
	post_entries = parse_article_entities(resp.text)
	next_link = parse_next_link(resp.text)

	metadata = [parse_article_meta(entry) for entry in post_entries]
	return metadata, next_link

def get_page_meta(url, num_pages):

	collected_meta = []
	for _ in range(num_pages):
		posts, link = get_metadata_from(url)
		collected_meta += posts
		url = link

	return collected_meta

def get_metadata_from_search(keyword):

	def parse_next_link(doc):
		html = HTML(html=doc)
		controls = html.find('.action-bar a.btn.wide')
		link = controls[1].attrs['href']
		return domain + link

	resp = requests.get(search_endpoint_url, params={'q': keyword})
	post_entries = parse_article_entities(resp.text)
	metadata = [parse_article_meta(entry) for entry in post_entries]
	return metadata


# start_url = 'https://www.ptt.cc/bbs/Beauty/index.html'
# metadata = get_page_meta(start_url, num_pages=5)
metadata = get_metadata_from_search("涼")
for meta in metadata:
	print(meta['title'], meta['push'], meta['date'], meta['author'], meta['link'])
