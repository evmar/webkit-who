#!/usr/bin/python

import re
import subprocess
import operator

commit_re = re.compile('^commit ')
author_re = re.compile('^Author: (\S+)')
date_re = re.compile('^Date:\s+(\S+)')
changelog_re = re.compile('^    \d\d\d\d-\d\d-\d\d  .+?  <(.+?)>')

counts = {}

log = subprocess.Popen(['git', 'log', '--date=short', '--since=6 months ago'],
                       stdout=subprocess.PIPE)
n = 0
for line in log.stdout.xreadlines():
    if commit_re.match(line):
        if n > 0:
            if '@' not in author:
                print 'XXX', author
            counts[author] = counts.get(author, 0) + 1
            print author, date
            print
        author = None
        date = None
        n += 1
        continue
    match = author_re.match(line)
    if match:
        author = match.group(1)
        print author
        continue
    match = date_re.match(line)
    if match:
        date = match.group(1)
        continue
    match = changelog_re.match(line)
    if match:
        author = match.group(1)
        print 'CL', author
        continue

domain_companies = {
    'chromium.org': 'google',
    'google.com': 'google',
    'apple.com': 'apple',
    'igalia.com': 'igalia',
    'nokia.com': 'nokia',
    'torchmobile.com.cn': 'torch mobile',
    'torchmobile.com': 'torch mobile',
    'rim.com': 'rim',
    'gnome.org': 'gnome',
}

other_google = [
    'kinuko@chromium.com',
    'eric@webkit.org',
    'jens@mooseyard.com',
    'rniwa@webkit.org',
    'antonm@chromium',
    'shinichiro.hamaji@gmail.com',
    'finnur.webkit@gmail.com',
    'yaar@chromium.src',
    'abarth@webkit.org',
    'abarth',
    'joel@jms.id.au',
]

other_apple = [
    'sam@webkit.org',
]

other_gnome = [
    'kov@webkit.org',
    'otte@webkit.org',
    'gustavo.noronha@collabora.co.uk',
    'christian@twotoasts.de',
    'xan@webkit.org',
    'jmalonzo@webkit.org',
]

other_qt = [
    'ariya.hidayat@gmail.com',
    'ariya@webkit.org',
    'hausmann@webkit.org',
    'vestbo@webkit.org',
]

people_companies = {
    'mike@belshe.com': 'google',
    'martin.james.robinson@gmail.com': 'appcelerator',
}

print counts
companies = {}
for email, count in counts.iteritems():
    company = None
    user = domain = None
    if '@' in email:
        user, domain = email.split('@')
    if domain and domain in domain_companies:
        company = domain_companies[domain]
    elif domain and domain.endswith('google.com'):
        company = 'google'
    elif email in people_companies:
        company = people_companies[email]
    elif email in other_google:
        company = 'google'
    elif email in other_apple:
        company = 'apple'
    elif email in other_gnome:
        company = 'gnome'
    elif email in other_qt:
        company = 'qt'

    if not company:
        print 'unknown:', email
        company = 'unknown'

    companies[company] = companies.get(company, 0) + count


for company, count in sorted(companies.iteritems(), key=operator.itemgetter(1),
                             reverse=True):
    print '%s: %d' % (company, count)

