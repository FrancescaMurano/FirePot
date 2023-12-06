from asyncssh import SFTPError
from twisted.protocols.ftp import FTP, FTPFactory, FTPRealm
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess
from twisted.internet import reactor

class MyFTP(FTP):
    def ftp_STOR(self, path):
        """
        Sovrascrivi questo metodo per gestire il comando STOR (PUT).
        """
        # Esegui la tua logica personalizzata qui
        try:
            self.dtpInstance = self.dtpFactory.buildDTPConnection(self)
            self.dtpInstance.startReceiver()
            self.dtpInstance.consumer = self.file_system.openForWritingAscii(path)
        except FileNotFoundError:
            self.respond("550 File not found")
        except PermissionError:
            self.respond("550 Permission denied")
        except SFTPError as e:
            self.respond(f"550 {e}")
        else:
            self.respond("150 File status okay; about to open data connection.")

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
