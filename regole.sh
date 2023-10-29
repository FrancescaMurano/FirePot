#!/bin/sh

echo 1 > /proc/sys/net/ipv4/ip_forward

iptables -F
iptables -t nat -F
iptables -X


iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A INPUT -s 192.168.0.0/24 -p tcp -m tcp --dport 23 -j ACCEPT
iptables -A INPUT -s 192.168.0.0/24 -p tcp -m tcp --dport 2222 -j ACCEPT
iptables -t nat -I PREROUTING -p tcp --dport 23 -j REDIRECT --to-ports 2222
iptables -t nat -I OUTPUT -p tcp -o lo --dport 23 -j REDIRECT --to-ports 2222



iptables -A INPUT -s 192.168.0.0/24 -p tcp -m tcp --dport 22 -j ACCEPT
iptables -t nat -I PREROUTING -p tcp --dport 22 -j REDIRECT --to-ports 2222
iptables -t nat -I OUTPUT -p tcp -o lo --dport 22 -j REDIRECT --to-ports 2222
