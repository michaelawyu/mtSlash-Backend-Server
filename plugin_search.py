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



def generate_json(parsed_html_data):
	#Implement the Code Here