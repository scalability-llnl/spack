# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsvm(MakefilePackage):
    """Libsvm is a simple, easy-to-use, and efficient software for SVM
    classification and regression."""

    homepage = "https://www.csie.ntu.edu.tw/~cjlin/libsvm/"
    url = "https://github.com/cjlin1/libsvm/archive/v322.tar.gz"

    license("BSD-3-Clause")

    version("323", sha256="7a466f90f327a98f8ed1cb217570547bcb00077933d1619f3cb9e73518f38196")
    version("322", sha256="a3469436f795bb3f8b1e65ea761e14e5599ec7ee941c001d771c07b7da318ac6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        install("svm-predict", prefix.bin)
        install("svm-scale", prefix.bin)
        install("svm-train", prefix.bin)
        install("svm.o", prefix.lib)
