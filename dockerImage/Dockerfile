FROM alpine:latest

MAINTAINER gitiserver

RUN apk update \
&&  apk add bind \
&&  apk add haproxy \
&&  mkdir /var/cache/bind/ \
&&  apk add --no-cache --update python3 \
&&  pip3 install --upgrade pip \
&&  pip3 install requests

ADD ./panel_API/bind/ /etc/bind/
ADD ./panel_API/haproxy/ /etc/haproxy/
ADD ./panel_API/ /etc/dnsifyPanel/
ADD ./panel_API/bind/root.hints /usr/share/dns/root.hints

EXPOSE 53 443 8585

CMD ["python3", "/etc/dnsifyPanel/Main.py"]

