# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RdmaCore(CMakePackage):
    """RDMA core userspace libraries and daemons"""

    homepage = "https://github.com/linux-rdma/rdma-core"
    url      = "https://github.com/linux-rdma/rdma-core/releases/download/v17.1/rdma-core-17.1.tar.gz"

    version('32.0', sha256='8197e20a59990b9b06a2e4c83f4a96802fc080ec1669392b643b59b6023931fc')
    version('31.0', sha256='51ae9a3ab81cd6834436813fafc310c8b7007feae9d09a53fdd5c169e648d50b')
    version('30.0', sha256='23e1bd2d7b38149a1621ee577a3428ac652e305adb8e0eee923cbe71356a9bf9')
    version('28.1', sha256='d9961fd9b0867f17cb6a30a728562f00528b63dd72d1168d838220ab44e5c713')
    version('27.1', sha256='39eeb3ab5f868ef3a5f7623d1ee69adca04efabe2a37de8080f354b8f4ef0ad7')
    version('26.2', sha256='115087ab438bea3530a0d520640f1eeb5872b902ee2263acf83dcc7835d296c6')
    version('25.4', sha256='f622491b0aac819f05c73174e0c7a9e630cc02fc0914d5ba1bb1d87fc4d313fd')
    version('24.3', sha256='3a02d2d864258acc763849c635c815e3fa6a798a1464511cd3a2a370ddd6ee89')
    version('23.4', sha256='6bfe009e9a382085def3b004d9396f7255a2e0c90c36647d1df0b86773d21a79')
    version('20', sha256='bc846989f807cd2b03643927d2b99fbf6f849cb1e766ab49bc9e81ce769d5421')
    version('17.1', sha256='b47444b7c05d3906deb8771eec3e634984dd83f5e620d5e37d3a83f74f0cc1ba')
    version('13', sha256='e5230fd7cda610753ad1252b40a28b1e9cf836423a10d8c2525b081527760d97')

    depends_on('pkgconfig', type='build')
    depends_on('py-docutils', type='build')
    depends_on('libnl')
    conflicts('platform=darwin', msg='rdma-core requires FreeBSD or Linux')
    conflicts('%intel', msg='rdma-core cannot be built with intel (use gcc instead)')

# NOTE: specify CMAKE_INSTALL_RUNDIR explicitly to prevent rdma-core from
#       using the spack staging build dir (which may be a very long file
#       system path) as a component in compile-time static strings such as
#       IBACM_SERVER_PATH.
    def cmake_args(self):
        cmake_args = ["-DCMAKE_INSTALL_SYSCONFDIR=" +
                      self.spec.prefix.etc,
                      "-DCMAKE_INSTALL_RUNDIR=/var/run"]
        return cmake_args
