# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPysmartdl(PythonPackage):
    """A Smart Download Manager for Python."""

    pypi = "pySmartDL/pySmartDL-1.3.2.tar.gz"

    license("Unlicense")

    version("1.3.2", sha256="9a96deb3ee4f4ab2279b22eb908d506f57215e1fbad290d540adcebff187a52c")
    version("1.2.5", sha256="d3968ce59412f99d8e17ca532a1d949d2aa770a914e3f5eb2c0385579dc2b6b8")

    depends_on("py-setuptools", type="build")
