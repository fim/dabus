"""
Map subarch to arch
"""
#!/usr/bin/env python

ARCH = {

    ####################
    # alpha

    'alpha': 'alpha',
    'ev4': 'alpha',
    'ev45': 'alpha',
    'ev5': 'alpha',
    'ev56': 'alpha',
    'ev6': 'alpha',
    'ev67': 'alpha',
    'pca56': 'alpha',

    ####################
    # amd64

    'amd64': 'amd64',
    'amdfam10': 'amd64',
    'athlon64': 'amd64',
    'athlon64-sse3': 'amd64',
    'athlonfx': 'amd64',
    'barcelona': 'amd64',
    'core2': 'amd64',
    'k8': 'amd64',
    'k8-sse3': 'amd64',
    'nocona': 'amd64',
    'opteron': 'amd64',
    'opteron-sse3': 'amd64',

    ####################
    # arm

    'arm': 'arm',
    'armeb': 'arm',
    'armv4l': 'arm',
    'armv4tl': 'arm',
    'armv5teb': 'arm',
    'armv5tejl': 'arm',
    'armv5tel': 'arm',
    'armv5tl': 'arm',
    'armv6j': 'arm',
    'armv6z': 'arm',
    'armv6zk': 'arm',
    'armv7a': 'arm',
    'armv7a_hardfp': 'arm',

    ####################
    # hppa

    'hppa': 'hppa',
    'hppa1.1': 'hppa',
    'hppa2.0': 'hppa',

    ####################
    # ia64

    'ia64': 'ia64',

    ####################
    # mips

    'cobalt': 'mips',
    'loongson2e': 'mips',
    'loongson2f': 'mips',
    'mips': 'mips',
    'mips1': 'mips',
    'mips3': 'mips',
    'mips32': 'mips',
    'mips32el': 'mips',
    'mips4': 'mips',
    'mips64': 'mips',
    'mips64el': 'mips',
    'mipsel': 'mips',
    'mipsel1': 'mips',
    'mipsel3': 'mips',
    'mipsel4': 'mips',

    ####################
    # mips64

    'cobalt_n32': 'mips64',
    'loongson2e_n32': 'mips64',
    'loongson2f_n32': 'mips64',
    'mips3_multilib': 'mips64',
    'mips3_n32': 'mips64',
    'mips3_n64': 'mips64',
    'mips4_multilib': 'mips64',
    'mips4_n32': 'mips64',
    'mips4_n64': 'mips64',
    'mips64_multilib': 'mips64',
    'mips64_n32': 'mips64',
    'mips64_n64': 'mips64',
    'mips64el_multilib': 'mips64',
    'mips64el_n32': 'mips64',
    'mips64el_n64': 'mips64',
    'mipsel3_multilib': 'mips64',
    'mipsel3_n32': 'mips64',
    'mipsel3_n64': 'mips64',
    'mipsel4_multilib': 'mips64',
    'mipsel4_n32': 'mips64',
    'mipsel4_n64': 'mips64',

    ####################
    # ppc

    'g3': 'ppc',
    'g4': 'ppc',
    'g5': 'ppc',
    'power': 'ppc',
    'power-ppc': 'ppc',
    'ppc': 'ppc',

    ####################
    # ppc64

    '970': 'ppc64',
    'cell': 'ppc64',
    'power3': 'ppc64',
    'power4': 'ppc64',
    'power5': 'ppc64',
    'power6': 'ppc64',
    'ppc64': 'ppc64',

    ####################
    # s390

    's390': 's390',

    ####################
    # s390x

    's390x': 's390x',

    ####################
    # sh

    'sh': 'sh',
    'sh2': 'sh',
    'sh2a': 'sh',
    'sh2aeb': 'sh',
    'sh2eb': 'sh',
    'sh3': 'sh',
    'sh3eb': 'sh',
    'sh4': 'sh',
    'sh4a': 'sh',
    'sh4aeb': 'sh',
    'sh4eb': 'sh',
    'sheb': 'sh',

    ####################
    # sparc

    'sparc': 'sparc',

    ####################
    # sparc64

    'sparc64': 'sparc64',

    ####################
    # x86

    'athlon': 'x86',
    'athlon-4': 'x86',
    'athlon-mp': 'x86',
    'athlon-tbird': 'x86',
    'athlon-xp': 'x86',
    'i386': 'x86',
    'i486': 'x86',
    'i586': 'x86',
    'i686': 'x86',
    'k6': 'x86',
    'k6-2': 'x86',
    'k6-3': 'x86',
    'pentium': 'x86',
    'pentium-m': 'x86',
    'pentium-mmx': 'x86',
    'pentium2': 'x86',
    'pentium3': 'x86',
    'pentium3m': 'x86',
    'pentium4': 'x86',
    'pentium4m': 'x86',
    'pentiumpro': 'x86',
    'prescott': 'x86',
    'x86': 'x86',
}

