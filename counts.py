#!/usr/bin/python

import operator
import webkit

counts = {}
for date, author in webkit.parse_log():
    author = webkit.canonicalize_email(author)
    counts[author] = counts.get(author, 0) + 1

companies = {}
unknown = {}
for email, count in counts.iteritems():
    company = webkit.classify_email(email)
    companies[company] = companies.get(company, 0) + count
    if company == 'unknown':
        unknown[email] = count
    elif company == 'misc':
        unknown['*' + email] = count


if unknown:
    print ("unclassified (star denotes \"commits examined, and their "
           "backer is a minor contributor\"):")
    for email, count in sorted(unknown.iteritems(), key=operator.itemgetter(1),
                               reverse=True):
        print '  %s (%d)' % (email, count)


for company, count in sorted(companies.iteritems(), key=operator.itemgetter(1),
                             reverse=True):
    print '%s: %d' % (company, count)

