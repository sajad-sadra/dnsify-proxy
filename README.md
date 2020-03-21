# Dnsify Proxy
It is use for load balancing layer7 with domain name.
This image use:
 - <code>HAproxy</code> the most popular layer7 load-balander
 - <code>Bind</code> the popular dns managing app
 - <code>Python</code> for managing services easily
## Setup
 Easy setup with docker-compose
 Also docker image is available in this <a href="https://hub.docker.com/repository/docker/sajadsadra/dnsify_proxy">link</a>
#### Change Enviroment_Variable in docker-compose.yml according this:
--> DP mean: Dnsify Proxy
 - DP_PASSWORD = the password for admin login
 - DP_EMAIL = email that used in dns zones (in simple form without end dot)
 - DP_NS = dns server name that used in zones (without end dot)
 
 ## How to use
 Click on <a href="https://github.com/sajad-sadra/dnsifyproxy/blob/master/dockerImage/panel_API/README.md">link</a> and read the README.md

<a><b><font color=red> New dnsifyproxy (envoy+nodejs) comming soon..... </font></b></a>
