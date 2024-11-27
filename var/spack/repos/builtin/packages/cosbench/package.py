# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cosbench(Package):
    """
    COSBench is a benchmarking tool to measure the performance of
    Cloud Object Storage services. Object storage is an emerging
    technology that is different from traditional file systems
    (e.g., NFS) or block device systems (e.g., iSCSI). Amazon S3
    and Openstack* swift are well-known object storage solutions
    """

    homepage = "https://github.com/intel-cloud/cosbench"
    url = "https://github.com/intel-cloud/cosbench/releases/download/v0.4.2/0.4.2.zip"

    license("Apache-2.0")

    version("0.4.2", sha256="9e82518d4fac3c23cfac47c8a571d4a61bf8e5f11286606c79a0f923e983dc61")
    version("0.4.1.0", sha256="a044cd232b3cc376802aa6a4a697988ec690a8b1d70040641710066acd322c5a")
    version("0.4.0.1", sha256="384e4de218a9a61040f45cf9aa0a555e88ff25fb2b5cd11c540627cd604b4961")

    depends_on("java@6:", type="run")
    depends_on("curl@7.22.0:", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)
