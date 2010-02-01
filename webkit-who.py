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

# See:  http://trac.webkit.org/wiki/WebKit%20Team

domain_companies = {
    'chromium.org': 'google',
    'google.com': 'google',
    'apple.com': 'apple',
    'igalia.com': 'igalia',
    'nokia.com': 'nokia',
    'torchmobile.com.cn': 'torch mobile',
    'torchmobile.com': 'torch mobile',
    'rim.com': 'rim',
}

other = {
    'google': [
        'abarth',
        'abarth@webkit.org',
        'antonm@chromium',
        'christian.plesner.hansen@gmail.com',  # v8
        'eric@webkit.org',
        'finnur.webkit@gmail.com',
        'jens@mooseyard.com',
        'joel@jms.id.au',  # intern
        'kinuko@chromium.com',
        'rniwa@webkit.org',  # intern
        'shinichiro.hamaji@gmail.com',
        'yaar@chromium.src',
    ],

    'apple': [
        'sam@webkit.org',
    ],

    'redhat': [
        'danw@gnome.org',
        'otte@webkit.org',
    ],

    'nokia': [
        'hausmann@webkit.org',
        'kenneth@webkit.org',
        'tonikitoo@webkit.org',
        'vestbo@webkit.org',
        'faw217@gmail.com',  # A guess, based on commits.

        'girish@forwardbias.in',  # Appears to be consulting for Qt = Nokia(?).
    ],

    'rim': [
        'dbates@webkit.org',
        'zimmermann@webkit.org',
    ],

    'misc (e.g. open source)': [
        'becsi.andras@stud.u-szeged.hu',
        'bfulgham@webkit.org',  # WinCairo
        'chris.jerdonek@gmail.com',  # Seems to be doing random script cleanups?
        'jmalonzo@webkit.org',  # GTK
        'joanmarie.diggs@gmail.com',  # GTK Accessibility (Sun?)
        'joepeck@webkit.org',   # Inspector.
        'krit@webkit.org',
        'ossy@webkit.org',
        'simon.maxime@gmail.com',  # Haiku
        'skyul@company100.net',  # BREWMP
        'zandobersek@gmail.com',  # GTK
        'zecke@webkit.org',  # GTK+Qt
        'zoltan@webkit.org',
    ]
}

people_companies = {
    'mike@belshe.com': 'google',
    'martin.james.robinson@gmail.com': 'appcelerator',
    'xan@webkit.org': 'igalia',

    'kevino@webkit.org': 'wx',
    'kevino@theollivers.com': 'wx',

    'gustavo.noronha@collabora.co.uk': 'collabora',
    'kov@webkit.org': 'collabora',

    'ariya.hidayat@gmail.com': 'qualcomm',
    'ariya@webkit.org': 'qualcomm',
}

print counts
companies = {}
unknown = {}
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
    else:
        for co, people in other.iteritems():
            if email in people:
                company = co
                break

    if not company:
        unknown[email] = count
        company = 'unknown'

    companies[company] = companies.get(company, 0) + count

for email, count in sorted(unknown.iteritems(), key=operator.itemgetter(1),
                           reverse=True):
    print 'unknown:', email, count


for company, count in sorted(companies.iteritems(), key=operator.itemgetter(1),
                             reverse=True):
    print '%s: %d' % (company, count)

