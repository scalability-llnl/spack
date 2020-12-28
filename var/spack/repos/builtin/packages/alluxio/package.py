# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Alluxio(Package):
    """Alluxio (formerly known as Tachyon) is a virtual distributed storage
    system. It bridges the gap between computation frameworks and storage
    systems, enabling computation applications to connect to numerous
    storage systems through a common interface."""

    homepage = "https://www.alluxio.io"
    url      = "https://downloads.alluxio.io/downloads/files/2.2.1/alluxio-2.2.1-bin.tar.gz"
    list_url = "https://downloads.alluxio.io/downloads/files"
    list_depth = 1

    version('2.2.1', sha256='0c6b0afcc4013437afb8113e1dfda9777561512269ea349c7fbf353dc0efd28a')
    version('2.2.0', sha256='635847ea1a0f8ad04c99518620de035d4962fbfa9e5920bb0911ccf8e5ea82fc')

    depends_on('java@8', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix)
