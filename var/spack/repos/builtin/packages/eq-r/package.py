# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class EqR(AutotoolsPackage):
    """
    EMEWS Queues for R (EQ/R)
    Installs EQ/R.
    """

    homepage = "http://emews.org"
    url = "https://github.com/emews/EQ-R/archive/1.0.tar.gz"
    git = "https://github.com/emews/EQ-R.git"

    version("master", branch="master")

    version("1.0", sha256="68047cb0edf088eaaefc5e36cefda9818292e5c832593e10a1dd9c73c27661b6")

    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("mpi")
    depends_on("r-rinside")
    depends_on("r-rcpp")
    depends_on("r")
    depends_on("tcl")
    depends_on("swig")

    configure_directory = "src"

    def setup_build_environment(self, env):
        spec = self.spec
        env.set("CC", spec["mpi"].mpicc)
        env.set("CXX", spec["mpi"].mpicxx)
        env.set("CXXLD", spec["mpi"].mpicxx)

    def configure_args(self):
        args = ["--with-tcl=" + self.spec["tcl"].prefix]
        r_location = "{0}/rlib/R".format(self.spec["r"].prefix)
        if not os.path.exists(r_location):
            rscript = which("Rscript")
            if rscript is not None:
                r_location = rscript("-e", "cat(R.home())", output=str)
            else:
                msg = "couldn't locate Rscript on your PATH"
                raise RuntimeError(msg)
        args.append("--with-r={0}".format(r_location))
        return args
