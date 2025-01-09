# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Opendatadetector(CMakePackage):
    """Open Data Detector for High Energy Physics."""

    homepage = "https://gitlab.cern.ch/acts/OpenDataDetector.git"
    git = "https://gitlab.cern.ch/acts/OpenDataDetector.git"

    maintainers("vvolkl")

    tags = ["hep"]

    license("MPL-2.0-no-copyleft-exception")

    version("main", branch="main")
    version("v3.0.0", tag="v3.0.0", commit="e3b1eceae96fd5dddf10223753964c570ee868c9")
    version("v2", tag="v2", commit="7041ae086dff4ee4a8d5b65f5d9559acc6dbec47")
    version("v1", tag="v1", commit="81c43c6511723c13c15327479082d3dcfa1947c7")

    depends_on("cxx", type="build")  # generated

    depends_on("dd4hep")
    depends_on("root")
    depends_on("boost")

    def cmake_args(self):
        args = []
        args.append("-DCMAKE_CXX_STANDARD=%s" % self.spec["root"].variants["cxxstd"].value)
        return args

    def setup_run_environment(self, env):
        env.set("OPENDATADETECTOR_DATA", join_path(self.prefix.share, "OpenDataDetector"))
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib64)
