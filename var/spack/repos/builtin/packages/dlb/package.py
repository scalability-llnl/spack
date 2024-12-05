# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dlb(AutotoolsPackage):
    """DLB is a dynamic library designed to speed up HPC hybrid applications
    (i.e., two levels of parallelism) by improving the load balance of the
    outer level of parallelism (e.g., MPI) by dynamically redistributing the
    computational resources at the inner level of parallelism (e.g., OpenMP).
    at run time."""

    homepage = "https://pm.bsc.es/dlb"
    url = "https://pm.bsc.es/ftp/dlb/releases/dlb-3.2.tar.gz"
    git = "https://github.com/bsc-pm/dlb.git"

    maintainers("vlopezh")

    license("LGPL-3.0-or-later")

    version("main", branch="main")
    version("3.4.1", sha256="7c071b75c126f8e77c1a30369348751624d5636edcbd663bf3d41fa04733c894")
    version("3.4", sha256="6091d032c11a094a3ce0bec11c0a164783fdff83cb4ec870c9d8e192410c353a")
    version("3.3.1", sha256="1b245acad80b03eb83e815fd59dcfc598cfddd899de4504cf6a9572fe5359f40")
    version("3.3", sha256="55b87aea14f3954d8878912f3134938db235e6984fae26fdf5134148007eb722")
    version("3.2", sha256="b1c65ce3179b5275cfdf0bf921c0565a4a3ebcfdab72d7cef014957c17136c7e")
    version("3.1", sha256="d63ee89429fdb54af5510ed956f86d11561911a7860b46324f25200d32d0d333")
    version("3.0.2", sha256="75b6cf83ea24bb0862db4ed86d073f335200a0b54e8af8fee6dcf32da443b6b8")
    version("3.0.1", sha256="04f8a7aa269d02fc8561d0a61d64786aa18850367ce4f95d086ca12ab3eb7d24")
    version("3.0", sha256="e3fc1d51e9ded6d4d40d37f8568da4c4d72d1a8996bdeff2dfbbd86c9b96e36a")

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    variant("debug", default=False, description="Build additional debug libraries")
    variant("mpi", default=True, description="Build MPI libraries")
    variant("hwloc", default=True, description="Enable HWLOC support")
    variant("papi", default=True, description="Enable PAPI support")

    depends_on("mpi", when="+mpi")
    depends_on("hwloc", when="+hwloc")
    depends_on("papi", when="@3.4: +papi")
    depends_on("python", type="build")
    depends_on("autoconf", type="build", when="@main")
    depends_on("automake", type="build", when="@main")
    depends_on("libtool", type="build", when="@main")

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable("debug"))
        args.extend(self.enable_or_disable("instrumentation-debug", variant="debug"))
        args.extend(self.with_or_without("mpi"))
        args.extend(self.with_or_without("hwloc"))
        if self.spec.satisfies("@3.4:"):
            args.extend(self.with_or_without("papi"))

        return args
