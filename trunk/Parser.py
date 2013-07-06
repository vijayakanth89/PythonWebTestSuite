
__author__ = "Harikrishnan R"
__copyright__ = "Copyright 2011, The MSF TestSuite Project"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Harikrishnan R"
__email__ = "harikrishnan@inxsasia.com"
__status__ = "Development"

def parse_800_params(params):
		d = {}
		for elem in params.split('|'):
				elem = elem.split('=')
				if len(elem) == 2 and elem[0].strip() != '' \
							  and elem[1].strip() != '':
					d[elem[0].strip().upper()] = elem[1].strip()

		return d

def parse_echo_params(echo_params):
		d = {}
		for elem in echo_params.split(','):
				elem = elem.split('=')
				if len(elem) == 2 and elem[0].strip() != '' \
							  and elem[1].strip() != '':
					d[elem[0].strip().upper()] = elem[1].strip()

		return d

if __name__ == '__main__':
	print parse_800_params("app_id=asdasd,RELEASE_MODE=DEVELOPMENT   ")
