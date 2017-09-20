import os, errno, shutil

while True:
    project = input('Enter the name of project (project.local): ')
    if (project != ""):
        break
docroot = input('Enter root folder (/var/www/html): ')

if (docroot == ""):
    docroot = "/var/www/html"

virtualhost="""
<VirtualHost *:80>
    ServerAdmin admin@example.com
    DocumentRoot """ +docroot+ """/""" +project+ """
    ServerName """ +project+ """
    ErrorLog logs/""" +project+ """-error_log
    CustomLog logs/""" +project+ """-access_log common
</VirtualHost>"""

def existsDirectory(directory):
    response = False
    if os.path.exists(directory):
        response = True
    return response
        
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

def createVirtualFile(project):
    try:
        f = open('/etc/apache2/sites-available/'+project+'.conf', 'w')
        f.write(virtualhost)
        f.close()
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def enableVirtualHost(project):
    status = os.system('sudo a2ensite '+project)
    print(status)

def updateHostsFile(project):
    with open("/etc/hosts","a") as f:
        f.write('127.0.0.1 '+ project + '\n')

def restartApache():
    status = os.system('sudo service apache2 restart')
    print(status)

if existsDirectory(docroot+ "/" +project):
    print('El directorio existe')

    while True:
        choice = input('Remove directory and create new [y/n]: ')
        if (choice == 'y' or choice == 'Y') or (choice == 'n' or choice == 'N'):
            break
    
    if (choice == 'y' or choice == 'Y'):
        shutil.rmtree(docroot+ "/" +project)
        createDirectory(docroot+ "/" +project)
        createVirtualFile(project)
        enableVirtualHost(project)
        updateHostsFile(project)
        restartApache()
    else:
        pass
else:
    print('El directorio NO existe')
    createDirectory(docroot+ "/" +project)
    createVirtualFile(project)
    enableVirtualHost(project)
    updateHostsFile(project)
    restartApache()


