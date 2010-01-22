'''
Created on Sep 16, 2009

@author: strider
'''
from lutris.config import LutrisConfig
import subprocess
import platform

class Runner(object):
    '''Generic runner (base class for other runners) '''
    def __init__(self,settings=None):
        ''' Initialize runner'''
        self.executable = None
        
    def load(self,game):
        self.game = game


    def config(self):
        """this is dumb and useless i guess"""
        subprocess.Popen([self.configscript],stdout=subprocess.PIPE).communicate()[0]

    def play(self):
        pass
    
    def is_installed(self):
        """ Check if runner is installed"""
        is_installed = None
        if not self.executable:
            return 
        cmdline = "which " + self.executable
        cmdline = str.split(cmdline," ")
        result = subprocess.Popen(cmdline,stdout=subprocess.PIPE).communicate()[0]
        if result == '' :
            is_installed = False
        else:
            is_installed = True
        return is_installed

    def get_game_options(self):
        return None

    def get_runner_options(self):
        return None


    def install(self):
        """Generic install method, for use with package management systems"""
        #Return false if runner has no package, must be then another method and
        # install method should be overridden by the specific runner
        if not hasattr(self,"package"):
            return False
        linux_dist = platform.linux_distribution()[0]
        #Add the package manager with arguments for your favorite distro :)
        if linux_dist == "Ubuntu" or linux_dist == "Debian":
            package_manager = "apt-get"
            install_args = "-y install"
        elif linux_dist == "Fedora":
            package_manager = "yum"
            install_args = "install"
        else:
            print """The distro you're running is not supported yet\n
            edit runners/runner.py to add support for it"""
            return False
        print subprocess.Popen("gksu \"%s %s %s\"" % (package_manager,install_args,self.package),shell=True,stdout=subprocess.PIPE).communicate()[0]

    def write_config(self,id,name,fullpath):
        """Writes game config to settings directory"""
        system = self.__class__.__name__
        index= fullpath.rindex("/")
        exe = fullpath[index+1:]
        path = fullpath[:index]
        if path.startswith("file://"):
            path = path[7:]
        gameConfig = LutrisConfig()
        values = {"main":{ "path":path, "exe":exe, "realname" : name, "system":system }}
        gameConfig.write_game_config(id, values)