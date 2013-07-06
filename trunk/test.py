import unittest
import server
import LoadFile
import RequestUtils
import Parser

class testLoadFile(unittest.TestCase):
		"""
		A test class for the TestSuite Module

		"""

		def setUp(self):
			LoadFile.load()

		def testOne(self):
			self.assertEqual(LoadFile.get_responses(),\
							{'436': '436 <FAIL>##ROUTER=KIMENG##', \
							'802': '802 <APP_ID=d26d9b499041e735d00c84676b58959a|SEC_CODES=|ROUND=2|ROUND-OPTION=3>##ROUTER=KIMENG,HTTPS=1,CLIENT_TYPE=ANDROID,VERSION=1.0.1,PLATFORM_MODE=development,TIME_OUT=25,MESSAGE_ID=428642b311979cfd9e40ebe8d19d8b07,PROTO_REV=2,ECHO=8f55f93d5f6b5f6f79a6b2abc6893565_0##'})

		def testException(self):
			try :
				server.main(['-p', 'asdgf'])
			except ValueError:
				pass

class testRequest(unittest.TestCase):
		"""
		Testing the RequestUtils module

		"""

		def setUp(self):
				pass

		def testValidator(self):
			self.assertEqual(RequestUtils.validate( \
							""), [])
			self.assertEqual(RequestUtils.validate( \
							"<>####"), [])
			self.assertEqual(RequestUtils.validate( \
							"600 <>####"), [])
			self.assertEqual(RequestUtils.validate( \
							"600 <>##ROUTER=OPX##"), ['600','','ROUTER=OPX'])
			self.assertEqual(RequestUtils.validate( \
							"800 app_id=?>##ROUTER=OPX##"), [])
			self.assertEqual(RequestUtils.validate( \
							"800 <app_id=?##ROUTER=OPX##"), [])
			self.assertEqual(RequestUtils.validate( \
							"800 <app_id=?>ROUTER=OPX##"), [])
			self.assertEqual(RequestUtils.validate( \
							"800 <app_id=?>##ROUTER=OPX"), [])
			self.assertEqual(RequestUtils.validate( \
							"800 <app_id=?>##ROUTER=OPX##"), \
							['800','app_id=?','ROUTER=OPX'])

		
class testParser(unittest.TestCase):

	def setUp(self):
		pass

	def testParams(self):
		self.assertEqual(Parser.parse_800_params("SEC_CODES|DEVICE=android| \
						MODEL=sdk|APP_VERSION=1.6.3|RELEASE_MODE=production| \
						OS_VERSION=4-1.6|APP_ID=?"),{'DEVICE':'android', \
						'MODEL':'sdk', 'APP_VERSION':'1.6.3', 'RELEASE_MODE' \
						:'production','OS_VERSION':'4-1.6','APP_ID':'?'})
		self.assertEqual(Parser.parse_800_params(""),{})



if __name__ == '__main__':
	unittest.main()
