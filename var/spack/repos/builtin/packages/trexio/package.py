# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Trexio(AutotoolsPackage):
    """TREXIO: TREX I/O library."""

    homepage = "https://trex-coe.github.io/trexio"
    git = "https://github.com/TREX-CoE/trexio.git"
    url = "https://github.com/TREX-CoE/trexio/releases/download/v2.2.0/trexio-2.2.0.tar.gz"

    # notify when the package is updated.
    maintainers("q-posev", "scemama")

    license("BSD-3-Clause")

    version("master", branch="master")
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

    depends_on("hdf5@1.8:+hl", when="+hdf5")

    # Append -lhdf5_hl to LIBS when hdf5 variant is activated
    # or use --without-hdf5 option otherwise.
    def configure_args(self):
        config_args = []
        if "+hdf5" in self.spec:
            config_args.append("LIBS=-lhdf5_hl")
        else:
            config_args.append("--without-hdf5")

        return config_args
