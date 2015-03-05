#!/usr/bin/python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import time, threading

starttime = time.time()

class RequestHandler(BaseHTTPRequestHandler):
	def _writeheaders(self, doc):
		if doc is None:
			self.send_response(404)
		else:
			self.send_response(200)

		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def _getdoc(self, filename):
		if filename == '/':
			return"""<html><head><title> Sample Page </title></head>
					<body>This is a sample page</body></html>"""
		elif filename == '/stats.html':
			return """<html><head><title> Statistics </title></head>
					<body>This is static page  running for %s second </body></html>""" \
					% int(time.time() - starttime)
		else:
			return None

	def do_HEAD(self):
		doc = self._getdoc(self.path)
		self._writeheaders(doc)

	def do_GET(self):
		print "Handling with thread", threading.currentThread().getName()
		print "path is %s" % self.path
		doc = self._getdoc(self.path)
		self._writeheaders(doc)
		if doc == None:
			self.wfile.write("""<html><head><title> Not Found </title></head>
				<body>The requested doc '%s' was not found</body></html>""" % self.path)
		else:
			self.wfile.write(doc)

class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
	pass

serveraddr = ('', 8765)
srvr = ThreadingHttpServer(serveraddr, RequestHandler)
srvr.serve_forever()
