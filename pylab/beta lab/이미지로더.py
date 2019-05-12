import ftplib
import os


def getCwdFileList():
    lstFile = []
    ftp.retrlines('MLSD', lstFile.append)

    sub = []
    file = []

    for fInfo in lstFile:
        infos = fInfo.split(";")
        name = infos.pop().lstrip()
        type = None
        for info in infos:
            if "type" in info:
                type = info.split("=")[1]
                break
        if type == 'dir':
            sub.append(name)
        else:
            file.append(name)

    return sub, file


def recurList (path):
    global ftp
    ftp.cwd(path)
    sub, file  = getCwdFileList()
    for f in file:
        fd = open("." + path + "/" + f, 'wb')
        ftp.retrbinary("RETR " + f, fd.write)
        fd.close()

    for s in sub:
        try: os.mkdir("." + path + "/" + s)
        except: pass
        recurList(path + "/" + s)


