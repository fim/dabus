
import os
import sys
import StringIO

#import dabus.arch
import dabus.config

class MakeConf(dabus.config.ConfigParser):

    def _load_defaults(self):
        self.conf = {
                'CFLAGS': ['-O2', '-pipe'],
                'CXXFLAGS': '${CFLAGS}',
                #'CHOST':  '{0}-pc-linux-gnu'.format(march),
                'VIDEO_CARDS': '',
                'USE': ['acpi', 'mmx', 'sse', 'sse2'],
                'FEATURES': ['parallel-fetch', '-preserve-libs', 'parallel-fetch', 'buildpkg'],
                'PYTHON_TARGETS': ['python2_7'],
                'ACCEPT_LICENSE': '*',
                'ACCEPT_PROPERTIES': ['*', '-interactive'],
                'INPUT_DEVICES': '',
                'RUBY_TARGETS': ['ruby18', 'ruby19'],
            }

    def _normalize_key(self, key):
        return key.upper()

   
