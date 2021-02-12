#from http.server import HTTPServer, BaseHTTPRequestHandler
from jsonrpcserver import method, dispatch
from jsonrpcclient import request as jsonrequest
from collections import defaultdict
import json
import time

@method
def eth_getWork(*params):
  response = jsonrequest("http://127.0.0.1:8545", "eth_getWork", *params)
  return response.data.result

@method
def eth_submitHashrate(*params):
  response = jsonrequest("http://127.0.0.1:8545", "eth_submitHashrate", *params)
  print("***** SUBMIT HASH RATE *****", params)
  return response.data.result

@method
def eth_submitWork(*params):
  response = jsonrequest("http://127.0.0.1:8545", "eth_submitWork", *params)
  print("***** SUBMIT WORK *****", params)
  return response.data.result

pcnt = defaultdict(int)
import socketserver
class MyTCPHandler(socketserver.StreamRequestHandler):
  def handle(self):
    cl = 0
    while 1:
      hh = self.rfile.readline().strip()
      if b'POST /' in hh:
        addr = hh.split(b'POST /')[1].split(b' ')[0]
      if b'Content-Length: ' in hh:
        cl = int(hh.split(b'Content-Length: ')[1])
      if hh == b"":
        #print("done")
        break
    idat = self.rfile.read(cl).decode('utf-8')
    print("<<", addr, idat)
    dat = dispatch(idat)
    print(">>", dat)
    print(pcnt)
    if 'eth_submitWork' in idat:
      pcnt[addr] += 1
    self.wfile.write(b'HTTP/1.0 200 OK\r\n\r\n'+str(dat).encode('utf-8'))

if __name__ == "__main__":
  HOST, PORT = "localhost", 8080

  socketserver.TCPServer.allow_reuse_address = True
  with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    server.serve_forever()

