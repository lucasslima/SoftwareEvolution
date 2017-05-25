import os
import re
import sys
import subprocess
import shutil
import datetime
from datetime import datetime

# get all tags from the git repository in order and with date
git_log_result = subprocess.check_output(["git", "log", "--tags", "--date-order",  "--reverse",  "--simplify-by-decoration", "--pretty=%ai %d"])

# get directory name and project name to create folders dynamically
directory = subprocess.check_output(["pwd"]).split()[0]
project_name = directory.decode('utf-8').split('/')[-1]


# #regex to eliminate folders that is not relevant for the analysis, like third party libraries and invisible files
file_regex = '\..*|sonar\.py'
directory_regex = '\..*|vendor|thirdparty|(:?ex|s)amples|doc(:?s|uments)|bin|node'
# Software version regex. This will match any tag with 0.0.0 or 0_0_0 format
tags_regex = r"(\d\d\d\d\-\d\d\-\d\d\s\d\d:\d\d:\d\d)|(tag: .*\d[.-]\d(?:[.-]\d)?)"

counter = 0
last_tag = None
#last_tag = "4.0.0"
for line in git_log_result.decode('utf-8').split('\n'):
    # for each line has matches
    if re.search(tags_regex, line) is not None:
        m = re.findall(tags_regex, line)
        # has match fot tag and date (merge has date but not tag)
        if len(m) == 2:
            # get result from the first tuple, first item (date)
            tag_date = m[0][0].split(' ')[0]
            # get result from the second tuple, second item (tag)
            tag = m[1][1].split(' ')[1]
            tag_number = re.findall(r"\d[.-]\d(?:[.-]\d)?", tag)
            if last_tag is not None:
                if  tag_number <= last_tag:
                  continue
            last_tag = tag_number
            print(tag)
            # checkout into each of them
            subprocess.call(["git", "checkout" , tag])

            # create sonar-project.properties file
            f = open("sonar-project.properties", "w")
            f.write("# Required metadata\n")

            f.write("sonar.projectBaseDir=" +os.getcwd()+"\n")
            f.write("sonar.projectDate=" + tag_date + "\n")

            f.write("sonar.projectKey=" +project_name+ "\n")
            f.write("sonar.projectName=" +project_name+ "\n")
            f.write("sonar.projectVersion=" +tag+ "\n")
            f.write("# Comma-separated paths to directories with sources (required)\n")
            f.write("sonar.sources=. \n")

            # f.write("sonar.tests=" +project_name+ "\n")
            f.write("# Language\n")

            f.write("# Encoding of sources files\n")
            f.write("sonar.sourceEncoding=UTF-8\n")
            f.close()

            subprocess.call(["sonar-scanner"])
            counter = counter + 1

            #print " # checkout: " + str(tag)
