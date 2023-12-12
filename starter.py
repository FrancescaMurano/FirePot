class UserInput:
    PORT_SSH_REMOTE = None
    PORT_SSH_REAL = None

    PORT_TELNET_REMOTE = None
    PORT_TELNET_REAL = None

    PORT_MODBUS_REMOTE = None
    PORT_MODBUS_REAL = None

    PORT_FTP_REMOTE = None
    PORT_FTP_REAL = None

    @classmethod
    def ssh_ports(cls):
        # Richiedi input all'utente o inserisci i dati in qualche altro modo
        cls.PORT_SSH_REMOTE = input("SSH remote port: ")
        cls.PORT_SSH_REAL = input("SSH real port: ")

    # @classmethod
    # def modbus_ports(cls):
    #     # Stampa i valori delle variabili statiche
    #     cls.PORT_SSH_REMOTE = input("Inserisci il valore per variabile_statica_1: ")
    #     cls.PORT_SSH_REAL = input("Inserisci il valore per variabile_statica_2: ")
    #     print(f"variabile_statica_1: {cls.variabile_statica_1}")
    #     print(f"variabile_statica_2: {cls.variabile_statica_2}")

    #     @classmethod
    # def ssh_ports(cls):
    #     # Richiedi input all'utente o inserisci i dati in qualche altro modo
    #     cls.variabile_statica_1 = input("Inserisci il valore per variabile_statica_1: ")
    #     cls.variabile_statica_2 = input("Inserisci il valore per variabile_statica_2: ")

    # @classmethod
    # def ftp_ports(cls):
    #     # Stampa i valori delle variabili statiche
    #     print(f"variabile_statica_1: {cls.variabile_statica_1}")
    #     print(f"variabile_statica_2: {cls.variabile_statica_2}")

    # @classmethod
    # def telnet_ports(cls):
    #     # Richiedi input all'utente o inserisci i dati in qualche altro modo
    #     cls.variabile_statica_1 = input("Inserisci il valore per variabile_statica_1: ")
    #     cls.variabile_statica_2 = input("Inserisci il valore per variabile_statica_2: ")

    # @classmethod
    # def modbus_ports(cls):
    #     # Stampa i valori delle variabili statiche
    #     print(f"variabile_statica_1: {cls.variabile_statica_1}")
    #     print(f"variabile_statica_2: {cls.variabile_statica_2}")

UserInput.ssh_ports()