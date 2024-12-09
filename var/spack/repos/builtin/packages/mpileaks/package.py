# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpileaks(AutotoolsPackage):
    """Tool to detect and report MPI objects like MPI_Requests and
    MPI_Datatypes."""

    homepage = "https://github.com/LLNL/mpileaks"
    url = "https://github.com/LLNL/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz"

    version("1.0", sha256="2e34cc4505556d1c1f085758e26f2f8eea0972db9382f051b2dcfb1d7d9e1825")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "stackstart",
        values=int,
        default=0,
        description="Specify the number of stack frames to truncate",
    )

    depends_on("mpi")
    depends_on("adept-utils")
    depends_on("callpath")

    def configure_args(self):
        stackstart = int(self.spec.variants["stackstart"].value)

        args = [
            "--with-adept-utils={0}".format(self.spec["adept-utils"].prefix),
            "--with-callpath={0}".format(self.spec["callpath"].prefix),
        ]

        if stackstart:
            args.extend(
                [
                    "--with-stack-start-c={0}".format(stackstart),
                    "--with-stack-start-fortran={0}".format(stackstart),
                ]
            )

        return args
