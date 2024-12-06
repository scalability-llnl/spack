# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWget(PythonPackage):
    """pure python download utility

    Download the file for your platform. If you're not sure which to choose,
    learn more about installing packages."""

    pypi = "wget/wget-3.2.zip"

    version("3.2", sha256="35e630eca2aa50ce998b9b1a127bb26b30dfee573702782aa982f875e3f16061")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
