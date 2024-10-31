# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Qcachegrind(QMakePackage):
    """{K,Q}Cachegrind is a KDE/Qt GUI to visualize profiling data.
    It's mainly used as visualization frontend for data measured
    by Cachegrind/Callgrind tools from the Valgrind package, but
    there are converters for other measurement tools available.
    Also provides the command-line tool 'cgview'"""

    homepage = "https://github.com/KDE/kcachegrind"
    url = "https://github.com/KDE/kcachegrind/archive/v20.08.0.tar.gz"

    license("GFDL-1.2-only")

    version("20.12.2", sha256="935cf6665fac274f84af84d0a30cc2fdf27d437234b9accbf8ec0a5dba6ad867")
    version("20.08.0", sha256="ffb50a7c536042ff11eed714b359b8bc419cb12402a31ebe78c3d06363f234e6")

    depends_on("cxx", type="build")  # generated

    depends_on("qt@5.2:")
    depends_on("graphviz", type="run")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("cgview/cgview", prefix.bin)
        install("qcachegrind/qcachegrind", prefix.bin)
