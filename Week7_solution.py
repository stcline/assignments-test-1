#!/usr/bin/env python3

# Import modules
import re
import csv
import operator
import sys

#Create empty dictionaries
per_user = {}
errors = {}

#Create variables for filepaths
logfile = 'syslog.log'
f = open(logfile, 'r')

#Create variables for files to be created
error_file = 'error_message.csv'
userfile = 'user_statistics.csv'

#Iterate over lines of log file, create a regex search to identify errors and info with user
#Build dictionaries from these results
for log in f:
    #look for the note, error and user see: https://regex101.com/r/uTDEft/1
    result = re.search(r"ticky: ([\w+]*):? ([\w' ]*) [\[[0-9#]*\]?]? ?\((.*)\)$", log)
    #Check for empty dictionary key
    if result.group(2) not in errors.keys():
        errors[result.group(2)] = 0
    #add to the value of key
    errors[result.group(2)] +=1
    #Check for username in dictionary keys
    if result.group(3) not in per_user.keys():
        per_user[result.group(3)] = {}
        per_user[result.group(3)]["INFO"] = 0
        per_user[result.group(3)]["ERROR"] = 0
    #Add 1 to "INFO" key if found in parsed result
    if result.group(1) == "INFO":
        per_user[result.group(3)]["INFO"] +=1
    #Add 1 to "ERROR" key if found in parsed result
    if result.group(1) == "ERROR":
        if result.group(2) not in errors.keys():
            errors[result.group(2)] = 0
        errors[result.group(2)] += 1

#sort errors and user stats
errors = sorted(errors.items(), key= operator.itemgetter(1), reverse= True)
per_user = sorted(per_user.items())[0:8]

f.close()

#create headers for error file
errors.insert(0, ('Error', 'Count'))

#Iterate over errors to create error_file.csv
f=open(error_file, 'w')
for error in errors:
    a,b = error
    f.write(str(a)+','+str(b)+'\n')
f.close()

#Iterate over errors to create userfile.csv
f=open(userfile, 'w')
f.write("Username,INFO,ERROR\n")
for stats in per_user:
    a,b = stats
    f.write(str(a)+',' +str(b["INFO"])+',' +str(b["ERROR"])+'\n')
f.close()
