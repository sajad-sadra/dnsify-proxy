IP = "This is changed after run in Main.py to host local IP"

import socket
import Dns
import Proxy

def getAdditinalArecord(args):
    try:
        arlist = []
        for i in range(int(args[4])):
            arlist.append(args[5 + i].split(','))
        return arlist
    except IndexError as ie:
        print(ie)
        return "invalid"
def my_help(descript):
    ans = ""
    file = open("/etc/dnsifyPanel/help.txt", "r")
    for i in file.readlines():
        if descript == True:
            ans += i
        else:
            if i.__contains__(">>>") or i.__contains__("------"):
                ans += i
    file.close()
    return ans
def restoreDefault():
    Proxy.setDefaultConf()
    Dns.deleteAll()
    return "done"
def __seperate__(cmd):
    cmd = str(cmd)
    cmd = cmd.replace("\n", "")
    cmd = cmd.replace("\r", "")
    args = cmd.split()
    return args
def show(args):
    if args[1] == "dns" and len(args) == 2:
        return Dns.show()
    elif args[1] == "dns" and len(args) == 3 and args[2].isdecimal() and int(args[2]) <= len(Dns.zonesList()):
        return Dns.showDns(int(args[2]) - 1)
    elif args[1] == "proxy" and len(args) == 2:
        return Proxy.show()
    elif args[1] == "proxy" and len(args) == 3:
        if args[2] == "-f" or args[2] == "--frontend":
            return Proxy.showFront()
        elif args[2] == "-b" or args[2] == "--backend":
            return Proxy.showBack()
        else:
            return "invalid"
    else:
        return "invalid"
def removegozar(domain):
    try:
        index = Dns.zonesList().index(domain) + 1
        ans1 = Dns.remove(index)
        if ans1 == "done":
            ans2 = Proxy.remove(domain)
            if ans2 == "done":
                return "done"
            else:
                return "error"
        else:
            return "error"
    except ValueError as ve:
        print(ve)
        return "notfound"
def addgozar(domain):
    try:
        ip = socket.gethostbyname(domain)  # resolve ip of website
        addAlist = [[IP, "www"], [IP, "@"]]
        Dns.addZone(domain, IP, addAlist)
        Proxy.__addFront__(domain)
        Proxy.__addBack__(domain, ip)
        return "done"
    except socket.gaierror as sgier:
        print(sgier)
        return "notfound"
    except UnicodeError as unce:
        print(unce)
        return "notfound"
def resetgozar():
    dnsResult = Dns.restart()
    if dnsResult == "done":
        return Proxy.restart()
    else:
        return "error"
def start(cmd):
    if cmd == "\r\n":
        return "invalid"
    elif cmd == "help\r\n":
        return my_help(False)
    elif cmd == "--help\r\n":
        return my_help(True)
    elif cmd == "restore\r\n":
        return restoreDefault()
    else:
        args = __seperate__(cmd)
        if len(args) < 2:
            return "invalid"
        elif (args[0] == "show") and (len(args) == 2 or len(args) == 3):
            return show(args)
        elif args[0] == "add" and args[1] == "dns" and len(args) >= 5 and args[4].isdecimal():
            return Dns.addZone(args[2], args[3], getAdditinalArecord(args))
        elif args[0] == "add" and args[1] == "proxy" and len(args) == 4:
            return Proxy.add(args)
        elif args[0] == "add" and args[1] == "gozar" and len(args) == 3:
            return addgozar(args[2])
        elif args[0] == "remove" and args[1] == "dns" and len(args) == 3 and args[2].isdecimal() and int(args[2]) != 0:
            return Dns.remove(int(args[2]))
        elif args[0] == "remove" and args[1] == "proxy" and len(args) == 3:
            return Proxy.remove(args[2])
        elif args[0] == "remove" and args[1] == "gozar" and len(args) == 3:
            return removegozar(args[2])
        elif args[0] == "restart" and args[1] == "dns":
            return Dns.restart()
        elif args[0] == "restart" and args[1] == "proxy":
            return Proxy.restart()
        elif args[0] == "restart" and args[1] == "gozar":
            return resetgozar()
        else:
            return "invalid"

