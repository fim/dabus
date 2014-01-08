#!/usr/bin/env python

from ctypes import *
from ctypes.util import find_library
import os

from dabus.log import logger

MS_BIND = 4096 # from linux/fs.h
MS_REC = 16384 # from linux/fs.h

BINDS = [
    '/proc',
    '/sys',
    '/dev',
    '/etc/resolv.conf',
    '/etc/localtime'
]

class Chroot(object):
    def __init__(self,root,dir=None,bind=True):
        self.root = root
        self.bind = bind
        self.dir = '/' if dir is None else dir

    def __enter__(self):
        logger.debug("Entering chroot at {}".format(self.root))
        if self.bind:
            libcver = find_library('c')
            libc = cdll.LoadLibrary(libcver)
            for bind in BINDS:
                dst = "{}{}".format(self.root, bind)
                if os.path.isfile(bind):
                    if not os.path.isfile(dst):
                        open(dst, 'w').close()
                elif os.path.isdir(bind):
                    if not os.path.isdir(dst):
                        os.mkdir(dst)
                s = libc.mount(bind, dst, "none", MS_BIND|MS_REC, 0)
                if s < 0: raise Exception("Error binding {} in chroot".format(bind))
        self.realdir = os.getcwd()
        self.realroot = os.open('/',os.O_RDONLY)
        os.chroot(self.root)
        os.chdir(self.dir)
        return self

    def __exit__(self,type,value,traceback):
        logger.debug("Exiting chroot at {}".format(self.root))
        os.fchdir(self.realroot)
        while os.stat('.')[1] != os.stat('..')[1]:
            os.chdir('..')
        os.chroot('.')
        os.close(self.realroot)
        os.chdir(self.realdir)
        if self.bind:
            libcver = find_library('c')
            libc = cdll.LoadLibrary(libcver)
            for bind in BINDS:
                dst = "{}/{}".format(self.root, bind)
                libc.umount(dst)
