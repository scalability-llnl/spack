# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rsl(AutotoolsPackage):
    """This library is an object oriented programming environment for writing
    software applicable to all RADAR data related to the TRMM GV effort."""

    homepage = "https://trmm-fc.gsfc.nasa.gov/trmm_gv/software/rsl/"
    url = "https://trmm-fc.gsfc.nasa.gov/trmm_gv/software/rsl/software/rsl-v1.50.tar.gz"

    license("LGPL-2.0-only")

    version("1.50", sha256="9e4e3fe45eb1e4aebea63255d4956b00eb69527044a83f182cde1b43510bd342")

    depends_on("c", type="build")  # generated

    depends_on("bzip2")
    depends_on("jpeg")
    depends_on("zlib-api")
    depends_on("rpc")

    def configure_args(self):
        config_args = [
            "LDFLAGS={0}".format(self.spec["rpc"].libs.ld_flags),
            "CPPFLAGS={0}".format(self.spec["rpc"].headers.cpp_flags),
        ]

        return config_args
