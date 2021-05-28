import socket
import threading
import time

class WebServer:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	routes = {}

	def __init__(self, host, port):
		self.host = host
		self.port = port

	def router(self, route, func):
		self.routes[route] = func

	def handleRequest(self, request):
		each_line = request.splitlines()
		first_line = each_line[0]
		
		content = request.split('\r\n\r\n')

		first_line_items = first_line.split(' ')

		method = first_line_items[0]
		uri = first_line_items[1]
		
		return method, uri, content

	def handleResponse(self, method, uri, content):
		print("new request{ method: "+method+", uri: "+uri+" }")
		if uri == "/":
			file_path = "/index.html"
		else:
			file_path = uri

		file_path = file_path[-(len(file_path)-1):]
		file_extension = file_path.split('.')[-1]
		if '.' not in file_path:
			http_header = b'HTTP/1.1 200 OK\r\ncontent-type: application/json\r\n\r\n'

			if file_path in self.routes:
				http_body = self.routes[file_path](content[1])
				response = http_header+str.encode(http_body)

			return response

		http_header = "HTTP/1.1 200 OK\r\ncontent-type: text/{}; charset=UTF-8\r\n\r\n".format(file_extension)
		try:
			file_path = "public/"+file_path
			if file_extension != "png":
				file = open(file_path, "r")
				http_body = file.read()
				http_body = str.encode(http_body)
			else:
				file = open(file_path, "rb")
				http_body = file.read()

			
			file.close()
			response = str.encode(http_header)+http_body
		except Exception as e:
			print(e)
			response = b"HTTP/1.1 404 NOT FOUND\r\n\r\nFile not found"

		return response

	def requestThread(self, server_input, address):
		try:
			print("connected with "+str(address))
			request = server_input.recv(1024)
			request = request.rstrip()
			request = request.decode("utf-8")

			if request:
				method, uri, content = self.handleRequest(request)
				response = self.handleResponse(method, uri, content)
			else:
				response = b"void"

			server_input.send(response)
			server_input.close()
			print("connection with "+str(address)+" closed")

		except:
			server_input.close()
			print("connection with "+str(address)+" closed")
			return False

	def startServer(self):
		self.sock.bind((self.host, self.port))
		self.sock.listen(5)
		print("server is listening at port "+str(self.port))

		while True:
			server_input, address = self.sock.accept()

			threading.Thread(target=self.requestThread, args=(server_input, address)).start()

		self.sock.close()



