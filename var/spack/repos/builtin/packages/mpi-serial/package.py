# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class MpiSerial(AutotoolsPackage):
    """A single processor implementation of the mpi library."""

    homepage = "https://github.com/ESMCI/mpi-serial"
    url = "https://github.com/ESMCI/mpi-serial/archive/refs/tags/MPIserial_2.3.0.tar.gz"

    # notify when the package is updated.
    maintainers("jedwards4b")

    version("2.5.0", sha256="2faf459ea1f37020662067e7ab6c76b926501c4b94e8fdf77591c0040ba1f006")
    version("2.3.0", sha256="cc55e6bf0ae5e1d93aafa31ba91bfc13e896642a511c3101695ea05eccf97988")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "fort-real-size",
        values=int,
        default=4,
        description="Specify the size of Fortran real variables",
    )

    variant(
        "fort-double-size",
        values=int,
        default=8,
        description="Specify the size of Fortran double precision variables",
    )

    provides("mpi")

    depends_on("autoconf", type="build", when="@2.5.0")
    depends_on("automake", type="build", when="@2.5.0")
    depends_on("libtool", type="build", when="@2.5.0")

    def flag_handler(self, name, flags):
        spec = self.spec
        config_flags = []

        if name == "cflags":
            config_flags.append(self.compiler.cc_pic_flag)
            if spec.satisfies("%oneapi"):
                # OneAPI fails due to these standards checks
                config_flags.append("-Wno-error=implicit-int")
                config_flags.append("-Wno-error=implicit-function-declaration")
        elif name == "fflags":
            config_flags.append(self.compiler.fc_pic_flag)

        return flags, None, (config_flags or None)

    def configure_args(self):
        args = []

        realsize = int(self.spec.variants["fort-real-size"].value)
        if realsize != 4:
            args.extend(["--enable-fort-real={0}".format(realsize)])
        doublesize = int(self.spec.variants["fort-double-size"].value)
        if doublesize != 8:
            args.extend(["--enable-fort-double={0}".format(doublesize)])

        return args

    def install(self, spec, prefix):
        mkdir(prefix.lib)
        mkdir(prefix.include)
        install("libmpi-serial.a", prefix.lib)
        install("mpi.h", prefix.include)
        install("mpif.h", prefix.include)
        if os.path.isfile("mpi.mod"):
            install("mpi.mod", prefix.include)
        if os.path.isfile("MPI.mod"):
            install("MPI.mod", prefix.include)
