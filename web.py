### doohickey that handles all the networking stuff.
print("initializing web...")

import ftplib
from ftplib import FTP
from parser import postlist
import config

def send():
    print(f"WEB: the following is FTP server responses from {config.FTPip}:")

    ftp = FTP()

    ftp.connect(config.FTPip, config.FTPport)
    print(ftp.login(config.FTPuser, config.FTPpass))
    print(f"WEB: connection establised with {config.FTPip}.")

    with open(f"output/{config.HTMLFileName}", "rb") as object:
        print("WEB: sending STOR command for test page...")
        print(ftp.storlines(F"STOR {config.HTMLFileName}", object))

    ftp.quit()
    print(f"WEB: transfer successful. connection with {config.FTPip} closed by client.")
