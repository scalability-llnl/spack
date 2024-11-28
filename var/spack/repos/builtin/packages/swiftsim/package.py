# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

from spack.package import *


class Swiftsim(AutotoolsPackage):
    """SPH With Inter-dependent Fine-grained Tasking (SWIFT) provides
    astrophysicists with a state of the art framework to perform
    particle based simulations.
    """

    homepage = "http://icc.dur.ac.uk/swift/"
    url = "https://gitlab.cosma.dur.ac.uk/api/v4/projects/swift%2Fswiftsim/repository/archive.tar.gz?sha=v0.9.0"

    license("GPL-3.0-only")

    version("0.9.0", sha256="5b4477289c165838c3823ef47a2a94eff7129927babbf5eb8785f8e4bf686117")
    version("0.7.0", sha256="d570e83e1038eb31bc7ae95d1903a2371fffbca90d08f60b6b32bb0fd8a6f516")
    version("0.3.0", sha256="dd26075315cb2754dc1292e8d838bbb83739cff7f068a98319b80b9c2b0f84bc")

    depends_on("c", type="build")  # generated

    variant("mpi", default=True, description="Enable distributed memory parallelism")

    # Build dependencies
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    # link-time / run-time dependencies
    # gsl is optional, but strong compiler settings choke on function without retval:
    depends_on("gsl")
    depends_on("mpi", when="+mpi")
    depends_on("metis")
    depends_on("hdf5~mpi", when="~mpi")
    depends_on("hdf5+mpi", when="+mpi")

    def setup_build_environment(self, env):
        # Needed to be able to download from the Durham gitlab repository
        tty.warn('Setting "GIT_SSL_NO_VERIFY=1"')
        tty.warn("This is needed to clone SWIFT repository")
        env.set("GIT_SSL_NO_VERIFY", 1)

    def configure_args(self):
        return [
            "--enable-mpi" if "+mpi" in self.spec else "--disable-mpi",
            "--with-metis={0}".format(self.spec["metis"].prefix),
            "--disable-dependency-tracking",
            "--enable-optimization",
            "--enable-compiler-warnings=yes",
        ]
