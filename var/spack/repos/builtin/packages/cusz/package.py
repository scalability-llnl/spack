# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install cusz
#
# You can edit this file again by typing:
#
#     spack edit cusz
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------


class Cusz(CMakePackage, CudaPackage):
    """A GPU accelerated error-bounded lossy compression for scientific data"""

    homepage = "https://szcompressor.org/"
    git = "https://github.com/robertu94/cusz"

    maintainers = ["jtian0", "dingwentao"]

    conflicts("~cuda")
    conflicts("cuda_arch=none", when="+cuda")

    version("develop", branch="develop")

    depends_on("cub", when="^ cuda@:10.2.89")

    def cmake_args(self):
        cuda_arch = self.spec.variants["cuda_arch"].value
        args = ["-DBUILD_TESTING=OFF", ("-DCMAKE_CUDA_ARCHITECTURES=%s" % cuda_arch)]
        return args
