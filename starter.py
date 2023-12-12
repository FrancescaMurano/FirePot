class UserInput:
    PORT_SSH_REMOTE = 22
    PORT_SSH_REAL = 2222

    PORT_TELNET_REMOTE = 23
    PORT_TELNET_REAL = 2323

    PORT_MODBUS_REMOTE = 502
    PORT_MODBUS_REAL = 5002

    PORT_FTP_REMOTE = 21
    PORT_FTP_REAL = 2121

    IP_ADDRESS = "localhost"
    FTP_PASSIVE_PORT_START = 6000
    FTP_PASSIVE_PORT_END = 6006

# 1. docker compose up --> elastic e kibana
# 2. POST delle dashboard
# 3. scelta degli honeypot da utilizzare (SSH,TELNET,MODBUS,FTP)
# 4. apertura delle porte -- abilitazione porte su iptables
# 5. scelta delle porte
# 6. docker con le porte scelte 
# 7. Menu:
#   - Visualizza dashboard
#   - exit and down
#   - exit 