# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libquo(AutotoolsPackage):
    """QUO (as in "status quo") is a runtime library that aids in accommodating
    thread-level heterogeneity in dynamic, phased MPI+X applications comprising
    single- and multi-threaded libraries."""

    homepage = "https://github.com/lanl/libquo"
    url = "https://lanl.github.io/libquo/dists/libquo-1.4.tar.gz"
    git = "https://github.com/lanl/libquo.git"

    maintainers("samuelkgutierrez")

    tags = ["e4s"]

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.4", sha256="82395148cdef43c37ef018672307316951e55fc6feffce5ab9b412cfafedffcb")
    version("1.3.1", sha256="407f7c61cc80aa934cf6086f3516a31dee3b803047713c297102452c3d7d6ed1")
    version("1.3", sha256="61b0beff15eae4be94b5d3cbcbf7bf757659604465709ed01827cbba45efcf90")
    version("1.2.9", sha256="0a64bea8f52f9eecd89e4ab82fde1c5bd271f3866c612da0ce7f38049409429b")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    depends_on("m4", when="@develop", type="build")
    depends_on("autoconf", when="@develop", type="build")
    depends_on("automake", when="@develop", type="build")
    depends_on("libtool", when="@develop", type="build")

    @when("@develop")
    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen")

    def configure_args(self):
        config_args = [
            "CC={0}".format(self.spec["mpi"].mpicc),
            "FC={0}".format(self.spec["mpi"].mpifc),
        ]
        if self.spec.satisfies("%pgi"):
            config_args.append("CFLAGS={0}".format(self.compiler.cc_pic_flag))
            config_args.append("FCFLAGS={0}".format(self.compiler.fc_pic_flag))
        return config_args
