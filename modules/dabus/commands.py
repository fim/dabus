import os
import inspect
from datetime import datetime
from optparse import OptionParser

import dabus.build
from dabus.stages import *
from dabus.log import logger

class CommandlineArgumentError(Exception):
    pass

class CreateException(Exception):
    pass

class DeleteException(Exception):
    pass

class BuildException(Exception):
    pass

def cmd_list(conf, argv):
    """
    List all existing build environments
    """
    usage = "usage: %prog [options] list [list_options]"
    description = inspect.getdoc(cmd_list)
    parser = OptionParser(usage=usage,description=description)
    (options, args) = parser.parse_args(argv)

    for f in os.listdir(conf['root']):
        if os.path.isdir("{}/{}".format(conf['root'],f)):
            d = dabus.build.Buildenv(name=f)
            if d.exists():
                logger.warning(" * {} ".format(f))

def cmd_build(conf, argv):
    """
    Build packages inside existing environments
    """
    usage = "usage: %prog [options] build [build_options]"
    description = inspect.getdoc(cmd_build)
    parser = OptionParser(usage=usage,description=description)
    parser.add_option("-E","--emptytree", action="store_true", dest="emptytree",
        default=False, help="File with packages")
    parser.add_option("-f","--file", action="store", dest="filename",
        default=[], help="File with packages")
    parser.add_option("-e","--env", action="store", dest="buildenv",
        default=[], help="Build environment")
    (options, args) = parser.parse_args(argv)

    if not options.buildenv:
        raise CommandlineArgumentError("You need to specify a build environment")

    packages = []

    if options.filename:
        with open(options.filename, 'r') as f:
            for package in f.readlines():
                packages.append(package)
    if args:
        for package in args:
            packages.append(package)

    if not packages:
        raise CommandlineArgumentError("No packages specified")

    d = dabus.build.Buildenv(name=options.buildenv)
    d.build(packages=packages, clean=options.emptytree)

def cmd_create(conf, argv):
    """
    Create new build environments
    """
    usage = "usage: %prog [options] create [create_options] name"
    description = inspect.getdoc(cmd_create)
    parser = OptionParser(usage=usage,description=description)
    parser.add_option("-a","--arch", action="store", dest="arch",
        help="Specify env arch")
    (options, args) = parser.parse_args(argv)
    if not args:
        raise CommandlineArgumentError("You need at least one name for a buildenv")

    if not options.arch:
        raise CommandlineArgumentError("You need to define an architecture")

    for arg in args:
        d = dabus.build.Buildenv(name=arg, arch=options.arch)
        if not d.exists():
            d.create()
        else:
            raise CreateException("Environment already exists")

def cmd_delete(conf,argv):
    """
    Delete existing environments
    """
    usage = "usage: %prog [options] delete [delete_options]"
    description = inspect.getdoc(cmd_delete)
    parser = OptionParser(usage=usage,description=description)
    parser.add_option("-c","--config", action="store_true", dest="config",
        default=False, help="Delete configuration")
    (options, args) = parser.parse_args(argv)

    if not args:
        raise CommandlineArgumentError("You need to define at least one environement")

    for arg in args:
        d = dabus.build.Buildenv(name=arg)
        if d.exists():
            d.delete(options.config)

def cmd_pack(conf, argv):
    """
    Create stage4 images from existing environments
    """
    usage = "usage: %prog [options] pack [pack_options] name"
    description = inspect.getdoc(cmd_pack)
    parser = OptionParser(usage=usage,description=description)
    parser.add_option("-o","--output", action="store", dest="output",
        default=None,help="output configuration")
    (options, args) = parser.parse_args(argv)
    if not args or len(args) > 1:
        raise CommandlineArgumentError("You need to specify exactly one buildenv")

    for arg in args:
        d = dabus.build.Buildenv(name=arg)
        if not d.exists():
            raise CommandlineArgumentError("Unkonwn environment {}".format(arg))
        else:
            fname = "{}-{}.tar.bz2".format(d.name, datetime.now().strftime("%Y%m%d"))
            if options.output:
                fname = os.path.join(options.output, fname) if os.path.isdir(options.output) else options.output

            s = dabus.stages.Stage4(arg)
            s.pack(fname)

def cmd_help(conf, argv):
    """
    List available commands
    """
    usage = "usage: %prog [options] help [help_options] [command_name]"
    description = inspect.getdoc(cmd_help)
    parser = OptionParser(usage=usage,description=description)
    (options, args) = parser.parse_args(argv)


    import dabus.util
    cmds = dabus.util.discover_commands()
    if len(args) == 1:
        try:
            cmds[argv[0]]({}, ['--help'])
        except KeyError:
            raise Exception("Command not found")

    logger.info("Available commands:")

    for k in sorted(cmds.keys()):
        logger.info("  {:16}\t{}".format(k, inspect.getdoc(cmds[k])))
