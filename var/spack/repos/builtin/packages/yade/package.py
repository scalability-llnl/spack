# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Yade(CMakePackage):
    """Yade is an free software for particle based simulations."""

    homepage = "https://gitlab.com/yade-dev/trunk"
    url = "https://gitlab.com/yade-dev/trunk/-/archive/2023.02a/trunk-2023.02a.tar.gz"

    maintainers("lmagdanello")

    license("GPL-2.0-only")

    version("2023.02a", sha256="f76b5a0aa7f202716efa94cd730e4bc442ffcb40a99caaf6e579ab8695efb0c1")
    version("2022.01a", sha256="3b76185b706aba6113d1e932c5b883cd772e8d8c6b4e5230a01f3370e2b6904c")
    version("2021.01a", sha256="3afab3380e8f5d185af7929213f63341445d6a5ee6bc21bbae102d8ffd93df1d")
    version("2020.01a", sha256="e4856aaa0141c32404355ce9de4f25076fe3940dbc8d0fdbc8ace8020c5191f1")
    version("2019.01a", sha256="7cb80b912cdc8752850de54ef3c084768c5ab69ce6af4b85dc3921674d7134a5")
    version("2018.02b", sha256="d1b2ed3751cd4661af1ad4058196adb16eb227845d874e1c221074a699876634")
    version("2018.02a", sha256="629a83ab71e2f47f2a7a83fd2c18ab5ce5573bf239445be0d4ff34ce08c11263")
    version("2017.01a", sha256="cd35caa6b6a017ee82f894e7d6f0826fddc1d921aea04b5896d3f1da95cb649b")
    version("2016.06a", sha256="6e7374d2dcb7c90026be9229a6b30373f9d82fdefd3dc1f952aa6262924f2579")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake", type="build")
    depends_on("gcc@11.4:", type=("build", "run"))
    depends_on("boost@1.47:", type=("build", "run"))
    depends_on("qt", type=("build", "run"))
    depends_on("freeglut", type=("build", "run"))
    depends_on("libqglviewer", type=("build", "run"))
    depends_on("python", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-ipython", type=("build", "run"))
    depends_on("py-sphinx", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("eigen@3.2.1:", type=("build", "run"))
    depends_on("gdb", type=("build", "run"))
    depends_on("sqlite", type=("build", "run"))

    def cmake_args(self):
        args = [self.define("CMAKE_BUILD_TYPE", "Release")]

        args.append("-DCMAKE_INSTALL_PREFIX={0}".format(self.stage.source_path))
        return args
