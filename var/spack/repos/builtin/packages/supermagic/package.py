# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Supermagic(AutotoolsPackage):
    """Supermagic is a very simple MPI sanity code. Nothing more, nothing less."""

    homepage = "https://hpc.github.io/supermagic"
    url = "https://hpc.github.io/supermagic/dists/supermagic-1.2.tar.gz"
    git = "https://github.com/hpc/supermagic.git"

    maintainers("marcodelapierre")

    version("master", branch="master")
    version("1.2", sha256="f8f6e0f74a58400d8d3c6b95c4b943aa8608e15a318fcfe12fc9abb008aed734")

    depends_on("mpi")

    depends_on("autoconf", when="@master", type="build")
    depends_on("automake", when="@master", type="build")
    depends_on("libtool", when="@master", type="build")

    @when("@master")
    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen")

    def configure_args(self):
        config_args = ["CC={0}".format(self.spec["mpi"].mpicc)]
        return config_args
