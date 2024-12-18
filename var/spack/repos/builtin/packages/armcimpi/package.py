# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Armcimpi(AutotoolsPackage):
    """ARMCI-MPI is an implementation of the ARMCI library used by Global Arrays.
    MPI-3 one-sided communication is used to implement ARMCI.
    """

    homepage = "https://github.com/pmodels/armci-mpi"
    url = "https://github.com/pmodels/armci-mpi/archive/refs/tags/v0.4.tar.gz"

    maintainers("jeffhammond")

    license("BSD-3-Clause", checked_by="jeffhammond")

    version("0.4", sha256="bcc3bb189b23bf653dcc69bc469eb86eae5ebc5ad94ab5f83e52ddbdbbebf1b1")
    version(
        "0.3.1-beta", sha256="f3eaa8f365fb55123ecd9ced401086b0732e37e4df592b27916d71a67ab34fe9"
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Builds a shared version of the library")
    variant("progress", default=False, description="Enable asynchronous progress")

    provides("armci")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("mpi")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = ["--enable-g"]
        args.extend(self.enable_or_disable("shared"))
        args.extend(self.with_or_without("progress"))
        return args

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("ARMCIMPI_DIR", self.prefix)
