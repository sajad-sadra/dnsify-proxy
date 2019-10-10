PATH_dns_config = "/etc/bind/named.conf.local"
PATH_dns_zones = "/etc/bind/zones/"
# Below Variables changed to enviroment_variable in Main.py
NS = "ns1.example.com."
EMAIL = "admin.example.com."

import os
from datetime import datetime

def zonesList():
    list = []
    file = open(PATH_dns_config, "r")
    for i in file.readlines():
        if i.__contains__('zone "'):
            i = i.replace('zone "', ' ')
            i = i.replace('" {', ' ')
            i = i.replace(" ", "")
            i = i.replace('\n', '')
            list.append(i)
    file.close()
    return list
def __getserialnum__():
    now = datetime.now()
    return str(now.strftime("%Y%m%d%H"))
def addZone(domain, ip, addAlist):
    if zonesList().__contains__(domain):
        return "dublicate"
    elif addAlist == "invalid":
        return addAlist
    else:
        path = PATH_dns_zones + domain
        file = open(path, "w")
        file.write("$ORIGIN "+domain+".\n")
        file.write("$TTL 1800\n")
        file.write("@       IN      SOA     "+NS+"      " + EMAIL + " (\n")
        file.write("                        " + __getserialnum__() + "        ; serial number\n")
        file.write("                        3600                    ; refresh\n                        900                     ; retry\n                        1209600                 ; expire\n                        1800                    ; ttl\n                        )\n")
        file.write("; Name servers\n")
        file.write("                    IN      NS      " + NS + "\n")
        file.write("\n; A records for name servers\n")
        file.write(NS.split('.')[0]+".             IN      A       "+ip+"\n")
        file.write("\n; Additional A records\n")
        for i in addAlist:
            file.write(i[1]+"               IN      A       "+i[0]+"\n")
        file.write("\n\n")
        __activezone__(domain)
        file.close()
        return "done"
def __activezone__(domain):
    file = open(PATH_dns_config, "a")
    file.write('zone "'+domain+'" {\n')
    file.write("    type master;\n")
    file.write('    file "' + PATH_dns_zones + domain+'";')
    file.write("\n};\n")
    file.close()
def deleteAll():
    for i in zonesList():
        os.remove(PATH_dns_zones + i.replace("\n", ""))
    os.remove(PATH_dns_config)
    file = open(PATH_dns_config, "w")
    file.write("# Actived Zones\n")
    file.close()
def show():
        index = 1
        dns_list = ""
        for i in zonesList():
            dns_list += (str(index) + "~" + i + '\n')
            index += 1
        return dns_list
def showDns(index):
   try:
    file = open(PATH_dns_zones + zonesList()[index].replace("\n", ""))
    ans = ""
    for i in file.readlines():
        ans += i
    file.close()
    return ans
   except IndexError as ie:
       print(ie)
       return "invalid"
def remove(index):
    try:
        domain = zonesList()[int(index) - 1]
        row = 0
        file = open(PATH_dns_config, "r")
        array = file.readlines()
        for i in range(len(array)):
            if array[i].__contains__(domain):
                row = i
                break
        array[index] = ""
        array[index+1] = ""
        array[index+2] = ""
        array[index+3] = ""
        file.close()

        file = open(PATH_dns_config, "w")
        for i in array:
            file.write(i)
        file.close()

        os.remove(PATH_dns_zones + domain)
        return "done"
    except:
        return "invalid"


def start():
    os.system("named")
def stop():
    os.system("killall named")
def restart():
    stop()
    start()
    return "done"
