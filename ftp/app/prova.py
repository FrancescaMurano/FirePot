from twisted.protocols.ftp import FTP, FTPFactory, FTPRealm, DTP
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess
from twisted.internet import reactor

class MyDTP(DTP):
    def __init__(self, consumer, offset=0):
        super(MyDTP, self).__init__(consumer, offset)
        self.upload_allowed = True

    def fileReceived(self, data):
        """
        Sovrascrivi questo metodo per personalizzare il comportamento dell'upload di file.
        """
        if self.upload_allowed:
            # Applica qui la logica desiderata per l'upload del file
            print("File received. Applying custom logic.")
            # In questo esempio, il file viene effettivamente ricevuto
            super(MyDTP, self).fileReceived(data)
        else:
            print("File upload not allowed.")

class MyFTP(FTP):
    def ftp_STOR(self, path):
        """
        Sovrascrivi questo metodo per gestire l'inizio del comando STOR.
        """
        self.dtpInstance = MyDTP(self, self.dtpInstance.consumer.offset)
        self.sendLine("150 Ok to send data")

# Definisci un realm personalizzato per FTP
class MyFTPRealm(FTPRealm):
    def buildProtocol(self, addr):
        p = MyFTP()
        p.portal = self.portal
        p.root = self
        return p

# Crea un portal con il realm e un checker AllowAnonymousAccess
p = Portal(MyFTPRealm("./"), [AllowAnonymousAccess()])

# Crea una FTPFactory con il portal
f = FTPFactory(p)

# Ascolta sulla porta 21
reactor.listenTCP(21, f)

# Avvia il loop degli eventi di Twisted
reactor.run()
