import os
import socket
import threading
import shelve as sh
import signal
import subprocess
import smtplib
import time
version="1.2"
with open("chat.save","r") as r:
   chat="Chat server python version\t"+version+"\n"+r.read()
sfile=sh.open("Ids.save")
s=socket.socket()
s.bind((socket.gethostname(), 8000))#"" for local use, use socket.gethostname() for internat acess
s.listen(100)
emaillist={"raymond":("raymond.peng07@gmail.com",'rp344060*')}
banlist=[]
class mod():
    def __init__(self,modname):
        self.name=modname
    def EventCommand(self,data):
        pass
    def NewThreadEvent(self):
        print("From mod:New Thread")
mod1=mod("RegularMod")

class Filter:
    def __init__(self):
        self.type="Filter"
    def Filter(self,msg):
        raise RuntimeError("Filter Filter must be overidden")
        return msg
class filter1(Filter):
    def Filter(self,msg):
        return msg.replace("~","#")
class cmdloader(Filter):
    def Filter(self,msg):
        global chat
        detect="cmd"
        if msg.startswith(detect):
            new=subprocess.check_output(msg[len(detect):].split(),shell=True).decode()
            chat=chat+"(Server) command result "+msg[len(detect):]+" :\t"+new+"\n"
        return msg
class emailloader(Filter):
    def Filter(self,msg):
        global chat
        detect="mail"
        if msg.startswith(detect):
            msg=msg.split()
            detail=emaillist[msg[1]]
            gmail_user = detail[0] 
            gmail_password = detail[1]

            sent_from = gmail_user  
            to = [msg[2]]  
            subject = 'Automated MSG from chat server'  
            body = "Message sent from chat server: \n"+" ".join(msg[2:]).replace("newline"," \n")+"\n You are reciving this email because someone in the server invoked a command to send"
            
            email_text = """\  
            From: %s  
            To: %s  
            Subject: %s
            
            %s
            """ % (sent_from, ", ".join(to), subject, body)
            print(to,subject,body,sent_from,gmail_user)
           
              
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()

            print('Email sent!')
            
            return "Email sent correctly(server filter altered to not show email command security) if chat says something went wrong there was a error acessesing your acount make sure you enable allow less secure ap ps to access your email"
        return msg        


                        
       
                    
filters=[filter1(),cmdloader(),emailloader()]#add   filters here
stop=False

class ExitCommand(Exception):
    pass


def signal_handler(signal, frame):
    raise ExitCommand()


def thread_job():
    global stop
    while not stop:
       pass
    os.kill(os.getpid(), signal.SIGINT)
signal.signal(signal.SIGINT, signal_handler)
threading.Thread(target=thread_job).start()
import random
new=str(random.randint(0,560978))
autho=["admin","admin"]
banlist=[]
class serve (threading.Thread):
   def __init__(self, client):
      threading.Thread.__init__(self)
      self.c=client
   def run(self):
        global stop,chat,new,authouser,authopassword,banlist
        f="UTF-8"
        conn=self.c
        print("new client")
        self.admin=False
        self.switchloop="none"
        try:
           conn.send(bytes("Connected","UTF-8"))
           
           while True:
               
               data = conn.recv(1024)
               if data.decode()=="Gamemode":
                   self.switchloop="game"
               mod1.EventCommand(data)
               if data.decode("UTF-8")=="Createkey":
                   newid=str(len(sfile)+1)
                   
                   conn.sendall(bytes(newid,f))
                   name=conn.recv(2094).decode()
                   sfile[newid]={"name":name}
                   chat=chat+"[Server]\t"+name+"joined the server      \n"
                   
               if data.decode()=="Runable":
                   time.sleep(0.02)
                   exec(conn.recv(19219))
              #conn.sendall(bytes("still in progress",f))
               if data.decode("UTF-8")=="Shutdown":
                  stop=True
               if data.decode()=="admin":
                   autho1=conn.recv(19078).decode().split("⎕")
                   if autho==autho1:
                       conn.send(bytes("1","UTF-8"))
                       self.admin=True
                   else:conn.send(bytes("0","UTF-8"))
               if data.decode()=="ban":
                   time.sleep(0.05)
                   if self.admin:
                       print("ban")
                       banlist.append(conn.recv(1024).decode())
                       
               if data.decode("UTF-8")=="load":
                  print("Client load")
                  conn.send(bytes(chat,"UTF-8"))
               if data.decode("UTF-8")=="update":
                  print("Client update")
                  conn.send(bytes(chat,"UTF-8"))
               if data.decode("UTF-8")=="get":
                  time.sleep(0.05)
                  bancheck=conn.recv(2000).decode()
                  
                  if not sfile[bancheck] in banlist:
                      
                      conn.send(bytes(new,"UTF-8"))
                  else:
                      print("Banned")
                      conn.send(bytes("BAN","UTF-8"))
                  #print("Get")
               if data.decode("UTF-8")=="chatmessage":
                  sup=conn.recv(50)
                  print(type(sup))
                  print(sup)
                  print(dir(sup))
                  sup=sup.decode()
                  print(type(sup))
                  print(sup)
                  sup=int(sup)
                  dict1=sfile[str(sup)]
                  msg=conn.recv(1092).decode("UTF-8")
                  for x in filters:
                      msg=x.Filter(msg)
                      try:
                          if x.type!="Filter":
                              print(" Non filter object warning")
                      except:
                          print("Non filter object warning")
                  
                  print("Incoming message"+str(dict1))
                  msg1="["+dict1["name"]+"]"+msg+"\n"
                  print("Message1")
                  chat=chat+msg1
                  new=msg1
                  with open("chat.save","w") as q:
                      q.write(chat)
                  
               if data.decode("UTF-8")=="exit":
                  
                  break
               
        finally:
            print("Connection exited")
try:
    while not stop:
        c,a=s.accept()
        x=serve(c)
        x.start()
        mod1.NewThreadEvent()
finally:
    print("Status program quit")
    with open("chat.save","w") as q:
       q.write(chat)
       
       
        
    
