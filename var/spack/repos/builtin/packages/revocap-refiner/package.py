# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RevocapRefiner(MakefilePackage):
    """The University of Tokyo, CISS Project:
    Library for refining of model meshes"""

    homepage = "https://www.frontistr.com"
    url = "https://www.frontistr.com/download/link.php?REVOCAP_Refiner-1.1.04.tar.gz"
    # git      = "https://gitlab.com/FrontISTR-Commons/REVOCAP_Refiner.git"

    maintainers("k-tokunaga", "kgoto", "tuna" "inagaki.kazuhisa")

    version("1.1.04", sha256="bf3d959f4c1ab08a7e99cd7e02e710c758af28d71500f4814eed8b4eb3fb2d13")

    parallel = False

    # add space between literal and identifier.
    patch("add_space.patch")
    # remove unused function getIndices.
    patch("delete_getIndices.patch")

    def edit(self, spec, prefix):
        cflags = ["-O3"]
        cxxflags = ["-O3", self.compiler.cxx_pic_flag]
        ldflags = [""]
        ldshare = [""]
        libs = [""]
        m = FileFilter("MakefileConfig.in")
        m.filter(r"ARCH\s*=.*$", "ARCH=")
        m.filter(r"CC\s*=.*$", "CC={0}".format(spack_cc))
        m.filter(r"CFLAGS\s*=.*$", "CFLAGS={0}".format(" ".join(cflags)))
        m.filter(r"CXX\s*=.*$", "CXX={0}".format(spack_cxx))
        m.filter(r"CXXFLAGS\s*=.*$", "CXXFLAGS={0}".format(" ".join(cxxflags)))
        m.filter(r"AR\s*=.*$", "AR=ar")
        m.filter(r"ARFLAGS\s*=.*$", "ARFLAGS=rsv")
        m.filter(r"LD\s*=.*$", "LD={0}".format(spack_fc))
        m.filter(r"LDFLAGS\s*=.*$", "LDFLAGS={0}".format(" ".join(ldflags)))
        m.filter(r"LDSHARE\s*=.*$", "LDSHARE={0}".format(" ".join(ldshare)))
        m.filter(r"LIBS\s*=.*$", "LIBS={0}".format(" ".join(libs)))
        m.filter(r"LIBPATH\s*=.*$", "LIBPATH= ")
        m.filter(r"RM\s*=.*$", "RM=rm -f")
        m.filter(r"TAR\s*=.*$", "TAR=tar")

    def install(self, spec, prefix):
        make()
        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
        install_tree("Refiner", prefix.include)
