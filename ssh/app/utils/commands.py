ERROR_GEN = "Error: The sintax of the command is incorrect."

ERROR_PATH = "Error: The system cannot find the path specified."

WHITELIST_COMMANDS = {
  "cd": ["cd keys",
     "cd keys/",
     "cd payments",
     "cd payments/",
     "cd users",
     "cd users/"],
  "dir":["dir"],
  "type":["type credit_cards.json"],
  "ls": ["ls","ls -l","ls -a", "ls -R","ls -d", "ls -R","ls -r","ls -t","ls ../keys","ls ../payments","ls ../users"],
  "cat": ["cat keys/p_key.pkcs1",
     "cat users/user.txt",
     "cat payments/credit_cards.json",
     "cat psw.txt", 
     "cat credit_cards.json", 
     "cat p_key.pkcs1", 
     "cat user.txt"],
  "ifconfig":["ifconfig","ifconfig -a"],
  "ip":["ip a"],
  "id":["id","id -a"],
  "echo": ["echo"],
  "clear": ["clear"],
  "pwd": ["pwd"],
  "whoami": ["whoami"],
}

IFCONFIG_SIMPLE_RESPONSE = "\r\nens4: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1460\r\n\
   \tinet 10.210.0.2 netmask 255.255.255.255 broadcast 10.210.0.2\r\n\
   \tinet6 fe80::4001:aff:fed2:2 prefixlen 64 scopeid 0x20<link>\r\n\
   \tether 42:01:0a:d2:00:02 txqueuelen 1000 (Ethernet)\r\n\
   \tRX packets 505310 bytes 923271011 (880.4 MiB)\r\n\
   \tRX errors 0 dropped 0 overruns 0 frame 0\r\n\
   \tTX packets 488031 bytes 270516440 (257.9 MiB)\r\n\
   \tTX errors 0 dropped 0 overruns 0 carrier 0 collisions 0\r\n\
\r\n\
lo: flags=73<UP,LOOPBACK,RUNNING> mtu 65536\r\n\
   \tinet 127.0.0.1 netmask 255.0.0.0\r\n\
   \tinet6 ::1 prefixlen 128 scopeid 0x10<host>\r\n\
   \tloop txqueuelen 1000 (Local Loopback)\r\n\
   \tRX packets 38 bytes 2868 (2.8 KiB)\r\n\
   \tRX errors 0 dropped 0 overruns 0 frame 0\r\n\
   \tTX packets 38 bytes 2868 (2.8 KiB)\r\n\
   \tTX errors 0 dropped 0 overruns 0 carrier 0 collisions 0\r\n"

IFCONFIG_FULL_RESPONSE = "\r\nens4: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1460\r\n\
   \tinet 10.210.0.2 netmask 255.255.255.255 broadcast 10.210.0.2\r\n\
   \tinet6 fe80::4001:aff:fed2:2 prefixlen 64 scopeid 0x20<link>\r\n\
   \tether 42:01:0a:d2:00:02 txqueuelen 1000 (Ethernet)\r\n\
   \tRX packets 505310 bytes 923271011 (880.4 MiB)\r\n\
   \tRX errors 0 dropped 0 overruns 0 frame 0\r\n\
   \tTX packets 488031 bytes 270516440 (257.9 MiB)\r\n\
   \tTX errors 0 dropped 0 overruns 0 carrier 0 collisions 0\r\n\
\r\n\
lo: flags=73<UP,LOOPBACK,RUNNING> mtu 65536\r\n\
   \tinet 127.0.0.1 netmask 255.0.0.0\r\n\
   \tinet6 ::1 prefixlen 128 scopeid 0x10<host>\r\n\
   \tloop txqueuelen 1000 (Local Loopback)\r\n\
   \tRX packets 38 bytes 2868 (2.8 KiB)\r\n\
   \tRX errors 0 dropped 0 overruns 0 frame 0\r\n\
   \tTX packets 38 bytes 2868 (2.8 KiB)\r\n\
   \tTX errors 0 dropped 0 overruns 0 carrier 0 collisions 0\r\n\
sit0: flags=128<NOARP>  mtu 1480\r\n\
        \tsit  txqueuelen 1000  (IPv6-in-IPv4)\r\n\
        \tRX packets 0  bytes 0 (0.0 B)\r\n\
        \tRX errors 0  dropped 0  overruns 0  frame 0\r\n\
        \tTX packets 0  bytes 0 (0.0 B)\r\n\
        \tTX errors 0  dropped 0 overruns 0  carrier 0  collisions 0\r\n\
\
tunl0: flags=128<NOARP>  mtu 1480\r\n\
        \ttunnel   txqueuelen 1000  (IPIP Tunnel)\r\n\
        \tRX packets 0  bytes 0 (0.0 B)\r\n\
        \tRX errors 0  dropped 0  overruns 0  frame 0\r\n\
        \tTX packets 0  bytes 0 (0.0 B)\r\n\
        \tTX errors 0  dropped 0 overruns 0  carrier 0  collisions 0\r\n"

IP_A_RESPONSE = "\
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000\r\n\
            \tlink/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00\r\n\
            \tinet 127.0.0.1/8 scope host lo\r\n\
            \tvalid_lft forever preferred_lft forever\r\n\
            \tinet6 ::1/128 scope host\r\n\
            \tvalid_lft forever preferred_lft forever\r\n\
2: bond0: <BROADCAST,MULTICAST,MASTER> mtu 1500 qdisc noop state DOWN group default qlen 1000\r\n\
      \tlink/ether 36:25:74:94:11:79 brd ff:ff:ff:ff:ff:ff\r\n\
3: dummy0: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN group default qlen 1000\r\n\
      \tlink/ether be:91:5f:da:e0:48 brd ff:ff:ff:ff:ff:ff\r\n\
4: tunl0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1000\r\n\
      \tlink/ipip 0.0.0.0 brd 0.0.0.0\r\n\
5: sit0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1000\r\n\
      \tlink/sit 0.0.0.0 brd 0.0.0.0\r\n\
6: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000\r\n\
   \tlink/ether 00:15:5d:f9:1b:74 brd ff:ff:ff:ff:ff:ff\r\n\
   \tinet 172.22.102.195/20 brd 172.22.111.255 scope global eth0\r\n\
   \tvalid_lft forever preferred_lft forever\r\n\
   \tinet6 fe80::215:5dff:fef9:1b74/64 scope link\r\n\
   \tvalid_lft forever preferred_lft forever\r\n"

