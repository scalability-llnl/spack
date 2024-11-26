# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TestsSos(AutotoolsPackage):
    """Sandia OpenSHMEM unit tests and performance testing suite."""

    homepage = "https://github.com/openshmem-org/tests-sos"
    url = "https://github.com/openshmem-org/tests-sos/archive/refs/tags/v1.5.2.tar.gz"

    maintainers("jack-morrison")

    version("1.5.2", sha256="3a063963ef779419aadc6b21ff2f1e4dcdd3e95fa8ed23545434e56757f3187f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("sos", type=("build", "run"))

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def setup_build_environment(self, env):
        env.set("CC", "oshcc")
        env.set("CXX", "oshc++")
        env.set("FC", "oshfort")
