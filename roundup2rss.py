#!/usr/bin/python

######################################################################
#
# Quick and dirty script to generate an RSS feed for the daily roundup
# posts on Whirlpool.net.au.  Just run it and pipe to a target file.
#
# Copyright 2009: Steve Smith (aka Tarka): tarkasteve@gmail.com
# Redistribution of this file is permitted under the terms of the GNU
# Public License (GPL) version 2.
#
######################################################################

import urllib2, re, sys, time

url = 'http://whirlpool.net.au/'

startre = re.compile('<div class="article roundup index">')
datere = re.compile("<h3>(2\d\d\d-\w+-\d+)</h3>")
titlere = re.compile("<h1>([^<]+)</h1>")
endre = re.compile("</div>")


########## RSS support ##########

def fetch(url):
    try:
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla")
        fd = urllib2.build_opener().open(req)
    except IOError, e:
        print "failed:",e
        sys.exit()
    return fd


def writeheader(title):
    print '<?xml version="1.0" encoding="ISO-8859-1"?>\n'
    print '<rss version="2.0">'
    print ' <channel>'
    print '   <title>%s</title>' % title
    print '   <description>%s</description>' % title
    print '   <language>en-AU</language>'

def writeentry(e):
    print "   <item>"
    print "     <title><![CDATA[ %s: %s ]]></title>" % (e['date'], e['title'])
    print "     <guid>%s</guid>" % e['date']
    print "     <description><![CDATA[%s]]></description>" % e['text']
    print "   </item>"

def writefooter():
    print ' </channel>'
    print '</rss>'


########################################

state = "end"
entry = None

fd = fetch(url)

writeheader("Whirlpool Daily Roundup")

for line in fd:
    match = startre.search(line)
    if match:
        state = "accum"
        entry = {'text':'',
                 'date':None,
                 'title':None}
        continue

    if state == "end":
        continue

    match = datere.search(line)
    if match:
        entry['date'] = match.group(1)
        continue

    match = titlere.search(line)
    if match:
        entry['title'] = match.group(1)
        continue

    match = endre.search(line)
    if match:
        writeentry(entry)
        state = "end"
        entry = None

    if state == "accum":
        entry['text'] += line
        
writefooter()
