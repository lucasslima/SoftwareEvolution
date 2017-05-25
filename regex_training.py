import os
import re
import sys
import subprocess
import shutil
import datetime
from datetime import datetime

regex = r"(\d\d\d\d\-\d\d\-\d\d\s\d\d:\d\d:\d\d)|(:?tag: release-\d(:?[._-]\d+)+(:?-rc\d)?)"

test_str = ("2015-03-19 16:15:13 -0700 tag: release-2.0.0-rc0\n"
	"2014-01-14 19:06:11 -0800 tag: release-1.4.3-rc0, tag: release-1.4.3, origin/branch-1.4.3\n")
# get all tags from the git repository in order and with date
git_log_result = subprocess.check_output(["git","--no-pager", "log", "--tags", "--date-order",  "--reverse",  "--simplify-by-decoration", "--pretty=%ai %D"])

# # get directory name and project name to create folders dynamically
directory = subprocess.check_output(["pwd"]).split()[0]
project_name = directory.decode('utf-8').split('/')[-1]

# # create folder to keep all the tags
#subprocess.call(["mkdir", "../"+project_name+"_tags"])

# #regex to eliminate folders that is not relevant for the analysis, like third party libraries and invisible files
file_regex = '\..*|sonar\.py' 
directory_regex = '\..*|vendor|thirdparty|(:?ex|s)amples|doc(:?s|uments)|bin|node'
tags_regex = r"(\d\d\d\d\-\d\d\-\d\d\s\d\d:\d\d:\d\d)|tag: (:?release-([^,]*))"
for line in git_log_result.decode('utf-8').split('\n'):
  #matches = re.finditer(tags_regex, line, re.IGNORECASE)
  if re.search(tags_regex, line) is not None:
    m = re.findall(tags_regex, line)
    print (m)
        # has match fot tag and date (merge has date but not tag)
  #for matchNum, match in enumerate(matches):
      #matchNum = matchNum + 1
      
      #print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
      #for groupNum in range(0, len(match.groups())):
          #groupNum = groupNum + 1
          
          #print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
