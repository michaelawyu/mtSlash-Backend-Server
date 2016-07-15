import re

def get_res():
	res = {}
	
	re_for_extracting_number_of_results = re.compile('[0-9]+')
	re_for_extracting_number_of_views_and_replies = re_for_extracting_number_of_results
	
	res['extracting_number_of_results'] = re_for_extracting_number_of_results
	res['extracting_number_of_views_and_replies'] = re_for_extracting_number_of_views_and_replies
	
	return res