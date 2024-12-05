# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mesquite(AutotoolsPackage):
    """Mesquite (Mesh Quality Improvement Toolkit) is designed to provide a
    stand-alone, portable, comprehensive suite of mesh quality improvement
    algorithms and components that can be used to construct custom quality
    improvement algorithms. Mesquite provides a robust and effective mesh
    improvement toolkit that allows both meshing researchers application
    scientists to benefit from the latest developments in mesh quality
    control and improvement."""

    homepage = "https://software.sandia.gov/mesquite"
    url = "https://software.sandia.gov/mesquite/mesquite-2.3.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.99", sha256="7d834dbcc3132d903dbecb59337dc5b47505b7fb579b68f1ce66e5df87106954")
    version("2.3.0", sha256="4ab4ceadfa596e16c00dbb0e8b830a9112fa1b73291ca07633ec379a39b8bb28")
    version("2.2.0", sha256="3d48322c3e148431ee1af155d6bb94dfeef15795da1f46996c112df27778a4a2")

    variant("mpi", default=True, description="Enable MPI parallel support")

    depends_on("mpi", when="+mpi")

    def configure_args(self):
        args = ["--enable-release", "--enable-shared"]

        if "+mpi" in self.spec:
            args.append("CC=%s" % self.spec["mpi"].mpicc)
            args.append("CXX=%s" % self.spec["mpi"].mpicxx)
            args.append("--with-mpi=%s" % self.spec["mpi"].prefix)
        else:
            args.append("--without-mpi")

        return args
