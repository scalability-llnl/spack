# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Htop(AutotoolsPackage):
    """htop is an interactive text-mode process viewer for Unix systems."""

    homepage = "https://github.com/htop-dev/htop/"
    url = "https://github.com/htop-dev/htop/archive/refs/tags/3.2.1.tar.gz"
    maintainers("sethrj")

    license("GPL-2.0-or-later")

    version("3.3.0", sha256="1e5cc328eee2bd1acff89f860e3179ea24b85df3ac483433f92a29977b14b045")
    version("3.2.2", sha256="3829c742a835a0426db41bb039d1b976420c21ec65e93b35cd9bfd2d57f44ac8")
    version("3.2.1", sha256="b5ffac1949a8daaabcffa659c0964360b5008782aae4dfa7702d2323cfb4f438")
    version("3.2.0", sha256="1a1dd174cc828521fe5fd0e052cff8c30aa50809cf80d3ce3a481c37d476ac54")
    version("3.1.2", sha256="fe9559637c8f21f5fd531a4c072048a404173806acbdad1359c6b82fd87aa001")
    version("3.1.1", sha256="b52280ad05a535ec632fbcd47e8e2c40a9376a9ddbd7caa00b38b9d6bb87ced6")
    version("3.0.5", sha256="4c2629bd50895bd24082ba2f81f8c972348aa2298cc6edc6a21a7fa18b73990c")
    version(
        "2.2.0",
        sha256="d9d6826f10ce3887950d709b53ee1d8c1849a70fa38e91d5896ad8cbc6ba3c57",
        url="https://hisham.hm/htop/releases/2.2.0/htop-2.2.0.tar.gz",
    )
    version(
        "2.0.2",
        sha256="179be9dccb80cee0c5e1a1f58c8f72ce7b2328ede30fb71dcdf336539be2f487",
        url="https://hisham.hm/htop/releases/2.0.2/htop-2.0.2.tar.gz",
    )

    depends_on("c", type="build")  # generated

    variant("unicode", default=True, description="Enable Unicode support dependency")
    variant("hwloc", default=False, description="Enable hwloc support for CPU affinity")
    variant("debug", default=False, description="Enable asserts and internal sanity checks")

    depends_on("ncurses")
    depends_on("ncurses@6:", when="@3:")
    depends_on("m4", type="build", when="@3:")
    depends_on("autoconf", type="build", when="@3:")
    depends_on("automake", type="build", when="@3:")
    depends_on("libtool", type="build", when="@3:")
    depends_on("hwloc", when="+hwloc")
    depends_on("python+pythoncmd", type="build")

    def configure_args(self):
        args = []
        args += self.enable_or_disable("unicode")
        args += self.enable_or_disable("hwloc")
        args += self.enable_or_disable("debug")
        return args
