'''
Created on Nov 8, 2016
@author: team 4
'''
from datetime import datetime
import os
import sys


def getLog(log_dir, runner_script_name):
    """
    Creates 'logs' directory, if it doesn't exist,
    creates or opens a log file in 'logs' directory.
    """
    try:
        # if logs directory(!) doesn't exist, create it
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        # open log file with prefix and timestamp (platform independent) in Append mode
        log = open(os.path.join(log_dir, runner_script_name+"_" +
                                getCurTime("%Y%m%d_%H-%M") + ".log"), "a")
        return log
    except IOError as e:
        print "log file: I/O error({0}): {1}".format(e.errno, e.strerror)
        return -1
    except:
        print "log file: Unexpected error:", sys.exc_info()[0]
        # return -1 in case of exception
        return -1

def qaPrint(log, message):
    """
    Prints 'timestamp + message' to console and writes it to the log file
    """
    # current date and time as string + message. example: [Oct 25 01:52:33.000001] TC1 - Passed
    log_message = getCurTime("[%b %d %H:%M:%S.%f]") + " " + message
    # prints log_message
    print log_message
    # writes message to a log file
    log.write(log_message + "\n")


def getCurTime(date_time_format):
    """
    Returns current date_time as a string formatted according to date_time_format
    """
    date_time = datetime.now().strftime(date_time_format)
    return date_time

def getLocalEnv(properties_file_name):
    '''Reads the content of the file and creates a dictionary,
    returns created dictionary or -1 on error'''
    my_props = {}
    try:
        with open(properties_file_name, 'r') as f:
            for line in f:
                line = line.strip() #removes whitespace and '\n' chars
                if "=" not in line: continue #skips blanks and comments w/o =
                if line.startswith("#"): continue #skips comments which contain =
                k, v = line.split("=", 1)
                if k == "" or v == "":
                    print "invalid properties"
                    f.close()
                    return -1
                my_props[k] = v
        f.close()
        if len(my_props) == 0:
            print "empty properties file"
            return -1
    except IOError as e:
        print properties_file_name+": I/O error({0}): {1}".format(e.errno, e.strerror)
        return -1
    except: #handle other exceptions such as attribute errors
        print properties_file_name+": Unexpected error:", sys.exc_info()[0]
        return -1
    return my_props


def getTestCases(testrun_id, properties_dict, log_file):
    """Creates test cases dictionary using file testrun_id.txt
    defines structure with tc_key_names and tc_key_types from local.properties
    Returns created dictionary or -1 on error"""

    #key_names is 'tc_key_names' ,key_types is 'tc_key_types' from local.properties
    #example:
    #key_names = "tcid|rest_URL|HTTP_method|HTTP_RC_desired|param_list"
    #key_types = "str|str|str|int|list"
    if ('tc_key_names' not in properties_dict.keys()) or ('tc_key_types' not in properties_dict.keys()):
        qaPrint(log_file, "invalid properties for test case keys/types, check keys 'tc_key_names', 'tc_key_types'")
        return -1
    else:
        try:
            key_list = properties_dict["tc_key_names"].split("|")
            key_types = properties_dict["tc_key_types"].split("|")
        except:
            qaPrint(log_file, str(sys.exc_info()[0]))
            return -1
    if len(key_list) <> len(key_types):
        qaPrint(log_file, "invalid properties for test case keys/types, check number of values")
        return -1

    tc_file_name = str(testrun_id)+".txt"
    try:
        tc_file = open(tc_file_name, "r")
        # create nested dictionary
        tc_dict = {}
        for line in tc_file:
            line = line.strip()
            splitLine = line.split("|")
            if len(splitLine) <> len(key_list):
                qaPrint(log_file, "number of test cases in file mismatches properties")
                return -1
            tc_values_from_file = {}
            for i in range(1, len(key_list)):
                if key_types[i] == 'int': # response code: cast to int
                    value_to_dict = int(splitLine[i])
                elif key_types[i] == 'list': # param_list: string to list
                    value_to_dict = splitLine[i].split(",")
                else:  # str
                    value_to_dict = splitLine[i]
                tc_values_from_file[key_list[i]] = value_to_dict
            tc_dict[splitLine[0]] = tc_values_from_file
        tc_file.close()
    except IOError as e:
        qaPrint(log_file, tc_file_name +": I/O error({0}): {1}".format(e.errno, e.strerror))
        return -1
    except:
        qaPrint(log_file, tc_file_name +": Unexpected error:"+str(sys.exc_info()[0]))
        return -1
    return tc_dict

def valid_search_RegEx(arg_list, reg_str):
    '''Scan through list 'arg_list' looking for a match to the pattern, returning a match object,
    or -1 if list is empty or no match was found'''
    import re
    if not arg_list:
        return -1
    else:
        for el in arg_list:
            matches = re.search(reg_str, el, re.IGNORECASE)
            if matches:
                return matches.group(1)
        return -1
        