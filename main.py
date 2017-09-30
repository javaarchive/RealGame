import socket as s
import socket
conn=s.socket(socket.AF_INET, socket.SOCK_STREAM)
ip="fathhomepc1.t-mobile.com"# Your ip or host here or out in a internet game host
port=8000
conn.connect((ip,8000))
print(conn.recv(10304).decode())
