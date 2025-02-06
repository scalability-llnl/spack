# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import autotools, cmake
from spack.package import *


class Trexio(AutotoolsPackage, CMakePackage):
    """TREXIO: TREX I/O library."""

    homepage = "https://trex-coe.github.io/trexio"
    git = "https://github.com/TREX-CoE/trexio.git"
    url = "https://github.com/TREX-CoE/trexio/releases/download/v2.2.0/trexio-2.2.0.tar.gz"

    # notify when the package is updated.
    maintainers("q-posev", "scemama")

    license("BSD-3-Clause")

    build_system("cmake", "autotools", default="autotools")

    version("master", branch="master")
    version("2.5.0", sha256="7bf7e0021467530b4946fb3f6ee39f393e2f4bd65a6f4debaec774120c29e4ee")
    version("2.4.2", sha256="074c7cf18ea7a8a1d5e29bde4a773d4fb80081c4eb52e2dc4299e6075b704c93")
    version("2.3.2", sha256="b6e831ea5430115a305626695649d823163e7404fd088fc265f0cbe2c1b46ee0")
    version("2.3.1", sha256="41145ec808f2fbb6b03e3b191b3828e5439cef0507c5afd1016b3cb4e31dde14")
    version("2.3.0", sha256="310a33cc2202bce09d2326708753f0866311854e6571e1ae50516f159ea47ca0")
    version("2.2.3", sha256="1c16987fa6afe400de8b1c0d98270263f6f380278d8c0f2b9ad5156352d653ff")
    version("2.2.0", sha256="e6340c424fcea18ae0b643a5707e16005c7576ee21a5aac679fbc132d70b36d9")
    version("2.1.0", sha256="232866c943b98fa8a42d34b55e940f7501634eb5bd426555ba970f5c09775e83")
    version("2.0.0", sha256="6eeef2da44259718b43991eedae4b20d4f90044e38f3b44a8beea52c38b14cb4")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("hdf5", default=True, description="Enable HDF5 support")

    depends_on("emacs@26.0:", type="build", when="@master")
    depends_on("python@3.6:", type="build", when="@master")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("hdf5@1.8:+hl", when="@:2.3.0 +hdf5")
    depends_on("hdf5@1.8:", when="+hdf5")

    # Append -lhdf5_hl to LIBS when hdf5 variant is activated
    # or use --without-hdf5 option otherwise.


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    def configure_args(self):
        config_args = []
        if "+hdf5" in self.spec:
            if self.spec("@:2.3.0"):
                config_args.append("LIBS=-lhdf5_hl")
            else:
                config.args.append("LIBS=-lhdf5")
        else:
            config_args.append("--without-hdf5")

        return config_args


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        args = [self.define_from_variant("ENABLE_HDF5", "hdf5")]

        return args
