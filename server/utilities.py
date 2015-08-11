#!/usr/bin/python
from subprocess import call
import requests

def call_optless_command(command):
	result = ''
        try:
    	    call([command], shell=True)
        except:
        	result += "command not run"
        else:
		result += "ran "+command
	return result

def call_command(command, flags):
	result = ''
	try:
		call([command, flags])
	except:
		result += "command not run"
	else:
		result += "ran "+command+" "+flags
	return result

def read_from_file(file):
	result = ''
	try:
		with open(file, "rw") as myfile:
			result += myfile.read()
	except IOError:
		return result
	return result

def write_to_file(data):
	with open("log.txt", "w+") as myfile:
		myfile.write(data)
	return ''

def check_module(module):
    if module_exists(module):
        message = module+" is  installed "
        return message
    else:
        message = module+" is not installed "
        return message

def module_exists(module):
    try:
        __import__(module)
    except:
        return False
    else:
        return True

def get_status_and_url(page, ip):
    URL = 'http://'+ip
    session = requests.session()
    if page is not None and page[:7] != 'http://':
        print(URL+page)
        r = session.get(URL+page)
        result = str(r.text)
        #result = str(r.status_code)+": "+URL+page
        return result


#
#
#
#
