# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Stc(AutotoolsPackage):
    """STC: The Swift-Turbine Compiler"""

    homepage = "http://swift-lang.org/Swift-T"
    url = "https://swift-lang.github.io/swift-t-downloads/spack/stc-0.9.0.tar.gz"
    git = "https://github.com/swift-lang/swift-t.git"

    tags = ["e4s"]

    version("master", branch="master")
    version("0.9.0", sha256="edf187344ce860476473ab6599f042cd22ed029aa186d512135990accb9d260f")
    version("0.8.3", sha256="d61ca80137a955b12e84e41cb8a78ce1a58289241a2665076f12f835cf68d798")
    version("0.8.2", sha256="13f0f03fdfcca3e63d2d58d7e7dbdddc113d5b9826c9357ab0713b63e8e42c5e")

    depends_on("java@11", type=("build", "run"))
    depends_on("ant", type="build")
    depends_on("turbine", type=("build", "run"))
    depends_on("turbine@master", type=("build", "run"), when="@master")
    depends_on("zsh", type=("build", "run"))
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    @property
    def configure_directory(self):
        if self.version == Version("master"):
            return "stc/code"
        else:
            return "."

    def configure_args(self):
        args = ["--with-turbine=" + self.spec["turbine"].prefix]
        return args
