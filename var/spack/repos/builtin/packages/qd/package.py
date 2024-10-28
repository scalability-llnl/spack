# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qd(AutotoolsPackage):
    """C++/Fortran-90 double-double and quad-double package.
    With modifications for easier integration with NJet.
    see http://crd-legacy.lbl.gov/~dhbailey/mpdist/ for authors page"""

    homepage = "https://bitbucket.org/njet/qd-library/src/master/"
    git = "https://bitbucket.org/njet/qd-library.git"
    url = "https://www.davidhbailey.com/dhbsoftware/qd-2.3.13.tar.gz"

    tags = ["hep"]

    license("BSD-3-Clause-LBNL")
    version("2.3.24", sha256="a47b6c73f86e6421e86a883568dd08e299b20e36c11a99bdfbe50e01bde60e38")
    version("2.3.23", sha256="b3eaf41ce413ec08f348ee73e606bd3ff9203e411c377c3c0467f89acf69ee26")
    # The sha256 for 2.3.23 and 2.3.13 are identical as they are the same content
    version("2.3.13", sha256="b3eaf41ce413ec08f348ee73e606bd3ff9203e411c377c3c0467f89acf69ee26")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def setup_build_environment(self, env):
        if self.spec.satisfies("%nvhpc"):
            env.append_flags("FCFLAGS", "-fPIC")

    def configure_args(self):
        args = ["--enable-shared"]
        return args
