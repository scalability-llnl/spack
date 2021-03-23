# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *
import llnl.util.tty as tty


class Rpm(AutotoolsPackage):
    """
    The RPM package manager
    https://github.com/rpm-software-management/rpm/blob/master/INSTALL
    Note that debugedit is an additional tool that *should* compile with
    adding libdw and elfutils, but the library (as of 4.16.1.2) is being
    removed from rpm and will be put somewhere else.
    """

    homepage = "https://github.com/rpm-software-management/rpm"
    url      = "https://github.com/rpm-software-management/rpm/archive/rpm-4.16.0-release.tar.gz"

    version('4.16.0', sha256='a62b744e3404b107e8467e1a36ff0f2bf9e5c1b748dbfeb36db54bbb859446ea')
    version('4.16.1.2', sha256='3d2807807a8ccaa92a8ced74e09b5bf5b2417a5bbf9bee4abc7c6aa497547bf3')

    variant('openssl', default=False, description='use openssl for cryptographic library')
    variant('sqlite', default=False, description='use sqlite instead of ndb')
    variant('bdb_ro', default=False, description='standalone support for read-only BDB databases')
    variant('selinux', default=False, description="enable support for SELinux")
    variant('python', default=False, description="build Python bindings to RPM library")
    variant('posix', default=False, description="enable POSIX.1e draft 15 file capabilities support")
    variant('gpg', default=False, description="install gpg for using cryptographic signatures")
    variant('openmp', default=True, description="OpenMP multithreading support")
    variant('docs', default=False, description='build documentation')

    # Always required
    depends_on('popt')

    # Without this file patch, we don't detect lua
    depends_on('lua+pcfile@5.3.5:')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')

    # Enable POSIX.1e draft 15 file capabilities support
    depends_on('libcap', when="+posix")
    depends_on('berkeley-db@4.5:')

    # Required for National Language Support, if not present autopoint error
    depends_on('gettext')
    depends_on('file')  # provides magic.h
    depends_on('libarchive')

    # suppot for cryptographic signatures
    depends_on('gnupg', when="+gpg")

    # cryptographic library to support digests and signatures
    depends_on('libgcrypt', when='-openssl')
    depends_on('openssl@1.0.2:', when='+openssl')

    # RPM needs some database, ndb requires no extra dependencies but sqlite does
    depends_on('sqlite@3.22.0:', when='+sqlite')

    # Python 2.x support is being deprecated
    depends_on('python@3.1:', when='+sqlite')

    # compression support
    depends_on('zlib')

    # Desired to install these formats for use
    depends_on('bzip2')
    depends_on('gzip')
    depends_on('xz')

    # java jar dependency analysis (already requirement for lua)
    depends_on('unzip', type='run')

    # Documentation dependencies
    depends_on('doxygen', type="build", when="+docs")

    def setup_build_environment(self, env):
        env.set('LIBS', self.spec['gettext'].libs.search_flags + ' -lintl')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh', '--noconfigure')

    def configure_args(self):
        spec = self.spec

        args = ["--enable-ndb"]

        pkg_config = os.path.join(spec['lua'].prefix.lib, "pkgconfig")
        os.environ['PKG_CONFIG_PATH'] = pkg_config
        os.putenv('PKG_CONFIG_PATH', pkg_config)

        # cryptography library defaults to libgcrypt, but doesn't hurt to specify
        if "+openssl" in spec:
            args.append("--with-crypto=openssl")
            tty.warning(openssl_warning)
        else:
            args.append("--with-crypto=libgcrypt")

        # Default to ndb (no deps) if sqlite not wanted
        if "+sqlite" in spec:
            args.append("--enable-sqlite")
        if "+bdb_ro" in spec:
            args.append("--bdb-ro")

        # Enable support for selinux
        if "+selinux" in spec:
            args.append('--with-selinux')
        if "+python" in spec:
            args.append("--enable-python")

        # enable POSIX.1e draft 15 file capabilities support
        if "+posix" in spec:
            args.append('--with-cap')

        # OpenMP multithreading support automatically enabled if C compiler has
        # support for OpenMP version 4.5 or higher
        if "~openmp" in spec:
            args.append("--disable-openmp")

        return args


# This warning is from the INSTALL about licensing when using openssl.
# We need to show it to the user if they choose the openssl variant.

openssl_warning = """
When compiling against OpenSSL, there is a possible license incompatibility.
For more details on this, see https://people.gnome.org/~markmc/openssl-and-the-gpl.html
Some Linux distributions have different legal interpretations of this
possible incompatibility. It is recommended to consult with a lawyer before
building RPM against OpenSSL.
Fedora: https://fedoraproject.org/wiki/Licensing:FAQ#What.27s_the_deal_with_the_OpenSSL_license.3F
Debian: https://lists.debian.org/debian-legal/2002/10/msg00113.html"""
