#import socket module 
from socket import * 
from email.utils import formatdate  
import sys


DEFAULT_HOST = ''
DEFAULT_PORT = 81

EOL = "\r\n"

STATUS_200_OK = 200
STATUS_404_NOT_FOUND = 404
STATUS_500_INTERNAL_SERVER_ERROR = 500

CONTENT_TPYE_HTML = 1
CONTENT_TYPE_IMAGE = 2

ERROR_404_HTML = "<html><b style='color: red'>404 Not Found</b></html>"
INTERNAL_ERROR_500_HTML = "<html><b style='color: red'>500 Internal Server Error</b></html>"


def constructResponse(content, status, contentType):

    if status == STATUS_200_OK:
        response = bytearray("HTTP/1.1 200 OK" + EOL)
    elif status == STATUS_500_INTERNAL_SERVER_ERROR:
        response = bytearray("HTTP/1.1 404 Not Found")
    else: #STATUS_500_INTERNAL_SERVER_ERROR
        response = bytearray("HTTP/1.1 500 Internal Server Error")

    response.extend("Data: " + formatdate(timeval=None, localtime=False, usegmt=True) + EOL)
    response.extend("Accept-Ranges: bytes" + EOL)
    response.extend("Content-Length: " + str(len(content)) + EOL)

    if contentType == CONTENT_TPYE_HTML:
        response.extend("Content-Type: text/html; charset=utf-8" + EOL)
    else:
        response.extend("Content-Type: image" + EOL)

    response.extend(EOL)
    response.extend(content)

    return response

def getContentType(filename):
    if filename.lower().endswith(".html"):
        return CONTENT_TPYE_HTML
    #elif filename.lower().endswith(".png")
    else:
        return CONTENT_TYPE_IMAGE

def sendRepsone(connectionSocket, response):
    connectionSocket.send(response)
    connectionSocket.send(EOL)      
    connectionSocket.close()


def startServer(host , port):
    serverSocket = socket(AF_INET, SOCK_STREAM) 

    serverSocket.bind((host, port))
    serverSocket.listen(1)

    while True: 
        #Establish the connection 
        print 'Ready to serve...' 
        connectionSocket, addr = serverSocket.accept()
        print "connected by ", addr
        try:
            request = connectionSocket.recv(1024)
            filename = request.split()[1][1:]
            
            f = open(filename, "rb") 
            content = f.read()

            contentType = getContentType(filename)
            response = constructResponse(content, STATUS_200_OK, contentType)
            sendRepsone(connectionSocket, response)

        except IOError: 

            content = bytearray(ERROR_404_HTML)
            
            response = constructResponse(content, STATUS_404_NOT_FOUND, CONTENT_TPYE_HTML)
            sendRepsone(connectionSocket, response)

        except Exception:

            content = bytearray(INTERNAL_ERROR_500_HTML)

            response = constructResponse(content, STATUS_500_INTERNAL_SERVER_ERROR, CONTENT_TPYE_HTML)
            sendRepsone(connectionSocket, response)

        connectionSocket.close()

    serverSocket.close() 

if __name__== "__main__": startServer(DEFAULT_HOST, DEFAULT_PORT)




