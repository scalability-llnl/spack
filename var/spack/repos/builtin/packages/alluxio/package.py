# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
    url = "https://downloads.alluxio.io/downloads/files/2.2.1/alluxio-2.2.1-bin.tar.gz"
    list_url = "https://downloads.alluxio.io/downloads/files"
    list_depth = 1

    license("CC0-1.0")

    version("309", sha256="50e031ebc4de257f5676eb8b33029c3017a2c7d6864a0f5fbc68210963a8c3e1")
    version("2.9.3", sha256="c71abc5e852d37cfd6b1dea076f056c6997e3f60fbb940bf005acb3a6354a369")
    version("2.9.1", sha256="e9456db7a08488af22dee3a44e4135bc03a0444e31c7753bf00f72465f68ffb9")

    # https://nvd.nist.gov/vuln/detail/CVE-2022-23848
    version(
        "2.7.2",
        sha256="e428acfe0704cc68801ae2aa7b7ba920a0e35af9dded66b280649fc1d280a3d4",
        deprecated=True,
    )
    version(
        "2.2.1",
        sha256="0c6b0afcc4013437afb8113e1dfda9777561512269ea349c7fbf353dc0efd28a",
        deprecated=True,
    )
    version(
        "2.2.0",
        sha256="635847ea1a0f8ad04c99518620de035d4962fbfa9e5920bb0911ccf8e5ea82fc",
        deprecated=True,
    )

    depends_on("java@8", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)
