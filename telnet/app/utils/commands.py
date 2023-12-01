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
  "id":["id","id -a"],
  "echo": ["echo"],
  "clear": ["clear"],
  "pwd": ["pwd"],
  "whoami": ["whoami"],
}

IFCONFIG_RESPONSE = "\r\nens4: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1460\r\n\
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
   \tTX errors 0 dropped 0 overruns 0 carrier 0 collisions 0\r\n\\"