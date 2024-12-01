# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIrpf90(PythonPackage):
    """IRPF90 is a Fortran90 preprocessor written in Python for programming
    using the Implicit Reference to Parameters (IRP) method. It simplifies the
    development of large fortran codes in the field of scientific high
    performance computing."""

    homepage = "http://irpf90.ups-tlse.fr"
    pypi = "irpf90/irpf90-2.0.5.tar.gz"

    maintainers("scemama")

    version("2.0.5", sha256="ac3b6a6dd50a93537c6068ed459d5ad75919cbd64cdbce870921da713b86ee37")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
