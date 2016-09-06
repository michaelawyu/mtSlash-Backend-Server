import plugin_sectionname2number
import re
from bs4 import BeautifulSoup
import requests

def retrieve_search_result(SEARCH_URL, keyword, payload, cookie):
	payload['srchtxt'] = keyword

	r = requests.get(SEARCH_URL, params = payload, cookies = cookie)
	html_data = r.text

	return html_data

def parse_html(html_data, res):
	# lxml Parser Required; Will Switch to Default Parser html.parser if lxml is Unavailable
	try:
		soup = BeautifulSoup(html_data, 'lxml')
	except:
		print('An error has occurred: lxml Parser is not installed. System will now switch to default parser.')
		soup = BeautifulSoup(html_data, 'html.parser')

	# Load Regular Expressions
	re_for_extracting_number_of_results = res['extracting_number_of_results']
	re_for_extracting_number_of_views_and_replies = res['extracting_number_of_views_and_replies']
	re_for_extracting_search_id = res['extracting_search_id']

	# Parse the Number of Results from html_data
	number_of_results_raw = soup.h2.em.contents[2]
	result_raw = re.findall(re_for_extracting_number_of_results, number_of_results_raw)
	number_of_results = int(result_raw[0])

	# Parse the Search Result
	results = []
	results_raw = soup.find_all('li', class_ = 'pbw')
	len_of_results_in_this_page = len(results_raw)

	for i in range(0, len_of_results_in_this_page):
		result = {}
		result_raw = results_raw[i]
		result['tid'] = int(result_raw['id'])
		topic_title_fragmentized = result_raw.h3.a.contents
		topic_title = ''
		for fragment in topic_title_fragmentized:
			current_part_of_title = fragment.string
			topic_title = topic_title + current_part_of_title
		result['topic_title'] = topic_title

		no_of_views_and_replies_raw = unicode(result_raw.find_all('p',class_='xg1')[0].contents[0])
		no_of_views_and_replies_in_list = re.findall(re_for_extracting_number_of_views_and_replies, no_of_views_and_replies_raw)
		no_of_views = no_of_views_and_replies_in_list[0]
		no_of_replies = no_of_views_and_replies_in_list[1]
		result['no_of_views'] = int(no_of_views)
		result['no_of_replies'] = int(no_of_replies)

		try:
			topic_summary_raw_fragmentized = result_raw.find_all('p',class_ = False)[0].contents
			topic_summary = ''
			for fragment in topic_summary_raw_fragmentized:
				current_part_of_summary = fragment.string	
				topic_summary = topic_summary + current_part_of_summary
			topic_summary_without_line_break = topic_summary.replace('\r\n',' ')
			result['topic_summary'] = topic_summary_without_line_break
		except:
			result['topic_summary'] = ''

		publish_time = unicode(result_raw.find_all('p',class_ = False)[1].span.contents[0])
		result['publish_time'] = publish_time

		author = unicode(result_raw.find_all('p',class_ = False)[1].find_all('a', class_=False)[0].contents[0])
		result['author'] = author

		section = unicode(result_raw.find_all('p',class_ = False)[1].find_all('a', class_='xi1')[0].contents[0])
		result['section'] = plugin_sectionname2number.sectionname2number_unicode(sectionname = section)

		results.append(result)

	# Parse the Link of other Pages (searchid)
	search_id = '-1'
	links_attached = soup.find_all('div', class_ = 'pg')
	if len(links_attached) != 0:
		link_attached_raw = links_attached[0].a
		link_attached = link_attached_raw['href']

		search_ids_raw = re.findall(re_for_extracting_search_id, link_attached)
		search_id_raw = search_ids_raw[0]
		search_id_as_string = str(search_id_raw)
		search_id_components = search_id_as_string.split('=')
		search_id = search_id_components[1]

	return (number_of_results, results, search_id)