from twisted.protocols.ftp import FTP, FTPFactory, FTPRealm
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess, FilePasswordDB
from twisted.internet import reactor
import sys
from twisted.python import log

log.startLogging(sys.stdout)

# class MyFTPRealm(FTPRealm):
#     def requestAvatar(self, avatarId, mind, *interfaces):
#         print("Request for avatarId:", avatarId)
#         avatar = super(MyFTPRealm, self).requestAvatar(avatarId, mind, *interfaces)
#         print("Avatar:", avatar)
#         return avatar

# with open("./pass.dat", "r") as file:
#     print("Contenuto di pass.dat:")
#     for line in file:
#         print(line.strip())

# try:
#     p = Portal(MyFTPRealm("./"), [AllowAnonymousAccess(), FilePasswordDB("./pass.dat")])

# except Exception as e:
#     print(f"Errore durante la creazione del portal: {e}")

# f = FTPFactory(p)
# reactor.listenTCP(21, f)
# reactor.run()
from twisted.cred.checkers import FilePasswordDB
from twisted.cred.portal import Portal
from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.internet import reactor
from twisted.cred.checkers import ICredentialsChecker,InMemoryUsernamePasswordDatabaseDontUse
from twisted.cred.credentials import IUsernamePassword
from twisted.cred.error import UnauthorizedLogin


from zope.interface import implementer

@implementer(ICredentialsChecker)
class SimpleUserChecker:
    credentialInterfaces = (IUsernamePassword,)

    def __init__(self, valid_user, valid_password):
        self.valid_user = valid_user
        self.valid_password = valid_password

    def requestAvatarId(self, credentials):
        print("Tentativo di login con username:", credentials.username, "e password:", credentials.password)
        if credentials.username == self.valid_user and credentials.password == self.valid_password:
            print("Credenziali valide")
            return credentials.username
        else:
            print("Credenziali non valide")
            raise UnauthorizedLogin("Credenziali non valide")


# Configurazione delle credenziali hard-coded
valid_user = "root"
valid_password = "root"
        
users_checker = InMemoryUsernamePasswordDatabaseDontUse()
users_checker.addUser("root","root")
# Configurazione del portal
p = Portal(FTPRealm("./"), [AllowAnonymousAccess()])
p.registerChecker(users_checker, IUsernamePassword)


# Configurazione della factory FTP
f = FTPFactory(p)

# Avvio del server FTP sulla porta 21
reactor.listenTCP(21, f)

# Avvio del reattore
reactor.run()
