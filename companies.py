#!/usr/bin/python

import webkit
import datetime
from collections import defaultdict

start = None
end = None
data = defaultdict(lambda: defaultdict(lambda: 0))
for date, author in webkit.parse_log(since='3 years ago'):
    author = webkit.canonicalize_email(author)
    company = webkit.classify_email(author)
    date = datetime.date(*map(int, date.split('-')))
    if start is None or date < start:
        start = date
    if end is None or date > end:
        end = date
    data[date][company] += 1

show_companies = set(['google', 'apple', 'nokia', 'rim'])
print "Date," + ','.join(show_companies) + ",other"
date = start
while date <= end:
    row = [date.strftime("%Y%m%d")]
    for company in show_companies:
        row.append(data[date][company])
    misc = 0
    for company in data[date].keys():
        if company not in show_companies:
            misc += data[date][company]
    row.append(misc)
    print ",".join(map(str, row))

    date += datetime.timedelta(days=1)
