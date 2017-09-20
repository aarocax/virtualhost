import os, errno, sys, stat, pwd


def createDirectory(directory):
    try:
        os.makedirs(directory)
        os.chmod(directory, 0o775)
        uid =  pwd.getpwnam('root').pw_uid
        gid = pwd.getpwnam('www-data').pw_uid
        os.chown(directory, uid, gid) # set user:group as root:www-data

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

createDirectory("anselmo5")
