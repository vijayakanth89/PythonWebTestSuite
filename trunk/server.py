#!/usr/bin/python
import re
import cgi 
import time
import sys
import traceback
import os
import logging
import getopt
import urlparse
import yaml
import glob
import simplejson as json
import httplib2
import urllib
import urllib2
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlite_helper import SqliteHelper
from SocketServer import ThreadingMixIn
from string import Template

import RequestUtils
import Parser
from ticker import Ticker

__author__ = "Harikrishnan R"
__copyright__ = "Copyright 2011, The MSF TestSuite Project"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Harikrishnan R"
__email__ = "harikrishnan@inxsasia.com"
__status__ = "Development"


MOBILE_REQUEST = "mobile_request"
UPLOAD_FILE_TAG = "upfile"
DEVICE_LISTS = "device_lists"
APP_ID = "app_id"
SELECTED_KEYS = "selected_keys"

BASE_DIR = os.path.abspath(__file__).rpartition('/')[0]
UPLOAD_FILES_DIR = os.path.join(BASE_DIR, "files/Custom")
GENERAL_FILES_DIR = os.path.join(BASE_DIR, "files/General")
LOG_FILE = os.path.join(BASE_DIR, "logs/server.log")
HTTP_PORT = 60000

devices = {}
configurations = {}

# This dictionary should be loaded with general responses corresponding to
# each broker. The YAML file should be loaded from GENERAL_FILES_DIR.
general_responses = {}

class RequestHandler(BaseHTTPRequestHandler):

        def handle_exception(self):
            print("Exception in user code:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)      

        def do_GET(self):
            try :
                if self.path == '/favicon.ico':
                    self.send_error(404, 'File Not Found: %s' % self.path)
                    return
                elif self.path == '/':
                    self.path = '/html/index.html'

                self.path = BASE_DIR + self.path
                logging.info("GET Request -> " + self.path)

                if self.path.endswith(".html") or self.path.endswith(".js") \
                        or self.path.endswith(".css") \
                        or self.path.endswith(".gif"):
                    f = open(self.path)
                    self.send_resp(f.read(), 'text/html')
                    f.close()
                else :
                    parsed_path = urlparse.urlparse(self.path)
                    query = parsed_path.query.split("=")

                    if query[0].lower() == APP_ID:
                        self.send_resp(\
                                self.create_manage_responses_page(\
                                        query[1]), 'text/html')
		    elif query[0].lower() == MOBILE_REQUEST : 
			self.handle_mobile_request ( urllib2.unquote(query[1]) )
			return
                    
            except :
                self.send_error(404, 'File Not Found: %s' % self.path)
                self.handle_exception()
            
        def do_POST(self):
            try :
                form = cgi.FieldStorage(headers=self.headers, fp=self.rfile, \
                        environ={'REQUEST_METHOD':'POST', \
                        'CONTENT_TYPE':self.headers['Content-Type']})

                if form.has_key(MOBILE_REQUEST):
                    request = form[MOBILE_REQUEST].value
                    self.handle_mobile_request(request)

                elif form.has_key(UPLOAD_FILE_TAG) and form.has_key(APP_ID):
                    self.handle_upload_file(form)

                elif form.has_key(DEVICE_LISTS):
                    self.send_resp(self.create_device_lists_response())        
                
                elif form.has_key(APP_ID) and form.has_key(SELECTED_KEYS):
                    self.save_configuration(form)

            except : 
                self.send_error(404, "Error")    
                self.handle_exception()

        def handle_upload_file(self, form):
            app_id = form[APP_ID].value
            router_file = devices[app_id]['ROUTER'].lower() + '.yml'

            fileitem = form[UPLOAD_FILE_TAG]
            if not fileitem.file:
                return

            s = "";
            while 1:
                chunk = fileitem.file.read(100000)
                if not chunk:
                    break
                s += chunk

            old_d = {}
            try :    
                fin = open (os.path.join(UPLOAD_FILES_DIR, router_file), 'r')
                old_d = yaml.load(fin.read())
            except:
                pass    


            d = yaml.load(s)
            for k, v in d.items():
                    if len(parser) != 3:
                        self.send_resp('fail')
                        return
                    else:
                        if old_d.has_key(k):
                            old_d[k].append(response)
                        else :
                            old_d[k] = [response]
                        


            self.send_resp('success|' + json.dumps(old_d))

            fout = open (os.path.join(UPLOAD_FILES_DIR, router_file), 'w')
            yaml.dump(old_d, fout)
            fout.close()

        def handle_mobile_request(self, request):
            logging.info("Mobile request -> " + request)
            parser = RequestUtils.validate(request)
            if len(parser) == 3:
                try :
                    request_code = int(parser[0])
                    self.send_mob_response(request_code, parser[1], parser[2])
                except :
                    self.handle_exception()
                    self.send_resp("640 <Invalid request format>##" \
                                            + parser[2] + "##")
            else :
                self.send_resp("640 <Invalid request format>####")

        def save_configuration(self, form):
            
            app_id = form[APP_ID].value
            selected_keys = form[SELECTED_KEYS].value
            d = {}
            for key in selected_keys.split(":"):
                if form.has_key(key):
                    d[key] = form[key].value

            configurations[app_id] = d
            self.send_resp('Configuration added successfully to ' + app_id)


        def send_mob_response(self, request_code, params, echo_params):
            app_id = ""
            response = "640 <This feature is not supported>##" \
                        + echo_params + "##"
            bypass = False;
	    if request_code == 800:
                app_id, response = self.create_802_response(params, echo_params)
                response +=  echo_params
	        self.send_device_resp(app_id, response);
            else :
                parsed_echo_params = Parser.parse_echo_params(echo_params)
                request_code = str(request_code)
		print parsed_echo_params;
                #router = parsed_echo_params['ROUTER'].lower()
		router = 'opx'
                if ( general_responses.has_key( router) ):
			if (general_responses[router].has_key(request_code)):
				response = re.findall("\d\d\d.*<.*>", general_responses[router][request_code] )[0]
				response = response + echo_params;
		            	self.send_device_resp(app_id, response);
			else:
				bypass = True;
	        else:
	   		bypass = True
		if bypass:
			req = request_code + " <" + params + ">##" + echo_params + "##"
			ubac_req = {"mobile_request" : req }
			r = "http://poolws2-us-beta.marketsimplified.com/raw/2?"+ urllib.urlencode(ubac_req) 
    			(a,b) = httplib2.Http().request(r)
			response = b;
	            	self.send_device_resp(app_id, response);
			return;
			
                    #else:
                    #    if devices.has_key(app_id):
                    #        router = devices[app_id]['ROUTER'].lower()
                    #    elif parsed_echo_params.has_key('ROUTER'):
                    #        router = parsed_echo_params['ROUTER'].lower()
                            
                    #    configurations[app_id] = general_responses[router]
                    #   response = self.create_response(\
                    #                    configurations[app_id][request_code], \
                    #                   echo_params)
                        
        def create_response(self, response, request_echo_params):
            parser = RequestUtils.validate(response)
            #merging the echo_params
            response = parser[0] + " <" + parser[1] + ">"
            response += "##" + request_echo_params + "##";
	    response = response.replace("<<","<").replace(">>",">");
            if len(parser) == 3 and parser[2] != '':
                response += "," + parser[2]
                parsed_echo_params = Parser.parse_echo_params(parser[2])
                if parsed_echo_params.has_key('TEST_TIMEOUT'):
                    time_out = int(parsed_echo_params['TEST_TIMEOUT'])
                    time.sleep(time_out)

            response += "##"

            return response


        def create_802_response(self, params, echo_params):
            params = Parser.parse_800_params(params)
            if len(params) == 0: return ["", "640 <Invalid Request>"]

            echo_params = Parser.parse_echo_params(echo_params)
            if not echo_params.has_key('ROUTER'):
                return ["", "640 <No Router>"]
        
            app_id = ""    
            if params.has_key('APP_ID'):

                app_id = params['APP_ID']
                if app_id == '?' or not devices.has_key(app_id):
                    app_id = RequestUtils.generateAppId()
                    self.addDeviceData(app_id, params, echo_params)

                response = "802 <APP_ID=" + app_id + ">"
            else :
                response = "640 <No app_id in the request>"

	    response = response.replace("####", "##");
            return [app_id, response]

        def create_manage_responses_page(self, app_id):      
            router_file = devices[app_id]['ROUTER'].lower() + '.yml'
            fout = file (os.path.join(GENERAL_FILES_DIR, router_file), 'rb')
	    print GENERAL_FILES_DIR , 
            general_config = yaml.load(fout)
        
            custom_config = {}
            try : 
                fout = file (os.path.join(UPLOAD_FILES_DIR, router_file), 'rb')
                custom_config = yaml.load(fout)
            except :
                pass
                
            fout.close()

            config = {}
	
	    print general_config
            for k in set(general_config.keys() + custom_config.keys()):
                l = []
                if general_config.has_key(k) and custom_config.has_key(k):
                    l = general_config[k] + custom_config[k]
                elif general_config.has_key(k):
                    l = general_config[k]        
                elif custom_config.has_key(k):
                    l = custom_config[k]

                config[k] = l    


            f = open(os.path.join(BASE_DIR, '/dummyPlatform/html/manage_responses.html'))
            t = Template(f.read())
            f.close()
            page = t.safe_substitute(app_id=app_id, \
                            d=json.dumps(config))
            return page



        def addDeviceData(self, app_id, params, echo_params):
            echo_params['CONNECTED_TIME'] = self.log_date_time_string()    
            del params['APP_ID']
            devices[app_id] = dict(params , **echo_params)
        
        def send_resp(self, response, content_type='text/plain'):
            self.send_response(200)
            self.send_header('content-type', content_type)
            self.end_headers()
            self.wfile.write(response)
            if content_type == 'text/plain':
                logging.info("RESPONSE -> " + response)

        def send_device_resp(self, app_id, response):
            self.send_resp(response)
            #log_db.insert(app_id, "response", response)

        def create_device_lists_response(self):
            response = "APP_ID,DEVICE,MODEL,OS_VERSION,APP_VERSION," \
                        + "ROUTER,RELEASE_MODE,CONNECTED_TIME|"
            for key, value in devices.iteritems():
                    response += key + "," + value.get('DEVICE', '') \
                                + "," + value.get('MODEL', '') \
                                + "," + value.get('OS_VERSION', '') \
                                + "," + value.get('APP_VERSION', '') \
                                + "," + value.get('ROUTER', '') \
                                + "," + value.get('RELEASE_MODE', '') \
                                + "," + value.get('CONNECTED_TIME', '') \
                                + "|"
            return response[0:len(response) - 1]
       
       

      
def load_general_responses():
    # Loading general responses
    print GENERAL_FILES_DIR , " << GENERAL_FILES_DIR "
    for f in glob.glob(os.path.join(GENERAL_FILES_DIR, "*.yml")):
        router, _ = f.split("/")[-1].split(".yml")      
        fout = file (f, 'rb')
        # Cannot load directly, yaml reads responseCodes as integer
        t = {}
        for k, v in yaml.load(fout).items():
            t[str(k)] = v[0]
                   
        general_responses[router] = t
        
def main(argv):
        try:
            opts, _ = getopt.getopt(argv, "p:", ["port"])
        except getopt.GetoptError:
            sys.exit(1)

        global HTTP_PORT
        global devices
        global configurations
        global log_db
        global general_responses

        for opt, arg in opts:
            if opt in ("-p", "--port"):
                try:
                    HTTP_PORT = int(arg)
                except ValueError:
                    raise ValueError
                    sys.exit(1)
        
        ticker = Ticker()
        try:
            logging.basicConfig(filename=LOG_FILE, \
                            level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%d/%m/%Y %I:%M:%S %p')
            log_db = SqliteHelper()
            load_general_responses()
            server = MyServer(('', HTTP_PORT), RequestHandler)
            ticker.start()
            print "Http server stated at %d" % HTTP_PORT
            server.serve_forever()
        except KeyboardInterrupt:
            print '^C received, shutting down server'
            ticker.stop()
            server.socket.close()

class MyServer(ThreadingMixIn, HTTPServer): 
        pass 

if __name__ == '__main__':
    main(sys.argv[1:])



