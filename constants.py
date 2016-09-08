# User Groups with Denied Access
# Group ID 4: Post Function Disabled
# Group ID 5: Access Denied
# Group ID 6: IP Blacklisted
# Group ID 7: Guest
# Group ID 8: Verfication Pending
forbidden_groups = [4, 5, 6, 7, 8]

# Names of Related Database Tables
members_ucenter = 'pre_ucenter_members'
member_discuz = 'pre_common_member'
forum_sections = 'pre_forum_forum'
forum_threads = 'pre_forum_thread'
forum_posts = 'pre_forum_post'

# IDs (FIDs) of Related Forum Sections
# Used when Client Requesting Section Info from Server
# Ordered as Displayed in Webpage
# Secret Gifts in Holiday Season, Movie Fanfic, Movie Fanfic/Avengers, Movie Fanfic/Popular Fandoms, TV Fanfic, TV Fanfic/Sherlock, TV Fanfic/Popular Fandoms, FANART, FANVID, FANBOOK, DISCUSSION, Song, Help Center
related_forum_ids = [41, 2, 37, 38, 36, 50, 49, 42, 43, 44, 45, 46, 47]

# Search URL
SEARCH_URL = 'http://mtslash.org/search.php'
SEARCH_RESULT_URL = 'http://www.mtslash.org/search.php?mod=forum&searchid=%s&orderby=lastpost&ascdesc=desc&searchsubmit=yes&page=%s' 

# Payload for Basic Search
payload_for_basic_search = {}
payload_for_basic_search['formhash'] = 'b6ba6cb8'
payload_for_basic_search['searchsubmit'] = 'yes'
payload_for_basic_search['srchtxt'] = ''