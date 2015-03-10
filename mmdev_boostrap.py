# Setup mailman interactively for development without any chaos

###########################################
#                                         #
#   author: black-perl aka Ankush Sharma  #
#                                         #
###########################################
import os,sys,subprocess
import colors,urllib2

# current execution directory
EXEC_DIR = os.getcwd()

# Dev Branch location
DEVSETUP_DIR = None

# Source code path variables
CORE_DIR = None # path for mailman-core
POSTORIUS_DIR = None # path for postorius-all

# base dir for ves'
INSTALL_DIR = None 
# VEs PATHs
VE_MAILMAN = None # mailman-core-ve
VE_POSTORIUS = None # postorius-all-ve


def internet_on():
    """
        Check for internet connection
    """
    try:
        sys.stdout.write('Checking for internet connection\n')
        response=urllib2.urlopen('http://74.125.228.100',timeout=1)
        sys.stdout.write(colors.success('Internet is Working\n\n'))
        return
    except urllib2.URLError as err: pass
    sys.stdout.write(colors.error('Internt not available\n'))
    sys.exit(0)

def is_installed(name):
    """
        Check if a program is installed on the system
    """
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name],stdout=devnull,stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True

def set_installation_path():
    """
        Sets the path for the mailman installation
    """
    global INSTALL_DIR
    if len(sys.argv) == 1:
        # There is no path specified, the installation will take place in the current directory
        INSTALL_DIR = os.path.abspath(os.getcwd())
        sys.stdout.write('Setting Up Mailman at' + colors.warning('{0}\n').format(INSTALL_DIR))
    elif len(sys.argv) == 2:
        # We need to install mailman at a given path
        # Validate the path first
        INSTALL_DIR = os.path.abspath(sys.argv[1])
        if os.path.exists(INSTALL_DIR):
            sys.stdout.write('Setting Up Mailman at ' + colors.warning('{0}\n').format(INSTALL_DIR))
        else:
            sys.stdout.write(colors.error('ERR: INVALID path specified\n'))
            sys.exit(0)
    else:
        keywords_len = len(sys.argv)
        sys.stdout.write(colors.error('ERR: Expected 1 argument, supplied {0} arguments\n'.format(keywords_len-1)))
        sys.stdout.write(colors.warning('USAGE: mmdev_bootstrap <path-to-install>\n'))
        sys.exit(0)

def check_prequisites():
    """
        Check if the system has all the requisites for setting up mailman for development
    """
    # list of requirements
    rlist = ['bzr','virtualenv']
    toInstall = []
    for package in rlist:
        if not is_installed(package):
            toInstall.append(package)
    if len(toInstall) != 0:
        # There are some unmet dependencies
        sys.stdout.write("You need to install the following first: \n")
        for package in toInstall:
            sys.stdout.write("{0}\n".format(package))
        sys.exit(0)
    else:
        sys.stdout.write(colors.warning('>> ') + 'All prequisites found...' + colors.success('Great\n\n'))
    # Everthing is OK
    return True

def install_ves():
    """
        Install the virtual environments for mailman-core and postorius
    """
    global VE_MAILMAN,VE_POSTORIUS
    # first change the directory
    os.chdir(INSTALL_DIR)
    # install vm for mailman-core
    sys.stdout.write('Setting up virtual env for ' + colors.draw('mailman-core',fg_orange=True))
    sys.stdout.write('\n')
    os.system('virtualenv --python python3 mailman-core-ve')
    sys.stdout.write(colors.error('>> ') + 'Virtual environment setup completed...' + colors.success('Great\n\n'))
    # install vm for postorius and rest
    sys.stdout.write('Setting up virtual env for ' + colors.draw('postorius, mailman-client and postorius-standalone',fg_orange=True))
    sys.stdout.write('\n')
    os.system('virtualenv --python python2 postorius-all-ve')
    sys.stdout.write(colors.error('>> ') + 'Virtual environment setup completed...' + colors.success('Great\n\n'))
    # Assign VE variables
    VE_MAILMAN = os.path.join(INSTALL_DIR,'mailman-core-ve')
    VE_POSTORIUS = os.path.join(INSTALL_DIR,'postorius-all-ve')

def get_path(repo):
    """ 
        Interactive writing path finding for a given repo
        :param repo :- the name of the repository 
    """
    global CORE_DIR,POSTORIUS_DIR
    sys.stdout.write(('Set up ' + colors.draw('{0}',fg_orange=True) + ' source code in the ' + colors.warning('current dir')+ ' or somewhere else (Y/N) ? ').format(repo))
    flag = sys.stdin.readline().rstrip('\n').rstrip()
    if flag.lower() == 'n':
        sys.stdout.write('Enter a valid path : ')
        _PATH = os.path.abspath(sys.stdin.readline().rstrip('\n').rstrip())
        if os.path.exists(_PATH):
            # Yes the path exists
            _PATH = os.path.abspath(_PATH)
            sys.stdout.write(('Setting Up ' + colors.draw('{0}',fg_orange=True) + ' at' + colors.warning('{1}.\n')).format(repo,_PATH))
        else:
            sys.stdout.write(colors.error("ERR: Path is not valid"))
            sys.exit(1)
    else:
        # Set up default path
        sys.stdout.write(('Setting Up ' + colors.draw('{0}',fg_orange=True) + ' in the ' + colors.warning('current directory') + ' itself.\n').format(repo))
        _PATH = os.path.abspath(os.getcwd())

    # modify the global path variables as per the repos
    if repo == 'mailman-core':
        CORE_DIR = _PATH
    elif repo == 'postorius-all':
        POSTORIUS_DIR = _PATH
    else:
        # Invalid option
        pass

def clone():
    """
        Clones the source code
    """
    # Get the mailman-core first
    os.chdir(CORE_DIR)
    sys.stdout.write('Getting ' + colors.draw('mailman-core',bold=True,underline=True,fg_orange=True) + ' from the launchpad.. ' + colors.draw('Wait\n',bold=True,fg_light_grey=True))
    if os.path.exists('mailman'):
        os.chdir('mailman')
        os.system('bzr pull')
    else:
        os.system('bzr branch lp:mailman')
    sys.stdout.write(colors.error('>> ') + 'mailman-core fetch successful...' + colors.success('Great\n\n'))
    
    # Get the postorius now
    os.chdir(POSTORIUS_DIR)
    sys.stdout.write('Getting ' + colors.draw('postorius',bold=True,underline=True,fg_orange=True) + ' from the launchpad.. ' + colors.draw('Wait\n',bold=True,fg_light_grey=True))
    if os.path.exists('postorius'):
        os.chdir('postorius')
        os.system('bzr pull')
    else:
        os.system('bzr branch lp:postorius')
    sys.stdout.write(colors.error('>> ') + 'postorius fetch successful...' + colors.success('Great\n\n'))
    # Get the mailman client
    os.chdir(POSTORIUS_DIR)
    sys.stdout.write('Getting ' + colors.draw('mailman-client',bold=True,underline=True,fg_orange=True) + ' from the launchpad.. ' + colors.draw('Wait\n',bold=True,fg_light_grey=True))
    if os.path.exists('mailman.client'):
        os.chdir('mailman.client')
        os.system('bzr pull')
    else:
        os.system('bzr branch lp:mailman.client')
    sys.stdout.write(colors.error('>> ') + 'mailman client fetch successful...' + colors.success('Great\n\n'))
    # Get the postorius standalone
    os.chdir(POSTORIUS_DIR)
    sys.stdout.write('Getting ' + colors.draw('postorius-standalone',bold=True,underline=True,fg_orange=True) + ' from the launchpad.. ' + colors.draw('Wait\n',bold=True,fg_light_grey=True))
    if os.path.exists('postorius_standalone'):
        sys.stdout.write(colors.draw('postorius-standalone',bold=True,underline=True,fg_orange=True) + ' is alreay preset.\n')
    else:
        os.system('bzr branch lp:~mailman-coders/postorius/postorius_standalone')
    sys.stdout.write(colors.error('>> ') + 'postorius-standalone fetch successful...' + colors.success('Great\n\n'))

def setup(repos,ve_path,source_path):
    """
        Set up the repositories for development
        :param repo:- repo name
        :param ve_path:- virtual environment path
        :parma source_path: source code path
    """
    # Set environment variables
    os.environ['VE_MAILMAN'] = VE_MAILMAN
    os.environ['VE_POSTORIUS'] = VE_POSTORIUS
    os.environ['CORE_DIR'] = CORE_DIR
    os.environ['POSTORIUS_DIR'] = POSTORIUS_DIR
    # set up repo for development
    for repo in repos:
        sys.stdout.write('Setting up ' + colors.draw('{0}'.format(repo),fg_yellow=True) + ' for development\n')
        os.chdir(EXEC_DIR)
        if repo == 'mailman':
            os.system('./mailman_setup.sh')
        else:
            os.system('./postorius_setup.sh')
        sys.stdout.write( colors.draw('{0}'.format(repo),fg_yellow=True) + ' up for development\n\n')

def fix_setup():
    """
        Set up environment for fixing
    """
    global DEVSETUP_DIR
    sys.stdout.write('Do you want to fix something in mailman today Y/N ? ')
    flag = sys.stdin.readline().rstrip('\n').rstrip()
    # Make sure we are in the executing directory
    os.chdir(EXEC_DIR)
    if flag.lower() == 'y':
        sys.stdout.write('Setup new branches in the current directory Y/N ? ')
        _flag = sys.stdin.readline().rstrip('\n').rstrip()
        if _flag.lower() == 'y':
            # Set up things here only
            DEVSETUP_DIR = EXEC_DIR
        else:
            # The user wants to enter his own path
            sys.stdout.write(colors.draw('Enter a path: '))
            _path = sys.stdin.readline().rstrip('\n').rstrip()
            if os.path.exists(_path):
                DEVSETUP_DIR = os.path.abspath(_path)
            else:
                # the path is not valid
                sys.stdout.write(colors.error("ERR: Path is not valid"))
                sys.exit(1)

    else:
        sys.stdout.write(colors.success('Happy Hunting :) \n'))
        sys.exit(1)

def create_dev():
    """
        Make branches in the setup environment
    """
    sys.stdout.write('Setting up ' + colors.draw('{0}'.format('branches'),fg_yellow=True) + ' for development at' + colors.warning('{0}\n'.format(DEVSETUP_DIR)))
    os.chdir(DEVSETUP_DIR)
    os.environ['DEVSETUP_DIR'] = DEVSETUP_DIR
    os.system('bzr branch {0}/mailman mailman'.format(CORE_DIR))
    os.system('bzr branch {0}/postorius postorius'.format(POSTORIUS_DIR))
    os.system('bzr branch {0}/mailman.client mailman.client'.format(POSTORIUS_DIR))
    os.system('bzr branch {0}/postorius_standalone postorius_standalone'.format(POSTORIUS_DIR))
    # Done
    sys.stdout.write(colors.error('>> ') + 'Branches setup sucessful' + colors.success(' Great\n\n'))
    sys.stdout.write(colors.warning('Installing branches\n'))
    # getting back to execution directory
    os.chdir(EXEC_DIR)
    os.system('./fix_setup.sh')
    sys.stdout.write(colors.error('>> ') + 'Working environment setup successful at ' + colors.warning('{0}'.format(DEVSETUP_DIR)) + colors.success(' Great\n\n'))
    sys.stdout.write(colors.success('Happy Hunting :) \n'))

def make_executables():
    for _file in os.listdir(EXEC_DIR):
        if _file.endswith('.sh'):
            os.system('chmod +x {0}'.format(_file))

def main():
    internet_on()
    make_executables()
    set_installation_path()
    check_prequisites()
    install_ves()
    get_path('mailman-core')
    get_path('postorius-all')
    clone()
    repo_list = ['mailman','postorius and others']
    setup(repo_list,VE_MAILMAN,CORE_DIR)
    fix_setup()
    create_dev()

if __name__ == '__main__':
    main()




