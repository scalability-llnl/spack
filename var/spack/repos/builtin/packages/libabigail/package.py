# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libabigail(AutotoolsPackage):
    """The ABI Generic Analysis and Instrumentation Library"""

    homepage = "https://sourceware.org/libabigail"
    url = "https://mirrors.kernel.org/sourceware/libabigail/libabigail-2.0.tar.gz"
    git = "https://sourceware.org/git/libabigail.git"

    license("Apache-2.0 WITH LLVM-exception")

    version("master", branch="master")
    version("2.1", sha256="4a6297d41d15d1936256117116bd61296e6b9bee23d54a0caf8d3f5ab8ddcc4c")
    version("2.0", sha256="3704ae97a56bf076ca08fb5dea6b21db998fbbf14c4f9de12824b78db53b6fda")
    version("1.8", sha256="1cbf260b894ccafc61b2673ba30c020c3f67dbba9dfa88dca3935dff661d665c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("docs", default=False, description="build documentation")

    depends_on("elfutils", type=("build", "link"))
    depends_on("libxml2", type=("build", "link"))

    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")

    # Libabigail won't generate it's bin without Python
    depends_on("python@3.8:")

    # Will not find libxml without this
    depends_on("pkgconfig", type="build")

    # Documentation dependencies
    depends_on("doxygen", type="build", when="+docs")
    depends_on("py-sphinx", type="build", when="+docs")

    def configure_args(self):
        spec = self.spec
        config_args = [f"CPPFLAGS=-I{spec['libxml2'].prefix}/include"]
        config_args.append(
            "LDFLAGS=-L{0} -Wl,-rpath,{0}".format(spec["libxml2"].libs.directories[0])
        )
        return config_args

    def autoreconf(self, spec, prefix):
        autoreconf = which("autoreconf")
        with working_dir(self.configure_directory):
            # We need force (f) because without it, looks for RedHat library
            autoreconf("-ivf")
