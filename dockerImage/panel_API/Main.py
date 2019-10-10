import Socket
from requests import get
import os
import Command
import Dns
import Proxy

def run(PASSWORD):
    loginFlag = True
    con = Socket.ServerSocket()
    # login
    con.send("$ ")
    password = con.recive().replace("\r\n", "")
    if password != PASSWORD:
        loginFlag = False
        print("^^ PASS Not Match ^^^")
    # do command
    con.send("\n>>> ")
    while loginFlag:
        cmd = con.recive()
        if cmd == "{error}":
            loginFlag = False
            con.stopCon()
        answer = Command.start(cmd)
        con.send(str(answer) + "\n>>> ")
def setPublicIP():
    # This functione use class (get) in (request.py) file in library
    try:
        Command.IP = get('https://api.ipify.org').text
    except:
        print("can not resolve server IP")
        Command.IP = get('https://api.ipify.org').text
def start():
    PASSWORD = os.getenv('DP_PASSWORD')
    Dns.NS = os.getenv('DP_NS') + '.'
    Dns.EMAIL = os.getenv('DP_EMAIL').replace('@', '.') + '.'
    setPublicIP()
    print("Host Public IP: " + Command.IP)
    print("NS name: " + Dns.NS)
    print("Email: " + Dns.EMAIL)
    print("Admin PASSWORD: " + str(PASSWORD))
    Proxy.start()
    Dns.start()
    while True:
        run(str(PASSWORD))



start()