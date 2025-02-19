# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpibenchmark(AutotoolsPackage):
    """MadMPI benchmark.

    MadMPI benchmark is benchmark designed to assess the performance
    of MPI libraries using various metrics. It may be used to
    benchmark any MPI library.
    """

    homepage = "https://pm2.gitlabpages.inria.fr/mpibenchmark/"
    url = "https://pm2.gitlabpages.inria.fr/releases/mpibenchmark-0.5.tar.gz"
    list_url = "https://pm2.gitlabpages.inria.fr/releases/"
    git = "https://gitlab.inria.fr/pm2/pm2.git"

    maintainers("a-denis")
    license("GPL-2.0-or-later", checked_by="a-denis")

    version("master", branch="master")
    version("0.5", sha256="bba9e5aa8b58c041f89e4518a0a7f80a63ebfaf0f90bb8bdd0976d1bf22bed83")
    version("0.4", sha256="f3d562683bad29e00efae11a449596feacdef5f29cd4f1d60d01368adacece37")
    version("0.3", sha256="af82d48a0a00971c9294725ea6944b8683c12ab3b8203357379fa0969e61325f")
    version("0.2", sha256="b9b09f4cabd954e42adb3d7deb9af155eb8044f94206d59181e0173e3f3879d8")
    version("0.1", sha256="c556d2339c00c4e4644de2dbf2e314ec117dbd3ea67c2ff7ebe5ddc0598a654e")

    variant("optimize", default=True, description="Build in optimized mode")
    variant("debug", default=False, description="Build in debug mode")
    variant("asan", default=False, description="Build with Address Sanitizer (ASAN)")

    depends_on("c", type="build")
    depends_on("autoconf@2.69:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("gmake", type="build")
    depends_on("hwloc")
    depends_on("mpi", type=("build", "link", "run"))
    depends_on("gnuplot+cairo", type=("build", "run"))

    build_directory = "build"

    @property
    def configure_directory(self) -> str:
        if "@master" in self.spec:
            return "mpibenchmark"
        else:
            return super().configure_directory

    def configure_args(self):
        config_args = [
            "--with-hwloc",  # always use hwloc in spack
            "--without-cuda",
            "--without-hip",
            self.enable_or_disable("optimize"),
            self.enable_or_disable("debug"),
            self.enable_or_disable("asan"),
        ]
        return config_args

    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            Executable("./autogen.sh")()
