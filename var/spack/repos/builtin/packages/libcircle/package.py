# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcircle(AutotoolsPackage):
    """libcircle provides an efficient distributed queue on a cluster,
    using self-stabilizing work stealing."""

    homepage = "https://github.com/hpc/libcircle"
    git = "https://github.com/hpc/libcircle.git"
    url = (
        "https://github.com/hpc/libcircle/releases/download/0.2.1-rc.1/libcircle-0.2.1-rc.1.tar.gz"
    )

    version("master", branch="master")
    version(
        "0.3.0",
        sha256="5ce38eb5b3c2b394bca1316310758f276c893dd3f4c15d7bc14ea05d3110ce58",
        url="https://github.com/hpc/libcircle/releases/download/v0.3/libcircle-0.3.0.tar.gz",
    )
    version(
        "0.2.1-rc.1", sha256="5747f91cf4417023304dcc92fd07e3617ac712ca1eeb698880979bbca3f54865"
    )

    depends_on("c", type="build")  # generated

    depends_on("mpi")
    depends_on("pkgconfig", type="build")
    depends_on("libpciaccess", type="link")
    depends_on("autoconf", when="%cce", type="build")
    depends_on("automake", when="%cce", type="build")
    depends_on("libtool", when="%cce", type="build")

    patch("CrayPE_configure-ac.patch", when="%cce")

    @property
    def force_autoreconf(self):
        return self.spec.satisfies("%cce")

    @when("@master")
    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            # Bootstrap with autotools
            bash = which("bash")
            bash("./autogen.sh")
