# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GridlabD(AutotoolsPackage):
    """
    Autotools package for Gridlab-D, a new power distribution system simulation
    and analysis tool that provides valuable information to users who design
    and operate distribution systems, and to utilities that wish to take
    advantage of the latest energy technologies. Gridlab-D is a flexible
    simulation environment that can be integrated with a variety of third-party
    data management and analysis tools.
    """

    homepage = "https://www.gridlabd.org/"
    git = "https://github.com/gridlab-d/gridlab-d"

    maintainers("0t1s1", "yee29", "afisher1")

    # Using only develop as other branches and releases did not build properly.
    version("develop", branch="develop")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mysql", default=False, description="Enable MySQL support for Gridlab-D.")
    variant("helics", default=False, description="Enable Helics support for Gridlab-D.")

    # Add dependencies.
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("xerces-c")
    depends_on("superlu-mt")
    depends_on("helics", when="+helics")

    def configure_args(self):
        args = []

        if self.spec.satisfies("+helics"):
            # Taken from
            # https://github.com/GMLC-TDC/HELICS-Tutorial/tree/master/setup
            args.append("--with-helics=" + self.spec["helics"].prefix)
            args.append("CFLAGS=-g -O0 -w")
            args.append("CXXFLAGS=-g -O0 -w -std=c++14")
            args.append("LDFLAGS=-g -O0 -w")
            args.append("--with-xerces=" + self.spec["xerces-c"].prefix)

        return args

    def setup_run_environment(self, env):
        # Need to add GLPATH otherwise Gridlab-D will not run.
        env.set("GLPATH", join_path(self.prefix, "lib", "gridlabd"))
        env.prepend_path("GLPATH", join_path(self.prefix, "share", "gridlabd"))
