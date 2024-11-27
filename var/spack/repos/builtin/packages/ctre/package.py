# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Ctre(CMakePackage):
    """Compile time regular expressions for C++"""

    homepage = "https://compile-time.re/"
    url = "https://github.com/hanickadot/compile-time-regular-expressions/archive/v2.8.3.tar.gz"
    git = "https://github.com/hanickadot/compile-time-regular-expressions.git"

    license("Apache-2.0")

    version("master", branch="master")
    version("3.8.1", sha256="0ce8760d43b3b97b43364cd32ee663e5c8b8b4bfd58e7890042eff6ac52db605")
    version("2.8.4", sha256="99b981857f1b66cab5e71161ae74deca268ed39a96ec6507def92d4f445cadd6")
    version("2.8.3", sha256="5833a9d0fbce39ee39bd6e29df2f7fcafc82e41c373e8675ed0774bcf76fdc7a")
    version("2.8.2", sha256="f89494f52ec31e5854fff3d2c5825474201476636c5d82a9365dad5188396314")
    version("2.8.1", sha256="a6153629751ba0adc039551d8ff8d7018972ce362d20c0f70135496d4e7721df")
    version("2.8", sha256="44ccdaa299dd43c351f208c5906422eb000e7cdcb53e4f3b7c7c094d0461ab2c")
    version("2.7", sha256="ccbf42515b27d542cd36104eb9548f288b0c1989cb584a518900ba1ca3619e12")
    version("2.6.4", sha256="ce216cfae0e7e1e8c7d7531cfcf81fa18f9bdbfcb800a3119788ca323bedbdac")
    version("2.6.3", sha256="bdf668b02f0b986dfc0fbc6066f446e2d0a9faa3347f00f53b19131297c84c4a")
    version("2.6.2", sha256="e82c87aeb0fc3f21ae8a2d3ffce2b1ef970fbea9c3e846ef1a6e5f81790f2946")
    version("2.6.1", sha256="58c623d9ea1cb7890aaa63c1a87f1a60a8acf31dbd4061ab672bea287ed689ac")

    depends_on("cxx", type="build")  # generated
