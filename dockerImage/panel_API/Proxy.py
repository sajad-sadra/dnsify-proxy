PATH_proxy = "/etc/haproxy/haproxy.cfg"

import os

def __getacl__(domain, bkORft) :
    ans = str(domain)
    while ans.__contains__("."):
        ans = ans.replace(".", "_")
    return (bkORft +"_"+ ans)
def __addBack__(domain, ip):
    file = open(PATH_proxy,"a")
    file.write("backend " + __getacl__(domain, "bk") + "\n")
#    file.write("  mode tcp\n")
    file.write("  server " + __getacl__(domain, "srv") + " " + ip + ":443 check sni req.ssl_sni\n")
    file.close()
def __addFront__(domain):
    result = "  acl " + __getacl__(domain, "ft") + "  req.ssl_sni -i " + domain + "\n"
    file = open(PATH_proxy, "r")
    list = file.readlines()
    index = 0
    for i in range(len(list)):
        if list[i].__contains__("acl"):
            index = i
            break
    list.insert(index,result)
    for i in range(len(list)):
        if list[i].__contains__("tcp-request content reject"):
            index = i
            break
    lstmp = list[index].split()
    lstmp.append("!" + __getacl__(domain, "ft"))
    tmp = "  "
    for i in lstmp:
        tmp += i +" "
    list[index] = tmp + "\n"

    result = "  use_backend " + __getacl__(domain, "bk") + " if " + __getacl__(domain, "ft") + "\n"
    for i in range(len(list)):
        if list[i].__contains__("use_backend"):
            index = i
            break
    list.insert(index, result)
    file.close()
    file = open(PATH_proxy, "w")
    for i in list:
        file.write(i)
    file.close()
def add(args):
    __addBack__(args[2], args[3])
    __addFront__(args[2])
    return "done"
def setDefaultConf():
    file = open(PATH_proxy, "w")
    file.write("global \n")
#    file.write("	log /dev/log	local0 \n")
#    file.write("	log /dev/log	local1 notice \n")
    file.write("	chroot /var/lib/haproxy \n")
    file.write("	stats socket /etc/haproxy/admin.sock mode 660 level admin expose-fd listeners \n")
    file.write("	stats timeout 30s \n")
    file.write("	user haproxy \n")
    file.write("	group haproxy \n")
    file.write("	daemon \n\n")
    file.write("	# Default SSL material locations \n")
    file.write("	ca-base /etc/ssl/certs \n")
    file.write("	crt-base /etc/ssl/private \n\n")
    file.write("	ssl-default-bind-ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!MD5:!DSS \n")
    file.write("	ssl-default-bind-options no-sslv3 \n")
    file.write("defaults \n")
#    file.write(" 	log	global\n")
    file.write("	mode	tcp \n")
#    file.write("	option	tcplog \n")
    file.write("	option	dontlognull \n")
    file.write("        timeout connect 5000 \n")
    file.write("        timeout client  50000 \n")
    file.write("        timeout server  50000\n")
    file.write("	errorfile 400 /etc/haproxy/errors/400.http \n")
    file.write("	errorfile 403 /etc/haproxy/errors/403.http \n")
    file.write("	errorfile 408 /etc/haproxy/errors/408.http \n")
    file.write("	errorfile 500 /etc/haproxy/errors/500.http \n")
    file.write("	errorfile 502 /etc/haproxy/errors/502.http \n")
    file.write("	errorfile 503 /etc/haproxy/errors/503.http \n")
    file.write("	errorfile 504 /etc/haproxy/errors/504.http \n\n\n")
    file.write("frontend ft_global \n")
    file.write("  bind 0.0.0.0:443 \n")
#    file.write("  mode tcp\n")
    file.write("  acl ft_gitiserver  req.ssl_sni -i gitiserver.com \n")
    file.write("  tcp-request inspect-delay 2s \n")
    file.write("  tcp-request content reject if !ft_gitiserver \n")
    file.write("  use_backend bk_gitiserver if ft_gitiserver \n")
    file.write("#----- \n")
    file.write("backend bk_gitiserver \n")
#    file.write("  mode tcp\n")
    file.write("  server srv_gitiserver 95.156.253.3:443 check sni req.ssl_sni \n")
    file.close()
def show():
    file = open(PATH_proxy, "r")
    ans = ""
    for i in file.readlines():
        ans += i
    file.close()
    return ans
def showFront():
    file = open(PATH_proxy, "r")
    ans = ""
    for i in file.readlines():
        if i.__contains__("acl") or i.__contains__("use_backend"):
            ans += i
    file.close()
    return ans
def showBack():
    flag = False
    file = open(PATH_proxy, "r")
    ans = ""
    for i in file.readlines():
        if flag is True:
            ans += i
        if i.__contains__("#-----"):
            flag = True
    file.close()
    return ans
def remove(domain):
    try:
        bk = __getacl__(domain, "bk")
        ft = __getacl__(domain, "ft")
        file = open(PATH_proxy, "r")
        ans = []
        counter = 0
        flag = False
        for i in file.readlines():
            i = i.replace(("!" + ft), " ")
            if i.__contains__("backend " + bk):
                flag = True
            if not (i.__contains__(domain) or i.__contains__("use_backend " + bk + " if " + ft)) and not (flag):
                ans.append(i)
            if flag:
                counter += 1
            if counter is 3:
                flag = False
        file.close()
        file = open(PATH_proxy, "w")
        for i in ans:
            file.write(i)
        file.close()
        return "done"
    except:
        return "notfound"

def start():
    os.system("haproxy -f " + PATH_proxy)
def stop():
    os.system("killall haproxy")
def restart():
    stop()
    start()
    return "done"
