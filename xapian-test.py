#!/usr/bin/python
# -*- coding: utf-8 -*-

import xapian
import sys
import apt.cache

cache = apt.cache.Cache()

# db
db = xapian.Database("/var/lib/apt-xapian-index/index")

# stemmer? cazzè?
stemmer = xapian.Stem("english")

terms = []
for word in sys.argv[1:]:
	if word.islower() and word.find("::") != -1:
		# tag
		terms.append("XT"+word)
	else:
		# normal
		word = word.lower()
		terms.append(word)
		stem = stemmer(word)
		if stem != word:
			terms.append("Z"+stem)

query = xapian.Query(xapian.Query.OP_OR, terms)

enquire = xapian.Enquire(db)
enquire.set_query(query)

# Display the top 20 results, sorted by how well they match
matches = enquire.get_mset(0, 20)
print "%i results found." % matches.get_matches_estimated()
print "Results 1-%i:" % matches.size()

for m in matches:
	# /var/lib/apt-xapian-index/README tells us that the Xapian document data
	# is the package name.
	name = m.document.get_data()

	# Get the package record out of the Apt cache, so we can retrieve the short
	# description
	pkg = cache[name]

	# Print the match, together with the short description
	print "%i%% %s - %s" % (m.percent, name, pkg.versions[0].summary)
