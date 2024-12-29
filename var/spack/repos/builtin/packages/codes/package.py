# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Codes(AutotoolsPackage):
    """CO-Design of multi-layer Exascale Storage (CODES) simulation framework"""

    homepage = "https://www.mcs.anl.gov/projects/codes"
    git = "https://xgitlab.cels.anl.gov/codes/codes.git"

    version("develop", branch="master")
    version("1.1.0", tag="1.1.0")
    version("1.0.0", tag="1.0.0")

    variant("dumpi", default=False, description="Enable DUMPI support")

    # Build dependencies
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("bison", type="build")
    depends_on("flex", type="build")

    depends_on("mpi")
    depends_on("ross")
    depends_on("sst-dumpi", when="+dumpi")

    # add the local m4 directory to the search path
    autoreconf_extra_args = ["-Im4"]
    # Testing if srcdir is '.' in configure.ac does not work with spack
    patch("codes-1.0.0.patch")

    def configure_args(self):
        spec = self.spec

        config_args = [
            "CC=%s" % spec["mpi"].mpicc,
            "CXX=%s" % spec["mpi"].mpicxx,
            "PKG_CONFIG_PATH=%s/pkgconfig" % spec["ross"].prefix.lib,
        ]

        if spec.satisfies("+dumpi"):
            config_args.extend(["--with-dumpi=%s" % spec["sst-dumpi"].prefix])

        return config_args
