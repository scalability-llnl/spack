# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPylabSdk(PythonPackage):
    """A development kit that collects simple utilities."""

    homepage = "https://github.com/PyLabCo/pylab-sdk"
    pypi = "pylab-sdk/pylab-sdk-1.3.2.tar.gz"

    license("MIT")

    version("1.3.2", sha256="ea53e97fec45ea15f65bd53da6b25dc16a9accf3a7f5decbaa970592d760148d")

    depends_on("python@3:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-requests", type=("build", "run"))
