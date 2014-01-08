import os
import re
import tarfile
import urllib2

import dabus.arch

class UnknownCommandError(Exception):
    pass

class ExtractError(Exception):
    pass

class DownloadError(Exception):
    pass

def get_latest_stage3(arch, site="http://distfiles.gentoo.org", dest="."):
    """
    Download latest available stage3
    """
    try:
        march = dabus.arch.ARCH[arch]
        url = "{site}/releases/{march}/autobuilds/latest-stage3-{arch}.txt".format(site=site, march=march, arch=arch)
        stages = urllib2.urlopen(url).read()
    except KeyError,e:
        raise Exception("Unknown/unsupported arch: {}".format(arch))
    except Exception,e:
        raise Exception("Couldn't get latest stage3 for arch {}: {}".format(arch, e))

    stage = re.findall(".*-{}-\d+.*".format(arch), stages)[0]

    if stage:
        lf = download("{0}/releases/{1}/autobuilds/{2}".format(site, march, stage), filename='stage3-{}.tar.bz2'.format(arch), local=dest)
    else:
        raise Exception("Couldn't get a stage3 URL for arch {}".format(arch))
    return lf


def get_latest_portage(site="http://distfiles.gentoo.org", dest="."):
    """
    Download latest portage snapshot
    """
    return download("{}/snapshots/portage-latest.tar.bz2".format(site), filename='portage.tar.bz2', local=dest)

def extract(filename, path):
    """
    Create a directory and extract a stage 3 in it

    If dest dir doesn't exist, try to create it.
    """

    try:
        if not os.path.isdir(path):
            os.mkdir(path)

        t = tarfile.open(filename, 'r:bz2')
        t.extractall(path=path)
        t.close()
    except Exception,e:
        raise ExtractError("Couldn't extract file to destination {}: {}".format(filename, e))


def download(url, local="/tmp", filename=None, force=False):
    """
    Download remote file and save it locally
    """
    filename = filename or url.split('/')[-1]
    try:
        data = urllib2.urlopen(url).read()
    except Exception,e:
        raise DownloadError("Couldn't download file {}: {}".format(url,e))

    absfpath = "{0}/{1}".format(local,filename)
    if os.path.isfile(absfpath): return absfpath

    with open(absfpath, 'wb') as f:
        f.write(data)
    return absfpath

def discover_commands():
    """
    Inspect commands.py and find all available commands
    """
    import inspect
    from dabus import commands

    command_table = {}
    fns = inspect.getmembers(commands, inspect.isfunction)

    for name, fn in fns:
        if name.startswith("cmd_"):
            command_table.update({
                name.split("cmd_")[1]:fn
            })

    return command_table


def exec_command(command, *args, **kwargs):
    """
    Execute given command
    """
    commands = discover_commands()
    try:
        cmd_fn = commands[command]
    except KeyError:
        raise UnknownCommandError
    cmd_fn(*args,**kwargs)
