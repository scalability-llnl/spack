# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Iegenlib(CMakePackage):
    """Inspector/Executor Generation Library for manipulating sets
    and relations with uninterpreted function symbols."""

    homepage = "https://github.com/CompOpt4Apps/IEGenLib"
    git = "https://github.com/CompOpt4Apps/IEGenLib.git"
    url = "https://github.com/CompOpt4Apps/IEGenLib/archive/fc479ee6ff01dba26beffc1dc6bacdba03262138.zip"

    maintainers("dhuth")

    license("BSD-2-Clause")

    version("master", branch="master")
    version(
        "2018-07-03",
        url="https://github.com/CompOpt4Apps/IEGenLib/archive/fc479ee6ff01dba26beffc1dc6bacdba03262138.zip",
        sha256="b4c0b368363fcc1e34b388057cc0940bb87fc336cebb0772fd6055f45009b12b",
    )

    depends_on("cmake@2.6:", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("texinfo", type="build")
    depends_on("isl")

    build_directory = "spack-build"

    @run_before("cmake")
    def make_dirs(self):
        autoreconf = which("autoreconf")
        with working_dir("lib/isl"):
            autoreconf("-i")
        mkdirp("spack-build/bin")

    def cmake_args(self):
        args = []
        args.append("-DGEN_PARSER=no")
        args.append("-DBUILD_PYTHON=no")
        return args
