sectionnames = [
	# Check-In
	u'\u65b0\u4eba\u7b7e\u5230',
	# Secret Gifts in Holiday Season
	u'\u65b0\u5e74\u795e\u79d8\u793c\u7269\u5b63 Secret Gifts in Holiday Season',
	# Gifts in the Past
	u'\u5386\u5e74\u793c\u7269\u50a8\u85cf\u5904',
	# MOVIE FANFIC
	u'MOVIE FANFIC',
	# MOVIE FANFIC - Avengers
	u'\u590d\u4ec7\u8005\u8054\u76df\u4e13\u533a',
	# MOVIE FANFIC / TV FANFIC - Popular Fandoms
	u'\u70ed\u95e8\u540c\u4eba\u533a',
	# TV FANFIC
	u'TV FANFIC',
	# TV FANFIC - Sherlock
	u'\u798f\u5c14\u6469\u65af\u4e13\u533a',
	# FANART
	u'FANART',
	# FANVID
	u'FANVID',
	# FANBOOK
	u'FANBOOK',
	# Flea Market
	u'\u6c42\u672c\u8f49\u672c',
	# DISCUSSION
	u'DISCUSSION',
	# Song
	u'Song',
	# Help Center
	u'Help Center'
]
sectionunmbers = [
	73, 74, 78, 2, 6, 84, 34, 83, 63, 64, 68, 69, 70, 71, 72
]
sectionname2number_unicode = {}

for i in range(0, len(sectionnames)):
	sectionname2number_unicode[sectionnames[i]] = sectionunmbers[i]

def sectionname2number_unicode(sectionname):
	try:
		return sectionname2number_unicode[sectionname]
	except:
		return 0