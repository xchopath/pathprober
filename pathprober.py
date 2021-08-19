#!/usr/bin/env python3
# PathProber - Probe and discover HTTP pathname using brute-force methodology and filtered by specific word or 2 words at once

import datetime
import requests
import json
import os
import argparse
import re
import urllib3
import sys
from urllib.parse import urlparse
import validators
import threading

urllib3.disable_warnings()

print("""
 ___  ____ ___ _  _ ___  ____ ____ ___  ____ ____ 
 |__] |__|  |  |__| |__] |__/ |  | |__] |___ |__/ 
 |    |  |  |  |  | |    |  \ |__| |__] |___ |  \ 
       Probe HTTP pathname filtered by words      
""")

### ARGS PARSER
parser = argparse.ArgumentParser(description='PathProber - Probe and discover HTTP pathname using brute-force methodology and filtered by specific word or 2 words at once')
parser.add_argument('-t', metavar='https://example.com', type=str, help='Single website target')
parser.add_argument('-p', metavar='pathname', type=str, help='Single pathname')
parser.add_argument('-T', metavar='target.txt', type=str, help='Multiple target separated by newline')
parser.add_argument('-P', metavar='path.txt', type=str, help='Multiple pathname separated by newline')
parser.add_argument('-w', metavar='Word', type=str, help='A word that you want to find in a path')
parser.add_argument('-w2', metavar='Word', type=str, help='A second word that you want to find in a path')
parser.add_argument('-o', metavar='output.txt', type=str, help='Save the results to file')
args = parser.parse_args()

### ARGS TO VARIABLE
target = args.t
pathname = args.p
multi_target_file = args.T
multi_pathname_file = args.P
word = args.w
word2 = args.w2
file_output = args.o

def CheckIfMatch(full_response, target_full, word, word2):
	try:
		if not word2 == None:
			if word in full_response and word2 in full_response:
				result = {'status': 'found', 'target_full': target_full, 'filter': '"' + word + '" AND "' + word2 + '"'}
			elif word2 in full_response:
				result = {'status': 'found', 'target_full': target_full, 'filter': '"' + word2 + '"'}
			elif word in full_response:
				result = {'status': 'found', 'target_full': target_full, 'filter': '"' + word + '"'}
			else:
				result = {'status': 'not_found', 'target_full': target_full, 'filter': None}
		elif word in full_response:
			result = {'status': 'found', 'target_full': target_full, 'filter': '"' + word + '"'}
		else:
			result = {'status': 'not_found', 'target_full': target_full, 'filter': None}
		return result
	except Exception as error:
		return None

def ParsedTarget(target, pathname):
	try:
		if not target.startswith("http://") and not target.startswith("https://"):
			target = 'http://' + target
		else:
			target = target
		url_parse = urlparse(target)
		target = url_parse.scheme + '://' + url_parse.netloc + '/' + url_parse.path
		target_full = re.sub('/+', '/', target + '/' + pathname)
		target_full = re.sub(':/', '://', target_full)
		return '{}'.format(str(target_full))
	except Exception as error:
		return None

def HeaderBodyMerger(headers, body):
	try:
		full_response = []
		for header in headers:
			full_response.append(str(header) + ': ' + str(headers[header]))
		full_response = '\n'.join([stings for stings in full_response])
		full_response = full_response + '\n\n' + body 
		return '{}'.format(str(full_response))
	except:
		return None

def GetFullResponse(url):
	try:
		req = requests.get('{}'.format(url), allow_redirects=True, verify=False, timeout=10)
		merge_response = []
		for redirect_response in req.history:
			get_redirect_response = HeaderBodyMerger(redirect_response.headers, redirect_response.text)
			merge_response.append(get_redirect_response)
		merge_response.append(HeaderBodyMerger(req.headers, req.text))
		merged_response = ''.join([stings for stings in merge_response])
		return '{}'.format(str(merged_response))
	except:
		return None

def SaveToFile(output, file_output):
	try:
		if not file_output == None:
			open_filename = open(file_output, 'a')
			open_filename.write(output + '\n')
			open_filename.close()
	except Exception as error:
		print('ERR: ({}) {}'.format(type(error).__name__, target_full))

def Workers(target, pathname, word, word2):
	try:
		target_full = ParsedTarget(target, pathname)
		full_response = GetFullResponse(target_full)
		result = CheckIfMatch(full_response, target_full, word, word2)
		if result['status'] == 'found':
			print("FOUND! {} (filter: {})".format(result['target_full'], result['filter']))
			SaveToFile(result['target_full'] + ' ({})'.format(result['filter']), file_output)
		else:
			print("INFO: {} not found".format(result['target_full']))
	except Exception as error:
		return None

### ARGS VALIDATOR
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if not target == None and not multi_target_file == None:
	print("ERR: -t and -T cannot be used in the same time")
	exit()
elif not pathname == None and not multi_pathname_file == None:
	print("ERR: -p and -P cannot be used in the same time")
	exit()
elif target == None and multi_target_file == None:
	print("ERR: Please add target")
	print("HINT: Use parameter -t or -T")
	exit()
elif pathname == None and multi_pathname_file == None:
	print("ERR: Please add target")
	print("HINT: Use parameter -p or -P")
	exit()
elif not multi_target_file == None and not os.path.isfile(multi_target_file):
	print("ERR: Could not find multi-target file")
	exit()
elif not multi_pathname_file == None and not os.path.isfile(multi_pathname_file):
	print("ERR: Could not find multi-pathname file")
	exit()
elif word == None:
	print("ERR: Please add specific word")
	print("HINT: Use parameter -w")
	exit()

### PRINT WORD FILTERS
if not word == None and not word2 == None:
	print("INFO: Word filters \"{}\" and \"{}\"".format(word, word2))
elif not word == None:
	print("INFO: Word filter \"{}\"".format(word))

### MULTIPLE TARGET AND SINGLE PATHNAME
if not multi_target_file == None and not pathname == None:
	try:
		open_multi_target_file = open(multi_target_file, "r")
		workers = [threading.Thread(target=Workers, args=(target_row.split()[0], pathname, word, word2,)) for target_row in open_multi_target_file]
		for thread in workers:
		    thread.start()
		for thread in workers:
		    thread.join()
		open_multi_target_file.close()
	except Exception as error:
		print('ERR: {} on line {}'.format(type(error).__name__, sys.exc_info()[-1].tb_lineno))

### MULTIPLE TARGET AND MULTIPLE PATHNAME
elif not multi_target_file == None and not multi_pathname_file == None:
	try:
		open_multi_target_file = open(multi_target_file, "r")
		for target_row in open_multi_target_file:
			target = target_row.split()[0]
			open_multi_pathname_file = open(multi_pathname_file, "r")
			workers = [threading.Thread(target=Workers, args=(target, pathname_row.split()[0], word, word2,)) for pathname_row in open_multi_pathname_file]
			for thread in workers:
			    thread.start()
			for thread in workers:
			    thread.join()
			open_multi_pathname_file.close()
		open_multi_target_file.close()
	except Exception as error:
		print('ERR: {} on line {}'.format(type(error).__name__, sys.exc_info()[-1].tb_lineno))

### SINGLE TARGET AND SINGLE PATHNAME
elif not target == None and not pathname == None:
	try:
		Workers(target, pathname, word, word2)
	except Exception as error:
		print('ERR: {} on line {}'.format(type(error).__name__, sys.exc_info()[-1].tb_lineno))

### SINGLE TARGET AND MULTIPLE PATHNAME
elif not target == None and not multi_pathname_file == None:
	try:
		open_multi_pathname_file = open(multi_pathname_file, "r")
		workers = [threading.Thread(target=Workers, args=(target, pathname_row.split()[0], word, word2,)) for pathname_row in open_multi_pathname_file]
		for thread in workers:
		    thread.start()
		for thread in workers:
		    thread.join()
		open_multi_pathname_file.close()
	except Exception as error:
		print('ERR: {} on line {}'.format(type(error).__name__, sys.exc_info()[-1].tb_lineno))
