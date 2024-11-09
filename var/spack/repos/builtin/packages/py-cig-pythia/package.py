# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCigPythia(AutotoolsPackage, PythonExtension):
    """This is the Computational Infrastructure for Geodynamics (CIG) fork of
    Pythia/Pyre originally written by Michael Aivazis (California Institute of Technology).

    Pythia/Pyre provides a Python framework for scientific simulations. This
    fork focuses (and maintains) functionality for:

    specification of simulation parameters
    specification of units and unit conversions
    user-friendly interface to popular batch job schedulers
    Python and C++ interfaces for logging"""

    homepage = "https://github.com/geodynamics/pythia/"
    url = "https://github.com/geodynamics/pythia/releases/download/v1.1.0/pythia-1.1.0.tar.gz"

    license("BSD-3-Clause", checked_by="downloadico")

    version("1.1.0", sha256="d8e941d2d0fa4772c3c0cb3d1d9b6acbb5fa01ef346dc0706a8da541a8f97731")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Build with MPI support.")

    depends_on("mpi", when="+mpi")
    depends_on("python@3.8:")
    depends_on("py-pip")
    depends_on("py-setuptools")

    def configure_args(self):
        spec = self.spec
        args = []
        if "+mpi" in spec:
            args.append("--enable-mpi")
            args.append(f"CC={spec['mpi'].mpicc}")
            args.append(f"CXX={spec['mpi'].mpicxx}")
        else:
            args.append("--disable-mpi")
        return args
