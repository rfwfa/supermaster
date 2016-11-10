'''
Created on Nov 8, 2016
@author: team 4
'''
from core.rfaUtils import getLog, qaPrint, getLocalEnv, getTestCases, valid_search_RegEx
import sys
def usage(correct_sample):
    print "incorrect usage of parameter, Correct sample is: "+ correct_sample

properties_fname = "local.properties" # hard-coded name
# create dictionary from properties file (local.properties)
env_dict = getLocalEnv(properties_fname)
if env_dict == -1:
    sys.exit("Unable to create dictionary from properties file")

# check if we have property 'log_dir'
if 'log_dir' not in env_dict.keys():
    sys.exit("No 'log_dir' in the properties file. Please check file: "+properties_fname)
# get 'log_dir' value
log_folder = env_dict['log_dir']

# check if we have command-line argument with script name like 'scriptname.py'
# and return name without '.py' if found
regex_pattern = r"\b\/?(\w*)\.py$"
runner_script_name = valid_search_RegEx(sys.argv, regex_pattern)
if runner_script_name == -1:
    usage("path_to_file/file_name.py")
    sys.exit()
# get the log file handle
log = getLog(log_folder, runner_script_name)

# exit if log creation failed
if log == -1:
    sys.exit("Unable to create log file")

message = "It is working, right?"

# call qaPrint to print a message with timestamp and write it to the log file
qaPrint(log, message)
qaPrint(log, "Me like what me see")

# search for command-line argument like '--testrun=[0-10000]'
# if found, return test run id as string
regex_pattern = r"^--testrun=(0|[1-9][0-9]{0,3}|10000)$"
# check if we have valid command line argument
trid_str = valid_search_RegEx(sys.argv, regex_pattern)
if trid_str == -1:
    usage("'--testrun=[0-10000]'")
    sys.exit("Unable to extract test run id from command-line argument")
# cast to int
trid = int(trid_str)

#create test cases dictionary
test_cases = getTestCases(trid, env_dict, log)
if test_cases == -1:
    sys.exit("Unable to get test cases from file with testrun id "+str(trid))
# pretty print (temporary)
#import pprint
#pprint.pprint(test_cases)
#

# close the log file if it open
if not log.closed:
    log.close()
    