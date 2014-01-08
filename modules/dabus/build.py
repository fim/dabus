
import os
import platform
import subprocess
import sys

import dabus.config
import dabus.build
import dabus.util
import dabus.chroot
import dabus.makeconf
from dabus.log import logger


class BuildenvInitError(Exception):
    pass

class EmergeError(Exception):
    pass

class ChrootError(Exception):
    pass
class ChrootCommandError(Exception):
    pass

class Buildenv:
    """
    Main class for build environments
    """

    conf = {}
    emerge_settings = [
            "--nospinner",
            "--deep",
            "--oneshot",
            "--update",
            "--newuse",
            "--selective=n",
            "--keep-going=y"
        ]
    root = ""
    real_root = os.open('/', os.O_RDONLY)

    @staticmethod
    def isbuildenv(self, path):
        """
        Check if path is a chroot buildenv
        """
        if os.path.isdir(self.root):
            try:
                with dabus.chroot.Chroot(self.root):
                    pass
            except Exception,e:
                return False
            else:
                return True


    def __init__(self, name, arch=None, conf={},  path="/usr/local/dabus"):
        """
        Initialize a new env
        """
        self.conf = conf # Global conf
        self.arch = arch # Actually this is the subarch
        self._loadconf() # build env conf
        self.name = name
        self.path = path
        self.root = "{}/{}".format(self.path, name)
        self.tmp = "{}/tmp".format(path, name)

    def exists(self):
        try:
            with dabus.chroot.Chroot(self.root) as c:
                subprocess.call(['/bin/sh', '-c', 'exit'])
        except Exception,e:
            return False

        return True

    def create(self):
        if not os.path.isdir(self.root):
            os.mkdir(self.root)

        if not os.path.isdir(self.tmp):
            os.mkdir(self.tmp)

        try:
            logger.info("Creating environment {}".format(self.name))
            stage = dabus.util.get_latest_stage3(self.arch, dest=self.tmp)
            portage = dabus.util.get_latest_portage(dest=self.tmp)
            dabus.util.extract(stage, self.root)
            dabus.util.extract(portage, "{0}/{1}".format(self.root, "/usr"))
            m = dabus.makeconf.MakeConf("{0}/{1}".format(self.root,
                "/etc/portage/make.conf"))
            m.save()
        except Exception,e:
            raise BuildenvInitError("Couldn't create new environment {}: {}".format(self.name, e))

    def delete(self, config=False):
        """
        Delete the build environment and accompanying configuration
        """
        import shutil
        if config:
            # Delete configuration
            pass
        logger.info("Deleting environment {}".format(self.name))
        shutil.rmtree(self.root)

    def build(self, packages="@world", clean=False):
        """
        Build a set of packages in the env
        """
        # redirect stdout to emerge logs
        # add Ctrl-C handler
        emptytree = ["--emptytree"] if clean else []
        packages = packages.split() if isinstance(packages, basestring) else packages

        logger.info("[{}] Building packages {}".format(self.name,
            ' '.join([p.strip() for p in packages])))
        self._run(' '.join(['emerge'] + self.emerge_settings + emptytree + packages))

    def _update_portage(self):
        """
        Update portage from file/url
        """
        logger.debug("[{}] Updating portage".format(self.name))
        portage = dabus.util.get_latest_portage()
        dabus.util.extract(portage, "{}/{}/usr".format(path, name))

    def _loadconf(self, filename=None):
        """
        Load env conf
        """
        self.conf = {}
        #conf = dabus.config.ConfigParser(filename).parse()

    def _run(self, command, quiet=False):
        """
        Run command inside chroot

        Returns a tupple with (stdout, stderr)
        """
        logger.debug("[{}] Running commnand inside chroot: {}".format(self.name, command))
        with dabus.chroot.Chroot(self.root):
            process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, close_fds=True)
            if not quiet:
                for line in iter(process.stdout.readline, b''):
                    logger.info(line.strip())
                if process.stderr:
                    logger.error(process.stderr.read())
            process.stdout.close()
            process.wait()

            if process.returncode:
                raise ChrootCommandError("Command returned non zero exit code: {}".format(
                    process.returncode))

    def _install(self, package, use=""):
        """
        Install package inside the chroot. Used internally
        """
        logger.debug("[{}] Installing package {}".format(self.name, package))
        with dabus.chroot.Chroot(self.root):
            rt = subprocess.call("USE=\"{}\" emerge -1 {}".format(use, package), shell=True)

        if rt != 0:
            raise EmergeError("Cannot install package {}".format(package))

    def _installed(self, package):
        """
        Check if package is available inside the chroot
        """
        with dabus.chroot.Chroot(self.root):
            if subprocess.call("[[ -n \"$(/usr/bin/portageq match / {} 2>/dev/null)\" ]]".format(package), shell=True):
                return False

            return True
