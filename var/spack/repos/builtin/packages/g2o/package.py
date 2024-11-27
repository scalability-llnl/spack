# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class G2o(CMakePackage):
    """g2o is an open-source C++ framework for optimizing graph-based nonlinear
    error functions.

    g2o has been designed to be easily extensible to a wide range of problems
    and a new problem typically can be specified in a few lines of code. The
    current implementation provides solutions to several variants of SLAM and
    BA."""

    homepage = "https://openslam-org.github.io/g2o.html"
    url = "https://github.com/RainerKuemmerle/g2o/archive/20200410_git.tar.gz"
    git = "https://github.com/RainerKuemmerle/g2o.git"

    version("master", branch="master")
    version(
        "20200410_git", sha256="b79eb1407ae7f2a9e6a002bb4b41d65402c185855db41a9ef4a6e3b42abaec4c"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type="build")
    depends_on("eigen@2.91.0:", type="link")
    depends_on("ceres-solver")
    depends_on("freeglut")
    depends_on("suite-sparse")
    depends_on("qt@5:+gui+opengl")
    depends_on("libqglviewer")

    def cmake_args(self):
        return [
            "-DBUILD_CSPARSE=OFF",
            "-DCSPARSE_INCLUDE_DIR=" + self.spec["suite-sparse:cxsparse"].headers.directories[0],
            "-DCSPARSE_LIBRARY=" + self.spec["suite-sparse:cxsparse"].libs[0],
            "-DQGLVIEWER_INCLUDE_DIR=" + self.spec["libqglviewer"].prefix.include.QGLViewer,
        ]

    @run_after("install")
    def darwin_fix(self):
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)
