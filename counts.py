#!/usr/bin/python

import operator
import webkit

counts = {}
for date, author in webkit.parse_log():
    counts[author] = counts.get(author, 0) + 1

print counts
companies = {}
unknown = {}
for email, count in counts.iteritems():
    company = webkit.classify_email(email)
    companies[company] = companies.get(company, 0) + count
    if company == 'unknown':
        unknown[email] = count


if unknown:
    print 'unclassified:'
    for email, count in sorted(unknown.iteritems(), key=operator.itemgetter(1),
                               reverse=True):
        print '  %s (%d)' % (email, count)


for company, count in sorted(companies.iteritems(), key=operator.itemgetter(1),
                             reverse=True):
    print '%s: %d' % (company, count)

