# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gnds(CMakePackage):
    """The GNDS package is an implementation of the OECD specifications for the
    Generalized Nuclear Database Structure used in the AMPX cross section
    processing code.
    """

    homepage = "https://code.ornl.gov/RNSD/gnds"
    url = "https://code.ornl.gov/RNSD/gnds/-/archive/v0.0.1/gnds-v0.0.1.tar.gz"

    version("0.0.1", sha256="4c8faaa01a3e6fb08ec3e8e126a76f75b5442509a46b993e325ec79dd9f04879")

    depends_on("cxx", type="build")

    variant("shared", default=True, description="Build shared libraries")

    depends_on("pugixml")

    def cmake_args(self):
        args = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
        return args
