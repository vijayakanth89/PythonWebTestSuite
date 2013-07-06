
__author__ = "Harikrishnan R"
__copyright__ = "Copyright 2011, The MSF TestSuite Project"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Harikrishnan R"
__email__ = "harikrishnan@inxsasia.com"
__status__ = "Development"


d = {}

def load():
		for line in open("file"):
			if len(line.strip()) > 9:
				d[line[:3]] = line.strip()	

def get_responses():
		return d
						
def main():
		load()
		print get_responses()
						
if __name__ == '__main__':
	main()
