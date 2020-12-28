# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bubblewrap(AutotoolsPackage):
    """Unprivileged sandboxing tool"""

    homepage = "https://github.com/containers/bubblewrap"
    url      = "https://github.com/containers/bubblewrap/archive/v0.4.0.tar.gz"

    version('0.4.0', sha256='dedea228f53dd5f589d8225b4584a9b354849a221caf7304874ca2e4d4bcdafb')
    version('0.3.3', sha256='439e4cd84d9d19c9e5b0c6aa0f0c3a55bbb893ae5ec112a5b575eadd2165f039')
    version('0.3.2', sha256='c66c1b6da3257e06b38a339611e76b21dc52a47975d55429071c22455259d010')
    version('0.3.1', sha256='3757cb021d1a3ccc36828a58363817e1923c458ed03260d0c2b3a99da61bfb81')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('libcap')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('autogen.sh')
