
import uuid
import time
from datetime import datetime

__author__ = "Harikrishnan R"
__copyright__ = "Copyright 2011, The MSF TestSuite Project"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Harikrishnan R"
__email__ = "harikrishnan@inxsasia.com"
__status__ = "Development"


import re
def validate(request):
	"""
	This function checks the validity of the MSF request. The MSF Request
	format is REQUEST_CODE <PARAMS>##ECHO-PARAMS##. For example
	800 <app_id=?,RELEASE_MODE=production>##ROUTER=KIMENG,
	CLIENT_TYPE=ANDROID## . Function will return an empty list if the request
	is invalid or return REQUEST_CODE, PARAMS, ECHO_PARAMS as a list.
	"""
	matches = re.findall( "\d\d\d.*<.*>##.*##" , request ) ;
	parser = []
	if matches:
		req = matches[0]
		parser.append(re.findall("\d\d\d", req )[0])
		parser.append(re.findall("<.*>", req )[0])
		parser.append(re.findall("##.*##", req ) [0])

	print parser
	return parser

def generateAppId():
#	return str(uuid.uuid1())
	return str(time.time())

if __name__ == '__main__':
	pass
