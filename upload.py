#!/usr/bin/python

import os
import commands
import cgi, cgitb

cgitb.enable()
print "Content-Type: text/html"
print
print 'start!'
form = cgi.FieldStorage()
if filedata.file: # field really is an upload
    with file("Beautiful.mp3", 'w') as outfile:
        outfile.write(filedata.file.read())
filedata = form['upload']