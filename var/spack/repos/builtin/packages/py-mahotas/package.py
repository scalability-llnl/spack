# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMahotas(PythonPackage):
    """Mahotas: Computer Vision Library."""

    homepage = "http://luispedro.org/software/mahotas"
    pypi = "mahotas/mahotas-1.4.13.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version("1.4.13", sha256="a78dfe15045a20a0d9e01538b80f874580cd3525ae3eaa2c83ced51eb455879c")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
