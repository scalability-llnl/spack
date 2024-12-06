# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycosat(PythonPackage):
    """PicoSAT is a popular SAT solver written by Armin Biere in pure C. This
    package provides efficient Python bindings to picosat on the C level, i.e.
    when importing pycosat, the picosat solver becomes part of the Python
    process itself. For ease of deployment, the picosat source (namely
    picosat.c and picosat.h) is included in this project. These files have been
    extracted from the picosat source (picosat-965.tar.gz)."""

    homepage = "https://github.com/ContinuumIO/pycosat"
    pypi = "pycosat/pycosat-0.6.3.zip"

    license("MIT")

    version("0.6.3", sha256="4c99874946a7e939bb941bbb019dd2c20e6068e3107c91366e7779c69d70e0ed")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
