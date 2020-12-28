# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xgboost(CMakePackage, CudaPackage):
    """Scalable, Portable and Distributed Gradient Boosting (GBDT, GBRT or GBM)
       Library, for Python, R, Java, Scala, C++ and more. Runs on single
       machine, Hadoop, Spark, Flink and DataFlow"""

    homepage = "https://xgboost.ai/"
    url      = "https://github.com/dmlc/xgboost/releases/download/v0.81/xgboost-0.81.tar.bz2"
    git      = "https://github.com/dmlc/xgboost.git"

    version('0.90', tag='v0.90', submodules=True)
    version('0.81', sha256='9d8ff161699111d45c96bd15229aa6d80eb1cab7cbbef7e8eaa60ccfb5a4f806')

    def cmake_args(self):
        return [
            '-DUSE_CUDA={0}'.format('YES' if '+cuda' in self.spec else 'NO')
        ]

    def install(self, spec, prefix):
        install_tree(str(self.stage.source_path), prefix)
        # create a bin directory for executable "xgboost" which is possibly
        # used in functional testing of the compilation target "libxgboost"
        mkdirp(prefix.bin)
        install('xgboost', prefix.bin)
