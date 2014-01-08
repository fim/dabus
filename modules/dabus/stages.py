import os
import re
import fnmatch
import tarfile

import dabus.build

class SystemPackException(Exception):
    pass

class SystemPacker(object):

    include = [
        "/dev/null",
        "/dev/console",
        "/mnt/.keep",
    ]

    exclude = [
        # Files
        "/etc/make.conf",

        # Dirs without rootdir
        "/dev/*",
        "/mnt/*",
        "/proc/*",
        "/sys/*",
        "/tmp/*",
        "/var/tmp/*",
        "/usr/portage/packages/*",
        "/usr/portage/distfiles/*",

        # Everything
        "/lost+found",
        "/var/cache/edb",

        # Now what?
        #"/usr/portage/*",
        #"/usr/src",
        #"/var/log",
        #"/var/db",
    ]


    def __init__(self, name, files_includes=[], folders_includes=[]):
        self.name = name
        self.env = dabus.build.Buildenv(name)
        self.root = self.env.root
        if not self.env.exists():
            raise SystemPackException("Environment {} doesn't exist".format(self.name))


    def _getfiles(self):
        """
        Get a list of all files/folders inside the environment that will be
        included in the system image
        """

        includes = r'|'.join([fnmatch.translate(os.path.normpath(self.root+x)) for x in self.include])
        excludes = r'|'.join([fnmatch.translate(os.path.normpath(self.root+x)) for x in self.exclude])
        directories = []
        filenames = []

        for root, dirs, files in os.walk(self.root):

            # exclude dirs
            dirs[:] = [os.path.join(root, d) for d in dirs]
            dirs[:] = [d for d in dirs if re.match(includes, d) or not re.match(excludes, d)]

            filenames += dirs

            # exclude/include files
            files = [os.path.join(root, f) for f in files]
            files = [f for f in files if re.match(includes, f) or not re.match(excludes, f)]

            filenames += files

        return filenames + directories

    def _compile_kernel(self, kernel_sources='gentoo-sources'):
        """
        Compile/install a kernel using genkernel

        Useful for creating ready-to-use stage4 images
        """

        if not self.env._installed('genkernel'):
            self.env._install('genkernel')

        if not self.env._installed(kernel_sources):
            self.env._install(kernel_sources)

        self.env._run("genkernel --no-clean --no-mrproper all")


    def pack(self, filename, compile_kernel=True):
        """
        Pack contents of build env in tar.bz2 archive

        Useful for creating stage4 images
        """

        self.files = self._getfiles()
        if compile_kernel:
            self._compile_kernel()

        with tarfile.open(filename, "w:bz2") as tar:
            for filename in self.files:
                tar.add(filename, arcname=os.path.relpath(filename, self.root), recursive=False)

class GentooPacker(SystemPacker):

    include = [
        "/dev/null",
        "/dev/console",
        "/mnt/.keep",
    ]

    exclude = [
        # Files
        "/etc/make.conf",

        # Dirs without rootdir
        "/dev/*",
        "/mnt/*",
        "/proc/*",
        "/sys/*",
        "/tmp/*",
        "/var/tmp/*",
        "/usr/portage/packages/*",
        "/usr/portage/distfiles/*",

        # Everything
        "/lost+found",
        "/var/cache/edb",

        # Now what?
        #"/usr/portage/*",
        #"/usr/src",
        #"/var/log",
        #"/var/db",
    ]


class LiveCD(GentooPacker):
    pass

class NetbootImage(GentooPacker):
    pass

class Stage3(GentooPacker):
    pass

class Stage4(GentooPacker):
    pass
