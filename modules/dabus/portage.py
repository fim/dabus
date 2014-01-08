class PortageException(Exception):
    pass

class Portage(object):

    def __init__(self, source="http://distfiles.gentoo.org/snapshots/portage-latest.tar.bz2"):
        if not source.endswith("tar.bz2"):
            raise PortageException("Unsupported source. File not bz2 tar archive")

        self.source = source


    def fetch(self):
        pass

    def pack(self):
        pass

    def unpack(self):
        pass
