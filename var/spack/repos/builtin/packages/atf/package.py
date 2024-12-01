# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Atf(AutotoolsPackage):
    """ATF, or Automated Testing Framework, is a collection of libraries
    to write test programs in C, C++ and POSIX shell."""

    homepage = "https://github.com/jmmv/atf"
    url = "https://github.com/jmmv/atf/archive/atf-0.21.tar.gz"

    license("BSD-2-Clause AND BSD-3-Clause", checked_by="tgamblin")

    version("0.21", sha256="da6b02d6e7242f768a7aaa7b7e52378680456e4bd9a913b6636187079c98f3cd")
    version("0.20", sha256="3677cf957d7f574835b8bdd385984ba928d5695b3ff28f958e4227f810483ab7")
    version("0.19", sha256="f9b1d76dad7c34ae61a75638edc517fc05b10fa4c8f97b1d13d739bffee79b16")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
