# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vite(CMakePackage):
    """ViTE is a trace explorer. It is a tool to visualize execution
    traces in Paje or OTF2 format for debugging and profiling parallel or
    distributed applications.
    """

    homepage = "https://solverstack.gitlabpages.inria.fr/vite/"
    maintainers("trahay")
    git = "https://gitlab.inria.fr/solverstack/vite.git"

    license("CECILL-2.0")

    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type="build")
    depends_on("qt+opengl")
    depends_on("glm")
    depends_on("glew")
    depends_on("otf2", when="+otf2")
    depends_on("tau", when="+tau")

    variant("tau", default=False, description="Support for TAU trace format")
    variant("otf2", default=False, description="Support for OTF2 trace format")

    def cmake_args(self):
        args = [
            self.define("USE_QT5", True),
            self.define("USE_OPENGL", True),
            self.define("USE_VBO", False),
            self.define_from_variant("VITE_ENABLE_OTF2", "otf2"),
            self.define_from_variant("VITE_ENABLE_TAU", "tau"),
        ]
        return args
