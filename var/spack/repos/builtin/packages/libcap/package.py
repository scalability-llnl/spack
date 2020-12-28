# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcap(MakefilePackage):
    """Libcap implements the user-space interfaces to the POSIX 1003.1e
    capabilities available in Linux kernels. These capabilities are a
    partitioning of the all powerful root privilege into a set of
    distinct privileges."""

    homepage = "https://sites.google.com/site/fullycapable/"
    url      = "https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/libcap-2.25.tar.gz"

    version('2.25', sha256='4ca80dc6f9f23d14747e4b619fd9784434c570e24a7346f326c692784ed83a86')

    patch('libcap-fix-the-libcap-native-building-failure-on-CentOS-6.7.patch')

    def install(self, spec, prefix):
        make_args = [
            'RAISE_SETFCAP=no',
            'lib=lib',
            'prefix={0}'.format(prefix),
            'install'
        ]
        make(*make_args)

        chmod = which('chmod')
        chmod('+x', join_path(prefix.lib, 'libcap.so'))
