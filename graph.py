#!/usr/bin/python

import webkit
import pylab
import matplotlib.pyplot as plot
import matplotlib.dates as dates
import datetime
import numpy
import sys

def load_from_git():
    data = []
    for date, author in webkit.parse_log(since='2 years ago'):
        author = webkit.canonicalize_email(author)
        company = webkit.classify_email(author)
        date = datetime.date(*map(int, date.split('-')))
        data.append((date, company))
    data.reverse()
    return data

def load_from_file():
    data = []
    for line in open('dates').readlines():
        date, company = line.strip().split(' ', 1)
        date = datetime.date(*map(int, date.split('-')))
        data.append((date, company))
    return data

def lin_smooth(array, window=7):
    out = numpy.zeros(len(array))
    avg = sum(array[0:window])
    for i in range(window, len(array)):
        avg += array[i]
        avg -= array[i - window]
        out[i] = avg / window
    return out

def gauss(window):
    gauss = numpy.exp(-numpy.arange(-window+1, window)**2/(2*float(window)))
    return gauss / gauss.sum()

def gauss_smooth(data, window=14):
    g = gauss(window)
    return numpy.convolve(data, g, mode='same')

data = load_from_git()

print data[0], data[-1]
start = pylab.date2num(data[0][0])
end = pylab.date2num(data[-1][0])

companies = set(['google', 'apple', 'other'])
commits = {}
for company in companies:
    commits[company] = numpy.zeros(end - start + 1)

for date, who in data:
    date = pylab.date2num(date)
    if who not in companies:
        who = 'other'
    commits[who][date - start] += 1

commits['google'] += commits['apple']
commits['other'] += commits['google']

smooth = lambda d: gauss_smooth(d, window=30)

fig = plot.figure()
ax = fig.add_subplot(111)
ax.plot_date(range(start, end + 1), smooth(commits['apple']), '-')
ax.plot_date(range(start, end + 1), smooth(commits['google']), '-')
ax.plot_date(range(start, end + 1), smooth(commits['other']), '-')
ax.xaxis.set_major_locator(dates.MonthLocator(range(1,13), bymonthday=1, interval=3))
ax.xaxis.set_minor_locator(dates.MonthLocator(range(1,13), bymonthday=1, interval=1))
fig.autofmt_xdate()
pylab.savefig('graph.png')
