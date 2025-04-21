from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# dummy auhtorizer to manage 'virtual' users
authorizer = DummyAuthorizer()

# user with full r/w permissions 
authorizer.add_user("ftpuser", "ftpuser", "/home/ftpuser", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

handler.masquerade_address = "192.168.1.70"
handler.passive_ports = range(40000, 50000)

# custom banner when client connects
handler.banner = "pyftpdlib based FTP server ready."

# server class that will listen on all interfaces on port 21
server = FTPServer(("", 21), handler)

# starts ftp server
server.serve_forever()