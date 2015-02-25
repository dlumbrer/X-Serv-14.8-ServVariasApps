#!/usr/bin/python

"""
webAppMulti class

Root for hierarchy of classes implementing web applications
Each class can dispatch to serveral web applications, depending
on the prefix of the resource name

Copyright Jesus M. Gonzalez-Barahona, Gregorio Robles (2009-15)
jgb @ gsyc.es
TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
October 2009, February 2015
"""

import socket
import random

class app:
    """Application to which webApp dispatches. Does the real work

    Usually real applications inherit from this class, and redefine
    parse and process methods"""

    def parse(self, request, rest):
        """Parse the received request, extracting the relevant information.

        request: HTTP request received from the client
        rest:    rest of the resource name after stripping the prefix
        """

        return None

    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>" +
                          "Dumb application just saying 'It works!'" +
                          "</h1><p>App id: " + str(self) + "<p></body></html>")


class webApp:
    """Root of a hierarchy of classes implementing web applications

    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def select(self, request):
        """Selects the application (in the app hierarchy) to run.

        Having into account the prefix of the resource obtained
        in the request, return the class in the app hierarchy to be
        invoked. If prefix is not found, return app class
        """

        resource = request.split(' ', 2)[1]
        for prefix in self.apps.keys():
            if resource.startswith(prefix):
                print "Running app for prefix: " + prefix + \
                    ", rest of resource: " + resource[len(prefix):] + "."
                return (self.apps[prefix], resource[len(prefix):])
        print "Running default app"
        return (self.myApp, resource)

    def __init__(self, hostname, port, apps):
        """Initialize the web application."""

        self.apps = apps
        self.myApp = app()

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)

        while True:
            print 'Waiting for connections'
            (recvSocket, address) = mySocket.accept()
            print 'HTTP request received (going to parse and process):'
            request = recvSocket.recv(2048)
            print request
            (theApp, rest) = self.select(request)
            parsedRequest = theApp.parse(request, rest)
            (returnCode, htmlAnswer) = theApp.process(parsedRequest)
            print 'Answering back...'
            recvSocket.send("HTTP/1.1 " + returnCode + " \r\n\r\n"
                            + htmlAnswer + "\r\n")
            recvSocket.close()

class holaApp(app):
	def process(self,parsedRequest):
		return ("200 OK", "<html><body><h1>" +
                          "Hola mundo" +
                          "</h1></body></html>")
                          
class adiosApp(app):
	def process(self,parsedRequest):
		return ("200 OK", "<html><body><h1>" +
                          "Adios mundo" +
                          "</h1></body></html>")                          

class sumaApp(app):
	def parse(self, request, rest):
		paquete = rest.split('/')[1:]
		# paquete es una lista con [num1, num2]
		return paquete
		
	def process(self,parsedRequest):
		suma = int(parsedRequest[0]) + int(parsedRequest[1])
		return ("200 OK", "<html><body><h1>" +
                          "La suma es" +
                          "</h1><p>" + parsedRequest[0] + " + " + parsedRequest[1] + " = " + str(suma) + "</body></html>")
                          
class aleatApp(app):

	def process(self, parsedRequest):
		return ("200 OK", "<html><body><h1>ALEATORIO</h1><p><a href='/aleat/"+
				str(random.randrange(10000000000000)) +
				"'>Dame Otra!!</a></p></body></html>")
				
class githubApp(app):
	
	def parse(self, request, rest):
		paquete = rest.split('/')[1:]
		return paquete
		
	def process(self, parsedRequest):
		if parsedRequest[0]:
			if parsedRequest[0] == "code":
				return ("200 OK", "<html><body><h1>CODE</h1>" + 
						"<p><a href='https://github.com/dlumbrer/X-Serv-14.8-ServVariasApps'>Aqui tienes el codigo</a></p>" +
						"</body></html>")
			elif parsedRequest[0] == "who":
				return ("200 OK", "<html><body><h1>Yo soy</h1>" + 
						"<p><a href='https://github.com/dlumbrer/'>David Moreno Lumbreras</a></p>" +
						"</body></html>")
						
		return ("200 OK", "<html><body><h1>UY</h1>" +
				"<p><a href='http://localhost:1234/github/code'>Quieres ver el codigo?</a></p>" + 
				"<p><a href='http://localhost:1234/github/who'>Quieres saber quien soy?</a></p></body></html>")                    

if __name__ == "__main__":
    anApp = app()
    otherApp = app()
    hola = holaApp()
    adios = adiosApp()
    suma = sumaApp()
    aleatorio = aleatApp()
    github = githubApp()
    testWebApp = webApp("localhost", 1234, {'/app': anApp,
                                            '/other': otherApp,
                                            '/hola': hola,
                                            '/adios': adios,
                                            '/suma': suma,
                                            '/aleat': aleatorio,
                                            '/github': github})
