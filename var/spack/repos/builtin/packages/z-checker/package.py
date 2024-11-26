# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# ----------------------------------------------------------------------------


class ZChecker(AutotoolsPackage):
    """a library to perform the compression assessment for lossy compressors"""

    homepage = "https://github.com/CODARcode/Z-checker"
    url = "https://github.com/CODARcode/Z-checker/releases/download/0.7.0/Z-checker-0.7.0.tar.gz"

    maintainers("disheng222")

    license("BSD-3-Clause")

    version("0.9.0", sha256="44436ad5971a24dd26a09d8262bc1fcd8c9fd0b746aff009a91ccbe57330baa1")
    version("0.7.0", sha256="02caf3af2dc59d116496f877da888dd2c2dffb9375c413b1d74401927963df3f")
    version("0.6.0", sha256="b01c2c78157234a734c2f4c10a7ab82c329d3cd1a8389d597e09386fa33a3117")
    version("0.5.0", sha256="ad5e68472c511b393ee1ae67d2e3072a22004001cf19a14bd99a2e322a6ce7f9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=False, description="Enable mpi compilation")

    depends_on("mpi", when="+mpi")

    def configure_args(self):
        args = []
        if "+mpi" in self.spec:
            args += ["--enable-mpi"]
        else:
            args += ["--disable-mpi"]
        return args
