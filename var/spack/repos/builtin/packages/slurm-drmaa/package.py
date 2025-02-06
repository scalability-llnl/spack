# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SlurmDrmaa(AutotoolsPackage):
    """
    DRMAA for Slurm is an implementation of Open Grid Forum DRMAA 1.0 (Distributed
    Resource Management Application API) specification for submission and control of
    jobs to Slurm.  Using DRMAA, grid applications builders, portal developers and
    ISVs can use the same high-level API to link their software with different
    cluster/resource management systems.
    """

    homepage = "https://github.com/natefoo/slurm-drmaa"
    url = "https://github.com/natefoo/slurm-drmaa/releases/download/1.1.2/slurm-drmaa-1.1.2.tar.gz"
    git = "https://github.com/natefoo/slurm-drmaa.git"

    maintainers("pwablito")

    license("GPL-3.0-or-later")

    version("main", branch="main", submodules=True)
    version("1.1.2", sha256="5bfe25d501de83729df3c8c8f28535b9da3e99aea7738e259903abd6f1f5c836")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build", when="@main")
    depends_on("automake", type="build", when="@main")
    depends_on("libtool", type="build", when="@main")
    depends_on("bison", type="build", when="@main")

    depends_on("slurm")
    depends_on("slurm@:20-11-8-1", when="@1.1.2")
    depends_on("gperf")
    depends_on("ragel")

    def check(self):
        pass
